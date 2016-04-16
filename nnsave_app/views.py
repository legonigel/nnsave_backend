from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

# Create your views here.

def location(request):
    response_data = {}
    response_data['test'] = 'test_str'
    return JsonResponse(response_data)

def index(request):
    return HttpResponse()


def get_all_locations(request):
    return None
