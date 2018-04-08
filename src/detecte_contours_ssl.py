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
import imageio
#import imutils

perimetre= lambda cnt: cv2.arcLength(cnt,True)

def epure_contours(contours,alpha,logfile):
    """epure la liste des contours pour n'afficher que les contours les plus significatif 
    l'unité de mesure ici est le périmètre d'un contour """
    contours=sorted(contours ,key=lambda contour :-cv2.arcLength(contour,True))
    #apres cette étape les contours sot classés par ordre decroissant de surface 
    nb_contours=len(contours)
    for i in range(nb_contours-1):
        perim_cour=perimetre(contours[i])
        perim_suiv=perimetre(contours[i+1])
        logfile.write("perimetre cour {}\n".format(perim_cour))
        logfile.write("perimetre suiv {}\n".format(perim_suiv))
        if (perim_suiv/perim_cour<alpha):
            contours=contours[:i+1]
            break
    return contours
    
def detecte_voix_frame_1(num_frame,frameSSL,logfile, path, epure=False,debug=False):
    """ detecte la voix dans une frameSSL correspondant au fait
    qu'une seule personne parle """
    #l'option debug permet d'afficher les images thresholdé des frames ayan plusieurs contours
    frameSSLgray= cv2.cvtColor(frameSSL, cv2.COLOR_BGR2GRAY)
    frameSSLthresh=cv2.threshold(frameSSLgray,0,255,cv2.THRESH_BINARY)[1]
    images_path=path+"/ssl_images"
    #contours = cv2.findContours(frameSSL.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    #contours = contours[0] if imutils.is_cv2() else contours[1]
    _, contours, hierarchy=cv2.findContours(frameSSLthresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    nb_contours=0
    centre_contours=[]
    n=len(contours)
    if n>1:
        if epure:
            #si l'option epuration est activé faire 
            contours=epure_contours(contours,1/2.0,logfile)
            m=len(contours)
            if(m<n):
                logfile.write("epuration de la frame n°{} on quitte de {} à {}\n".format(num_frame,n,m))
            else:
                logfile.write("alpha faible pas eu d'epuration pour la frame {} et il reste {} contours \n".format(num_frame,n))
        else:
            logfile.write("IL y'a plusieurs contours {} et il n'y a pas eu d'épuration pour la frame {}".format(n,num_frame))
    for contour in contours:
        nb_contours+=1
        cv2.drawContours(frameSSLthresh, contour, -1, (25,25,127),1)
        #calcul du centre
        M = cv2.moments(contour)
        cX=int(M["m10"]/ M["m00"])
        cY=int(M["m01"] / M["m00"])
        centre_contours.append([cX,cY])
        #print("Le centre du cercle se trouve a ",cX,cY)
        cv2.circle(frameSSLthresh, (cX,cY), 5,[120,120,120], 5)
    if n>1 and debug:
        #On verifie que y'a plusieurs contours et que le mode debug est activé
        frameSSLtresh=cv2.threshold(frameSSLgray,0,255,cv2.THRESH_BINARY)[1]
        imageio.imwrite(images_path+'/ssl_image_{}_thresh.jpg'.format(num_frame),frameSSLtresh)
    #cv2.imshow('Observations',frameSSLthresh)
    #cv2.waitKey(2000)
    if n==0:
        #si on ne trouve rien sur l'image on ajoute  -1 
        centre_contours.append([-1,-1])
    return centre_contours

def detecte_voix_1(path):
    detection_ssl=open(path+"/ssl_detections.txt","w")
    logfile=open(path+"/log_ssl_detections.txt","w")
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

        #redimensionnement 
        frameSSL=cv2.resize(frameSSL,(frameShape[1],frameShape[0]), interpolation=cv2.INTER_CUBIC)
            #modifier cette partie pour le cas ou plusieurs personnes parle donc plusieurs intensité lumineuse 
        #y,x=detection_max_intensite(frameSSL)[0:2]

        centre_contours=detecte_voix_frame_1(num_frame,frameSSL,logfile, path,epure=False)
        n=len(centre_contours)
        for i in range(n):
            y,x=centre_contours[i]
            #print("Le maximum d'intensité est a ",x,y)
            detection_ssl.write("{}".format(num_frame))
            detection_ssl.write(" {} {}".format(x,y))
            detection_ssl.write("\n")
        num_frame+=1
    detection_ssl.close()
    logfile.close()
    return x,y


# path=sys.argv[1]
# detecte_voix_1(path)




                
                
