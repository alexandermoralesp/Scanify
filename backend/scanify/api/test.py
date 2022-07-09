# Test cases

"""Generate image encondings"""
from models import *

number_of_images = 1
enconding_images = EncondingImages(number_of_images)
encoding_values = enconding_images.get()
"""KNN Range Search Testing"""
# knn = KNN()
# print(knn.get_search(encoding_values[0],encoding_values, 1))
# print(knn.get_priority(encoding_values[0], encoding_values, 3))
# knn_rtree = KNN_RTree()
# print(knn_rtree.get(encoding_values[0],encoding_values, 2))
# kd_rtree = KD_Tree()
# print(kd_rtree.get(encoding_values, encoding_values[0], 2))

