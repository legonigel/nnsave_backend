"""
Urls for nnsave_app

Copyright (C) 2016 Nigel Armstrong legonigel@gmail.com
All rights reserved.

This software may be modified and distributed under the terms
of the MIT license. See LICENSE file for details
"""

from django.conf.urls import url
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    #url(r'^/?$', TemplateView.as_view(template_name='nnsave_app/index.html'), name='index'),
    url(r'^locations/?(?P<id>[0-9]+)?$',views.location, name='location'),
    url(r'^categories/?(?P<id>[0-9]+)?$',views.category, name='category'),
]
