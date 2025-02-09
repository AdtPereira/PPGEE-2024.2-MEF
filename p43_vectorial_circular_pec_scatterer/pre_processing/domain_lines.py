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

MATERIAL = [{'tag': 201, 'name': 'free_space', 'relative_magnetic_permeability': 1, 'relative_electric_permittivity': 1},
             {'tag': 202, 'name': 'pml', 'relative_magnetic_permeability': 1, 'relative_electric_permittivity': 1}]

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
xa = x0
xb = x0 + L
x_ext = x0 + L
y_ext = y0 + L

# Criar as superfícies retangulares externa e interna
rect_outer = factory.addRectangle(-(x0 + L), -(y0 + L), 0, 2 * (x0 + L), 2 * (y0 + L))
rect_inner = factory.addRectangle(-x0, -y0, 0, 2 * x0, 2 * y0)

# Criar o furo circular no centro do retângulo interno
disk = factory.addDisk(0, 0, 0, ra, ra)

# Criar um contorno de integração no espaço livre
fs_contour = factory.addLine(
    factory.addPoint(ra, 0, 0, h),
    factory.addPoint(xa, 0, 0, h))

# Criar um contorno de integração na PML
pml_contour = factory.addLine(
    factory.addPoint(xa, 0, 0, h),
    factory.addPoint(xb, 0, 0, h))

# Subtrair o retângulo interno do retângulo externo
outDimTags_omega_plm, _ = factory.cut([(2, rect_outer)], [(2, rect_inner)], removeTool=False)
print("outDimTags_omega_plm:", outDimTags_omega_plm)

# Subtrair o furo circular do retângulo interno
outDimTags_omega_fs, _ = factory.cut([(2, rect_inner)], [(2, disk)], removeTool=True)
print("outDimTags_omega_fs:", outDimTags_omega_fs)

# Fragmentar todas as regiões para garantir interfaces conformais
objectDimTags = outDimTags_omega_fs + outDimTags_omega_plm + [(1, fs_contour)] + [(1, pml_contour)]
print("Pares (Dim, Tag) dos objetos para conformação:\n", objectDimTags)

outDimTags, outDimTagsMap = factory.fragment(objectDimTags, objectDimTags)
print("Pares (Dim, Tag) dos objetos conformados:\n", outDimTags)

# Sincronizar após o corte do retângulo interno
factory.synchronize()

# Obter as TAGs das superfícies
SurfaceTags = [DimTag[1] for DimTag in gmsh.model.getEntities(dim=2)]
print("TAGs das Superfícies:", SurfaceTags)

# Obter os contorno de fronteira
LineTags = [DimTag[1] for DimTag in gmsh.model.getEntities(dim=1)]
print("TAGs dos Contornos:", LineTags)

# Obter os contornos (curvas, dim=1) de cada superfície
boundary_pml_ext = gmsh.model.getBoundary(outDimTags_omega_plm, oriented=True)
boundary_pml_inn = gmsh.model.getBoundary(outDimTags_omega_fs, oriented=True)

# Obter os TAGs das curvas de interesse
ScattererTag = [-tag[1] for tag in boundary_pml_inn if tag[1] < 0]
print("Curvas do contorno do espalhador (ScattererTag):", ScattererTag)

PmlInnTags = [tag[1] for tag in boundary_pml_inn if tag[1] > 0]
print("Curvas do contorno interno (PmlInnTags):", sorted(PmlInnTags))

PmlExtTags = [tag[1] for tag in boundary_pml_ext if tag[1] > 0]
print("Curvas do contorno externo (PmlExtTags):", sorted(PmlExtTags))

# Obter os contornos internos
boundary_list = PmlInnTags + PmlExtTags + ScattererTag
InnerLineTags = [tag for tag in LineTags if tag not in boundary_list]
print("TAGs dos Contornos Internos:", sorted(InnerLineTags))

# Definir ordem dos elementos
gmsh.option.setNumber("Mesh.MeshSizeMax", h)
gmsh.option.setNumber("Mesh.MeshSizeMin", h)
gmsh.model.mesh.generate(2)
gmsh.model.mesh.setOrder(order)

# Visualizar a malha no ambiente Gmsh (opcional)
gmsh.fltk.run()

# Finalizar o Gmsh
gmsh.finalize()