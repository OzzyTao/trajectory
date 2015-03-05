from showpath.geojson import GeojsonEncoder
from models import EcourierOneday, Hh2Po4Pgr

class ModelEncoder(GeojsonEncoder):
	def default(self,obj):
		if isinstance(obj,EcourierOneday) or isinstance(obj,Hh2Po4Pgr):
			return obj.to_JSON()
		return GeojsonEncoder.default(self,obj)