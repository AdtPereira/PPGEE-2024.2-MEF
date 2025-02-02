import numpy as np
import matplotlib.pyplot as plt

def shape_functions_n0_tetra(xi, eta, zeta):
    """
    Retorna as funções de forma vetoriais para o elemento tetraédrico do tipo 1, ordem 0.
    """
    return [
        np.array([[1 - eta - zeta], [xi], [xi]]),
        np.array([[eta], [1 - xi - eta], [eta]]),
        np.array([[zeta], [zeta], [1 - xi - eta]]),
        np.array([[-eta], [xi], [0]]),
        np.array([[-zeta], [0], [xi]]),
        np.array([[0], [-zeta], [eta]])
    ]

def plot_shape_functions_n0_tetra(idx_selected=None):
    """
    Plota uma ou todas as funções de forma vetoriais de Nedelec do tipo 1 no tetraedro de referência.
    """
    num_points = 10  # Aumentar para uma visualização mais densa
    xi_vals = np.linspace(0, 1, num_points)
    eta_vals = np.linspace(0, 1, num_points)
    zeta_vals = np.linspace(0, 1, num_points)

    xi_grid, eta_grid, zeta_grid = np.meshgrid(xi_vals, eta_vals, zeta_vals)
    inside_tetra = (xi_grid + eta_grid + zeta_grid) <= 1
    xi_grid, eta_grid, zeta_grid = xi_grid[inside_tetra], eta_grid[inside_tetra], zeta_grid[inside_tetra]

    colors = ['blue', 'red', 'green', 'purple', 'orange', 'brown']
    functions_to_plot = [idx_selected] if idx_selected is not None else range(6)
    fig = plt.figure(figsize=(15, 10))

    for i, idx in enumerate(functions_to_plot):
        ax = fig.add_subplot(1, len(functions_to_plot), i + 1, projection='3d')
        u = np.zeros_like(xi_grid)
        v = np.zeros_like(eta_grid)
        w = np.zeros_like(zeta_grid)

        for j, (xi, eta, zeta) in enumerate(zip(xi_grid, eta_grid, zeta_grid)):
            N = shape_functions_n0_tetra(xi, eta, zeta)
            u[j], v[j], w[j] = N[idx][0, 0], N[idx][1, 0], N[idx][2, 0]

        ax.quiver(xi_grid, eta_grid, zeta_grid, u, v, w, length=0.05, color=colors[idx])

        vertices = np.array([[0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1]])
        edges = [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)]
        for edge in edges:
            ax.plot(*zip(*vertices[list(edge)]), color='black')

        ax.set_title(fr'$\hat{{\varphi}}_{{{idx+1}}}$', fontsize=12)
        ax.set_xlabel(r'$\xi$')
        ax.set_ylabel(r'$\eta$')
        ax.set_zlabel(r'$\zeta$')
        ax.set_xlim(-0.1, 1.1)
        ax.set_ylim(-0.1, 1.1)
        ax.set_zlim(-0.1, 1.1)

    plt.tight_layout()
    plt.show()

# Exemplo de uso: plotar apenas a função de forma 1
plot_shape_functions_n0_tetra(idx_selected=2)
