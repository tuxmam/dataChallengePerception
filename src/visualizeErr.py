import random
import numpy as np
import matplotlib.pyplot as plt
import math
import json
import sys
from collections import Counter
import cv2
from random import randint
import scipy.io
from matplotlib.patches import Ellipse
from sklearn.mixture import *
from scipy.stats import multivariate_normal
import cv2
import numpy as np
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import scipy.stats as stat

predictionFileName=sys.argv[1]
path='/'.join(predictionFileName.split("/")[:-1])

colors = [[255, 0, 0], [255, 85, 0], [255, 170, 0], [255, 255, 0], [170, 255, 0], [85, 255, 0], [0, 255, 0],
          [0, 255, 85], [0, 255, 170], [0, 255, 255], [0, 170, 255], [0, 85, 255], [0, 0, 255], [85, 0, 255],
          [170, 0, 255], [255, 0, 255], [255, 0, 170], [255, 0, 85]]

idFrame = 101

image = mpimg.imread(path+"/ssl_images/ssl_image_"+str(idFrame)+".jpg")
data = image[:,:,0]
nb_fig = 2
col = ["blue", "red", "green", "yellow"]
def traite_data(data):
    res = []
    for y, l in enumerate(data):
        for x, i in enumerate(l):
            i /= 20
            for _ in range(i):
                res.append([x,y])
    return np.array(res)
res = traite_data(data)
model = GaussianMixture(n_components=nb_fig,covariance_type="spherical")
model.fit(res)
print(model.bic(res))
from matplotlib.patches import Ellipse
plt.imshow(image)
ax = plt.gca()
for i in range(nb_fig):
    ell = Ellipse(model.means_[i],model.covariances_[i]/5, model.covariances_[i]/5, fill=False, color=col[i])
    ax.add_patch(ell)


idx=1
cap = cv2.VideoCapture(path+"/video.avi")
capssl = cv2.VideoCapture(path+"/ssl.avi")
numberFrame=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
frameShape=(int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)))
framesDic=[{'det':[],'idx':[],'speaking':[]} for n in range(numberFrame)]


preds= open(predictionFileName)
lines =preds.readlines()


for idx, line in enumerate(lines):
    elements = line.split(' ')
    idxFrame = int(elements[0]) - 1
    framesDic[idxFrame]['det'].append(map(lambda x: int(float(x)), elements[3:]))
    framesDic[idxFrame]['idx'].append(int(elements[1]))
    framesDic[idxFrame]['speaking'].append(int(elements[2]))

idxFrame = 0
while True:
    ret2, frameSSL = capssl.read()
    if (not ret2):
        end = True
        break

    ssl = cv2.resize(frameSSL, (frameShape[1], frameShape[0]), interpolation=cv2.INTER_CUBIC)
    framesDic[idxFrame]['ssl'] = ssl
    idxFrame += 1

idxFrame = 0
k=0
# We display all the element of the dict
while True:
    ret, frame = cap.read()
    if (not ret) or 'ssl' not in framesDic[idxFrame]:
        end = True
        break

    # we convert the ssl to color heatmap
    sslDisplay = cv2.applyColorMap(framesDic[idxFrame]['ssl'], cv2.COLORMAP_JET)
    matdisp = cv2.addWeighted(frame, 0.7, sslDisplay, 0.3, 0)

    # we display the poses

    for nbDet, detm in enumerate(framesDic[idxFrame]['det']):
        det = list(detm)
        for pt in range(0, 35, 2):
            # we display in bigger if the person is speaking
            if framesDic[idxFrame]['speaking'][nbDet] == 1:  # The person is speaking
                size = 5
            else:
                size = 2
            yi = det[pt]
            xi = det[pt + 1]
            if xi > 0 and yi > 0:
                cv2.circle(matdisp, (yi, xi), size, colors[framesDic[idxFrame]['idx'][nbDet]], size)

    cv2.imshow('Predictions', matdisp)
    cv2.waitKey(10)
    idxFrame += 1

    while idxFrame == idFrame:
        k += 1
        plt.show()



