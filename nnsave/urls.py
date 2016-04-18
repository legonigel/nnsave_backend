"""
Urls for root server

Copyright (C) 2016 Nigel Armstrong legonigel@gmail.com
All rights reserved.

This software may be modified and distributed under the terms
of the MIT license. See LICENSE file for details
"""

from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'nnsave_backend.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('nnsave_app.urls')),
)
