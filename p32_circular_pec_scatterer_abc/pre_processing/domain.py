import gmsh
import numpy as np
from scipy.constants import mu_0, epsilon_0

OMEGA = 2 * np.pi * 3E8

K0 = OMEGA * np.sqrt(mu_0 * epsilon_0)

WAVELENGTH = 2 * np.pi / K0

FINITE_ELEMENT = ("Triangle", 1)

BOUNDARY = [{'tag': 101, 'type': 'Dirichlet', 'value': None, 'name': 'circular_scatterer'},
            {'tag': 102, 'type': 'BGT', 'value': None, 'name': 'truncated_domain'}]

MATERIAL = [{'tag': 201, 'name': 'free_space', 
             'relative_magnetic_permeability': 1, 'relative_electric_permittivity': 1}]

RADII = {'a': WAVELENGTH/2, 
            'R1': WAVELENGTH * 0.75, 'R2': WAVELENGTH, 
            'R3': WAVELENGTH * 1.25, 'R4': WAVELENGTH * 1.5}

R = 'R4'
h = WAVELENGTH/10

# Define os parâmetros de entrada
type, order = FINITE_ELEMENT

# Inicializar o Gmsh
gmsh.initialize()
gmsh.model.add("circular_pec")
factory = gmsh.model.occ

# Criar os círculos com `gmsh.model.occ.addCircle`
gamma_s = factory.addCircle(0, 0, 0, RADII['a'])
gamma_a = factory.addCircle(0, 0, 0, RADII[R])

# Criar loops das curvas
scatterer = factory.addCurveLoop([gamma_s])
artificial_domain = factory.addCurveLoop([gamma_a])

# Criar superfícies para os dielétricos
free_space = factory.addPlaneSurface([artificial_domain, scatterer])

# Sincronizar geometria
factory.synchronize()

# Adicionar grupos físicos para Dim=1
for i, tag in enumerate([gamma_s, gamma_a]):
    gmsh.model.addPhysicalGroup(1, [tag], tag=BOUNDARY[i]['tag'], name=BOUNDARY[i]['name'])

# Adicionar grupos físicos para Dim=2
gmsh.model.addPhysicalGroup(2, [free_space], tag=MATERIAL[0]['tag'], name=MATERIAL[0]['name'])

# Refinar a malha na borda do espalhador
h_refined = h / 2  # Tamanho menor para o espalhador
gmsh.model.mesh.field.add("Distance", 1)
gmsh.model.mesh.field.setNumbers(1, "CurvesList", [gamma_s])
gmsh.model.mesh.field.setNumber(1, "Sampling", 100)

# Definir um campo de tamanho para refinamento local
gmsh.model.mesh.field.add("Threshold", 2)
gmsh.model.mesh.field.setNumber(2, "InField", 1)
gmsh.model.mesh.field.setNumber(2, "SizeMin", h_refined)
gmsh.model.mesh.field.setNumber(2, "SizeMax", h)
gmsh.model.mesh.field.setNumber(2, "DistMin", RADII['a'] / 10)
gmsh.model.mesh.field.setNumber(2, "DistMax", RADII['a'])

# Ativar o campo de malha
gmsh.model.mesh.field.setAsBackgroundMesh(2)

# Gerar malha 2D
gmsh.option.setNumber("Mesh.SaveAll", 1)

# Definir ordem dos elementos
gmsh.model.mesh.generate(2)
gmsh.model.mesh.setOrder(order)

# Visualizar a malha no ambiente Gmsh (opcional)
gmsh.fltk.run()

gmsh.finalize()
