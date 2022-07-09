# .env
# Import dependencies
import os
import rtree
from rtree import Rtree
import rtree
import random
import numpy as np
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
        if os.path.exists(os.path.join(LFW_PATH,"./encoding.npy")) and not self.type == "forced":
            self.data_enconding = np.load("./encoding.npy")
            self.data_enconding_reference = np.load("./encoding_reference.npy")
            return self.data_enconding
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
    def __init__(self):
        ...
    def _range_search(self,Q, D, r):
        result = []
        for i in range(len(D)):
            dist = euclidean_distance(Q, D[i])
            if dist < r:
                result.append((i, dist))
        return result

    def _priority_search(self,Q, D, k):
        # TODO: Change to priority queue
        result = []
        for i in range(len(D)):
            dist = euclidean_distance(Q, D[i])
            result.append((i, dist))
        result.sort(key=lambda y: y[1])
        return result[:k]

    def get_priority(self, Q: np.ndarray,data_encoding : np.ndarray, k: float):
        return self._priority_search(Q, data_encoding, k)

    def get_search(self, Q: np.ndarray, data_encoding: np.ndarray, r: float):
        return self._range_search(Q, data_encoding, r)

class KNN_RTree:
    def __init__(self, type: str = "create"):
        self._is_builded = False
        self._ind = None
        self.type = type
    def _build(self, data_encoding : np.ndarray):
        if os.path.exists("puntos.data"):
            os.remove("puntos.data")
        if os.path.exists("puntos.index"):
            os.remove("puntos.index")
        prop = rtree.index.Property()
        prop.dimension = 128
        prop.buffering_capacity = 3
        prop.dat_extension = "data"
        prop.idx_extension = "index"
        self._ind = rtree.index.Index("puntos", properties=prop)
        for i in range(data_encoding.shape[0]):
            self._ind.insert(i, tuple(data_encoding[i]))

    def get(self,Q: np.ndarray,data_encoding : np.ndarray, k: int):
        output = []
        if not self._is_builded or self.type == "create":
            self._build(data_encoding)
            self._is_builded = True
        query = tuple(Q)
        for p in self._ind.nearest(query, num_results=k):
            output.append(p)
        # print("First: ", self._ind.bounds[1])
        return output

class KD_Tree:
    def __init__(self):
        pass
    def get(self,data_encoding : np.ndarray, Q: np.ndarray, k, leaf_size=3):
        tree = KDTree(data_encoding, leaf_size=leaf_size)
        q_reshaped = Q.reshape(1,-1)
        dist, ind = tree.query(q_reshaped, k)
        return dist