import numpy as np
import gmsh 

FINITE_ELEMENT = ("Triangle", 1)
BOUNDARY = [{'tag': 101, 'type': 'Dirichlet', 'value': 0.0, 'name': 'omega'}]
MATERIAL = [{'tag': 201, 'name': 'free_space', 'a_constant': 1}]

mesh_data = {}
type, order = FINITE_ELEMENT
vertices = [(0, 0, 0), (0, -1, 0), (1, -1, 0), (1, 1, 0), (-1, 1, 0), (-1, 0, 0)]
h = 1

# Inicializar o Gmsh
gmsh.initialize()
gmsh.model.add("L_domain")

# Adicionar pontos ao modelo
point_tags = []
for vertex in vertices:
    # Refinar no ponto (0, 0)
    local_lc = h * 0.2 if vertex == (0, 0, 0) else h  
    tag = gmsh.model.geo.addPoint(*vertex, local_lc)
    point_tags.append(tag)

# Criar as linhas conectando os pontos
line_tags = [gmsh.model.geo.addLine(point_tags[i], point_tags[(i + 1) % len(point_tags)])
    for i in range(len(point_tags))]
print(line_tags)

# Criar os loops e as superfícies
contour = gmsh.model.geo.addCurveLoop(line_tags, 1)
free_space = gmsh.model.geo.addPlaneSurface([contour])

# Adicionar grupos físicos para Dim=1
for i, tag in enumerate([line_tags]):
        gmsh.model.addPhysicalGroup(dim=1, tags=tag, tag=BOUNDARY[i]['tag'], name=BOUNDARY[i]['name'])

# Adicionar grupos físicos para Dim=2
gmsh.model.addPhysicalGroup(dim=2, tags=[free_space], tag=MATERIAL[0]['tag'], name=MATERIAL[0]['name']) 

# Gerar a malha 2D
gmsh.model.geo.synchronize()
gmsh.option.setNumber("Mesh.SaveAll", 1)
gmsh.model.mesh.generate(2)
gmsh.model.mesh.setOrder(order)

gmsh.fltk.run()

# if auto_save:
#     os.makedirs("pre_processing/mesh", exist_ok=True)
#     gmsh.write(f"pre_processing/mesh/L_domain_{type}{order}.msh")
#     read_mesh.basic_info()

# Create mesh Structure Data from gmsh
# mesh_data['cell'] = read_mesh.get_cell_data(MATERIAL)
# mesh_data['nodes'] = read_mesh.get_nodes_data(BOUNDARY)
# mesh_data['edges'] = read_mesh.get_edge_data()

# Apply physics to the problem
# mesh_data = apply_physics(FINITE_ELEMENT, mesh_data)

gmsh.finalize()
