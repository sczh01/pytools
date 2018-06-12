from skimage import data
import matplotlib.pyplot as plt
img=data.camera()
plt.figure("hist")
arr=img.flatten()
n, bins, patches = plt.hist(arr, bins=256, normed=1,edgecolor='None',facecolor='red')  
plt.show()