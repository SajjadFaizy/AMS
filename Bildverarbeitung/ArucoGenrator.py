# Libraries
from cv2 import aruco
import matplotlib.pyplot as plt

# Generate Aruco
ar_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)

# Plot SetUp
fig = plt.figure() # New fig

nx = 4 #Columns     | In total there will
ny = 3 #Rows        | be 12 Arucos displayed

for k in range(1, nx*ny+1):
    ax = fig.add_subplot(ny, nx, k) # Generates 12 subplots
    img = aruco.generateImageMarker(ar_dict, k, 700) # Generates 12 700x700px images for each subplot
    plt.imshow(img, cmap='gray', interpolation="nearest") # Grayscale, nearest= sharp and pixelated scalation of images
    ax.axis("off")

# plt.savefig("markers.pdf") - Si no funciona plt.show() para generar un pdf
plt.show()