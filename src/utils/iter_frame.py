# coding=utf-8
import numpy as np


def iter_frame(data, skip = True):
    """
    iter sur les frame d'un jeu de donnée (les ligne ayan le meme indice)
    si skip = True : evide les frame phantomes
    :param data:
    :return:
    """
    last_frame_size = 0
    frame = []
    next_frame = []
    last_id = data[0][0]
    for line in data:
        if line[0] == last_id:
            next_frame.append(line)
        else:
            if skip and len(frame) > last_frame_size and len(frame) > len(next_frame):
                # a reflechir : elever la ligne la plus etrange:
                ligne_a_retirer = max(frame, key=lambda l: list(l).count(-1))
                # print("to remove : " + str(ligne_a_retirer))
                frame = ([l for l in frame if (ligne_a_retirer[1] != l[1] and ligne_a_retirer[2] != l[2] and ligne_a_retirer[3] != l[3])])

            yield np.array(frame)
            last_frame_size = len(frame)
            frame = next_frame
            next_frame = [line]
            last_id = line[0]

def iter_frame_sync(data_pos, data_son, skip = True):
    """
    iter de maniere sincronisée sur data1 et data2 (de la maniere de zip)
    si Skip = True pass les frame désincronisée,
    sinon :
        injecte None si il n'y a pas de frame corespondantes
    :param data1:
    :param data2:
    :return:
    """
    ite_pos = iter_frame(data_pos)
    ite_son = iter_frame(data_son, skip=False)
    fpos = ite_pos.next()
    fson = ite_son.next()
    fpos = ite_pos.next()
    fson = ite_son.next()
    try:
        while 1:

            if fpos[0][0] < fson[0][0]:
                if not skip:
                    yield (fpos, None)
                fpos = ite_pos.next()
            elif fpos[0][0] > fson[0][0]:
                if not skip:
                    yield (None, fson)
                fson = ite_son.next()
            else:
                yield (fpos, fson)
                fpos = ite_pos.next()
                fson = ite_son.next()

    except StopIteration:
        pass


def clean_lines(data):
    for frame in iter_frame(data):
        for line in frame:
            yield line