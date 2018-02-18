# coding=utf-8
from Point import Point
from barycenter import body_barycenter, head_barycenter
from size import body_size, head_size
from labels import Labels

class Corp:
    """
    implemente la sauvegarde des donnee d'un corps
    """

    def __init__(self, ligne):
        # print("hd size : " + str(head_size(ligne)))
        self.hd_bary = head_barycenter(ligne)
        self.bd_bary = body_barycenter(ligne)
        self.hd_size = head_size(ligne)
        self.bd_size = body_size(ligne)
        self.cache = pt_cache(ligne)

        self.nb_of_use = 0


    def dist(self, other):
        cout = self.hd_bary.dist(other.hd_bary)
        cout += self.bd_bary.dist(other.bd_bary)
        cout += self.hd_size.dist(other.hd_size)
        cout += self.bd_size.dist(other.bd_size)
        cout += abs(self.cache-other.cache) * 100
        # print( "comp : " + str(self) + " \n et \n" + str(other))
        # print("cout :" + str(cout))
        # print("\n")
        return cout

    def __hash__(self):
        return hash((self.hd_bary, self.bd_bary, self.hd_size, self.bd_size, self.cache))

    def __eq__(self, other):
        return self.hd_size == other.hd_size and self.bd_size == other.bd_size and self.bd_bary == other.bd_bary and self.hd_bary == other.hd_bary and self.cache == other.cache

    def __str__(self):
        return ("Corp : " + "hd : " + str(self.hd_bary) + " size : " + str(self.hd_size) + "\n" +
                "bd : " + str(self.bd_bary) + " size :" + str(self.bd_size) + " cachee : " + str(self.cache))



def pt_cache(ligne):
    c = 0
    for i in range(2, 37):
        if ligne[i] == -1:
            c += 1
    return c
