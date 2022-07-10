# .env
# Import dependencies
import os
import rtree
from rtree import Rtree
import rtree
import random
import numpy as np
import pickle
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
OUTPUT_ENCODING_PATH = os.path.join(OUTPUT_FOLDER_NUMPY_BINARY, "encodings.pkl")

def enconding_image(file_img):
    file_encoding = face_recognition.face_encodings(file_img)
    if file_encoding != []:
        return file_encoding[0]
    raise Exception("No enconding processed")

"""Enconding images of dataset"""
class EncondingImages:
    def __init__(self, N: int, type : str = "created"):
        self.data_enconding = dict()
        self.N = N
        self.type = type

    def get(self):
        # Verifiy if encoding file exists
        if os.path.exists(OUTPUT_ENCODING_PATH) and self.type != "created":
            with open(OUTPUT_ENCODING_PATH, "rb") as f:
                # TODO: Test Here
                self.data_enconding = pickle.load(f)
            return self.data_enconding

        # If not exists forced or previous data, process
        counter = 0

        for folder in os.listdir(LFW_PATH):
            image_path = os.path.join(LFW_PATH,folder)
            if counter > self.N: break
            for file in os.listdir(image_path):
                file_src = os.path.join(image_path,file)
                file_img = face_recognition.load_image_file(file_src)
                file_enconding = face_recognition.face_encodings(file_img)
                # If file_encoding is processed corrected
                if file_enconding != []:
                    # assign file source and encoding
                    self.data_enconding[file] = file_enconding[0]
                    counter += 1
                else:
                    print(file_src, "is not working")
                if counter % 10 == 0: print("Image processed", counter)
            if counter > self.N: break

        # Save encodings
        with open(OUTPUT_ENCODING_PATH, "wb") as f:
            pickle.dump(self.data_enconding, f)

        return self.data_enconding


class KNN:
    def _range_search(self,Q : np.ndarray, D : dict, r : float):
        result = []
        for id, row in D.items():
            dist = euclidean_distance(Q, row)
            if dist < r:
                result.append((id, dist))
        return result

    def _priority_search(self,Q : np.ndarray, D : dict, k : int):
        # TODO: Change to priority queue
        result = []
        for id, row in D.items():
            dist = euclidean_distance(Q, row)
            result.append((id, dist))
        result.sort(key=lambda y: y[1])
        return result[:k]

    def get_priority(self, Q: np.ndarray,data_encoding : dict, k: int):
        return self._priority_search(Q, data_encoding, k)

    def get_search(self, Q: np.ndarray, data_encoding: dict, r: float):
        return self._range_search(Q, data_encoding, r)

class KNN_RTree:
    def __init__(self, type: str = "create"):
        self._is_builded = False
        self._ind = None
        self.type = type
    def _build(self, data_encoding : dict):
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
        for i, value in enumerate(data_encoding.values()):
        # for i in range(data_encoding.shape[0]):
            # print("Key: ", key)
            # print("Value: ", value)
            self._ind.insert(i, tuple(value))

    def get(self,Q: np.ndarray,data_encoding : dict, k: int):
        output = []
        keys = list(data_encoding.keys())
        self._build(data_encoding=data_encoding)
        # if not self._is_builded or self.type == "create":
        #     self._build(data_encoding)
        #     self._is_builded = True
        query = tuple(Q)
        for p in self._ind.nearest(query, num_results=k):
            # TODO: Verify if self._ind.bounds is correct
            output.append((keys[p], self._ind.bounds[p]))
            # output.append(p)
        # # print("First: ", self._ind.bounds[1])
        return output

class KD_Tree:
    def __init__(self):
        pass
    def get(self,data_encoding : dict, Q: np.ndarray, k, leaf_size=3):
        output = []
        keys = list(data_encoding.keys())
        enconding = list(data_encoding.values())
        tree = KDTree(enconding, leaf_size=leaf_size)
        q_reshaped = Q.reshape(1,-1)
        dist, ind = tree.query(q_reshaped, k)
        for indexes in ind[0]:
            output.append(keys[indexes])
        # print("Dist: ", dist)
        # print("Ind: ", ind)
        return output