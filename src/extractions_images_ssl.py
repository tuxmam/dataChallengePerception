#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 25 15:58:40 2018

@author: bandian
"""
import cv2
import os 
import imageio
import sys
import shutil
def stocke_ssl(path):
    """ prend une video ssl et genere toutes les images contenus dans ces vidéos"""
    capssl = cv2.VideoCapture(path+"/ssl.avi")
    cap = cv2.VideoCapture(path+"/video.avi")
    frameShape=(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    images_path=path+"/ssl_images"
    try:
        os.mkdir(images_path)
    except FileExistsError:
        shutil.rmtree(images_path)
        os.mkdir(images_path)
    print("Le dossier {} vient d'etre  crée ".format(images_path))
    num_frame=1
    while True:
        ret2, frameSSL = capssl.read()
        #print("type de la frame ",type(frameSSL))
        if (not ret2):
            break
        #transformation de la frame en image 
        #redimensionnement 
        frameSSL=cv2.resize(frameSSL,(frameShape[1],frameShape[0]), interpolation=cv2.INTER_CUBIC)
        imageio.imwrite(images_path+'/ssl_image_{}.jpg'.format(num_frame),frameSSL)
        num_frame+=1
        
        

path=sys.argv[1]
stocke_ssl(path)


