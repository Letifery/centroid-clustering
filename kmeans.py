import warnings
from random import randint

class KMeans():
	def kmeans(
		self, 
		data:[[float]], 
		boundaries:[(float,float)]=None, 
		dist:str="manhattan", 
		ver:str="lloyd", 
		epochs:int=10, 
		k:int=3, 
		centroids:[[float]]=None) -> [int,[float]]: 

		'''
		Implements the kmeans clusterization algorithm on n-dimensional data
		
		Parameters
		------------
		data		: Your Input - Has to be a list of numeric vectors of equal shape
		boundaries	: Specifies	the space for centroid generation. It will be calculated 
					  automatically if specified but could be useful for testing purposes. 
					  Has to be a list of n tuples [(min,max),...], where n = dimension
		dist		: Used distance metric. Currently available are: "manhattan"
		ver			: Specifies the kmeans variant. Currently available are: "llyod"
		epochs		: How often kmeans should run over each iteration
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
	
		if boundaries is None:
			boundaries_max = list(map(max, zip(*data)))
			boundaries_min = list(map(min, zip(*data)))
		
		if centroids is None:
			if boundaries is None:
				centroids = [[randint(boundaries_min[x], boundaries_max[x]) for x in range(len(boundaries_max))] for _ in range(k)]
			else:
				centroids = [[randint(boundaries[x][0], boundaries[x][1]) for x in range(len(boundaries))] for _ in range(k)]
		
		dist, label = [None]*k, [None]*len(data)
		
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
				pass
			case _:
				raise NameError("[ERROR] Kmeans Version '%s' doesn't exist" % ver)
				
		return (label, centroids)	
	
	def calc_distance(self, centroid, data:[(int,int)], ver="manhattan") -> [float]:
		centroid_distance = [None]*len(data)			
		
		match ver:
			case "manhattan":
				for i in range(len(data)):
					centroid_distance[i] = abs(centroid[0]-data[i][0])+abs(centroid[1]-data[i][1])
			case _:
				warnings.warn("\n[WARNING] Distance metric '%s' doesn't exist. Will use Manhattan metric instead..." % ver)
				centroid_distance = self.calc_distance(centroid, data)		#Might be possible to jump directly to case "manhattan"
		return(centroid_distance)
