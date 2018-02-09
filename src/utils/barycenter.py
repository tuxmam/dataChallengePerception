from labels import Labels, head_labels, body_labels
from Point import Point


def head_barycenter(line):
    """
    calcule le baricentre de la tete
    :param line:
    :return:
    """
    res = [0, 0]
    i = 0
    for pt_x, pt_y in head_labels():
        x = line[pt_x]
        y = line[pt_y]
        if not (x == -1 or y == -1):
           res[0] += x
           res[1] += y
           i += 1
    if (i != 0):    
        res[0] /= i
        res[1] /= i
    else:
        res = [0, 0]
    return Point(res[0], res[1])


def body_barycenter(line):
    """
    calcule le baricentre du corp
    :param line:
    :return:
    """
    res = [0, 0]
    i = 0
    for pt_x, pt_y in body_labels():
        x = line[pt_x]
        y = line[pt_y]
        if not (x == -1 or y == -1):
            res[0] += x
            res[1] += y
            i += 1
    if (i != 0):    
        res[0] /= i
        res[1] /= i
    else:
        res = [0, 0]

    return Point(res[0], res[1])
