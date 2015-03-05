# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals

from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField



class EcourierOneday(models.Model):
    id = models.BigIntegerField(primary_key=True)
    vehicleid = models.IntegerField(blank=True, null=True)
    type = models.TextField(blank=True)
    # longitude = models.FloatField(blank=True, null=True)
    # latitude = models.FloatField(blank=True, null=True)
    timestamp = models.DateTimeField(blank=True, null=True)
    geom = models.PointField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'ecourier_oneday'


class Hh2Po4Pgr(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    source = models.IntegerField(blank=True, null=True)
    target = models.IntegerField(blank=True, null=True)
    km = models.FloatField(blank=True, null=True)
    geom_way = models.LineStringField(blank=True, null=True)
    # source_geom = models.PointField(blank=True, null=True)
    # target_geom = models.PointField(blank=True, null=True)
    objects = models.GeoManager()

    class Meta:
        managed = False
        db_table = 'hh_2po_4pgr'


class ProjectionPoint(models.Model):
    test_id = models.IntegerField()
    measurement_id = models.IntegerField()
    geom = models.PointField()
    objects = models.GeoManager()

    def to_obj(self):
        return {"type":"Feature",
            "properties":{"id":self.measurement_id},
            "geometry":{'type':self.geom.geom_type,'coordinates':self.geom.coords}}

    class Meta:
        managed=False
        db_table = 'measurements_proj3'

class Testcases(models.Model):
    test_id = models.IntegerField(primary_key=True)
    time_slot = models.IntegerField()
    start_num = models.IntegerField()
    end_num = models.IntegerField()
    measurements = ArrayField(models.IntegerField())
    gt_manul_edges = ArrayField(models.IntegerField())
    gt_mm_edges = ArrayField(models.IntegerField())

    class Meta:
        managed = False
        db_table = 'testcases3'











