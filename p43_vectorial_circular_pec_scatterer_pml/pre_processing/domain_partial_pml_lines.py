import gmsh
import os
import numpy as np
from scipy.constants import mu_0, epsilon_0

# Limpar o terminal
os.system('cls' if os.name == 'nt' else 'clear')

DOMAIN = 2 * np.pi * 3E8
K0 = DOMAIN * np.sqrt(mu_0 * epsilon_0)
WAVELENGTH = 2 * np.pi / K0
FINITE_ELEMENT = ("Triangle", 1)

BOUNDARY = [{'tag': 101, 'type': 'Dirichlet', 'value': None, 'name': 'circular_scatterer'},
            {'tag': 102, 'type': 'Free', 'value': None, 'name': 'free_space'},
            {'tag': 103, 'type': 'Free', 'value': None, 'name': 'outer_pml'},
            {'tag': 104, 'type': 'Free', 'value': None, 'name': 'horizontal_cut_line'}]

MATERIAL = [{'tag': 201, 'name': 'free_space', 'relative_magnetic_permeability': 1, 'relative_electric_permittivity': 1},
            {'tag': 202, 'name': 'pml_xy', 'relative_magnetic_permeability': 1, 'relative_electric_permittivity': 1},
            {'tag': 203, 'name': 'pml_x', 'relative_magnetic_permeability': 1, 'relative_electric_permittivity': 1},
            {'tag': 204, 'name': 'pml_y', 'relative_magnetic_permeability': 1, 'relative_electric_permittivity': 1}]

DOMAIN = {'a': {'h': WAVELENGTH/5, 'L': WAVELENGTH/2, 'ra': WAVELENGTH/2, 'x0': WAVELENGTH}}
DOMAIN_KEY = 'a'

# Define os parâmetros de entrada
_, order = FINITE_ELEMENT

# Inicializar o Gmsh
gmsh.initialize()
gmsh.model.add("rectangular_pml")
factory = gmsh.model.occ

# Dimensões do domínio 
h = DOMAIN[DOMAIN_KEY]['h']     # Tamanho do elemento finito
L = DOMAIN[DOMAIN_KEY]['L']     # Lado do retângulo externo
ra = DOMAIN[DOMAIN_KEY]['ra']   # Raio do furo circular
x0 = DOMAIN[DOMAIN_KEY]['x0']   # Lado do retângulo interno
xa = x0
xb = x0 + L
y0 = x0
x_ext = x0 + L
y_ext = y0 + L

# Criar regiões absorvedoras retangulares, omega_PML
region_a = factory.addRectangle(-xb, -xb, 0, L, L)
region_e = factory.addRectangle(-xa, -xb, 0, 2*x0, L)
region_b = factory.addRectangle(xa, -xb, 0, L, L)
region_f = factory.addRectangle(xa, -xa, 0, L, 2*x0)
region_c = factory.addRectangle(xa, xa, 0, L, L)
region_g = factory.addRectangle(-xa, xa, 0, 2*x0, L)
region_d = factory.addRectangle(-xb, xa, 0, L, L)
region_h = factory.addRectangle(-xb, -xa, 0, L, 2*x0)

# Criar região do espaço livre, omega_fs
region_fs = factory.addRectangle(-xa, -xa, 0, 2*x0, 2*x0)

# Criar uma linha de integração
CutLineTags = factory.addLine(
    factory.addPoint(ra, 0, 0, h),
    factory.addPoint(xb, 0, 0, h))

# Criar região do espalhador, omega_s
disk = factory.addDisk(0, 0, 0, ra, ra)
outDimTags_omega_s, _ = factory.cut([(2, region_fs)], [(2, disk)], removeTool=True)

# Obter as TAGs das superfícies fragmentadas
factory.synchronize()
FragmentedSurfaceTags = [DimTag[1] for DimTag in gmsh.model.getEntities(dim=2)]
print("TAGs das Superfícies Fragmentadas:", sorted(FragmentedSurfaceTags))

# Fragmentar todas as regiões para garantir interfaces conformais
fragmentedObject = [
    (2, region_fs), (2, region_a), (2, region_e), (2, region_b),
    (2, region_f), (2, region_c), (2, region_g), (2, region_d),
    (2, region_h), (1, CutLineTags)
]
print("Pares (Dim, Tag) dos objetos para conformação:\n", fragmentedObject)

