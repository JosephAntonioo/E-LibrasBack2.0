from typing import Sized
from flask.wrappers import Request
from werkzeug.utils import redirect, secure_filename
from MediaPipe.mediapipeMain import handtracked
from flask import Flask, request, flash,jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands
import json
import base64
import re
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import cv2
import io

## Start Stuffs
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
## Start Stuffs

def decode_base64(data, altchars=b'+/'):
    """Decode base64, padding being optional.

    :param data: Base64 data as an ASCII byte string
    :returns: The decoded byte string.

    """
    data = re.sub(rb'[^a-zA-Z0-9%s]+' % altchars, b'', data)  # normalize
    missing_padding = len(data) % 4
    if missing_padding:
        data += b'='* (4 - missing_padding)
    return base64.b64decode(data, altchars)


class HelloWorld(Resource):
    def get(self):
        handtracked()
        return {"data" : "Hello World"}


# Método Get que leva a um def com uma img já setada, usa isso como base para o post
class HandTracked(Resource):
    def get(self):
        return handtracked()

# Método post já recebe a img em base64 por string em um json que é alocada em uma const aqui
class ImgString(Resource):
    def post(self):
        data = request.json
        dataI = str(jsonify(data).data)
        print(str.__sizeof__(dataI))
        print(dataI)
        return dataI



        




api.add_resource(HelloWorld, "/helloworld")
api.add_resource(HandTracked, "/hts")
api.add_resource(ImgString, "/post")
##Starta o server no debugger mode entao devmode
if __name__ == "__main__":
	app.run(debug=True, host= '0.0.0.0')