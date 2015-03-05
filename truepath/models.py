from django.db import models
from django.contrib.gis.db import models
from django.contrib.postgres.fields import ArrayField
from showpath.geojson import GeojsonEncoder
# Create your models here.

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
        db_table = 'testcases'


class EcourierOneday(models.Model):
    id = models.BigIntegerField(primary_key=True)
    # vehicleid = models.IntegerField(blank=True, null=True)
    # type = models.TextField(blank=True)
    # longitude = models.FloatField(blank=True, null=True)
    # latitude = models.FloatField(blank=True, null=True)
    # timestamp = models.DateTimeField(blank=True, null=True)
    geom = models.PointField(blank=True, null=True)
    objects = models.GeoManager()

    def to_JSON(self):
    	obj={}
    	obj["type"]="Feature"
    	obj["geometry"]=self.geom
    	obj["properties"]={"id":self.id}
    	return obj
    def to_obj(self):
    	return {"type":"Feature",
    		"properties":{"id":self.id},
    		"geometry":{'type':self.geom.geom_type,'coordinates':self.geom.coords}}
    class Meta:
        managed = False
        db_table = 'ecourier_oneday'

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
        db_table = 'measurements_proj'


class Hh2Po4Pgr(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    # source = models.IntegerField(blank=True, null=True)
    # target = models.IntegerField(blank=True, null=True)
    # km = models.FloatField(blank=True, null=True)
    geom_way = models.LineStringField(blank=True, null=True)
    # source_geom = models.PointField(blank=True, null=True)
    # target_geom = models.PointField(blank=True, null=True)
    objects = models.GeoManager()

    def to_JSON(self):
    	obj={}
    	obj["type"]="Feature"
    	obj["geometry"]=self.geom_way
    	obj["properties"]={"id":self.id}
    	return obj
    def to_obj(self):
    	return {"type":"Feature",
    		"properties":{"id":self.id},
    		"geometry":{'type':self.geom_way.geom_type,'coordinates':self.geom_way.coords}}
    class Meta:
        managed = False
        db_table = 'hh_2po_4pgr'
