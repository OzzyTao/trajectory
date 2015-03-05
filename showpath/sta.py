import pickle
import operator
from scipy.stats import pearsonr


def compare(col):
	def temp(x,y):
		if x[col]==y[col]:
			return x['possibility_Rank']-y['possibility_Rank']
		else:
			if col=='CLength':
				return 1 if y[col]-x[col]>0 else -1
			else:
				return 1 if x[col]-y[col]>0 else -1
	def possi(x,y):
		return 1 if y[col]-x[col]>0 else -1
	if col=='possibility':
		return possi
	else:
		return temp

class Test:
	def __init__(self,records):
		self.ranked = False
		self.routes = []
		for record in records:
			self.routes.append({
				'route':record['route'],
				'edgeIDList':record['edgeIDList'],
				'possibility':float(record['possibility']),
				'RMSE':float(record['RMSE']),
				'TRMSE':float(record['temporal_RMSE']),
				'area':float(record['area']),
				'CLength':float(record['common_length'])
					})
		self.ranking()
		self.corr()
	def best_ranking(self,key):
		if self.ranked:
			self.routes.sort(key=operator.itemgetter(key+'_Rank'))
		else:
			self.routes.sort(cmp=compare(key))
		return self.routes[0]
	def ranking(self):
		keys = ['possibility','RMSE','TRMSE','area','CLength']
		for key in keys:
			self.best_ranking(key)
			rank = 1
			for route in self.routes:
				route[key+'_Rank']=rank
				rank+=1
		self.ranked = True
	def corr(self):
		index=['RMSE','TRMSE','area','CLength']
		index_Rank = [e+'_Rank' for e in index]
		for i in index:
			setattr(self,i+'_corr',pearsonr([route[i] for route in self.routes],[route['possibility'] for route in self.routes]))
		for i in index_Rank:
			setattr(self,i+'_corr',pearsonr([route[i] for route in self.routes],[route['possibility_Rank'] for route in self.routes]))

