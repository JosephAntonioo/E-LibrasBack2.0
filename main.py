from typing import Sized
from flask.wrappers import Request, Response
from werkzeug.utils import redirect, secure_filename
from flask import Flask, request, flash,jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
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
import HT
import time
import json


## Start Stuffs
app = Flask(__name__)
api = Api(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db = SQLAlchemy(app)
## Start Stuffs

class HelloWorld(Resource):
    def get(self):
        # handtracked()
        print('deu boa')
        return {"data" : "Hello World"}

class HandTracked(Resource):
    def get(self):
        return handtracked()

class ImgPost(Resource):
    def post(self):

        file = request.files['image']
        img = Image.open(file.stream)
        handtracked(img)
        return jsonify({'msg':'sucess','size':[img.width, img.height]}) 

@app.route('/post', methods = ['POST'])
def upload_file():
   ini = time.time()
   print('inicio do metodo:')
   print(ini)
   #Aqui precisa mt rodar um metodo pegando essa img entao vamos la
   file = request.files['imgData']
   img = Image.open(file.stream)
   nome = 'teste.png'
   img.save(nome)
   #Aqui temos um metodo para selecionar a img e processar os pontos chave das mãos, deixa salvo a img com os pontos
   #Logo em seguida processa os pontos chave da mão para fazer uma leitura de como ela está
   #Porfim passa pelo array de array do alfabeto assim concluindo o metodo
   #Caso tudo ocorra bem o retorno é a letra do alfabeto correspondente ao gest
   #Por enquanto retornos de teste 
   statusCode = HT.srcPicture('./' + nome)
   fin = time.time()
   print('final do  metodo:')
   print(fin)
   temp = fin - ini
   print('tempo de execução:')
   print(temp)
   print('statusCode: ')
   print(statusCode)
   return {'data':statusCode}

#method, request route
api.add_resource(HelloWorld, "/helloworld")
api.add_resource(HandTracked, "/hts")
# api.add_resource(ImgPost, "/post")


##Starta o server no debugger mode entao devmode
if __name__ == "__main__":
	app.run(debug=True, host= '0.0.0.0')