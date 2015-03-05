import json
from django.contrib.gis.geos import GEOSGeometry
# from loaddata import Test

class GeojsonEncoder(json.JSONEncoder):
	def default(self,obj):
		if isinstance(obj,GEOSGeometry):
			return {'type':obj.geom_type,'coordinates':obj.coords}
		return json.JSONEncoder.default(self,obj)

# class TestEncoder(json.JSONEncoder):
# 	def default(self,obj):
# 		if isinstance(obj,Test):
# 			return {'truepath':obj.test_para,'predictions':obj.routes}
# 		elif isinstance()