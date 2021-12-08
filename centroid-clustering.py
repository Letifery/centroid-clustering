from warnings import warn
from random import randint, sample
from copy import deepcopy
from math import inf

class CentroidClustering():
	def c_clustering(
		self, 
		data:[[float]], 
		boundaries:[(float,float)]=None, 
		dist:str="manhattan", 
		ver:str="lloyd", 
		epochs:int=10, 
		k:int=3, 
		centroids:[[float]]=None) -> [int,[float]]:
		
		'''
		Implements some centroid based clustering algorithms on n-dimensional data
		
		Parameters
		------------
		data		:Your Input - Has to be a list of numeric vectors of equal shape
		boundaries	:Specifies the space for random centroid generation. It will be calculated 
					automatically if specified but could be useful for testing purposes. 
					Has to be a list of n tuples [(min,max),...], where n = dimension
		dist 		: Used distance metric. Currently available are: "manhattan"
		ver 		: Specifies the clustering variant. Currently available are: "llyod", "queen", "PAM"
		epochs	 	: How often kmeans should run over each iteration
		k			: Number of centroids
		centroids	: Start position of centroids (will be random if not specified). 
					The shape must be equal to your datapoint vector
					  
		Returns
		------------
		label		: A list which contains the label of each data point. Label contains
					only positive integers whose are <=k
		centroids	: A list which contains the position of each centroid. Consists of k
					sublists, which have always the same dimension as a datapoint in 'data'
		'''
		
		if ver != "PAM" and boundaries is None:
			boundaries_max = list(map(max, zip(*data)))
			boundaries_min = list(map(min, zip(*data)))
		
		if centroids is None:
			if ver != "PAM":
				if boundaries is None:
					centroids = [[randint(boundaries_min[x], boundaries_max[x]) for x in range(len(boundaries_max))] for _ in range(k)]
				else:
					centroids = [[randint(boundaries[x][0], boundaries[x][1]) for x in range(len(boundaries))] for _ in range(k)]
			else:
				centroids = sample(data, k)
		
		dist, label = [None]*k, [[None] for _ in data]
		
		match ver:
			case "lloyd":
				for z in range(epochs):
					#Calculates the distance with the specific metric of a centroid to each data point
					for i in range(k):
						dist[i] = self.calc_distance(centroids[i], data)
					#Each data point receives the label corresponding to the index of the closest centroid
					for i in range(len(data)):
						tmp = [x[i] for x in dist]
						label[i] = min(range(len((tmp))), key=tmp.__getitem__)
					#Calculates the new position of each centroid; The position is the mean over each
					#datapoint where the label is equal to the index of the centroid (therefore in the same group)
					for i in range(k):
						pos = [data[x] for x in range(len(data)) if label[x] == i]
						centroids[i] = [sum(x)/len(x) for x in zip(*pos)] if pos != [] else centroids[i]
					
			case "queen":
				for z in range(epochs):
					for i in range(len(data)):
						tmp = self.calc_distance(data[i], centroids)						#Calculating distance of datapoint[i] to each centroid
						label[i] = min(range(len((tmp))), key=tmp.__getitem__)				#Get index(=centroid) of smallest distance
						pos = [data[x] for x in range(len(label)) if label[x] == label[i]]	#Calculating new position
						centroids[label[i]] = [sum(x)/len(x) for x in zip(*pos)] if pos != [] else centroids[i]

			case "PAM":
				best_cost, best_centroid, tmp_label = inf, [], [[None] for _ in data]
				for z in range(epochs):
					#Calculates the distance with the specific metric of a centroid to each data point
					for i in range(k):
						dist[i] = self.calc_distance(centroids[i], data)
					#Each data point receives the label corresponding to the index of the closest centroid
					cost = 0
					for i in range(len(data)):
						tmp = [x[i] for x in dist]
						tmp_label[i] = min(range(len((tmp))), key=tmp.__getitem__)
						cost += dist[tmp_label[i]][i]										
					if best_cost > cost: 
						label, best_cost, best_centroid = deepcopy(tmp_label), deepcopy(cost), deepcopy(centroids)
					#Takes one random centroid and reassigns it to another random point which isn't currently a centroid.
					centroids[randint(0,k-1)] = sample(list(set(centroids)^set(data)), 1)[0]
				centroids = best_centroid
					
			case _:
				raise NameError("[ERROR] K-Means variant '%s' doesn't exist" % ver)			
		return (label, centroids)	
	
	def calc_distance(self, centroid, data:[(int,int)], ver="manhattan") -> [float]:
		centroid_distance = [None]*len(data)			
		
		match ver:
			case "manhattan":
				for i in range(len(data)):
					centroid_distance[i] = abs(centroid[0]-data[i][0])+abs(centroid[1]-data[i][1])
			case _:
				warn("\n[WARNING] Distance metric '%s' doesn't exist. Will use Manhattan metric instead..." % ver)
				centroid_distance = self.calc_distance(centroid, data)		#Might be possible to jump directly to case "manhattan"
		return(centroid_distance)
		
		
		
#data = [[randint(0,10),randint(0,10)] for x in range(80)]
data = [(2,10),(2,8),(2,5),(1,2),(2,3),(4,8),(7,4),(6,2),(8,4),(8,2)]
start = [(2,10),(1,2),(8,4)]
cm = CentroidClustering()
label, centroid = cm.c_clustering(data, ver="PAM", epochs=250)
import matplotlib.pyplot as plt
x,y = zip(*data)
plt.scatter(x,y, c=label)
x,y = zip(*centroid)
plt.scatter(x,y, c="red", s=200)
plt.show()
