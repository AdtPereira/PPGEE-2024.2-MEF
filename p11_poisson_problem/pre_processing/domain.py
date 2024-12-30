import gmsh
import os

# Limpar o terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Define os parâmetros de entrada
element, order = ("Triangle", 2)
h = 2

# Inicializar o Gmsh
gmsh.initialize()
gmsh.model.add("rectangular_poisson")

# Criar superfície retangular
TagSurface = gmsh.model.occ.addRectangle(-1, -1, 0, 2, 2)
gmsh.model.occ.synchronize()
gmsh.option.setNumber("Mesh.MeshSizeMin", h)
gmsh.model.mesh.generate(dim=2)
gmsh.model.mesh.setOrder(order)

print("#--------------------------------------------------#")
# Like elements, mesh edges and faces are described by (an ordered list of)
# their nodes. Let us retrieve the edges of all the second order triangles in the mesh:
elementType = gmsh.model.mesh.getElementType(element, order)

# Exibir informações sobre o elemento
print("Tipos de elementos disponíveis:", elementType)
if elementType == 2:
    print("Tipo de elemento: 3-node triangle.")
elif elementType == 9:
    print("Tipo de elemento: 6-node second order triangle.")

# Obter os contornos (curvas, dim=1) de cada superfície
outDimTags = gmsh.model.getBoundary([(2, TagSurface)], oriented=True, recursive=False)
print("TAG da superfície (TagSurface):", TagSurface)
print("Contornos da superfície (outDimTags):", outDimTags)

# Exibir os TAGs das curvas associadas a cada contorno
tagList_boundary = [Dimtags[1] for Dimtags in outDimTags]
print("TAGs das curvas do contorno externo:", tagList_boundary)

# Get the nodes of the edges of the element
NodeTags = gmsh.model.mesh.getElementEdgeNodes(elementType, tag=TagSurface, primary=True)
print("Nós das arestas do elemento (NodeTags):", NodeTags)

# Gmsh can also identify unique edges and faces (a single edge or face whatever
# the ordering of their nodes) and assign them a unique tag. This identification
# can be done internally by Gmsh (e.g. when generating keys for basis
# functions), or requested explicitly as follows:
gmsh.model.mesh.createEdges()

# Edge and face tags can then be retrieved by providing their nodes:
edgeTags, edgeOrientations = gmsh.model.mesh.getEdges(NodeTags)
print("TAGs das arestas do elemento (edgeTags):", edgeTags)
print("Orientações das arestas do elemento (edgeOrientations):", edgeOrientations)

# Since element edge and face nodes are returned in the same order as the
# elements, one can easily keep track of which element(s) each edge or face is
# connected to:
elementTags, elementNodeTags = gmsh.model.mesh.getElementsByType(elementType)
print("TAGs dos elementos (elementTags):", elementTags)
print("Nós dos elementos (elementNodeTags):", elementNodeTags)

# # Inicializa o dicionário de mapeamento de arestas
# # edges2Elements = {}

# # Verifica se o número total de edges é múltiplo de 3
# # if len(edgeTags) % 3 != 0:
# #     print("Erro: O número total de arestas não é múltiplo de 3. Verifique a malha gerada.")
# # else:
# #     Percorre edgeTags em blocos de três
# #     for i in range(0, len(edgeTags), 3):
# #         Cria uma entrada no dicionário para o triângulo
# #         edges2Elements[i // 3 + 1] = edgeTags[i : i + 3].tolist()

# # print("Arestas conectadas aos elementos (edges2Elements):", edges2Elements)

# # If all you need is the list of all edges or faces in terms of their nodes, you
# # can also directly call:
# # All_edgeTags, All_edgeNodes = gmsh.model.mesh.getAllEdges()
# # print("TAGs das arestas (AlledgeTags):", All_edgeTags)
# # print("Nós das arestas (AlledgeNodes):", All_edgeNodes)

# # Create connection between edges and elements
# # edge_mapping = {}

# # Percorre os nós em pares e associa aos AlledgeTags
# # for i, tag in enumerate(All_edgeTags):
# #     Adiciona ao mapeamento usando o TAG da aresta como chave
# #     edge_mapping[tag] = sorted([All_edgeNodes[2 * i], All_edgeNodes[2 * i + 1]])

# # Ordena o dicionário edge_mapping com base nas chaves
# # sorted_edge_mapping = {key: edge_mapping[key] for key in sorted(edge_mapping.keys())}

# # Exibe o mapeamento de arestas
# # print("Mapeamento de arestas (edge_mapping):", edge_mapping)
# # print("Mapeamento de arestas ordenado (sorted_edge_mapping):", sorted_edge_mapping)

print("#--------------------------------------------------#")
# Visualizar a malha no ambiente Gmsh (opcional)
# gmsh.fltk.run()

# Finalizar o Gmsh
gmsh.finalize()