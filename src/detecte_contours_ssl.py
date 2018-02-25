#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""
Created on Sun Feb 25 15:16:33 2018
Pour l'instant je traite que le cas ou  une seul personne parle 
la recherche par maximum d'intensité est trop couteuse j'ai pris les barycentres
des contours a la place

Comment on fai dans le cas ou il y'a des frame dans lequel personne ne parle ?
Faut il  les enlevés 
@author: bandian
"""
import cv2
import sys
#import imutils

def detecte_voix_frame_1(frameSSL):
    """ detecte la voix dans une frameSSL correspondant au fait
    qu'une seule personne parle """
    frameSSLgray= cv2.cvtColor(frameSSL, cv2.COLOR_BGR2GRAY)
    frameSSLthresh=cv2.threshold(frameSSLgray,0,255,cv2.THRESH_BINARY)[1]
    #contours = cv2.findContours(frameSSL.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #contours = contours[0] if imutils.is_cv2() else contours[1]
    _, contours, hierarchy=cv2.findContours(frameSSLthresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    nb_contours=0
    centre_contours=[]
    for contour in contours:
        nb_contours+=1
        cv2.drawContours(frameSSLthresh, contour, -1, (25,25,127),1)
        #calcul du centre
        M = cv2.moments(contour)
        cX=int(M["m10"]/ M["m00"])
        cY=int(M["m01"] / M["m00"])
        centre_contours.append([cX,cY])
        print("Le centre du cercle se trouve a ",cX,cY)
        cv2.circle(frameSSLthresh, (cX,cY), 2,[0,0,0], 5)

    #cv2.imshow('Observations',frameSSLthresh)
    #cv2.waitKey(2000)
    return centre_contours

def detection_max_intensite(frameSSL):
    """ renvoie le point le plus lumineux d'une frame """ 
    def intensite(point):
        return sum(point)
    nb_lignes,nb_col=frameSSL.shape[0:2]
    # (i,j,rgb)
    point_lum=(0,0,[0,0,0])
    intensite_cour=0
    for i in range(nb_lignes):
        for j in range(nb_col):
            coul=frameSSL[i][j]
            val=intensite(coul)
            if val>intensite_cour:
                intensite_cour=val
                point_lum=(i,j,coul)
    return point_lum
                
def detecte_voix_1(path):
    detection_ssl=open(path+"/ssl_detections.txt","w")
    cap = cv2.VideoCapture(path+"/video.avi")
    capssl = cv2.VideoCapture(path+"/ssl.avi")
    frameShape=(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
    capssl = cv2.VideoCapture(path+"/ssl.avi")
    num_frame=1
    while True:
        ret2, frameSSL = capssl.read()
        #print("type de la frame ",type(frameSSL))
        if (not ret2):
            break

        detection_ssl.write("{}".format(num_frame))
        #redimensionnement 
        frameSSL=cv2.resize(frameSSL,(frameShape[1],frameShape[0]), interpolation=cv2.INTER_CUBIC)
            #modifier cette partie pour le cas ou plusieurs personnes parle donc plusieurs intensité lumineuse 
        #y,x=detection_max_intensite(frameSSL)[0:2]
        centre_contours=detecte_voix_frame_1(frameSSL)
        if len(centre_contours)!=0:
            y,x=centre_contours[0]
            detection_ssl.write(" {} {}".format(x,y))
            print("Le maximum d'intensité est a ",x,y)
        detection_ssl.write("\n")

        num_frame+=1
    detection_ssl.close()
    return x,y
path=sys.argv[1]
detecte_voix_1(path)

        
        

                
                