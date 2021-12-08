<!-- ABOUT THE PROJECT -->
## About the project

This project implements several unsupervised clustering algorithms based on centroids from scratch with parameters to tweak them to your liking and some other options to play with. 

Currently implemented are:
- `Partition around medoids (PAM) Clustering`
- `Naive k-mean clustering (Lloyd's algorithm)`
- `MacQueens k-mean clustering`

## Prerequisites

- `Python ≥3.10.0`

## Installation

Just clone the repository, extract the python file and you are ready to go! Make sure to read the description of the function `c_clustering` to fully understand on how to use it (or see `Parameters` below)

## Parameters & Return values

**Parameters**

- `data`: Your Input - Has to be a list of numeric vectors of equal shape
- `boundaries`: Specifies	the space for centroid generation. It will be calculated automatically if it isn't specified but could be useful for testing purposes. Has to be a set of n tuples [(min,max),...], where n = dimension of your used datapoints.
- `dist`: Used distance metric. Currently available are: "manhattan"
- `ver`: Specifies the clustering variant. Currently available are: "llyod", "queen", "PAM"
- `epochs`: How often the specified algorithm should run over the dataset 
- `k`: Number of centroids
- `centroids`: Start position of centroids (They will be randomly generated inside the boundary space if not specified). The shape must be equal to your datapoint vector

**Returns**

-	`label`		: A list which contains the label of each data point (same order as your input). It contains only positive integers whose are ≤ k
-	`centroids`: 	A list which contains the position of each centroid. Consists of k sublists, which have always the same dimension as a datapoint in 'data'

<!-- LICENSE -->
## License

Distributed under the Apache License 2.0 License. See `LICENSE.txt` for more information.
