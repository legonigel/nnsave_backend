"""
Models for this app

Copyright (C) 2016 Nigel Armstrong legonigel@gmail.com
All rights reserved.

This software may be modified and distributed under the terms
of the MIT license. See LICENSE file for details
"""

from django.contrib.gis.db import models

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
	return unicode("Category %s" % self.name)

class Location(models.Model):
    name = models.CharField(max_length=150)
    phone = models.CharField(max_length=100)
    website = models.URLField(blank = True)
    email = models.EmailField(blank = True)
    address = models.TextField(blank = True)
    loc = models.PointField()
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete = models.CASCADE)
    visit_count = models.IntegerField(default = 0)

    def __unicode__(self):
	return unicode('Location %s (%s, visits %s)' %
		       (self.name,
			self.category.__unicode__(),
			self.visit_count))

class DetectedLocation(models.Model):
    location = models.ForeignKey('Location', on_delete = models.CASCADE)
    device_id = models.CharField(max_length = 32)
    date = models.DateTimeField(auto_now_add = True )
