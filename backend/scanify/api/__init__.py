import json
import os
import dotenv
from models import *
from flask import Blueprint, Response, jsonify, request
from werkzeug.utils import secure_filename
api = Blueprint('api', __name__)
load_dotenv()
UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER')

"""Sequential Controlers"""
# localhost/api/sequential
@api.post("/sequential")
def post_sequential():
    if request.data:
        data = json.loads(request.data)
        # If data type doesnt exists
        if not data.get("type"):
            return Response(jsonify({"error": "Missing type"}), 400)
        # If data type is not a valid type
        if data.get("type") not in ["range", "priority"]:
            return Response(jsonify({"error": "Type must be either range or priority"}), 400)

        # Ratio is k or r in KNN
        if isinstance(data.get("ratio"), int):
            return Response(jsonify({"error": "Missing ratio"}), 400)
        ratio = data.get("ratio")
        assert(isinstance(ratio, int))
        # Golbal KNN
        sequential_knn = KNN()
        N = 0
        if not data.get("cantidad"):
            N = 10
        else:
            N = data.get("cantidad")
        # If data type is range
        if data.get("type") == "range":
            # TODO: Change img_filename to real filename
            pic = request.files["img_filename"]
            if not pic:
                return Response(jsonify({"error": "Missing img_filename"}), 400)
            # Query is a feature vector of uploaded image
            query = enconding_image(pic)
            # type="create" for generate encodings, "passed" for load encodings
            data_encoding = EncondingImages(N, type="passed").get()

            output = sequential_knn.get_search(query, data_encoding, ratio)
            # filename = secure_filename(pic.filename)
            # pic.save(os.path.join(UPLOAD_FOLDER, filename))
            return Response(jsonify({"success": 200, data: output}), 200)
        if data.get("type") == "priority":
            pic = request.files["img_filename"]
            if not pic:
                return Response(jsonify({"error": "Missing img_filename"}), 400)
            query = enconding_image(pic)
            data_encoding = EncondingImages(N, type="passed").get()
            output = sequential_knn.get_priority(query, data_encoding, ratio)
            # filename = secure_filename(pic.filename)
            # pic.save(os.path.join(UPLOAD_FOLDER, filename))
            return Response(jsonify({"success": 200, data: output}), 200)
    return Response(status=400)

"""KNN R-Tree Controllers"""
# localhost/api/knn-rtree
@api.post("/knn-rtree")
def post_knnrtree():
    if request.data:
        data = json.loads(request.data)# If data type doesnt exists
        if not data.get("type"):
            return Response(jsonify({"error": "Missing type"}), 400)
        # If data type is not a valid type
        if data.get("type") not in ["range", "priority"]:
            return Response(jsonify({"error": "Type must be either range or priority"}), 400)

        # Ratio is k or r in KNN
        if isinstance(data.get("ratio"), int):
            return Response(jsonify({"error": "Missing ratio"}), 400)
        ratio = data.get("ratio")
        assert(isinstance(ratio, int))
        # Golbal KNN
        sequential_knn = KNN_RTree()
        N = 0
        if not data.get("cantidad"):
            N = 10
        else:
            N = data.get("cantidad")
        # If data type is range
        if data.get("type") == "range":
            # TODO: Change img_filename to real filename
            pic = request.files["img_filename"]
            if not pic:
                return Response(jsonify({"error": "Missing img_filename"}), 400)
            # Query is a feature vector of uploaded image
            query = enconding_image(pic)
            # type="create" for generate encodings, "passed" for load encodings
            data_encoding = EncondingImages(N, type="passed").get()

            output = sequential_knn.get(query, data_encoding, ratio)
            # filename = secure_filename(pic.filename)
            # pic.save(os.path.join(UPLOAD_FOLDER, filename))
            return Response(jsonify({"success": 200, data: output}), 200)
    return Response(status=400)

"""KNN-HighD Controllers"""
# localhost/api/knn-rtree
@api.post("/knn-highd/*")
def post_knnhighd():
    if request.data:
        data = json.loads(request.data)# If data type doesnt exists
        if not data.get("type"):
            return Response(jsonify({"error": "Missing type"}), 400)
        # If data type is not a valid type
        if data.get("type") not in ["range", "priority"]:
            return Response(jsonify({"error": "Type must be either range or priority"}), 400)

        # Ratio is k or r in KNN
        if isinstance(data.get("ratio"), int):
            return Response(jsonify({"error": "Missing ratio"}), 400)
        ratio = data.get("ratio")
        assert(isinstance(ratio, int))
        # Golbal KNN
        sequential_knn = KD_Tree()
        N = 0
        if not data.get("cantidad"):
            N = 10
        else:
            N = data.get("cantidad")
        # If data type is range
        if data.get("type") == "range":
            # TODO: Change img_filename to real filename
            pic = request.files["img_filename"]
            if not pic:
                return Response(jsonify({"error": "Missing img_filename"}), 400)
            # Query is a feature vector of uploaded image
            query = enconding_image(pic)
            # type="create" for generate encodings, "passed" for load encodings
            data_encoding = EncondingImages(N, type="passed").get()

            output = sequential_knn.get(query, data_encoding, ratio)
            # filename = secure_filename(pic.filename)
            # pic.save(os.path.join(UPLOAD_FOLDER, filename))
            return Response(jsonify({"success": 200, data: output}), 200)
    return Response(status=400)