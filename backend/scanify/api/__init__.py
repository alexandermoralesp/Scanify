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
@api.post("/sequential")
def post_sequential():
    if request.data:
        data = json.loads(request.data)
        # If data type doesnt exists
        if not data.get("type"):
            return Response(jsonify({"error": "Missing type"}), 400)
        # If data type is not a string
        if not isinstance(data.get("type"), str):
            return Response(jsonify({"error": "Type must be a string"}), 400)
        # If data type is not a valid type
        if data.get("type") not in ["range", "priority"]:
            return Response(jsonify({"error": "Type must be either range or priority"}), 400)
        # If data type is range
        if data.get("type") == "range":
            # TODO: Change img_filename to real filename
            pic = request.files["img_filename"]
            if not pic:
                return Response(jsonify({"error": "Missing img_filename"}), 400)
            filename = secure_filename(pic.filename)
            pic.save(os.path.join(UPLOAD_FOLDER, filename))
            return Response(jsonify({"success": "[RANGE]: File uploaded"}), 200)
            # return "range"
        if data.get("type") == "priority":
            pic = request.files["img_filename"]
            if not pic:
                return Response(jsonify({"error": "Missing img_filename"}), 400)
            filename = secure_filename(pic.filename)
            pic.save(os.path.join(UPLOAD_FOLDER, filename))
            return Response(jsonify({"success": "[PRIORITY]: File uploaded"}), 200)
            # return "priority"
        # return Response(json.dumps(data), status=201, mimetype='application/json')
    return Response(status=400)

"""KNN R-Tree Controllers"""
@api.post("/knn-rtree")
def post_knnrtree():
    if request.data:
        data = json.loads(request.data)
        return Response(json.dumps(data), status=201, mimetype='application/json')
    return Response(status=400)

"""KNN-HighD Controllers"""
@api.post("/knn-highd/*")
def post_knnhighd():
    if request.data:
        data = json.loads(request.data)
        return Response(json.dumps(data), status=201, mimetype='application/json')
    return Response(status=400)