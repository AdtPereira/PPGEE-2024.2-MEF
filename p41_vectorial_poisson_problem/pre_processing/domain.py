import gmsh
import os

# Limpar o terminal
os.system('cls' if os.name == 'nt' else 'clear')

FINITE_ELEMENT = ("Triangle", 1)

BOUNDARY = [{'tag': 101, 'type': 'Dirichlet', 'value': 0.0, 'name': 'outer_domain'}]

MATERIAL = [{'tag': 201, 'name': 'free_space',
             'relative_magnetic_permeability': 1, 'relative_electric_permittivity': 1}]

# Define os parâmetros de entrada
element, order = FINITE_ELEMENT
h = 2

# Inicializar o Gmsh
gmsh.initialize()
gmsh.model.add("rectangular_pml")
factory = gmsh.model.occ

# Criar as superfícies retangulares externa e interna
TagSurface = factory.addRectangle(-1, -1, 0, 2, 2)
print("Tag da superfície retangular:", TagSurface)

# Sincronizar após o corte do retângulo interno
factory.synchronize()

# Obter os contornos (curvas, dim=1) de cada superfície
outDimTags_boundary = gmsh.model.getBoundary([(2, TagSurface)], oriented=True, recursive=False)
print("Contornos da superfície externa:", outDimTags_boundary)

# Exibir os TAGs das curvas associadas a cada contorno
tagList_boundary = [Dimtags[1] for Dimtags in outDimTags_boundary]
print("TAGs das curvas do contorno externo:", tagList_boundary)

# Definir ordem dos elementos
gmsh.option.setNumber("Mesh.MeshSizeMin", h)
gmsh.model.mesh.generate(2)
gmsh.model.mesh.setOrder(order)

# # Like elements, mesh edges and faces are described by (an ordered list of)
# # their nodes. Let us retrieve the edges and the (triangular) faces of all the
# # first order tetrahedra in the mesh:
# elementType = gmsh.model.mesh.getElementType(element, order)
# if elementType == 2:
#     print("Tipo de elemento: 3-node triangle.")

# NodeTags = gmsh.model.mesh.getElementEdgeNodes(elementType)
# print("Nós das arestas do elemento:", NodeTags)

# Edges and faces are returned for each element as a list of nodes corresponding
# to the canonical orientation of the edges and faces for a given element type.

# Gmsh can also identify unique edges and faces (a single edge or face whatever
# the ordering of their nodes) and assign them a unique tag. This identification
# can be done internally by Gmsh (e.g. when generating keys for basis
# functions), or requested explicitly as follows:
gmsh.model.mesh.createEdges()

# # Edge and face tags can then be retrieved by providing their nodes:
# edgeTags, edgeOrientations = gmsh.model.mesh.getEdges(NodeTags)
# print("TAGs das arestas do elemento: (edgeTags)", edgeTags)
# print("Orientações das arestas do elemento:", edgeOrientations)

# # Since element edge and face nodes are returned in the same order as the
# # elements, one can easily keep track of which element(s) each edge or face is
# # connected to:
# elementTags, elementNodeTags = gmsh.model.mesh.getElementsByType(elementType)

# print("TAGs dos elementos:", elementTags)
# print("Nós dos elementos:", elementNodeTags)

# # Inicializa o dicionário de mapeamento de arestas
# edges2Elements = {}

# # Verifica se o número total de edges é múltiplo de 3
# if len(edgeTags) % 3 != 0:
#     print("Erro: O número total de arestas não é múltiplo de 3. Verifique a malha gerada.")
# else:
#     # Percorre edgeTags em blocos de três
#     for i in range(0, len(edgeTags), 3):
#         # Cria uma entrada no dicionário para o triângulo
#         edges2Elements[i // 3 + 1] = edgeTags[i : i + 3].tolist()

# print("Arestas conectadas aos elementos (edges2Elements):", edges2Elements)

# If all you need is the list of all edges or faces in terms of their nodes, you
# can also directly call:
All_edgeTags, All_edgeNodes = gmsh.model.mesh.getAllEdges()
print("TAGs das arestas (AlledgeTags):", All_edgeTags)
print("Nós das arestas (AlledgeNodes):", All_edgeNodes)

# Create connection between edges and elements
edge_mapping = {}

# Percorre os nós em pares e associa aos AlledgeTags
for i, tag in enumerate(All_edgeTags):
    # Adiciona ao mapeamento usando o TAG da aresta como chave
    edge_mapping[tag] = sorted([All_edgeNodes[2 * i], All_edgeNodes[2 * i + 1]])

# Ordena o dicionário edge_mapping com base nas chaves
sorted_edge_mapping = {key: edge_mapping[key] for key in sorted(edge_mapping.keys())}

# Exibe o mapeamento de arestas
print("Mapeamento de arestas (edge_mapping):", edge_mapping)
print("Mapeamento de arestas ordenado (sorted_edge_mapping):", sorted_edge_mapping)

# Visualizar a malha no ambiente Gmsh (opcional)
# gmsh.fltk.run()

# Finalizar o Gmsh
gmsh.finalize()