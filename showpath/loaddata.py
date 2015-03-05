import pickle
from geomcollection import multipoints, multilines, truepath, projectedpoints
from sta import Test
from django.conf import settings
import sta
import os
import sys
sys.modules['sta'] = sta

def geomtransfer(test):
	test.best_ranking('possibility')
	test_para = {'period':test.test_para['period'],
		'measurements':multipoints(test.test_para['test_id']),
		'truepath':truepath(test.test_para['test_id']),
		'projected':projectedpoints(test.test_para['test_id'])
	}
	routes = []
	for route in test.routes:
		tmp={
		'modeledpath':multilines(route['edgeIDList']),
		'possibility':route['possibility'],
		'RMSE':route['RMSE'],
		'TRMSE':route['TRMSE'],
		'area':route['area'],
		'CLength':route['CLength']
		}
		routes.append(tmp)
	return {'test_para':test_para,'routes':routes}

# def loaddata():
# 	path = 'f:/London/statistics/'
# 	names = ['RMSE','TRMSE','area','CLength','RMSE_Rank','TRMSE_Rank','area_Rank','CLength_Rank']
# 	# K values
# 	fields = ['30s','40s','50s','60s','90s','120s','150s'] 
# 	seconds = [30,40,50,60,90,120,150]
# 	suffix = 'econds101test.p'
# 	binaryfiles=[field+suffix for field in fields[:-1]]+['150seconds111test.p']
# 	# binaryfiles = ['60seconds115test10k.p','60seconds101test20k.p','60seconds115test30k.p','60seconds115test50k.p','60seconds101test.p','60seconds115test150k.p']
# 	typetest = {}
# 	for typeid in range(7):
# 		with open(path+binaryfiles[typeid],'rb') as binary:
# 			testgroup = pickle.load(binary)
# 			typetest[fields[typeid]]=testgroup[:100]
# 	print 'loading data.....'
# 	return typetest

def loaddata():
	path=os.path.join(settings.DATA_DIR,'statistics6')
	names = ['RMSE','TRMSE','area','CLength','RMSE_Rank','TRMSE_Rank','area_Rank','CLength_Rank']
	fields = ['30s','60s','90s','120s','150s','180s']
	seconds = [30,60,90,120,150,180]
	binaryfiles=[field+'econds151test.p' for field in fields]
	# binaryfiles = ['30seconds217test.p','60seconds208test.p','90seconds203test.p','120seconds203test.p','150seconds202test.p','180seconds31test.p']
	typetest={}
	for typeid in range(len(seconds)):
		with open(os.path.join(path,binaryfiles[typeid]),'rb') as binary:
			testgroup = pickle.load(binary)
			typetest[fields[typeid]]=testgroup
	print 'loading data......'
	return typetest



testgroups = loaddata()