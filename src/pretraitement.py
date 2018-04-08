from utils import pretraitement
from detecte_contours_ssl import detecte_voix_1
import os


"""
fait le pretraitement de toute les video
"""

PATH = "../data/"
for vid in os.listdir(PATH):
    print("traitement de : " + vid)
    detecte_voix_1(PATH + vid + "/")
    pretraitement(PATH + vid + "/")
