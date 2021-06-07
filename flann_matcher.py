import numpy as np
import cv2

CAMINHO_CIGARRAS = 'D:/#Faculdade/WSPython/Trabalho Final - Reconhecimento de imagens/Cigarrinhas' # colocar o caminho da pasta que contem as pastas das cigarras

img_busca= 'Cicadellini/Pawiloma victima/IMG_0004.JPG';
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

print("Busca: " + img_busca)
img = cv2.imread(CAMINHO_CIGARRAS + '/' + img_busca,cv2.IMREAD_GRAYSCALE)
kp, des = sift.detectAndCompute(img,None)

FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks=50)   # or pass empty dictionary
flann = cv2.FlannBasedMatcher(index_params,search_params)

for img_referencia in img_referencias:
	print("Ref: " + img_referencia)
	
	img_ref = cv2.imread(CAMINHO_CIGARRAS + '/' + img_referencia,cv2.IMREAD_GRAYSCALE)
	kp_ref, des_ref = sift.detectAndCompute(img_ref,None)
	
	matches = flann.knnMatch(des_ref,des,k=2)
	
	hits = 0
	
	for i,(m,n) in enumerate(matches):
		if m.distance < 0.97*n.distance: # ratio test as per Lowe's paper
		# ~ if (m.distance / n.distance) < 0.96:
			hits = hits + 1
	#img=cv2.drawKeypoints(kp_ref,img_ref)
	ratio = hits / len(kp_ref)
	print(ratio)

    
    

    
