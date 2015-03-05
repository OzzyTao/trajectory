import json
from django.shortcuts import render, render_to_response
from django.http import HttpResponse
from django.template import RequestContext
from models import EcourierOneday, Hh2Po4Pgr
from geomcollection import multilines, multipoints
from geojson import GeojsonEncoder
from loaddata import testgroups, geomtransfer
# Create your views here.
def measurement(request,id):
	point = EcourierOneday.objects.get(id=id)
	return HttpResponse(point.geom.json, content_type='application/json')

def roadseg(request,id):
	edge = Hh2Po4Pgr.objects.get(id=id)
	return HttpResponse(edge.geom_way.json, content_type='application/json')

def pointgroup(request,id):
	idlist = id.split('+')
	# return HttpResponse(multipoints(idlist).json,content_type='application/json')
	return HttpResponse(GeojsonEncoder().encode(multipoints(idlist)),content_type='application/json')

def linegroup(request,id):
	idlist = id.split('+')
	# return HttpResponse(multilines(idlist).json, content_type='application/json')
	return HttpResponse(GeojsonEncoder().encode(multilines(idlist)), content_type='application/json')

def test(request,time,id):
	timefield = time+'s'
	test = testgroups[timefield][int(id)-1]
	testgeom = geomtransfer(test)
	return HttpResponse(GeojsonEncoder().encode(testgeom),content_type='application/json')

def testlist(request,time):
	timefield = time +'s'
	testgroup = testgroups[timefield]
	tlist = [{'id': i+1,'num':len(testgroup[i].routes),'testid':testgroup[i].test_para['test_id']} for i in range(len(testgroup))]
	return HttpResponse(json.dumps(tlist),content_type='application/json')


def index(request):
	context = RequestContext(request)
	periods = ['30','60','90','120','150','180']
	return render_to_response('showpath/index.html',{'periods':periods},context)


	

