from Point import Point
from labels import Labels, head_labels, body_labels


def size(liste_point):
    """
    revoie la distance max (x et y) entre les point de la liste
    :return point:
    """
    max_x = max(liste_point, key=lambda p: p.x).x
    max_y = max(liste_point, key=lambda p: p.y).y
    min_x = min(liste_point, key=lambda p: p.x).x
    min_y = min(liste_point, key=lambda p: p.y).y
    return Point(max_x - min_x, max_y - min_y)


def head_size(line):
    l_pt = []
    i = 0
    for pt_x, pt_y in head_labels():
        x = line[pt_x]
        y = line[pt_y]
        if not (x == -1 or y == -1):
            i += 1
            l_pt.append(Point(x, y))
    if (i != 0):
        return size(l_pt)
    else:
        return Point(0,0)


def body_size(line):
    l_pt = []
    i = 0
    for pt_x, pt_y in body_labels():
        x = line[pt_x]
        y = line[pt_y]
        if not (x == -1 or y == -1):
            i += 1
            l_pt.append(Point(x, y))
    if (i != 0):
        return size(l_pt)
    else:
        return Point(0,0)
