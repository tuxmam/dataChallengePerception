# coding=utf-8
import numpy as np


def iter_frame(data):
    """
    iter sur les frame d'un jeu de donnée (les ligne ayan le meme indice)
    :param data:
    :return:
    """
    frame = []
    last_id = data[0][0]
    for line in data:

        if line[0] == last_id:
            frame.append(line)
        else:
            yield np.array(frame)
            frame = [line]
            last_id = line[0]
