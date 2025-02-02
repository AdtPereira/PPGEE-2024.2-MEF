import pickle
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ipywidgets as widgets
from IPython.display import display
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

# Adicionando sliders para controle de elevação e azimute
def plot_3d_mesh(FINITE_ELEMENT, INFO_GRAPH, mesh_data):
    # Dados do gráfico
    show_cell = INFO_GRAPH['cell']
    show_nodes = INFO_GRAPH['nodes']
    show_edges = INFO_GRAPH['edges']
    show_edges_numb = INFO_GRAPH['edges_numb']

    # Tipo de Elemento
    ElementType, _ = FINITE_ELEMENT
    
    # Estruturando os dados da malha
    nodes_data = mesh_data['nodes']
    
    # Função para atualizar o gráfico com base nos sliders
    def update_plot(elev=20, azim=30):
        fig = plt.figure(figsize=(8, 6))
        ax = fig.add_subplot(111, projection='3d')
        
        if ElementType == "Tetrahedron":
            # Plotando a malha de elementos finitos
            for cell in mesh_data['cell'].values():
                vertices = [nodes_data[node]['xg'] for node in cell['conn']]
                faces = [[vertices[i] for i in face] for face in [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]]
                ax.add_collection3d(Poly3DCollection(faces, alpha=0.3, edgecolor='gray'))

            # Plotando as arestas
            if show_edges or show_edges_numb:
                for key, edge in mesh_data['edges'].items():
                    x0, y0, z0 = nodes_data[edge['conn'][0]]['xg']
                    x1, y1, z1 = nodes_data[edge['conn'][1]]['xg']
                    ax.plot([x0, x1], [y0, y1], [z0, z1], 'b', lw=0.5)
                    
                    if show_edges_numb:
                        mid_point = np.mean([nodes_data[edge['conn'][0]]['xg'], nodes_data[edge['conn'][1]]['xg']], axis=0)
                        ax.text(*mid_point, str(key), color='blue', fontsize=6)

            # Adicionando nós
            if show_nodes:
                for key, node in nodes_data.items():
                    x, y, z = node['xg']
                    ax.scatter(x, y, z, color='white', edgecolor='black', s=30)
                    ax.text(x, y, z, str(key), color='red', fontsize=6)
            
            # Adicionando rótulo dos elementos
            if show_cell:
                for key, cell in mesh_data['cell'].items():
                    centroid = np.mean([nodes_data[node]['xg'] for node in cell['conn']], axis=0)
                    ax.text(*centroid, str(key), fontweight='bold', color='black', fontsize=6)

        # Ajustando rótulos e layout
        ax.set_xlabel(r'$x$')
        ax.set_ylabel(r'$y$')
        ax.set_zlabel(r'$z$')
        ax.view_init(elev=elev, azim=azim)
        plt.tight_layout()
        plt.show()

    # Criando sliders para controlar a elevação e azimute
    elev_slider = widgets.IntSlider(min=0, max=90, step=1, value=20, description='Elevação')
    azim_slider = widgets.IntSlider(min=0, max=360, step=1, value=30, description='Azimute')

    # Exibindo os sliders
    display(widgets.interactive(update_plot, elev=elev_slider, azim=azim_slider))

# Carregar mesh_data com pickle
with open('p53_rectangular_cavity/mesh_data.pkl', 'rb') as f:
    mesh_data = pickle.load(f)

# Dados do gráfico
FINITE_ELEMENT = ('Tetrahedron', 1)
INFO_GRAPH = {'cell': False, 'nodes': True, 'edges': False, 'edges_numb': False}

plot_3d_mesh(FINITE_ELEMENT, INFO_GRAPH, mesh_data)
