# Test cases

"""Generate image encondings"""
from models import *
number_of_images = 1
enconding_images = EncondingImages(number_of_images)
encoding_values : dict = enconding_images.get()
# print(encoding_values)
"""KNN Range Search Testing"""
knn = KNN()
query = encoding_values.get("Boris_Trajkovski_0001.jpg")
# print(knn.get_search(query, encoding_values, 1))
print(knn.get_priority(query, encoding_values, 2))

# print(knn.get_search(np.ndarray(encoding_values.values[0]),encoding_values, 1))
# print(knn.get_priority(encoding_values[0], encoding_values, 3))
# knn_rtree = KNN_RTree()
# print(knn_rtree.get(encoding_values[0],encoding_values, 2))
# kd_rtree = KD_Tree()
# print(kd_rtree.get(encoding_values, encoding_values[0], 2))

