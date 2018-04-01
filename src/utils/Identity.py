# coding=utf-8
from Corp import Corp
from Point import Point
import numpy as np


class Identity:
    max_id = 1

    def __init__(self, pos, conf=None):
        """
        crée une nouvelle identitée
        :param pos: un corps, la position initiale de la personne
        :param conf:
        """
        self.list_old_pos = []
        self.list_old_pos.append(pos)
        self.curent_pos = pos
        self.id = Identity.max_id
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
            dist += ((self.curent_pos.hd_bary + self.vect_tete).dist(body.hd_bary) ** self.exposant * self.coef_ine_hd)
            dist += ((self.curent_pos.bd_bary + self.vect_corp).dist(body.bd_bary) ** self.exposant * self.coef_ine_bd)
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
        return np.concatenate(([(self.curent_pos.hd_bary + self.vect_tete).dist(body.hd_bary),
                                (self.curent_pos.bd_bary + self.vect_corp).dist(body.bd_bary),
                                self.dist_col(body)]
                               , self.curent_pos.comp(body)))

    def dist_col(self, body):
        dist = self.curent_pos.dist_col(self.list_old_pos[0])
        return dist

    def calc_inertie(self, nb_phase):
        if nb_phase >= len(self.list_old_pos):
            nb_phase = len(self.list_old_pos)

        vect_tete = Point(0, 0)
        vect_corp = Point(0, 0)

        vect_tete += self.curent_pos.hd_bary - self.list_old_pos[-nb_phase].hd_bary
        vect_corp += self.curent_pos.bd_bary - self.list_old_pos[-nb_phase].bd_bary

        # print(self.curent_pos)
        # print(self.list_old_pos[-nb_phase])
        self.vect_tete = vect_tete / nb_phase
        self.vect_corp = vect_corp / nb_phase

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

    def __hash__(self):
        return hash(self.curent_pos)

    def __str__(self):
        return "identité " + str(self.id) + " coef hd : " + str(self.coef_ine_hd) + " coef bd : " + str(
            self.coef_ine_bd) + " mem :" + str(self.retard_inertie)
