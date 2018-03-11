# coding=utf-8
from munkres import Munkres
from utils import Corp, CorpCol
from Identity import Identity


def identity_assignation(frame, dicId, conf, dist):
    """
    dist :
    :param frame: la frame a traité
    :param dicId: un dictionaire associant a chaque identitée un id unique
    :param conf: dictionaire de configuration pour les class Identité et Corp, peut etre None
    :param dist:  fonction de distance entre identitée et corp
    :return: dicId mis a jour
    """
    pos_to_assin = []
    new_pos = []
    rep = dict()
    for line in frame:
        pos_to_assin.append(CorpCol(line))
        new_pos.append(0)

    pos_traite = []
    id_traite = []

    m = Munkres()
    matrice = []
    pos_order = dicId.keys()
    for id in dicId:
        l = []
        for pos in pos_to_assin:
            l.append(dist(id, pos))
        matrice.append(l)

    if len(matrice) != 0:
        indice = m.compute(matrice)
        i_min = min((len(pos_order), len(pos_to_assin)))
        indice = indice[:i_min]  # on suprime le 0 pading
        for (id, pos) in indice:
            id_old = pos_order[id]
            pt_new = pos_to_assin[pos]
            id_traite.append(id_old)
            pos_traite.append(pt_new)
            id_old.new_pos(pt_new)
            rep[id_old] = id_old.id

    for id in pos_to_assin:
        if id not in pos_traite:
            new_id = Identity(id, conf)
            rep[new_id] = new_id.id
            pos_traite.append(id)

    for id in dicId.keys():
        if id not in id_traite:
            rep[id] = dicId[id]
            id_traite.append(id)

    return rep