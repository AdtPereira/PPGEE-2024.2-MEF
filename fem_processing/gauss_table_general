import numpy as np

def gauss(n, a, b):
    """
    Gera pontos de quadratura e pesos no intervalo I = [a, b] (para quadratura de Gauss).
    
    Referências:
        1. https://en.wikipedia.org/wiki/Gaussian_quadrature#The_Golub-Welsch_algorithm
        2. https://basicfem.ju.se/NumericalIntegration/
    
    Parâmetros:
    ----------
    n : int
        Número de pontos de quadratura.
    a : float
        Extremidade esquerda do intervalo.
    b : float
        Extremidade direita do intervalo.
    
    Retorna:
    -------
    x : numpy.ndarray
        Pontos de quadratura.
    w : numpy.ndarray
        Pesos de quadratura.
    A : float
        Área do domínio (extensão do intervalo).
    """
    
    if n <= 0 or not isinstance(n, int):
        raise ValueError("O número de pontos 'n' deve ser um inteiro positivo.")
    
    if a >= b:
        raise ValueError("O extremo esquerdo 'a' deve ser menor que o extremo direito 'b'.")

    # Coeficientes de recorrência de 3 termos
    indices = np.arange(1, n)
    beta = 1.0 / np.sqrt(4.0 - 1.0 / (indices * indices))
    
    # Matriz de Jacobi
    J = np.diag(beta, 1) + np.diag(beta, -1)
    
    # Decomposição espectral (autovalores e autovetores)
    D, V = np.linalg.eig(J)
    
    # Pontos de quadratura (autovalores de J)
    x = np.sort(D)
    
    # Área do domínio
    A = b - a
    
    # Mudança de intervalo (mapeia de [-1, 1] para [a, b])
    if not (a == -1 and b == 1):
        x = 0.5 * A * x + 0.5 * (b + a)
    
    # Pesos de quadratura (quadrado da primeira linha de V)
    w = (V[0, :] ** 2) * 2
    
    return x, w, A

# Teste
x, w, A = gauss(n=4, a=0, b=1)
print("Pontos de quadratura:", x)
print("Pesos de quadratura:", w)
print("Área do domínio:", A)
