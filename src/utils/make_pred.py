# coding=utf-8
import numpy as np


def make_pred(data, fonction):
    """
    renvoie un tableau de donnée formaté pour etre évalué
    :param data: les donnée brutes (ou aumentée en respectant l'ordre des 37 première colone)
    :param fonction: une fonction d'évaluation prenant en paramètre les donnée et itérant dessus pour renvoyer l'identité et si la personne parle
     renvoyant l'identité et si la personne parle (dans un tuple)
    :return:
    """
    res = []
    for line, (identite, speak) in zip(data, fonction(data)):
        res.append(np.concatenate((line[0:1], [identite], [speak], line[1:37])))
    return np.array(res)
