from email import message
from flask import Blueprint, Response
api = Blueprint('api', __name__)

"""Sequential Controlers"""
@api.get("/sequential")
def get_sequential():
    return "<h1>Sequential</h1>"

@api.post("/sequential")
def post_sequential():
    return "<h1> Hello sequential </h1>"

"""KNN R-Tree Controllers"""
@api.get("/knn-rtree")
def get_knnrteee():
    return "KNN R-Tree"

@api.post("/knn-rtree")
def post_knnrtree():
    return "<h1> Hello knn-rtree </h1>"
"""KNN-HighD Controllers"""
@api.get("/knn-highd")
def get_knnhighd():
    return "KNN HighD"

@api.post("/knn-highd/*")
def post_knnhighd():
    response = Response(status=200, message="Set type of KNN-HighD" )
    return response
