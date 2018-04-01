from utils import pretraitement
import os


"""
fait le pretraitement de toute les video
"""

PATH = "../data/"
for vid in os.listdir(PATH):
    print("traitement de : " + vid)
    pretraitement(PATH + vid + "/")