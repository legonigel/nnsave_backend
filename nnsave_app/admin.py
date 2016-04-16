from django.contrib.gis import admin
from .models import Location, Category

# Register your models here.
admin.site.register(Location, admin.OSMGeoAdmin)
admin.site.register(Category)
