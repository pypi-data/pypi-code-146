import numpy as np
from typing import Union


def euclidean_distance(array_1, array_2):
    if isinstance(array_1, np.ndarray)==False:
        array_1 = np.array(array_1)
    if isinstance(array_2, np.ndarray)==False:
        array_2 = np.array(array_2)
    
    distance = np.linalg.norm(array_1-array_2)
    return distance


def create_clusters(elements:Union[list, tuple, np.ndarray], distance_threshold:Union[float, int], sort=False) -> Union[list, np.ndarray]:
    #checks    
    assert len(elements)>0, "input list is empty"
    assert len(elements)<=1000000, "found more than 1 Million elements in input list"
    assert distance_threshold>=0.0, "distance threshold cannot be negative"
    
    if isinstance(elements, np.ndarray)==False:
        elements = np.array(elements).squeeze()
    
    if sort:
        elements = np.sort(elements, axis=0)

    # ragged means internal elements are of different dimensions
    is_ragged = (elements.dtype==object)  
    
    if is_ragged:
        raise ValueError("Input array is ragged. Please make sure all the internal elements are of same dimension") 

    #squeezing to get rid of empty dimensions
    elements = elements.squeeze()
    
    leaders = []
    clusters = []

    for element in elements:
        cluster_found = False
    
        for idx in range(len(leaders)):
            distance = euclidean_distance(leaders[idx],element)
            if distance<=distance_threshold:
                clusters[idx].append(element)
                cluster_found = True
                break

        if not cluster_found:
            leaders.append(element)
            clusters.append([element])
    
    num_clusters = len(leaders)
    
    return num_clusters, leaders, clusters
