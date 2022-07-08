# Import dependencies
import numpy as np


def euclidean_distance(Q, row):
    return np.sqrt(np.power(np.sum(Q-row)))


