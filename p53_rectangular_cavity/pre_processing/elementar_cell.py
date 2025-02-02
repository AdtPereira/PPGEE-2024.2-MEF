import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def plot_tetrahedral_decomposition():
    # Definição dos vértices do cubo
    vertices = np.array([
        [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
        [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1]
    ])
    
    # Conectividades dos 6 tetraedros
    tetrahedra = [
        [0, 1, 3, 5],
        [3, 1, 2, 5],
        [3, 5, 2, 7],
        [2, 5, 6, 7],
        [0, 3, 5, 4],
        [5, 4, 7, 3]
    ]
    
    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan']
    
    for i, tet in enumerate(tetrahedra):
        faces = [
            [vertices[tet[0]], vertices[tet[1]], vertices[tet[2]]],
            [vertices[tet[0]], vertices[tet[1]], vertices[tet[3]]],
            [vertices[tet[1]], vertices[tet[2]], vertices[tet[3]]],
            [vertices[tet[0]], vertices[tet[2]], vertices[tet[3]]]
        ]
        
        poly3d = [[list(p) for p in face] for face in faces]
        ax.add_collection3d(Poly3DCollection(poly3d, alpha=0.5, facecolor=colors[i]))
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_zlim([0, 1])
    plt.show()

plot_tetrahedral_decomposition()
