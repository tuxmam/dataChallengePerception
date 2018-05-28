from metric.read_file import read_file
from utils import save_data, iter_frame, add_col
from utils import CorpCol
from utils import Identity
import numpy as np


def proces_data(path):
    data = read_file(path + "groundTruth.txt")
    data = add_col(data, path)
    data_traite = []
    labels = []
    data_tot = []
    identite = dict()
    for frame in iter_frame(data):
        for line in frame:
            id_ligne = line[1]

            if id_ligne not in identite:
                identite[id_ligne] = Identity(CorpCol(line[2:], (line[-3], line[-2], line[-1])))

            cur_id = identite[id_ligne]

            for other_line in frame:
                id_other_line = other_line[1]
                res_comp = cur_id.comp(CorpCol(other_line[2:], (line[-3], line[-2], line[-1])))
                same = 0
                if id_other_line == id_ligne:
                    same = 1
                # print(res_comp)
                if sum(res_comp) < 600:
                    data_tot.append(np.concatenate(([same], res_comp)))
                data_traite.append(res_comp)
                labels.append(same)

            cur_id.new_pos(CorpCol(line[2:], (line[-3], line[-2], line[-1])))
    data_traite = np.array(data_traite)
    labels = np.array(labels)
    data_tot = np.array(data_tot)
    return data_traite, labels, data_tot


import os

PATH = "../data/"
data_traite = np.array([])
labels = np.array([])
for dir in os.listdir(PATH):
# for dir in ["Scenario05-05"]:
    if (dir not in ["Scenario04-02"]):

        print("traitement de : " + dir)
        data_traite_tmp, labels_tmp, data_tot_tmp = proces_data(PATH + dir + "/")
        if len(data_traite) == 0:
            data_traite = data_traite_tmp
            labels = labels_tmp
            data_tot = data_tot_tmp
        else:
            labels = np.concatenate((labels, labels_tmp))
            data_traite = np.concatenate((data_traite, data_traite_tmp))
            data_tot = np.concatenate((data_tot, data_tot_tmp))

suffix = "_all_max_200"
save_data(data_traite, "../learn/data_traite" + suffix)
save_data(labels, "../learn/label" + suffix)
save_data(data_tot, "../learn/data_tot" + suffix)

print("done")