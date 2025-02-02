import gmsh
import os

# Limpar o terminal
os.system('cls' if os.name == 'nt' else 'clear')

# Define os parâmetros de entrada
FINITE_ELEMENT = ("Tetrahedron", 1)
BOUNDARY = [{'tag': 201, 'type': 'Dirichlet', 'value': 0.0, 'name': 'nxE=0'}]
MATERIAL = [{'tag': 301, 'name': 'free_space', 'ur': 1, 'er': 1}]

element, order = FINITE_ELEMENT
h = 1  # Tamanho do elemento da malha

# Dimensões da cavidade retangular, metros
# a, b, c = 1.0, 0.6, 0.4
a, b, c = 1.0, 1.0, 1.0

# Inicializar o Gmsh
gmsh.initialize()
gmsh.model.add("rectangular_cavity")

# Criar volume retangular (caixa)
TagVolume = gmsh.model.occ.addBox(0, 0, 0, a, b, c)
print(f"\nTagVolume: {TagVolume}")
gmsh.model.occ.synchronize()

# gmsh.option.setNumber("Mesh.MeshSizeMax", h)
gmsh.option.setNumber("Mesh.MeshSizeMin", h)
gmsh.model.mesh.generate(dim=3)
gmsh.model.mesh.setOrder(order)

print("\n----------- Beginning of edge mapping --------------------")
# If all you need is the list of all edges or faces in terms of their nodes:
# gmsh.model.mesh.createEdges([(3, 1)])
gmsh.model.mesh.createEdges()
edgeTags, edgeNodes = gmsh.model.mesh.getAllEdges()
print(f"Total number of edges: {len(edgeTags)}")

# Criar edge_key_map diretamente sem edge_mapping
edge_key_map = {tuple(sorted([edgeNodes[2*i], edgeNodes[2*i+1]])): tag
                 for i, tag in enumerate(sorted(edgeTags))}
print(f"edge_key_map:\n {edge_key_map}")
print("----------- Ending of edge mapping --------------------")

print("\n----------- Beginning of Boundary DimTags --------------------")
# Obter os contornos (superfícies, dim=2) do volume
BoundaryDimTags = gmsh.model.getBoundary([(3, TagVolume)], oriented=True, recursive=False)
print(f"BoundaryDimTags: {BoundaryDimTags}")

# Exibir os TAGs das superfícies associadas a cada contorno
BoundaryTags = [Dimtags[1] for Dimtags in BoundaryDimTags]

# Definindo as superfícies de contorno de Dirichlet (dim=2)
gmsh.model.addPhysicalGroup(dim=2, tags=BoundaryTags, tag=BOUNDARY[0]['tag'], name=BOUNDARY[0]['name'])

# Adicionar grupos físicos para Dim=3 (volume)
gmsh.model.addPhysicalGroup(dim=3, tags=[TagVolume], tag=MATERIAL[0]['tag'], name=MATERIAL[0]['name'])
print("----------- Ending of Boundary DimTags --------------------")

## ------------------##
## `get_cell_data()` ##
## ------------------##

# 1. Obter os elementos da malha
elemTypes, elemTags, nodeTags = gmsh.model.mesh.getElements(dim=3)
print(f"elemTypes with dim 3: {elemTypes}")
print(f"elemTags with dim 3: {elemTags}")
print(f"len(elemTags[0]): {len(elemTags[0])}")
print(f"elemNodeTags: {nodeTags}")
print(f"len(nodeTags[0]): {len(nodeTags[0])}")
conn_dict = {}

# 2. Obter as entidades geometricas do modelo
print(f"Entities with dim 0 (Points): {gmsh.model.getEntities(dim=0)}")
print(f"Entities with dim 1 (Edges): {gmsh.model.getEntities(dim=1)}")
print(f"Entities with dim 2 (Faces): {gmsh.model.getEntities(dim=2)}")
print(f"Entities with dim 3 (Regions): {gmsh.model.getEntities(dim=3)}")

# 3. Criar um mapa entre cada entidade física (grupo físico) e os elementos correspondentes
print("\nMaterial Physical groups with dim=3:")
material_dim3 = {}

for mat in MATERIAL:
    MaterialEntitiesTags = gmsh.model.getEntitiesForPhysicalGroup(dim=3, tag=mat['tag'])
    print(f"Entities of {mat['name']} with dim3: {MaterialEntitiesTags}")
    
    for EntityTag in MaterialEntitiesTags:
        elemTypes, elemTags, nodeTags = gmsh.model.mesh.getElements(dim=3, tag=EntityTag)
        print(f"mesh_elements of entity (dim, tag) = (3, {EntityTag}): elemTags = {elemTags[0]}")
        print(f"mesh_elements of entity (dim, tag) = (3, {EntityTag}): nodeTags = {nodeTags[0]}")
        
        # Criar dicionário associando cada elemento à sua conectividade de nós
        for i, elemTag in enumerate(elemTags[0]):
            node_conn = list(sorted(nodeTags[0][4 * i : 4 * (i + 1)])) # Tetrahedron element
            edge_conn = [
                edge_key_map[(node_conn[0], node_conn[1])],  # e1: 1 -> 2
                edge_key_map[(node_conn[0], node_conn[2])],  # e2: 1 -> 3
                edge_key_map[(node_conn[0], node_conn[3])],  # e3: 1 -> 4
                edge_key_map[(node_conn[1], node_conn[2])],  # e4: 2 -> 3
                edge_key_map[(node_conn[1], node_conn[3])],  # e5: 2 -> 4
                edge_key_map[(node_conn[2], node_conn[3])]   # e6: 3 -> 4
            ]
            material_dim3[elemTag] = {
                'node_conn': node_conn,
                'edge_conn': edge_conn,
                'bc_tag': mat['tag']}
print(f"material_dim3: {material_dim3}")
            
# 4. Criar um mapa entre cada entidade física (grupo físico) e os elementos correspondentes
print("\nBoundary Physical groups with dim2:")
boundary_dim2 = {}

for bc in BOUNDARY:
    BoundaryEntitiesTags = gmsh.model.getEntitiesForPhysicalGroup(dim=2, tag=bc['tag'])
    print(f"Entities of {bc['name']} with dim2: {BoundaryEntitiesTags}")
    
    for EntityTag in BoundaryEntitiesTags:
        elemTypes, elemTags, nodeTags = gmsh.model.mesh.getElements(dim=2, tag=EntityTag)
        print(f"mesh_elements of entity (dim, tag) = (2, {EntityTag}): elemTags = {elemTags[0]} | nodeTags = {nodeTags[0]}")

        # Criar dicionário associando cada elemento à sua conectividade de nós
        for i, elemTag in enumerate(elemTags[0]):
            node_conn = list(sorted(nodeTags[0][3 * i : 3 * (i + 1)]))
            edge_conn = [
                edge_key_map[(node_conn[0], node_conn[1])],  # e1: 1 -> 2
                edge_key_map[(node_conn[0], node_conn[2])],  # e2: 1 -> 3
                edge_key_map[(node_conn[1], node_conn[2])],  # e3: 2 -> 3
            ]
            boundary_dim2[elemTag] = {
                'node_conn': node_conn,
                'edge_conn': edge_conn,
                'bc_tag': bc['tag']}

print(f"boundary_dim2: {boundary_dim2}")

# Visualizar a malha no ambiente Gmsh (opcional)
# gmsh.fltk.run()

# Finalizar o Gmsh
gmsh.finalize()
