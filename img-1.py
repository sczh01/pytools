import numpy as np
from skimage import exposure,data
image =data.camera()*1.0
hist1=np.histogram(image, bins=2)   #用numpy包计算直方图
hist2=exposure.histogram(image, nbins=2)  #用skimage计算直方图
print(hist1)
print(hist2)