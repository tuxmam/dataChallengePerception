# coding=utf-8
import numpy as np
from iter_frame import clean_lines
from metric.read_file import read_file


def make_pred(data, fonction, data_son = None):
    """
    renvoie un tableau de donnée formaté pour etre évalué
    si donnée particuliere pour le sons, les ajouter.
    :param data: les donnée brutes (ou aumentée en respectant l'ordre des 37 première colone)
    :param fonction: une fonction d'évaluation prenant en paramètre les donnée et itérant dessus pour renvoyer l'identité et si la personne parle
     renvoyant l'identité et si la personne parle (dans un tuple)
     Si data_son est renségée, fontion auras les deux donnée en parametre
    :return:
    """
    res = []
    if data_son is not None:
        data_fun = (data, data_son)
    else :
        data_fun = data
    for line, (identite, speak) in zip(clean_lines(data), fonction(data_fun)):
        res.append(np.concatenate((line[0:1], [identite%8], [speak], line[1:37])))
    return np.array(res)


def make_mult_pred(ite_data, function):
    for data in ite_data:
        yield make_pred(data, function)


def mult_load(ite_path, son = False):
    """
    renvoie un itérateur contenant les donée chargée : des tuple, (data_ref, data_exp)
    si son = true renvoie : ((data_pos, data_son), data_exp)
    :param ite_path:
    :return:
    """
    data = []
    data_ref = []
    for path in ite_path:
        data_ref.append(read_file(path+"groundTruth.txt"))
        if son:
            data.append((np.loadtxt(path+"augmented_data.txt"), np.loadtxt(path+"ssl_detections.txt")))
        else:
            data.append(np.loadtxt(path+"augmented_data.txt"))
    return np.array(data_ref), np.array(data)

def make_mult_eval(ite_data, function):
    """
    renvoie les resultas sur les donnée formatée
    :param ite_data:
    :param function:
    :return:
    """
    res = [0,0,0,0]
    for data in ite_data:
        res[0], res[1], res[2], res[3] = make_pred(data, function)
    n = len(tab_data)
    return res[0] / n, res[1] / n, res[2] / n, res[3] /n
