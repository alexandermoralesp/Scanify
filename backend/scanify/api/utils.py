"""
General functions
"""
# Import dependencies
import numpy as np

"""
Euclidean distance:
Q: query
feature_vector: vector representation of image
return np.ndarray
"""
def euclidean_distance(Q, feature_vector):
    return np.sqrt(np.power(np.sum(Q-feature_vector), 2))


