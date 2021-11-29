from typing import Sized
from flask.sessions import NullSession
from flask.wrappers import Request, Response
import numpy as np
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
import asyncio
from modulos import alfabeto 
import MediaPipeHP
import os
## Start Stuffs
app = Flask(__name__)
api = Api(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# db = SQLAlchemy(app)
## Start Stuffs

# class HelloWorld(Resource):
#     def get(self):
#         handtracked()
#         print('deu boa')
#         return {"data" : "Hello World"}

# class HandTracked(Resource):
#     def get(self):
#         return handtracked()

# class ImgPost(Resource):
#     def post(self):

#         file = request.files['image']
#         img = Image.open(file.stream)
#         handtracked(img)
#         return jsonify({'msg':'sucess','size':[img.width, img.height]}) 

async def teste():
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
    statusCode  =  HT.srcPicture('./' + nome)
    fin = time.time()
    print('final do  metodo:')
    print(fin)
    temp = fin - ini
    print('tempo de execução:')
    print(temp)
    print('statusCode: ')
    letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W']
    print(letras[statusCode])
    return {'data':letras[statusCode]}

@app.route('/post', methods = ['POST'])
async def upload_file():
    ini = time.time()
    print('inicio do metodo:')
    print(ini)
    #Aqui precisa mt rodar um metodo pegando essa img entao vamos la
    file = request.files['imgData']
    img = Image.open(file.stream)
    nome = 'teste.jpg'
    img.save(nome)
    #Aqui temos um metodo para selecionar a img e processar os pontos chave das mãos, deixa salvo a img com os pontos
    #Logo em seguida processa os pontos chave da mão para fazer uma leitura de como ela está
    #Porfim passa pelo array de array do alfabeto assim concluindo o metodo
    #Caso tudo ocorra bem o retorno é a letra do alfabeto correspondente ao gest
    #Por enquanto retornos de teste 
    
    statusCode = await HT.final('./' + nome)
    fin = time.time()
    print('final do  metodo:')
    print(fin)
    temp = fin - ini
    print('tempo de execução:')
    print(temp)
    print('statusCode: ')
    letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W']
    print(statusCode)
    return {'data':statusCode}

@app.route('/hw', methods = ['GET'])
def hw():
    return 'Hello World!'

@app.route('/mediapipe', methods= ['POST'])
async def teste():
    file = request.files['imgData']
    file.seek(0, os.SEEK_END)
    if file.tell() == 0:
        return 'Nao contem imagem!'
    img = Image.open(file.stream)
    nome = 'teste.png' #Mudar nome da img
    img.save(nome) #Salvar img é importante para o media pipe, final do metodo pode excluir eu acho
    print('ok')
    statusCode = await MediaPipeHP.handPoseM('./' + nome) #Aqui ele envia o path da img e retorna uma lista dos pontos mas sem tratar é uma strng enorme chatona de pegar os pontos replace ajuda
    if(statusCode == 'Nao foi possivel identificar a mao!'):
        return statusCode
    pontosHP = [] #Var para tratar e armazenar pontos elevado a 1000 para ficar como int
    print(statusCode.count)
    # print(statusCode)
    j = 0
    #float to int ponto * 1000
    # For para percorrer a string de cada ponto letra por letra,
    # Assim que chegar no x e no y pega os valores nas casas seguintes
    # Armazena esses valores em variaveis x y
    # Multiplica por 1000 para ajudar na visualização e comparação dos dados
    # Salva o ponto(x,y)
    # Salva o ponto em pontos(ponto(x,y))
    for pontos in statusCode:
        # print('j:',j)
        ponto = str(pontos)
        pontoX = 0
        pontoY = 0 
        # print(ponto)
        i = 0
        for l in ponto:
            # print('i:',i)
            if(l == 'x'):
                # print(ponto[i+3:i+10])
                pontoX = float(ponto[i+3:i+10]) 
                pontoX = pontoX * 1000
                pontoX = int(pontoX)
                # print(str(pontoX))
            if(l == 'y'):
                # print(ponto[i+3:i+10])
                pontoY = float(ponto[i+3:i+10]) 
                pontoY = pontoY * 1000
                pontoY = int(pontoY)
                
                # print(str(pontoY))
            i+=1
        final = [pontoX,pontoY]
        pontosHP.append(final)
        j+=1
    print(pontosHP)
    print('[x,y]:', j)
    # if(j == 0):
    #     return 'Nao foi possivel identificar a mao!'
    print('letras para pegar o x e y:', i)                
    print(pontosHP[1])

    # ------------- Leitura dos gestos
    print('--------Descrição Gesto')
    descricaoGesto = await HT.MediaPipeTranslate(pontosHP)
    print(descricaoGesto)

    # ------------- Comparação das descrições dos gestos
    print('--------Comparação Gesto')
    letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'L', 'M', 'N', 'O[BUG]', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W']
    indexAlfabeto = -1
    for i, a in enumerate(alfabeto.letras):
            if(alfabeto.letras[i] == descricaoGesto):
                print('I(index do alfabeto):')
                print(i)
                print('A(descricao do gesto):')
                print(a)
                print('Deu boa!!!!!!!!')
                final = []
                final.append(a)
                print('ok')
                print(a)
                final.append(i)
                indexAlfabeto = i
                break
    if(indexAlfabeto != -1):
        print('Index encontrado:', indexAlfabeto)
        if(indexAlfabeto < len(letras)):
            print(letras[indexAlfabeto])
            return {'data':str(letras[indexAlfabeto])}
    else:
        print('Nao foi possivel identificar o gesto!')
        return 'Nao foi possivel identificar o gesto!'

#method, request route [END POINT]
# api.add_resource(HelloWorld, "/helloworld")
# api.add_resource(HandTracked, "/hts")
# api.add_resource(ImgPost, "/post")


##Starta o server no debugger mode entao devmode
if __name__ == "__main__":
	app.run(debug=True, host= '0.0.0.0')