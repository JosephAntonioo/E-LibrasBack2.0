## Código serve para receber uma img, salvar ela com um nome fixo, desenhar os pontos nas maos salvar essa img tambem,
## E por fim retornar os pares_poses da imagem

import sys
import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

from modulos.alfabeto import A

sys.path.append('./modulos/')
#sys.path



import extrator_POSICAO as posicao
import extrator_ALTURA as altura
import extrator_PROXIMIDADE as proximidade
import alfabeto as alfabeto
import cv2



def srcPicture(img):
    # print('ok')
    img = cv2.imread(img, flags=cv2.IMREAD_COLOR)
    # print(img)
    pontos = handTrack(img)
    verifDedos(pontos)
    verifProxi(pontos)
    resultado = []
    resultado = leituraGesto(pontos)
    descricaoG = resultado
    # print('Descrição do gesto :')
    print(descricaoG)
    # print('Letra Index :')
    # print(indexLetra)
    str1 = ''.join(descricaoG)
    finalS = 'Descrição do gesto :' + str1
    #Agora precisa rodar um metodo para fazer os parangole de sc
    return finalS

def handTrack(img):
    #Modulo extrator:
        #ALTURA: verifica se um ponto está acima ou abaixo de outro ponto
        #POSICAO: funcoes para verificar se os dedos estao dobrados ou esticados, horizontal vertical
        # tambem recebe o resultado do modulo altura para saber em que posicao a mao estao acima ou abaixo
        #PROXIMIDADE: funcoes que compara a proximidade entre os pontos detectados, se o resultado de posicao
        # for igual dobrado para o indicador e dedo medio e ambos estiverem na mesma altura entao eles estao proximos
    
    #ALFABETO***: apos extrair todas as caracteristicas foi melhorado o alfabeto de caracteristicas base,
    # onde um vetor de vetores recebe o resultado de todos os modulos extratores. Assim usamos este modulo para
    # para compara com uma nova analise (nova img) de entrada

    # ANOTAÇÕES PARA CORRIGIR POSSIVELMENTE COM MACHINE LEARNING E ANALISE DE DADOS COM TESTES AUTOMATIZADOS DE ENTREVISTAS COM TRADUÇÃO PARA LIBRAS E TRANSCRIÇÕES 

    # Não foram usadas as letras: H, J, K, X, ,Y , Z devido ao movimento adicional para a execução correta das letras.

    # Estas letras podem ser analisadas em uma função diferente, semelhante a função de análise de posicionamento do corpo, onde comparamos a transição entre pontos

    # Letra T: para o dedo polegar, devido a estar sobreposto pelo dedo indicador, o algoritmo não reconhece os pontos da ponta do dedo

    # Letra N e U se confundem
    arquivo_proto = "./modulos/pose_deploy.prototxt"
    arquivo_pesos = "./modulos/pose_iter_102000.caffemodel"
    numero_pontos = 22
    pares_poses = [[0, 1], [1, 2], [2, 3], [3, 4], [0, 5], [5, 6], [6, 7], [7, 8], 
                [0, 9], [9, 10], [10, 11], [11, 12], [0, 13], [13, 14], [14, 15],
                [15, 16], [0, 17], [17, 18], [18, 19], [19, 20]]
    
    # AQUI PODEMOS IMPLEMENTAR MAIS LETRAS OU EASTER EGGS DE SIMBOLOS UNIVERSAIS
    letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'L', 'M', 'N', 'O', 'P', 'Q',
          'R', 'S', 'T', 'U', 'V', 'W']

    # AQUI ELE CARREGA O MODELO QUE VAI FAZER O HAND TRACK DA MAO E ASSIM PREENCHER OS PARES DE PONTOS
    modelo = cv2.dnn.readNetFromCaffe(arquivo_proto, arquivo_pesos)


    #provavel q precise salvar a img para usar aqui****
    imagem_copia = np.copy(img)

    # DIMENSIONA
    dimensions = img.shape
    height = dimensions[0]
    width = dimensions[1]
    imagem_largura = width
    imagem_altura = height
    proporcao = imagem_largura / imagem_altura

    # CONFIG DAS CORES DOS PONTOS, TAMANHO DAS LINHAS E FONTE, APENAS DETALHE
    cor_pontoA, cor_pontoB, cor_linha = (14, 201, 255), (255, 0, 128), (192, 192, 192)
    cor_txtponto = (10, 216, 245)
    tamanho_fonte, tamanho_linha, tamanho_circulo, espessura = 5, 1, 4, 2
    fonte = cv2.FONT_HERSHEY_SIMPLEX

    # DIMENSIONA ENTRADA
    entrada_altura = 256
    entrada_largura = int(((proporcao * entrada_altura) * 8) // 8)

    # AQUI COMEÇA A USAR EFETIVAMENTE O CV2
    # CONVERTE IMG DO FORMATO OPENCV PARA O BLOBCAFFE Q É O TIPO DO MODELO QUE ESTAMOS USANDO
    entrada_blob = cv2.dnn.blobFromImage(img, 1.0 / 255, 
                                     (entrada_largura, entrada_altura), 
                                     (0, 0, 0), swapRB=False, crop=False)
    
    # SAIDA DOS DADOS
    modelo.setInput(entrada_blob)
    saida = modelo.forward()

    # APARTIR DESSE MOMENTO VAMOS COLOCAR ESSES DADOS NA IMAGEM ENTAO PODE COMENTAR NO FUTURO
    pontos = []
    limite = 0.1
    for i in range(numero_pontos):
        mapa_confianca = saida[0, i, :, :]
        mapa_confianca = cv2.resize(mapa_confianca, (imagem_largura, imagem_altura))

        _, confianca, _, ponto = cv2.minMaxLoc(mapa_confianca)

        if confianca > limite:
            cv2.circle(imagem_copia, (int(ponto[0]), int(ponto[1])), 5, cor_pontoA, 
                    thickness=espessura, lineType=cv2.FILLED)
            cv2.putText(imagem_copia, ' ' + (str(int(ponto[0]))) + ',' + 
                        str(int(ponto[1])), (int(ponto[0]), int(ponto[1])),
                        fonte, 0.3, cor_txtponto, 0, lineType=cv2.LINE_AA)

            cv2.circle(img, (int(ponto[0]), int(ponto[1])), tamanho_circulo,
                    cor_pontoA,
                    thickness=espessura, lineType=cv2.FILLED)
            cv2.putText(img, ' ' + "{}".format(i), (int(ponto[0]), 
                                                    int(ponto[1])), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.3,
                        cor_txtponto,
                        0, lineType=cv2.LINE_AA)

            pontos.append((int(ponto[0]), int(ponto[1])))

        else:
            pontos.append((0, 0))
    
    ## DESENHA O ESQUELETO TENDO OS PONTO CHAVE APENAS JUNTAMOS OS PARES
    for par in pares_poses:
        parteA = par[0]
        parteB = par[1]

        if pontos[parteA] != (0,0) and pontos[parteB] != (0,0):
            cv2.line(imagem_copia, pontos[parteA], pontos[parteB], cor_linha, 
                 tamanho_linha, lineType=cv2.LINE_AA)
            cv2.line(img, pontos[parteA], pontos[parteB], cor_linha, tamanho_linha, 
                    lineType=cv2.LINE_AA)
    
    cv2.imwrite('testeHT.png', img)
    return pontos
    # OK AQUI PODEMOS SALVAR A IMAGEM AFIM DE TESTES POIS A PARTE DE RECONHECER OS PONTOS DA MÃO FOI CONCLUIDO
    # A META AGORA É AJUSTAR O NECESSARIO E DAR SEQUENCIA COM A TRADUCAO

def verifDedos(pontos):
    # Verifica se os dedos estão dobrados, esticados na vertical ou esticados na horizontal
    # Pontos do 1 ao 5, correspondem ao dedo polegar
    # Para o dedo polegar, precisa de uma verificação adicional para saber se está esticado ou dobrado comparando a diferença dos pontos na vertical e na horizontal
    # Pontos do 5 ao 9, correspondem ao dedo indicador
    # Pontos do 9 ao 13, correspondem ao dedo médio
    # Pontos do 13 ao 17, correspondem ao dedo anelar
    # Pontos do 17 ao 21, correspondem ao dedo mínimo
    posicao.posicoes = []
    # Dedo polegar
    # print('------POSICOES DOS DEDOS------')
    posicao.verificar_posicao_DEDOS(pontos[1:5], 'polegar', altura.verificar_altura_MAO(pontos))
    # Dedo indicador
    posicao.verificar_posicao_DEDOS(pontos[5:9], 'indicador', altura.verificar_altura_MAO(pontos))
    # Dedo médio
    posicao.verificar_posicao_DEDOS(pontos[9:13], 'medio', altura.verificar_altura_MAO(pontos))
    # Dedo anelar
    posicao.verificar_posicao_DEDOS(pontos[13:17], 'anelar', altura.verificar_altura_MAO(pontos))
    # Dedo mínimo
    posicao.verificar_posicao_DEDOS(pontos[17:21], 'minimo', altura.verificar_altura_MAO(pontos))
    # print('------POSICOES DOS DEDOS------')
    
    # print('Dedo polegar :')
    # print(posicao.posicoes[0])
    # print('Dedo anelar :')
    # print(posicao.posicoes[1])
    # print('Dedo mínimo :')
    # print(posicao.posicoes[2])
    # print('Dedo medio :')
    # print(posicao.posicoes[3])
    # print('Dedo indicador :')
    # print(posicao.posicoes[4])

    return posicao.posicoes

def verifProxi(pontos):
    # Verifica a proximidade entre os dedos, compara se os dedos estao lado a lado e se estao na mesma posicao
    # esticados ou dobrados, se forem iguais significa que estão proximos
    # ['polegar esticado vertical: afastado do indicador',
    #  'indicador dobrado: proximo ao medio',
    #  'medio dobrado: proximo ao anelar',
    #  'anelar dobrado: proximo ao minimo',
    #  'minimo dobrado: proximo ao anelar']
    p = proximidade.verificar_proximidade_DEDOS(pontos)
    return p

def leituraGesto(pontos):
    # print('------------------------xx---------xx--------------------')
    # Faz o link com o array de array de alfabeto letras, que pode ser incrementado no futuro
    atual = proximidade.verificar_proximidade_DEDOS(pontos)
    return atual
    # for i, a in enumerate(alfabeto.letras):
        # if(alfabeto.letras[i] == atual):
        #     # print('I(index do alfabeto):')
        #     # print(i)
        #     # print('A(descricao do gesto):')
        #     # print(a)
        #     # print('Deu boa!!!!!!!!')
        #     final = []
        #     final.append(a)
        #     final.append(i)
        #     # print('return é [a,i]')
        #     return final

    # print('Deu ruim')
    # return 'deu em nada'

    #     if proximidade.verificar_proximidade_DEDOS(pontos) == alfabeto.letras[i]:
    #         print(alfabeto.letras[i])
    #     else:
    #         print('ainda nao')
    # return 'finalizou tudo amem ate q enfim rx o pae'