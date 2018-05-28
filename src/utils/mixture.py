# coding=utf-8
import os
import numpy as np
from sklearn.mixture import *
import matplotlib.image as mpimg

from utils import Point


def make_mixture(path):
    """
    crée le fichier mixture.txt pour un chemins vers une vidéo
    a besoin du dossier, ssl_images
    :param path:
    :return:
    """
    res = []
    l = [c for c in os.listdir(path+"/ssl_images")]
    l.sort(key=lambda x: int(x[10:-4]))
    for i, file in enumerate(l):
        nb, mixture = calc_mix(path+"/ssl_images/"+file)
        print(file)
        # print(mixture)
        if nb == 0:
            res.append(np.array([i+1, -1, -1, -1, -1]))
        for k in range(nb):
            res.append(np.concatenate(([i+1], mixture[k])))
    np.savetxt(path+"/mixture", res, fmt="%i")

def calc_mix(path):
    """
    calcule les mixture d'une images ssl
    :param path:
    :return: (nombre de mixture, [(x_mixture, y_mixture, var_mixture, prob_mixture])
    """
    N_MIXTURE = 2
    image = mpimg.imread(path)
    data = image[:, :, 0]
    data = traite_data(data)
    s = len(data)
    if s>0:
        model = GaussianMixture(n_components=N_MIXTURE, covariance_type="spherical")
        model.fit(data)
        res = []
        for i in range(N_MIXTURE):
            res.append(np.concatenate(([model.means_[i][1]], [model.means_[i][0]], [model.covariances_[i]], [s*model.weights_[i]])))
            # res.append(([model.means_[i][1]], [model.means_[i][0]], [model.covariances_[i]]))

        return (N_MIXTURE, np.array(res))
    else:
        return 0,None

def traite_data(data):
    res = []
    for y, l in enumerate(data):
        for x, i in enumerate(l):
            i /= 30
            for _ in range(i):
                res.append([x,y])
    return np.array(res)

def compare_corp_son(frame, corp):
    """
    compare une fraime de sons avec un corp
    :param frame:
    :return: [d1, c1, p1, d2, c2, p2]
    """
    e1 = frame[0]
    e2 = frame[1]
    p1 = Point(e1[2], e1[1])
    p2 = Point(e2[2], e2[1])
    return np.concatenate(([p1.dist(corp.hd_bary)], e1[3:], [p2.dist(corp.hd_bary)], e2[3:]))