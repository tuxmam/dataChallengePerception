# coding=utf-8
from labels import Labels
import numpy as np
from iter_frame import iter_frame
from Corp import Corp
import cv2
from Point import Point
from labels import Labels


def pretraitement(path):
    row_data = np.loadtxt(path + "detections.txt")
    data_passe1 = []

    # premiere passe, on detecte les position des corps
    for frame in iter_frame(row_data):
        for line in frame:
            cp = Corp(line)
            data_passe1.append(np.concatenate((line,[cp.hd_bary.x, cp.hd_bary.y, cp.bd_bary.x,
                                               cp.bd_bary.y, len(cp.cache)])))
    data_passe2 = add_col(data_passe1, path)
    np.savetxt(path+"augmented_data.txt", data_passe2, fmt="%i")

def add_col(data, path):
    """
    ajoute une colone couleur a un jeux de donné
    :param data:
    :param path:
    :return:
    """
    data_traite = []
    cap = cv2.VideoCapture(path+"video.avi")
    i = 1
    ligne = 0
    reussi = True
    while reussi:
        reussi, image = cap.read()
        while ligne<len(data) and i > data[ligne][0]:
            ligne += 1
        while ligne<len(data) and i == data[ligne][0]:
            cp = Corp(data[ligne])
            r, g, b = col_extraction(image, cp.bd_bary, 30)
            data_traite.append(np.concatenate((data[ligne], [r, g, b])))
            ligne += 1
        i += 1

    data_traite = np.array(data_traite)
    return data_traite


def col_extraction(image, pt, rayon):
    """
    fait la moyenne des couleur de l'image contenue dans un carée de coté 2*rayon et centré sur le point pt
    :param image:
    :param pt:
    :param rayon:
    :return:
    """
    r = 0
    g = 0
    b = 0
    for x in range(max(int(pt.x) - rayon,0), min(int(pt.x)+rayon, image.shape[1])):
        for y in range(max(int(pt.y) - rayon,0), min(int(pt.y)+rayon, image.shape[0])):
            r += image[y][x][0]
            g += image[y][x][1]
            b += image[y][x][2]
    r /= (rayon*2)**2
    g /= (rayon*2)**2
    b /= (rayon*2)**2
    return (r,g,b)