from django.contrib.gis import admin
from .models import Location, Category, DetectedLocation

# Register your models here.
admin.site.register(Location, admin.OSMGeoAdmin)
admin.site.register(Category)
admin.site.register(DetectedLocation)

admin.site.site_header = 'NNSave Admin'
admin.site.site_title = 'NNSave site admin'
admin.site.index_title = 'NNSave Administration'
