# coding=utf-8
from Corp import Corp
from Point import Point
import numpy as np


class Identity:
    """
    La classe identitée suis une personne. Elle permet de sauvegarder les différentes positions a cour du temps.
    """
    max_id = 1

    def __init__(self, pos, conf=None):
        """
        crée une nouvelle identitée
        :param pos: un corps, la position initiale de la personne
        :param conf:
        """
        self.list_old_pos = []  #  listes des positions de la personnes
        self.list_speak = [] # on sauvegarde les frames ou la personne parle ou non
        self.list_old_pos.append(pos)
        self.curent_pos = pos  #  dernieres positions vue
        self.id = Identity.max_id  # id uniques de la personnes
        Identity.max_id += 1

        self.vect_corp = Point(0, 0)
        self.vect_tete = Point(0, 0)

        self.calc_inertie(10)
        self.coef_ine_hd = 50
        self.coef_ine_bd = 20
        self.retard_inertie = 50
        self.retard_col = 50
        self.mem_lenght = 100
        self.exposant = 0.3
        self.conf = conf
        if (conf is not None):
            self.config(conf)

    def set_speak(self, speak):
        """
        ajout l'information de parole pour la derniere frame a la personne
        :param speak: true/false
        :return:
        """
        self.list_speak.append(speak)
        if len(self.list_speak) > self.mem_lenght:
            self.list_speak.pop(0)

    def new_pos(self, pos):
        """
        ajoute la position (un Corp) a l'identité
        :param pos:
        :return:
        """
        self.curent_pos = pos
        self.list_old_pos.append(pos)
        if len(self.list_old_pos) > self.mem_lenght:
            self.list_old_pos.pop(0)
        self.curent_pos.config(self.conf)
        self.calc_inertie(self.retard_inertie)

    def __eq__(self, other):
        if isinstance(other, Identity):
            return self.curent_pos == other.curent_pos
        elif isinstance(other, Corp):
            return self.curent_pos == other
        else:
            return False

    def dist(self, body):
        """
        comparaison entre identitée et corp
        :param body:
        :return:
        """
        # print(self)
        dist = 0
        if isinstance(body, Corp):
            # print (self.curent_pos)
            dist = self.curent_pos.dist(body)
            dist += ((body.hd_bary - self.get_pos(0).hd_bary).dist(self.vect_tete) ** self.exposant * self.coef_ine_hd)
            dist += ((body.bd_bary - self.get_pos(0).bd_bary).dist(self.vect_corp) ** self.exposant * self.coef_ine_bd)
            for i in range(2, 10):
                dist += self.get_pos(i).dist_pt_cache(body) * self.curent_pos.coef_pt_cache / 10
            for i in range(2, 30, 3):
                dist += self.get_pos(i).dist_col(body) / 10

        elif isinstance(body, Identity):
            dist = self.curent_pos.dist(body.curent_pos)
            dist += (self.vect_tete.dist(body.vect_tete) ** self.exposant * self.coef_ine_hd)
            dist += (self.vect_corp.dist(body.vect_corp) ** self.exposant * self.coef_ine_bd)
        return dist

    def comp(self, body):
        """
        renvoie les different atribut de comparaison dans un tableau, dans l'ordre:
        ine_tete, ine_corp, col, tete, corp, pt_cache
        :param body:
        :return:
        """
        dist_col = 0
        for i in range(2, 30, 3):
            dist_col += self.get_pos(i).dist_col(body)
        dist_pt = 0
        for i in range(2, 20, 2):
            dist_pt += self.get_pos(i).dist_pt_cache(body)

        return np.array([(body.hd_bary - self.get_pos(0).hd_bary).dist(self.vect_tete),
                         (body.bd_bary - self.get_pos(0).bd_bary).dist(self.vect_corp),
                         dist_col,
                         self.curent_pos.hd_bary.dist(body.hd_bary),
                         self.curent_pos.bd_bary.dist(body.bd_bary),
                         dist_pt])

    def dist_col(self, body):
        dist = self.curent_pos.dist_col(self.list_old_pos[0])
        return dist

    def calc_inertie(self, delta_frame):
        """
        calcule l'inertie.
        :param delta_frame:
        :return:
        """
        if delta_frame >= len(self.list_old_pos):
            delta_frame = len(self.list_old_pos)

        vect_tete = Point(0, 0)
        vect_corp = Point(0, 0)

        vect_tete += self.curent_pos.hd_bary - self.list_old_pos[-delta_frame].hd_bary
        vect_corp += self.curent_pos.bd_bary - self.list_old_pos[-delta_frame].bd_bary

        self.vect_tete = vect_tete / delta_frame
        self.vect_corp = vect_corp / delta_frame

    def config(self, conf=None, **args):
        """
        configuration du et de l'identité corp
        :param args: coef_ine_hd, coef_ine_bd, retard_inertie
        coef_dist_hd, coef_dist_bd, coef_size_hd, coef_size_bd, coef_pt_cache
        exposant
        """
        if (conf is not None):
            args = conf
        # print (args)
        if "coef_ine_hd" in args:
            self.coef_ine_hd = args["coef_ine_hd"]
        if "coef_ine_bd" in args:
            self.coef_ine_bd = args["coef_ine_bd"]
        if "retard_inertie" in args:
            self.retard_inertie = args["retard_inertie"]
        if "exposant" in args:
            self.exposant = args["exposant"]
        self.curent_pos.config(par_dict=args)
        self.conf = args

    def get_pos(self, frame=0):
        """
        Renvoie la position de l'identité x frame dans le passée.
        :param frame: nb de frame dans le passé : 0 frame actuelle, 3 : trois frame dans le passé
        :return: Le corp corespondant
        """
        if frame >= len(self.list_old_pos):
            return self.list_old_pos[0]
        else:
            return self.list_old_pos[-frame - 1]

    def get_speak(self, frame=0):
        """
        revoie si la personne parlais x frame dans le passé
        :param frame:
        :return: ture/false
        """
        if frame >= len(self.list_speak):
            return False
        else:
            return self.list_speak[-frame - 1]

    def __hash__(self):
        return hash(self.curent_pos)

    def __str__(self):
        return "identité " + str(self.id) + " coef hd : " + str(self.coef_ine_hd) + " coef bd : " + str(
            self.coef_ine_bd) + " mem :" + str(self.retard_inertie)
