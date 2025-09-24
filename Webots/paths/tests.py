import matplotlib.pyplot as plt
import numpy as np
import os.path as osp

def plot_matrix(matrix, title="Unnamed Matrix"):
    """
    Plot a wavefront- or a binary-matrix (0/1)
    """
    plt.figure(figsize=(8, 8))
    plt.imshow(matrix, cmap="viridis", interpolation="nearest")
    plt.colorbar(label="Value")  # Color scale legend
    plt.title(title)
    
    rows, cols = matrix.shape
    for i in range(rows):
        for j in range(cols):
            value = matrix[i, j]
            plt.text(j, i, str(value), ha='center', va='center', color="white" if value > 0 else "black")
    
    plt.xlabel("X (Columns)")
    plt.ylabel("Y (Rows)")
    plt.gca().invert_yaxis()  # Invertir el eje Y para que (0, 0) esté en la esquina superior izquierda
    plt.grid(False)
    plt.show()









wavefront_matrix = osp.abspath(osp.join(osp.dirname(__file__), "mapa_post_findpath_1.2.npy"))
matrix = np.load(wavefront_matrix)
plot_matrix(matrix,"Optimized Wavefront")