outDimTags, outDimTagsMap = factory.fragment(fragmentedObject, fragmentedObject)
print("Pares (Dim, Tag) dos objetos conformados:\n", outDimTags)

# Sincronizar após o corte do retângulo interno
factory.synchronize()

# Obter os contorno de fronteira
LineTags = [DimTag[1] for DimTag in gmsh.model.getEntities(dim=1)]
print("TAGs dos Contornos:", sorted(LineTags))

# Obter as TAGs das superfícies
SurfaceTags = [DimTag[1] for DimTag in gmsh.model.getEntities(dim=2)]
print("TAGs das Superfícies:", sorted(SurfaceTags))

# Obter o contorno (curva, dim=1) de gamma_s
boundary_free_space = gmsh.model.getBoundary(outDimTags_omega_s, oriented=True)

# Obter o contorno do espalhador e do espaço livre
ScattererTags = [-DimTag[1] for DimTag in boundary_free_space if DimTag[1] < 0]
print("Contorno do espalhador:", ScattererTags)

FreeSpaceTags = [DimTag[1] for DimTag in boundary_free_space if DimTag[1] > 0]
print("Contorno do espaço livre:", FreeSpaceTags)

def get_pml_boundary(tag_region, name):
    tags = sorted([DimTag[1] for DimTag in gmsh.model.getBoundary([(2, tag_region)], oriented=False)])
    print(f"Contorno de {name}:", tags)
    return tags

# Obter o contorno (curva, dim=1) de PML
pml_a = get_pml_boundary(1, 'PML_a')
pml_b = get_pml_boundary(3, 'PML_b')
pml_c = get_pml_boundary(5, 'PML_c')
pml_d = get_pml_boundary(7, 'PML_d')
pml_i = get_pml_boundary(2, 'PML_i')
pml_ii = get_pml_boundary(10, 'PML_ii')
pml_iii = get_pml_boundary(11, 'PML_iii')
pml_iv = get_pml_boundary(6, 'PML_iv')
pml_v = get_pml_boundary(8, 'PML_v')

# Obter o conjunto de contornos pml
pml_xy = pml_a + pml_b + pml_c + pml_d
pml_x = pml_ii + pml_iii + pml_v
pml_y = pml_i + pml_iv
pml_list = pml_xy + pml_x + pml_y
print("Contorno da PML:", pml_list)

# Obter os contornos internos
cut_line_pml = list(set(pml_ii) & set(pml_iii))
cut_line_fs = list(set(LineTags) - set(pml_list) - set(ScattererTags))
CutLineTags = cut_line_pml + cut_line_fs
print("Contornos internos:", CutLineTags)

# Obter o contorno externo da PML
from collections import Counter
PmlOuterTags = sorted([key for key, value in Counter(pml_list+FreeSpaceTags).items() if value == 1])
print("Contorno externo da PML:", PmlOuterTags)

# Adicionar grupos físicos para curvas (Dim=1)
print("Grupos físicos de Dim=1")
PhysicalGroupsDim1 = [ScattererTags, FreeSpaceTags, PmlOuterTags, CutLineTags]
for i, curves in enumerate(PhysicalGroupsDim1):
    print(BOUNDARY[i]['tag'], curves)
    gmsh.model.addPhysicalGroup(1, curves, tag=BOUNDARY[i]['tag'], name=BOUNDARY[i]['name'])

# Adicionar grupos físicos para superfícies (Dim=2)    
print("Grupos físicos de Dim=2")
PhysicalGroupsDim2 = [[9], [1, 3, 5, 7], [8, 10, 11], [2, 6]]
for i, surfaces in enumerate(PhysicalGroupsDim2):
    print(MATERIAL[i]['tag'], surfaces)
    gmsh.model.addPhysicalGroup(2, surfaces, tag=MATERIAL[i]['tag'], name=MATERIAL[i]['name'])

# Definir ordem dos elementos
gmsh.option.setNumber("Mesh.MeshSizeMax", h)
gmsh.option.setNumber("Mesh.MeshSizeMin", h)
gmsh.model.mesh.generate(2)
gmsh.model.mesh.setOrder(order)

# Visualizar a malha no ambiente Gmsh (opcional)
gmsh.fltk.run()

# Finalizar o Gmsh
gmsh.finalize()