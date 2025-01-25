import gmsh
import os
import numpy as np
from scipy.constants import speed_of_light

# Limpar o terminal
os.system('cls' if os.name == 'nt' else 'clear')

FREQUENCY = 3E8 # Hz
WAVELENGTH = speed_of_light/FREQUENCY
K0 = 2 * np.pi / WAVELENGTH
OMEGA = 2 * np.pi * FREQUENCY

FINITE_ELEMENT = ("Triangle", 1)

BOUNDARY = [{'tag': 101,'type': 'ABC', 'value': None, 'name': 'x0'},
            {'tag': 102, 'type': 'ABC', 'value': None, 'name': 'xL'}]

MATERIAL = [{'tag': 201, 'name': 'free_space',
                'relative_magnetic_permeability': 1,
                'relative_electric_permittivity': 1},
            {'tag': 202, 'name': 'lossy_slab',
                'relative_magnetic_permeability': 1,
                'electric_conductivity': 1,
                'relative_electric_permittivity': 1}]

INTERFACES = [{'tag': 301, 'type': 'fs_slab', 'value': None, 'name': 'xa'},
              {'tag': 302, 'type': 'slab_fs', 'value': None, 'name': 'xb'}]

GEOMETRY = {'a': {'h': WAVELENGTH/10, 'L': 2, 'd': 0.25}}
GEO_KEY = 'a'

# Define os parâmetros de entrada
_, order = FINITE_ELEMENT

# Inicializar o Gmsh
gmsh.initialize()
gmsh.model.add("lossy_dielectric_slab_abc")
factory = gmsh.model.occ

# Dimensões do domínio 
h = GEOMETRY[GEO_KEY]['h']     # Tamanho do elemento finito
L = GEOMETRY[GEO_KEY]['L']     # Tamanho do domínio computacional 1-D
d = GEOMETRY[GEO_KEY]['d']     # Espessura da placa dielétrica
xa, xb = L/2 - d/2, L/2 + d/2

# Criar domínio computacional omega_c
left_fs = factory.addLine(
    factory.addPoint(0, 0, 0, h),
    factory.addPoint(xa, 0, 0, h))

# Criar domínio computacional omega_c
lossy_slab = factory.addLine(
    factory.addPoint(xa, 0, 0, h),
    factory.addPoint(xb, 0, 0, h))

# Criar domínio computacional omega_c
right_fs = factory.addLine(
    factory.addPoint(xb, 0, 0, h),
    factory.addPoint(L, 0, 0, h))

# Fragmentar todas as regiões para garantir interfaces conformais
fragmentedObject = [(1, left_fs), (1, lossy_slab), (1, right_fs)]
outDimTags, outDimTagsMap = factory.fragment(fragmentedObject, fragmentedObject)
print("Pares (Dim, Tag) dos objetos conformados:\n", outDimTags)

# Sincronizar após o corte do retângulo interno
factory.synchronize()

# Obter os domínios 1D de fronteira
OmegacTags = [DimTag[1] for DimTag in gmsh.model.getEntities(dim=1)]
print("TAGs dos contornos (Dim=1):\n", sorted(OmegacTags))

# Obter as fronteiras do domínio (curva, dim=1)
BoundariesDimTags = gmsh.model.getBoundary(outDimTags, oriented=True)
print("Fronteiras do domínio:\n", BoundariesDimTags)

# Obter as fronteira da interface (curva, dim=1)
InterfacesDimTags = gmsh.model.getBoundary([(1, 2)], oriented=True)
print("Fronteiras da interface:\n", InterfacesDimTags)

# Adicionar grupos físicos para pontos (Dim=0)
print("Grupos físicos para contornos (Dim=0)")
for i, dots in enumerate([DimTag[1] for DimTag in BoundariesDimTags]):
    print(BOUNDARY[i]['tag'], [dots])
    gmsh.model.addPhysicalGroup(0, [dots], tag=BOUNDARY[i]['tag'], name=BOUNDARY[i]['name'])

# Adicionar grupos físicos para pontos (Dim=0)
print("Grupos físicos para interfaces (Dim=0)")
for i, dots in enumerate([DimTag[1] for DimTag in InterfacesDimTags]):
    print(INTERFACES[i]['tag'], [dots])
    gmsh.model.addPhysicalGroup(0, [dots], tag=INTERFACES[i]['tag'], name=INTERFACES[i]['name'])

# Adicionar grupos físicos dos contornos (Dim=1)    
print("Grupos físicos para os contornos (Dim=2)")
for i, contours in enumerate([[1, 3], [2]]):
    print(MATERIAL[i]['tag'], contours)
    gmsh.model.addPhysicalGroup(1, contours, tag=MATERIAL[i]['tag'], name=MATERIAL[i]['name'])

# Definir ordem dos elementos
gmsh.option.setNumber("Mesh.MeshSizeMax", h)
gmsh.option.setNumber("Mesh.MeshSizeMin", h)
gmsh.model.mesh.generate(1)
gmsh.model.mesh.setOrder(order)

# Visualizar a malha no ambiente Gmsh (opcional)
gmsh.fltk.run()

# Finalizar o Gmsh
gmsh.finalize()