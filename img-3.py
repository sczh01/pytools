

from skimage import io,data
import matplotlib.pyplot as plt
img=data.rocket()
ar=img[:,:,0].flatten()
plt.hist(ar, bins=256, normed=1,facecolor='r',edgecolor='r',hold=1)
ag=img[:,:,1].flatten()
plt.hist(ag, bins=256, normed=1, facecolor='g',edgecolor='g',hold=1)
ab=img[:,:,2].flatten()
plt.hist(ab, bins=256, normed=1, facecolor='b',edgecolor='b')
plt.show()

