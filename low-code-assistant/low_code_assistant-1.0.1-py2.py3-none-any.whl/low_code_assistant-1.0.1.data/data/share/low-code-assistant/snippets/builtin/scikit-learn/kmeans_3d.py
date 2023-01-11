# author: Maarten Breddels
# date: Wed 8 Sep 2022
# requires plotly and scikit-learn:
#  pip install plotly scikit-learn
# scikit learn documentation:
#   https://scikit-learn.org/stable/modules/generated/sklearn.cluster.KMeans.html
import numpy as np
import plotly.express as px
from sklearn.cluster import KMeans

df = px.data.iris()


xcol, ycol, zcol = "petal_length", "sepal_length", "sepal_width"

X = np.array(df[[xcol, ycol, zcol]])
kmeans = KMeans(n_clusters=3, random_state=0).fit(X)
df["cluster_id"] = kmeans.predict(X)

print("Cluster centers:\n", kmeans.cluster_centers_)

#
fig1 = px.scatter_3d(df, xcol, ycol, zcol, color="species", title="Species from data")
fig2 = px.scatter_3d(df, xcol, ycol, zcol, color="cluster_id", title="Clusters found using k-means clustering")
display(fig1, fig2)
