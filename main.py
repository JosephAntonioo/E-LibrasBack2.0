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
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db = SQLAlchemy(app)
## Start Stuffs
class HelloWorld(Resource):
    def get(self):
        handtracked()
        return {"data" : "Hello World"}


class HandTracked(Resource):
    def get(self):
        return handtracked()

class ImgPost(Resource):
    def post(self):
        file = request.files['image']
        img = Image.open(file.stream)
        img.save('teste.jpg')
        handtracked()
        return jsonify({'msg':'sucess','size':[img.width, img.height]}) 


#method, request route
api.add_resource(HelloWorld, "/helloworld")
api.add_resource(HandTracked, "/hts")
api.add_resource(ImgPost, "/post")


##Starta o server no debugger mode entao devmode
if __name__ == "__main__":
	app.run(debug=True, host= '0.0.0.0')