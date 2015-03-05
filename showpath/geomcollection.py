from models import EcourierOneday, Hh2Po4Pgr, ProjectionPoint, Testcases
from django.contrib.gis.geos import MultiPoint, MultiLineString

def multipoints(test_id):
	nodes = Testcases.objects.get(test_id=int(test_id)).measurements
	geomlist = [EcourierOneday.objects.get(id=int(x)).geom for x in nodes]
	return MultiPoint(geomlist)

def multilines(lines):
	geomlist = [Hh2Po4Pgr.objects.get(id=int(x)).geom_way for x in lines]
	return MultiLineString(geomlist)

def truepath(test_id):
	lines = Testcases.objects.get(test_id=int(test_id)).gt_mm_edges
	return multilines(lines)

def projectedpoints(test_id):
	nodes = ProjectionPoint.objects.filter(test_id=int(test_id))
	geomlist = [node.geom for node in nodes]
	return MultiPoint(geomlist)