# -*- coding: utf-8 -*-
"""
@author: 
    Alex Eitelven,
    Diego Augusto Ertel,
    Eduardo Eitelven e
    Ricardo Turella
    
Aplicativo Utilizando algoritmo SIFT (Scale Invariant Feature Transform) 
para extrair as características comuns entre a imagem do banco de dados e a imagem informada
--- Como usar? ---
1- Ajustar caminho do banco de dados linha 39
2- Selecionar uma imagem.
3- clicar em "Buscar".
4- Aguardar pesquisa no banco de dados.
"""

import numpy as np
import cv2
import io
import os
import PySimpleGUI as sg
from PIL import Image
import cv2 as cv2
import matplotlib.pyplot as plt

#-----------------------------------------------------------------------------
#Definições
if os.name == 'posix':
    import pyautogui
    dimensoes = pyautogui.size()
    larguraTela = dimensoes[0]
    alturaTela = dimensoes[1]
else:
    from win32api import GetSystemMetrics
    larguraTela = GetSystemMetrics(0)
    alturaTela = GetSystemMetrics(1)
#Local do banco de dados de imagens
CAMINHO_CIGARRAS = 'D:/#Faculdade/WSPython/Trabalho Final - Reconhecimento de imagens/Cigarrinhas' # colocar o caminho da pasta que contem as pastas das cigarras

if os.name == 'posix':
    CAMINHO_CIGARRAS = '/home/penguin/Documentos/processamento_imagens/cigarras/'

file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]

#----------------------------------------------------------------------------
# Retorna o Caminho dos arquivos
def files_path06(*args):
    lista = []
    for item in args:
        for p, _, files in os.walk(os.path.abspath(item)):
            for file in files:
                lista.append((p+ os.sep + file))
    return lista

#----------------------------------------------------------------------------
def pesquisa_imagem(img_carregada):
    img_busca= img_carregada
    img_referencias = []

    listaArquivos=files_path06(CAMINHO_CIGARRAS)
    for i in range(len(listaArquivos)):
        if (not'IMG_' in listaArquivos[i])\
            and  (not'.db' in listaArquivos[i])\
                and (not'.psd' in listaArquivos[i])\
                    and (not'.py' in listaArquivos[i]):
                            img_referencias.append(listaArquivos[i])

    sift = cv2.SIFT_create(400)
    
    img = cv2.imread(img_busca,cv2.IMREAD_GRAYSCALE)
    kp, des = sift.detectAndCompute(img,None)
    
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params,search_params)
        
    max_ratio = 0
    
    for i in  range(len(img_referencias)):
        print('Carregando %d de %d \n' % (i+1 , len(img_referencias)))        
        print("Imagem de Ref: " + img_referencias[i])        
        img_ref = cv2.imread(img_referencias[i],cv2.IMREAD_GRAYSCALE)
        kp_ref, des_ref = sift.detectAndCompute(img_ref,None)
    	
        matches = flann.knnMatch(des_ref,des,k=2)
    	
        hits = 0
    	
        for x,(m,n) in enumerate(matches):
            if m.distance < 0.97*n.distance: # ratio test as per Lowe's paper
                hits = hits + 1
    	#img=cv2.drawKeypoints(kp_ref,img_ref)
        ratio = (hits / len(kp_ref))*100
        print("Percentual de Caracteristicas parecidas é %.4f \n" % (ratio))
        
        if ratio >= max_ratio:
            max_ratio = ratio
            max_img_referencias = img_referencias[i]
            max_matches = matches 
            max_kp_ref = kp_ref
            
    print("----------------------------------------------------------------------------------------------------------------\n")
    print("- A cigarra com mais caracteristicas parecidas da imagem referencia: \n")
    print(" %s \n" % (max_img_referencias,))
    print("-Com %.4f caracteristicas parecidas.\n" % (max_ratio))
    print("----------------------------------------------------------------------------------------------------------------\n")
    # Need to draw only good matches, so create a mask
    matchesMask = [[0,0] for i in range(len(max_matches))]

    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(max_matches):
        if m.distance < 0.7*n.distance:
            matchesMask[i]=[1,0]
    draw_params = dict(matchColor = (0,255,0),
                       singlePointColor = (255,0,0),
                       matchesMask = matchesMask,
                       flags = cv2.DrawMatchesFlags_DEFAULT)

    img_busca_carregada= cv2.imread(img_busca,cv2.IMREAD_GRAYSCALE)
    img_referencia_carregada = cv2.imread(max_img_referencias,cv2.IMREAD_GRAYSCALE)

    imagem_hitpoints = cv2.drawMatchesKnn(img_busca_carregada,kp,img_referencia_carregada,max_kp_ref,max_matches,None,**draw_params)
    
    cv2.imwrite("hitPoints.png",imagem_hitpoints)


#-----------------------------------------------------------------------------

def main():

    #sg.theme('Gray')
    layout = [      
        [
            sg.Text("Cigarra escolhida"),
            sg.Input(size=(25, 1), key="Arquivo"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Buscar"),
        ],
        [
            sg.Output(size=(larguraTela,15)),
        ],
        [
            sg.Image(key="-imagemCigarra-")
        ],
    ]
    
    window = sg.Window("Reconhecimento de padrões de cigarrinhas",layout,finalize=True,resizable=True)
    if os.name != 'posix':
        window.maximize()
    
    
    while True:
        # enquanto o programa estiver aberto verifica a ocorrencia dos eventos
        event, values = window.read()
        
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
        if event == "Buscar":
            filename = values["Arquivo"]
            if os.path.exists(filename):
                pesquisa_imagem(filename)
                image = Image.open("hitPoints.png")
                image.thumbnail((larguraTela, alturaTela/1.3))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-imagemCigarra-"].update(data=bio.getvalue())
            
    window.close()
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#-----------------------------------------------------------------------------
