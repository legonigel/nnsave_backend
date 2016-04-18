"""
Views for nnsave_app

Copyright (C) 2016 Nigel Armstrong legonigel@gmail.com
All rights reserved.

This software may be modified and distributed under the terms
of the MIT license. See LICENSE file for details
"""

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .models import Location, Category, DetectedLocation
from django.core import serializers
from django.forms.models import model_to_dict
import json
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import D
from django.contrib.gis.db.models.functions import Distance
from django.views.decorators.csrf import csrf_exempt
import hashlib
import datetime as dt
from django.utils import timezone
# Create your views here.

@csrf_exempt
def location(request, **kwargs):
    if request.method != 'GET' and request.method != 'POST':
	return HttpResponseBadRequest("Only GET or POST Request allowed")
    elif request.method == 'GET':
	return get_location(request, **kwargs)
    elif request.method == 'POST':
	return detected_location(request, **kwargs)

def get_location(request, **kwargs):
    if kwargs['id']:
	#get only a single location
	objects = [get_object_or_404(Location, pk=kwargs['id'])]
    else:
	query_params = ['latitude','longitude','distance','count']
	if any([param in request.GET for param in query_params]):
	    if not ('latitude' in request.GET and 'longitude' in request.GET):
		return HttpResponseBadRequest("When using optional parameters, latitude and longitude must be specified")
	    objects = get_locations_by_params(request.GET)
	else:
	    objects = Location.objects.all()
    return get_http_from_location_list(objects)

def get_http_from_location_list(locations):
    data = []
    for obj in locations:
	data.append(get_location_as_dict(obj))
    data = json.dumps(data)
    if not locations:
	return HttpResponse(data, content_type = 'application/json', status=204)
    return HttpResponse(data, content_type = 'application/json')

def get_location_as_dict(location):
    tmp_dict = location.__dict__
    tmp_dict['latitude'] = tmp_dict['loc'].coords[0]
    tmp_dict['longitude'] = tmp_dict['loc'].coords[1]
    del tmp_dict['loc']
    del tmp_dict['_state']
    tmp_dict['category'] = Category.objects.get(pk=tmp_dict['category_id']).name
    del tmp_dict['category_id']
    if '_category_cache' in tmp_dict:
	del tmp_dict['_category_cache']
    if 'distance' in tmp_dict:
	tmp_dict['distance'] = tmp_dict['distance'].m
    return tmp_dict

def get_locations_by_params(params_dict):
    latitude = float(params_dict.get('latitude'))
    longitude = float(params_dict.get('longitude'))
    distance = float(params_dict.get('distance', float("inf")))
    if 'distance' in params_dict:
	count = float(params_dict.get('count', float("inf")))
    else:
	#no distance
	count = float(params_dict.get('count', 1))

    ref_loc = Point(latitude, longitude)
    locs = Location.objects.filter(loc__distance_lte=(ref_loc,D(m=distance))).annotate(distance=Distance('loc', ref_loc)).order_by('distance')
    if count != float('inf'):
	locs = locs[:count]
    return locs

def category(request, **kwargs):
    if request.method != 'GET':
	return HttpResponseBadRequest("Only GET Request allowed")
    if kwargs['id']:
	#get only a single location
	objects = [get_object_or_404(Category, pk=kwargs['id'])]
    else:
	objects = Category.objects.all()

    return get_http_from_category_list(objects)

def get_http_from_category_list(categories):
    data = []
    for obj in categories:
	tmp_dict = obj.__dict__
	del tmp_dict['_state']
	if '_category_cache' in tmp_dict:
	    del tmp_dict['_category_cache']
	data.append(tmp_dict)
    data = json.dumps(data)
    return HttpResponse(data, content_type = 'application/json')

#Detect time between matches
DETECT_TIME_BETWEEN = dt.timedelta(hours = 12)

def detected_location(request, **kwargs):
    json_data = json.loads(request.body)
    params = dict(json_data)
    params['count'] = 1
    locations = get_locations_by_params(params)
    if not locations:
	return HttpResponse("", content_type = 'application/json', status=204)
    loc = locations[0]
    loc_pk = loc.id
    dev_hash = hashlib.md5(params['deviceID']).hexdigest()
    try:
	last_visit_this_loc = DetectedLocation.objects.filter(location_id=loc_pk,device_id__exact=dev_hash).latest('date')
    except DetectedLocation.DoesNotExist:
	pass
    else:
	#check the detected location
	if timezone.now() - last_visit_this_loc.date < DETECT_TIME_BETWEEN:
	    #too soon, no new loc
	    return HttpResponse("", content_type = 'application/json', status=204)

    #create a new detected location for this detection
    d_loc = DetectedLocation(location=loc, device_id = dev_hash )
    d_loc.save()

    data = json.dumps(get_location_as_dict(loc))
    response = HttpResponse(data, content_type = 'application/json')
    response.__setitem__('Location', '/locations/'+str(loc_pk))
    return response
