# -*- coding: utf-8 -*-
"""
@author: 
    Alex Eitelvene,
    Diego Augusto Ertel,
    Eduardo Eitelven e
    Ricardo Turella
    
Aplicativo Utilizando algoritmo SIFT (Scale Invariant Feature Transform) 
para extrair as características comuns entre a imagem do banco de dados e a imagem informada

--- Como usar? ---
1- Selecionar uma imagem.
2- clicar em "Fazer Busca".
3- Aguardar pesquisa no banco de dados.

"""

import numpy as np
import cv2
import io
import os
import PySimpleGUI as sg
from PIL import Image
import cv2 as cv2
from win32api import GetSystemMetrics

#-----------------------------------------------------------------------------
#Definições
larguraTela = GetSystemMetrics(0)
alturaTela = GetSystemMetrics(1)
#Local do banco de dados de imagens
#CAMINHO_CIGARRAS = 'D:/#Faculdade/WSPython/Trabalho Final - Reconhecimento de imagens/Cigarrinhas' # colocar o caminho da pasta que contem as pastas das cigarras


file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]




#-----------------------------------------------------------------------------
def pesquisa_imagem(img_carregada):
    CAMINHO_CIGARRAS = 'D:/#Faculdade/WSPython/Trabalho Final - Reconhecimento de imagens/Cigarrinhas' # colocar o caminho da pasta que contem as pastas das cigarras
    
    #img_busca= 'Cicadellini/Pawiloma victima/IMG_0004.JPG';
    img_busca= img_carregada
    
    #img_busca = 'Cicadellini/Pawiloma victima/IMG_0004.JPG'
    
    img_referencias=[
    	'Cicadellini/Pawiloma victima/P victima.jpg',
    	'Cicadellini/Erythrogonia dorsalis (Signoret, 1853)/E dorsalis.jpg',
    	'Cicadellini/Hortensia similis/H similis.jpg',
    	'Gyponini/Gypona validana DeLong, 1980/Gypona validana.JPG',
    	'Gyponini/Gypona sellata Berg, 1899/Gypona sellata.JPG',
    	'Proconiini/Aulacizes obsoleta Melichar, 1926/Aulacizes obsoleta.JPG',
    	'Cicadellini/Hortensia similis/H similis.jpg',
    	'Cicadellini/Parathona gratiosa/P gratiosa.jpg',
    	'Cicadellini/Erythrogonia dorsalis/E dorsalis.jpg',
    ]
    
    sift = cv2.SIFT_create(400)
    
    #print("Busca: " + img_busca)
    #img = cv2.imread(CAMINHO_CIGARRAS + '/' + img_busca,cv2.IMREAD_GRAYSCALE)
    img = cv2.imread(img_busca,cv2.IMREAD_GRAYSCALE)
    kp, des = sift.detectAndCompute(img,None)
    
    FLANN_INDEX_KDTREE = 1
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params,search_params)
    
    for img_referencia in img_referencias:
    	print("Imagem de Ref: " + img_referencia)
    	
    	img_ref = cv2.imread(CAMINHO_CIGARRAS + '/' + img_referencia,cv2.IMREAD_GRAYSCALE)
    	kp_ref, des_ref = sift.detectAndCompute(img_ref,None)
    	
    	matches = flann.knnMatch(des_ref,des,k=2)
    	
    	hits = 0
    	
    	for i,(m,n) in enumerate(matches):
    		if m.distance < 0.97*n.distance: # ratio test as per Lowe's paper
    		# ~ if (m.distance / n.distance) < 0.96:
    			hits = hits + 1
    	#img=cv2.drawKeypoints(kp_ref,img_ref)
    	ratio = (hits / len(kp_ref))*100
    	print("Percentual de Caracteristicas parecidas é %.4f \n" % (ratio))
#-----------------------------------------------------------------------------

def main():

    #sg.theme('Gray')
    layout = [      
        [
            sg.Text("Cigarra Escolhida"),
            sg.Input(size=(25, 1), key="Arquivo"),
            sg.FileBrowse(file_types=file_types),
            sg.Button("Fazer Busca"),
        ],
        [
            
            #sg.Image(key="-imgEditada-") 
            sg.Output(size=(100,35)),
            sg.Image(key="-imagemCigarra-")
        ],
    ]
    
    window = sg.Window("Reconhecimento de padrões de cigarrinhas",layout,finalize=True,resizable=True)
    window.maximize()
    
    
    while True:
        # enquanto o programa estiver aberto verifica a ocorrencia dos eventos
        event, values = window.read()
        
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        
        if event == "Fazer Busca":
            filename = values["Arquivo"]
            if os.path.exists(filename):
                image = Image.open(values["Arquivo"])
                pesquisa_imagem(filename)
                image.thumbnail((larguraTela/2, alturaTela/2))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window["-imagemCigarra-"].update(data=bio.getvalue())
                #window["-imgEditada-"].update(data=bio.getvalue())

            
    window.close()
#-----------------------------------------------------------------------------
if __name__ == "__main__":
    main()
#-----------------------------------------------------------------------------



