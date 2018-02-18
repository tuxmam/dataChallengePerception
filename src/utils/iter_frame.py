# coding=utf-8
import numpy as np


def iter_frame(data):
    """
    iter sur les frame d'un jeu de donnée (les ligne ayan le meme indice)
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
            if len(frame) > last_frame_size and len(frame) > len(next_frame):
                # a reflechir : elever la ligne la plus etrange:
                ligne_a_retirer = max(frame, key=lambda l: list(l).count(-1))
                # print("to remove : " + str(ligne_a_retirer))
                frame = ([l for l in frame if (ligne_a_retirer[1] != l[1] and ligne_a_retirer[2] != l[2] and ligne_a_retirer[3] != l[3])])

            yield np.array(frame)
            last_frame_size = len(frame)
            frame = next_frame
            next_frame = [line]
            last_id = line[0]


def clean_lines(data):
    for frame in iter_frame(data):
        for line in frame:
            yield line