

import matplotlib.pyplot as plot
import seaborn as seasns; seasns.set()  
import numpy as nump
from sklearn.cluster import KMeans as skKMeans

from sklearn.datasets.samples_generator import make_blobs
X, y_true = make_blobs(n_samples=250, centers=4,
                       cluster_std=0.60, random_state=0)
plot.scatter(X[:, 0], X[:, 1], s=50);

plot.show()

kmeans_res = skKMeans(n_clusters=4)
kmeans_res.fit(X)
y_val_kmeans = kmeans_res.predict(X)

plot.scatter(X[:, 0], X[:, 1], c=y_val_kmeans, s=50, cmap='viridis')

centers = kmeans_res.cluster_centers_

plot.scatter(centers[:, 0], centers[:, 1], c='grey', s=200, alpha=0.5);

plot.show()