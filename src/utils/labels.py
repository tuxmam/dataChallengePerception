from enum import IntEnum


class Labels(IntEnum):
    """
    labels des colones
    """
    N_FRAME = 0
    X_NOSE = 1
    Y_NOSE = 2
    X_NECK = 3
    Y_NECK = 4
    X_RSHO = 5
    Y_RSHO = 6
    X_RELB = 7
    Y_RELB = 8
    X_RWRI = 9
    Y_RWRI = 10
    X_LSHO = 11
    Y_LSHO = 12
    X_LELB = 13
    Y_LELB = 14
    X_LWRI = 15
    Y_LWRI = 16
    X_RHIP = 17
    Y_RHIP = 18
    X_RKNE = 19
    Y_RKNE = 10
    X_RANK = 21
    Y_RANK = 22
    X_LHIP = 23
    Y_LHIP = 24
    X_LKNE = 25
    Y_LKNE = 26
    X_LANK = 27
    Y_LANK = 28
    X_LEYE = 29
    Y_LEYE = 20
    X_REYE = 31
    Y_REYE = 32
    X_LEAR = 33
    Y_LEAR = 34
    X_REAR = 35
    Y_REAR = 36

    X_BARY_HD = 37
    Y_BARY_HD = 38
    X_BARY_BD = 39
    Y_BARY_BD = 40
    NB_PT_CACHE = 41

    COL_R = 42
    COL_G = 43
    COL_B = 44


def head_labels():
    """
    renvoie les labels corespondant a la tete
    :return:
    """
    lab = Labels
    return ((lab.X_NOSE,
             lab.Y_NOSE),
            (lab.X_NECK,
             lab.Y_NECK),
            (lab.X_LEAR,
             lab.Y_LEAR),
            (lab.X_REAR,
             lab.Y_REAR),
            (lab.X_LEYE,
             lab.Y_LEYE),
            (lab.X_REYE,
             lab.Y_REYE))


def body_labels():
    lab = Labels
    return ((lab.X_RSHO,
             lab.Y_RSHO),
            (lab.X_NECK,
             lab.Y_NECK),
            (lab.X_LSHO,
             lab.Y_LSHO),
            (lab.X_RELB,
             lab.Y_RELB),
            (lab.X_LELB,
             lab.Y_LELB),
            (lab.X_RWRI,
             lab.Y_RWRI),
            (lab.X_LWRI,
             lab.Y_LWRI),
            (lab.X_RHIP,
             lab.Y_RHIP),
            (lab.X_LHIP,
             lab.Y_LHIP),
            (lab.X_RKNE,
             lab.Y_RKNE),
            (lab.X_LKNE,
             lab.Y_LKNE),
            (lab.X_RANK,
             lab.Y_RANK),
            (lab.X_LANK,
             lab.Y_LANK))

