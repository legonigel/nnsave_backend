from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^locations/?(?P<id>[0-9]+)?$',views.location, name='location'),
    url(r'^categories/?(?P<id>[0-9]+)?$',views.category, name='category'),
]
