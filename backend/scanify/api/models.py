# Import dependencies
import os
import rtree
import random
import dotenv
import numpy as np
from sqlite3 import DataError
import matplotlib.pyplot as plt
from .utils import euclidean_distance
# Initialize dotenv
dotenv.dotenv_values()

# Data representation
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# General path for LFW
LFW_PATH = dotenv.get("LFW_PATH")


"""Enconding images of dataset"""


class EncondingImages:
    def __init__(self, N: int):
        self.data_enconding = []
        self.data_enconding_reference = dict()
        self.N = N

    def get(self):
        # Verifiy if encoding file exists
        if os.path.exists("./encoding.npy"):
            self.data_enconding = np.load("./encoding.npy")
            self.data_enconding_reference = np.load("./encoding_reference.npy")
        for folder in os.listdir(LFW_PATH):
            for file in os.listdir(os.path.join(LFW_PATH, folder)):
                file_src = os.path.join(folder, file)
                file_load = face_recognition.load_image_file(file_src)
                file_encoding = face_recognition.face_encodings(file_load)
                if len(file_encoding) > 0:
                    # TODO: El enconding_reference guarda el id de cada imagen. Corregir para dict
                    self.data_enconding.append(file_encoding[0])
                    self.data_enconding_reference[file_src] = file_src
                else:
                    print("No encodings found for file: {}".format(file_src))
            self.data_enconding = np.array(self.data_enconding)
            # Save encodings
            np.save(os.path.join(os.getcwd(), "encodings.npy"),
                    self.data_enconding)
            np.save(os.path.join(os.getcwd(), "encodings_reference.npy"),
                    self.data_enconding_reference)
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
        
    def get(self, Q: np.ndarray, k : int):
        output = []
        if not self._is_builded:
            self._build()
        for i in range(self.data_encoding.shape[0]):
            self.ind.insert(i, tuple(data_enconding[i]))
        query = tuple(Q)
        for p in self.ind.nearest(query, k=k):
            output.append(p)
        return output
        
