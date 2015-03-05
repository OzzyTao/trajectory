from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.core.serializers import serialize
from modeljson import ModelEncoder
from models import EcourierOneday, Hh2Po4Pgr, Testcases, ProjectionPoint
from django.template import RequestContext
import json
import psycopg2
# Create your views here.

def cal_min_bbox(allmeasurements):
	boundingboxratio=1.0
	conn = psycopg2.connect("dbname=gis user=postgres password=peach")
	cur = conn.cursor()
	raw_query = '''select id from hh_2po_4pgr,(select st_buffer(st_envelope(st_collect(geom)),200/111320.0) as box from ecourier_oneday where id = any(array[%s])) as f 
	where geom_way && f.box''' % ','.join([str(m) for m in allmeasurements])
	cur.execute(raw_query)
	edgelist = [row[0] for row in cur]
	cur.close()
	conn.close()
	return edgelist

def measurements(request,id):
	measurement_array=Testcases.objects.get(test_id=id)
	geometry_array = EcourierOneday.objects.filter(id__in=measurement_array.measurements)
	objects = [x.to_obj() for x in geometry_array]
	return HttpResponse(json.dumps(objects),content_type='application/json')

def projected_points(request,id):
	point_array = ProjectionPoint.objects.filter(test_id=id)
	objects = [x.to_obj() for x in point_array]
	return HttpResponse(json.dumps(objects),content_type='application/json')

def mm_segments(request,id):
	measurement_array = Testcases.objects.get(test_id=id)
	objects=[]
	if measurement_array.gt_mm_edges:
		geometry_array = Hh2Po4Pgr.objects.filter(id__in=measurement_array.gt_mm_edges)
		objects = [x.to_obj() for x in geometry_array]
	return HttpResponse(json.dumps(objects),content_type='application/json')
	
def segments(request,id):
	measurement_array=Testcases.objects.get(test_id=id)
	objects=[]
	if measurement_array.gt_manul_edges:
		geometry_array =Hh2Po4Pgr.objects.filter(id__in=measurement_array.gt_manul_edges)
		objects = [x.to_obj() for x in geometry_array]
	# return HttpResponse(serialize('geojson',geometry_array,fields=('id',)),content_type='application/json')
	return HttpResponse(json.dumps(objects),content_type='application/json')

def edges(request,id):
	thistest = Testcases.objects.get(test_id=id)
	edgelist = cal_min_bbox(thistest.measurements)
	print len(edgelist)
	geometry_array = Hh2Po4Pgr.objects.filter(id__in=edgelist)
	objects = [x.to_obj() for x in geometry_array]
	return HttpResponse(json.dumps(objects),content_type="application/json")

# def index(request):
# 	context = RequestContext(request)
# 	periods = ['30','60','90','120','150']
# 	return render_to_response('truepath/index.html',{'periods':periods},context)

def testlist(request):
	context = RequestContext(request)
	tests = Testcases.objects.order_by('test_id')
	return render_to_response('truepath/testlist.html',{'tests':tests},context)

def test(request,id):
	context = RequestContext(request)
	thistest = Testcases.objects.get(test_id=id)
	return render_to_response('truepath/test.html',{'test':thistest},context)

def update(request):
	id= int(request.POST['id'])
	truepath = [int(x) for x in request.POST.getlist('path[]')]
	thistest = Testcases.objects.get(test_id=id)
	thistest.gt_manul_edges = truepath
	thistest.save()
	return redirect('/truepath/')
