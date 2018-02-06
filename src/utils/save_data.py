# coding=utf-8
import numpy as np


def save_data(data, path):
    """
    sauvegarde les donnée a l'endois indiqué
    """
    np.savetxt(path, data, fmt="%i")
