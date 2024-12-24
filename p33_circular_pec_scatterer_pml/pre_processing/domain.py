import gmsh
import os
import numpy as np
from scipy.constants import mu_0, epsilon_0

# Limpar o terminal
os.system('cls' if os.name == 'nt' else 'clear')

OMEGA = 2 * np.pi * 3E8

K0 = OMEGA * np.sqrt(mu_0 * epsilon_0)

WAVELENGTH = 2 * np.pi / K0

FINITE_ELEMENT = ("Triangle", 1)

BOUNDARY = [{'tag': 101, 'type': 'Dirichlet', 'value': None, 'name': 'circular_scatterer'},
            {'tag': 102, 'type': 'PML', 'value': None, 'name': 'inner_truncated_domain'},
            {'tag': 103, 'type': 'PML', 'value': None, 'name': 'outer_truncated_domain'}]

MATERIAL = [{'tag': 201, 'name': 'PML',
             'relative_magnetic_permeability': 1, 'relative_electric_permittivity': 1},
             {'tag': 202, 'name': 'free_space',
             'relative_magnetic_permeability': 1, 'relative_electric_permittivity': 1}]

RADII = {'a': WAVELENGTH/2, 
            'R1': WAVELENGTH * 0.75, 'R2': WAVELENGTH, 
            'R3': WAVELENGTH * 1.25, 'R4': WAVELENGTH * 1.5}

OMEGA = {'a': {'h': WAVELENGTH/10, 'L': WAVELENGTH/2, 'ra': WAVELENGTH/2, 'x0': WAVELENGTH}}

# Define os parâmetros de entrada
_, order = FINITE_ELEMENT

# Inicializar o Gmsh
gmsh.initialize()
gmsh.model.add("rectangular_pml")
factory = gmsh.model.occ

# Dimensões do domínio 
h = OMEGA['a']['h']     # Tamanho do elemento
L = OMEGA['a']['L']     # Lado do retângulo externo
ra = OMEGA['a']['ra']   # Raio do furo circular
x0 = OMEGA['a']['x0']   # Lado do retângulo interno
y0 = x0
x_ext = x0 + L
y_ext = y0 + L

# Criar as superfícies retangulares externa e interna
rect_outer = factory.addRectangle(-(x0 + L), -(y0 + L), 0, 2 * (x0 + L), 2 * (y0 + L))
rect_inner = factory.addRectangle(-x0, -y0, 0, 2 * x0, 2 * y0)

# Criar o furo circular no centro do retângulo interno
disk = factory.addDisk(0, 0, 0, ra, ra)

# Subtrair o retângulo interno do retângulo externo
outDimTags_plm_omega, _ = factory.cut([(2, rect_outer)], [(2, rect_inner)], removeTool=False)

# Subtrair o furo circular do retângulo interno
outDimTags_fs_omega, _ = factory.cut([(2, rect_inner)], [(2, disk)], removeTool=True)

# Sincronizar após o corte do retângulo interno
factory.synchronize()

# Obter os contornos (curvas, dim=1) de cada superfície
boundary_pml_ext = gmsh.model.getBoundary(outDimTags_plm_omega, oriented=True, recursive=False)
boundary_pml_inn = gmsh.model.getBoundary(outDimTags_fs_omega, oriented=True, recursive=False)

# Exibir os TAGs das curvas associadas a cada contorno
print("Curvas do contorno externo (rect_outer):", boundary_pml_ext)
print("Curvas do contorno interno (rect_inner):", boundary_pml_inn)

tagList_scatterer = [-tag[1] for tag in boundary_pml_inn if tag[1] < 0]
tagList_pml_inn = [tag[1] for tag in boundary_pml_inn if tag[1] > 0]
tagList_pml_ext = [tag[1] for tag in boundary_pml_ext if tag[1] > 0]

# Adicionar grupos físicos para curvas (Dim=1)
print("Grupos físicos de Dim=1")
for i, CurveTagList in enumerate([tagList_scatterer, tagList_pml_inn, tagList_pml_ext]):
    print(BOUNDARY[i]['tag'], CurveTagList)
    gmsh.model.addPhysicalGroup(1, CurveTagList, tag=BOUNDARY[i]['tag'], name=BOUNDARY[i]['name'])

# Adicionar grupos físicos para superfícies (Dim=2)	    
print("Grupos físicos de Dim=2")
for i, SurfaceList in enumerate([outDimTags_plm_omega, outDimTags_fs_omega]):
    SurfaceTagList = [DimTag[1] for DimTag in SurfaceList]
    print(MATERIAL[i]['tag'], SurfaceTagList)
    gmsh.model.addPhysicalGroup(2, SurfaceTagList, tag=MATERIAL[i]['tag'], name=MATERIAL[i]['name'])

# Definir ordem dos elementos
gmsh.option.setNumber("Mesh.MeshSizeMax", h)
gmsh.option.setNumber("Mesh.MeshSizeMin", h)
gmsh.model.mesh.generate(2)
gmsh.model.mesh.setOrder(order)

# Visualizar a malha no ambiente Gmsh (opcional)
gmsh.fltk.run()

# Finalizar o Gmsh
gmsh.finalize()