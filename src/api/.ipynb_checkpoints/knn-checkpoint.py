# Import libraries
import os
import random
import numpy as np
import face_recognition
from queue import PriorityQueue
from abc import ABC, abstractmethod
from importlib.resources import path

# import pandas as pd
# import matplotlib.pyplot as plt


# Available extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
SCANIFY_DIRECTORY = ""


# General path for LFW

# TODO: Change with os.path
lfw_path = "/home/moralespanitz/UTEC/Advanced-Databases/Lab10.0/lfw"

# General methods
def euclidean_distance(Q, row):
    return np.sqrt(np.power(np.sum(Q-row), 2))

class KNN(ABC):
    def __init__(self, file_stream : str):
        self.data_row = dict()
        self.vector_dist = list()

    def upload(self, file_stream : str):
        if (file_stream is None): return
        upload_image = face_recognition.load_image_file(file_stream)
        unknown_face_encodings = face_recognition.face_encodings(upload_image)
        return unknown_face_encodings
    def compute(self):
        for folder in os.listdir(lfw_path):
            image_path = os.path.join(path, folder)
            for image in os.listdir(image_path):
                image_src = os.path.join(image_path, image)
                self.data_row[image] = face_recognition.load_image_file(image_src)

    @abstractmethod
    def get(self, N):
        pass
    
class KNN_Range(KNN):
    def __init__(self,radius):
        self.radius = radius

    def _range_search(Q, D, r):
        result = []
        for id, row in D.iterrows():
            dist = euclidean_distance(Q,row)
            if dist < r:
                result.append(dist)
        return result

    def get(self, N):
        for i in range(N):
            obj_1 = random.choice(list(self.data_row.values()))
            obj_2 = random.choice(list(self.data_row.values()))
            dist = self._range_search(obj_1, obj_2, self.radius)
            self.vector_dist.append(dist)


class KNN_Priority(KNN):
    def __init__(self, ktop):
        self.ktop = ktop
    def _priority_search(Q, D, k):
        result = PriorityQueue()
        for id, row in D.iterrows():
            dist = euclidean_distance(Q,row)
            result.put(dist)
        # TODO: Change with k return
        return result
    def get(self, N):
        for i in range(N):
            obj_1 = random.choice(list(self.data_row.values()))
            obj_2 = random.choice(list(self.data_row.values()))
            dist = self._priority_search(obj_1, obj_2, self.ktop)
            self.vector_dist.append(dist)
