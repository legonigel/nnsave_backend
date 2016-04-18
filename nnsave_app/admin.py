"""
Admin pages for nnsave_app

Copyright (C) 2016 Nigel Armstrong legonigel@gmail.com
All rights reserved.

This software may be modified and distributed under the terms
of the MIT license. See LICENSE file for details
"""

from django.contrib.gis import admin
from .models import Location, Category, DetectedLocation
from import_export import resources
from import_export.admin import ImportExportModelAdmin

# Register your models here.
admin.site.register(Location, admin.OSMGeoAdmin)
admin.site.register(Category)
admin.site.register(DetectedLocation)

admin.site.site_header = 'NNSave Admin'
admin.site.site_title = 'NNSave site admin'
admin.site.index_title = 'NNSave Administration'

class LocationResource(resources.ModelResource):
    class Meta:
	model = Location
