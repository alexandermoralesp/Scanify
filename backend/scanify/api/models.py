# Import dependencies
import os
import rtree
import random
import numpy as np
from sqlite3 import DataError
from dotenv import load_dotenv
import face_recognition
from utils import euclidean_distance
from sklearn.neighbors import KDTree
# Initialize dotenv
load_dotenv()

# Data representation
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# General path for LFW
LFW_PATH = os.environ.get("LFW_PATH")
OUTPUT_FOLDER_NUMPY_BINARY = os.environ.get("OUTPUT_FOLDER_NUMPY_BINARY")

"""Enconding images of dataset"""
class EncondingImages:
    def __init__(self, N: int, type : str = "created"):
        self.data_enconding = []
        self.data_enconding_reference = dict()
        self.N = N
        self.type = type

    def get(self):
        # Verifiy if encoding file exists
        if os.path.exists("./encoding.npy") and self.type=="forced":
            self.data_enconding = np.load("./encoding.npy")
            self.data_enconding_reference = np.load("./encoding_reference.npy")
        counter = 0
        for folder in os.listdir(LFW_PATH):
            image_path = os.path.join(LFW_PATH,folder)
            if counter > self.N: break
            for file in os.listdir(image_path):
                file_src = os.path.join(image_path,file)
                file_img = face_recognition.load_image_file(file_src)
                file_enconding = face_recognition.face_encodings(file_img)
                if file_enconding != []:
                    self.data_enconding.append(file_enconding[0])
                    counter += 1
                else:
                    print(file_src, "is not working")
                if counter % 10 == 0: print("Image processed", counter)
            if counter > self.N: break
        self.data_enconding = np.array(self.data_enconding)
        # Save encodings
        np.save(os.path.join(OUTPUT_FOLDER_NUMPY_BINARY, "encodings.npy"), self.data_enconding)
        np.save(os.path.join(OUTPUT_FOLDER_NUMPY_BINARY, "encodings_reference.npy"), self.data_enconding_reference)
        return self.data_enconding


class KNN:
    def __init__(self, data_enconding: np.ndarray, k: int):
        self.data_enconding = data_enconding

    def _range_search(Q, D, r):
        result = []
        for i in range(len(D)):
            dist = euclidean_distance(Q, D[i])
            if dist < r:
                result.append((i, dist))
        return np.array(result)

    def _priority_search(Q, D, k):
        # TODO: Change to priority queue
        result = []
        for i in range(len(D)):
            dist = euclidean_distance(Q, D[i])
            result.append((i, dist))
        result.sort(key=lambda y: y[1])
        return result[:k]

    def get_priority(self, Q: np.ndarray, r: float):
        return self._priority_search(Q, self.data_enconding, r)

    def get_search(self, Q: np.ndarray, r: float):
        return self._range_search(Q, self.data_enconding, r)


class KNN_RTree:
    def __init__(self, data_encoding: np.ndarray):
        self.data_encoding = data_encoding
        self._is_builded = False
        self._prop = rtree.index.Property()
        self.ind = rtree.index.Index(properties=self._prop)

    def _build(self):
        if os.path.exists("puntos.data"):
            os.remove("puntos.data")
        if os.path.exists("puntos.index"):
            os.remove("puntos.index")
        self._ind = rtree.index.Index("puntos", self._prop)

    def get(self, Q: np.ndarray, k: int):
        output = []
        if not self._is_builded:
            self._build()
        for i in range(self.data_encoding.shape[0]):
            self.ind.insert(i, tuple(self.data_enconding[i]))
        query = tuple(Q)
        for p in self.ind.nearest(query, k=k):
            output.append(p)
        return output


class KD_Tree:
    def __init__(self, data_enconding: np.ndarray):
        self.data_enconding = data_enconding

    def get(self, Q: np.ndarray, k):
        tree = KDTree(self.data_enconding, leaf_size=3)
        dist, ind = tree.query(Q, k)
        return dist

# class PCA:
#     def __init__(self, data_enconding: np.ndarray):
#         self.data_enconding = data_enconding

#     def get(self, Q: np.ndarray, k):
