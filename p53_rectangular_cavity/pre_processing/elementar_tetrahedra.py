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
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10), subplot_kw={'projection': '3d'})
    axes = axes.flatten()
    
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'cyan']
    
    for i, tet in enumerate(tetrahedra):
        ax = axes[i]
        for j, ref_tet in enumerate(tetrahedra):
            faces = [
                [vertices[ref_tet[0]], vertices[ref_tet[1]], vertices[ref_tet[2]]],
                [vertices[ref_tet[0]], vertices[ref_tet[1]], vertices[ref_tet[3]]],
                [vertices[ref_tet[1]], vertices[ref_tet[2]], vertices[ref_tet[3]]],
                [vertices[ref_tet[0]], vertices[ref_tet[2]], vertices[ref_tet[3]]]
            ]
            poly3d = [[list(p) for p in face] for face in faces]
            face_color = colors[j] if j == i else 'gray'
            alpha = 0.8 if j == i else 0.2
            ax.add_collection3d(Poly3DCollection(poly3d, alpha=alpha, facecolor=face_color))
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim([0, 1])
        ax.set_ylim([0, 1])
        ax.set_zlim([0, 1])
        ax.set_title(f'Tetraedro {i+1}')
    
    plt.tight_layout()
    plt.show()

plot_tetrahedral_decomposition()
