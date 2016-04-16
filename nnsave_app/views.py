from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, HttpResponseBadRequest
from .models import Location, Category, DetectedLocation
from django.core import serializers
from django.forms.models import model_to_dict
import json
from django.contrib.gis.geos import Point
from django.views.decorators.csrf import csrf_exempt
# Create your views here.

@csrf_exempt
def location(request, **kwargs):
    if request.method != 'GET':
	return HttpResponseBadRequest("Only get Request allowed")
    if kwargs['id']:
	#get only a single location
	objects = [get_object_or_404(Location, pk=kwargs['id'])]
    else:
	query_params = ['latitude','longitude','distance','count']
	if any([param in request.GET for param in query_params]):
	    print 'found param'
	    objects = []
	else:
	    objects = Location.objects.all()
    #data = serializers.serialize('geojson', all_objects)['features']
    data = []
    for obj in objects:
	tmp_dict = obj.__dict__
	tmp_dict['latitude'] = tmp_dict['loc'].coords[0]
	tmp_dict['longitude'] = tmp_dict['loc'].coords[1]
	del tmp_dict['loc']
	del tmp_dict['_state']
	tmp_dict['category'] = Category.objects.get(pk=tmp_dict['category_id']).name
	del tmp_dict['category_id']
	data.append(tmp_dict)
    data = json.dumps(data)
    return HttpResponse(data, content_type = 'application/json')

def index(request):
    return HttpResponse()


def get_all_locations(request):
    return None
