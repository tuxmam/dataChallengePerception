# coding=utf-8
from Point import Point
from barycenter import body_barycenter, head_barycenter
from size import body_size, head_size
from labels import Labels
import numpy as np


class Corp(object):
    """
    implemente la sauvegarde des donnee d'un corps
    """

    def __init__(self, ligne):
        # print("hd size : " + str(head_size(ligne)))
        if (len(ligne) >= 41):
            self.hd_bary = Point(ligne[Labels.X_BARY_HD], ligne[Labels.Y_BARY_HD])
            self.bd_bary = Point(ligne[Labels.X_BARY_BD], ligne[Labels.Y_BARY_BD])
        else:
            self.hd_bary = head_barycenter(ligne)
            self.bd_bary = body_barycenter(ligne)
        # self.hd_size = head_size(ligne)
        # self.bd_size = body_size(ligne)
        self.cache = pt_cache(ligne)

        self.coef_dist_hd = 1
        self.coef_dist_bd = 1
        # self.coef_size_hd = 0
        # self.coef_size_bd = 0
        self.coef_pt_cache = 50
        self.exposant = 0.3
        self.nb_of_use = 0

    def dist(self, other):
        cout = self.hd_bary.dist(other.hd_bary) ** self.exposant * self.coef_dist_hd
        cout += self.bd_bary.dist(other.bd_bary) ** self.exposant * self.coef_dist_bd
        # cout += self.hd_size.dist(other.hd_size)**self.exposant * self.coef_size_hd
        # cout += self.bd_size.dist(other.bd_size)**self.exposant * self.coef_size_bd
        cout += abs(self.dist_pt_cache(other)) ** self.exposant * self.coef_pt_cache
        # print( "comp : " + str(self) + " \n et \n" + str(other))
        # print("cout :" + str(cout))
        # print("\n")
        return cout

    def comp(self, other):
        return np.array([self.hd_bary.dist(other.hd_bary),
                         self.bd_bary.dist(other.bd_bary),
                         abs(self.dist_pt_cache(other))])

    def config(self, par_dict=None, **args):
        """
        configuration du corp
        :param args: coef_dist_hd, coef_dist_bd, coef_size_hd, coef_size_bd, coef_pt_cache
        """
        if (par_dict is not None):
            args = par_dict
        if "coef_dist_hd" in args:
            self.coef_dist_hd = args["coef_dist_hd"]
        if "coef_dist_bd" in args:
            self.coef_dist_bd = args["coef_dist_bd"]
        # if "coef_size_hd" in args:
        #     self.coef_size_hd = args["coef_size_hd"]
        # if "coef_size_bd" in args:
        #     self.coef_size_bd = args["coef_size_bd"]
        if "coef_pt_cache" in args:
            self.coef_pt_cache = args["coef_pt_cache"]
        if "exposant" in args:
            self.exposant = args["exposant"]

    def __hash__(self):
        return hash((self.hd_bary, self.bd_bary, len(self.cache)))

    def __eq__(self, other):
        return self.bd_bary == other.bd_bary and self.hd_bary == other.hd_bary and self.cache == other.cache

    def __str__(self):
        return ("Corp : " + "hd : " + str(self.hd_bary) + " size : " +
                "bd : " + str(self.bd_bary) + " size :" + " cachee : " + str(self.cache) + "\n" +
                "Coef : " + " pt :" + str(self.coef_pt_cache) + " sbd " + " hd " + str(self.coef_dist_hd) +
                " bd " + str(self.coef_dist_bd))

    def dist_pt_cache(self, other):
        return len(self.cache.symmetric_difference(other.cache))


def pt_cache(ligne):
    c = 0
    s = set()
    for i in range(2, 37):
        if ligne[i] == -1:
            s.add(i)
    return s


class CorpCol(Corp):

    def __init__(self, ligne, col=None):
        """
        crée un corp avec gestion de la couleur en la précisant
        :param ligne:
        :param col: un triplet (R, G, B)
        """
        Corp.__init__(self, ligne)
        if col != None:
            self.col = col
        else:
            self.col = (ligne[Labels.COL_R], ligne[Labels.COL_G], ligne[Labels.COL_B])
        self.coef_col = 1

    def dist_col(self, other):
        dist = np.sqrt(sum([(self.col[i] - other.col[i]) ** 2 for i in (0, 1, 2)])) ** self.exposant
        return dist

    def config(self, par_dict=None, **args):
        """
        configuration du corp
        :param args: coef_dist_hd, coef_dist_bd, coef_size_hd, coef_size_bd, coef_pt_cache
        """
        if par_dict is not None:
            args = par_dict

        super(CorpCol, self).config(args)

        if "coef_col" in args:
            self.coef_col = args["coef_col"]
