from django.contrib.gis.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
	return unicode("Category %s" % self.name)

class Location(models.Model):
    name = models.TextField()
    phone = models.CharField(max_length=13)
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
