import gmsh

FINITE_ELEMENT = ("Triangle", 1)

BOUNDARY = [{'type': 'Dirichlet', 'tag': 101, 'value': 0.0, 'name': 'Az_0'}, 
            {'type': 'Dirichlet', 'tag': 102, 'value': 0.05, 'name': 'Az_0.05'}]

MATERIAL = [{'type': 'relative_magnetic_permeability', 'tag': 201, 'value': 1, 'name': 'cavity'},
            {'type': 'relative_magnetic_permeability', 'tag': 202, 'value': 1E4, 'name': 'magnetic_shell'},
            {'type': 'relative_magnetic_permeability', 'tag': 203, 'value': 1, 'name': 'free_space'}]

# Inicializar o Gmsh
gmsh.initialize()

# Nome do modelo
gmsh.model.add("Malha Triangular Refinada Localmente")
factory = gmsh.model.geo

# Dimensões do retângulo
width = 0.5
height = 0.5
ra = 0.1
rb = ra + 0.02205

# Tamanhos de malha
min_size = 0.005  # Tamanho mínimo nas linhas refinadas e na casca
max_size = 0.1    # Tamanho no restante do domínio

# Criação dos pontos
p1 = factory.addPoint(0, 0, 0)  # Inferior esquerdo
p2 = factory.addPoint(width, 0, 0)  # Inferior direito
p3 = factory.addPoint(width, height, 0)  # Superior direito
p4 = factory.addPoint(0, height, 0)  # Superior esquerdo

# Pontos da casca esférica
p11 = factory.addPoint(ra, 0, 0)  
p12 = factory.addPoint(rb, 0, 0)  
p41 = factory.addPoint(0, rb, 0)  
p42 = factory.addPoint(0, ra, 0)  

# Criação dos domínios Neumann Homogêneo Inferior
l11 = factory.addLine(p1, p11)
l12 = factory.addLine(p11, p12)
l13 = factory.addLine(p12, p2)

# Criação do domínio Dirichlet não-homogêneo
l2 = factory.addLine(p2, p3)  

# Superior
l3 = factory.addLine(p3, p4)

# Criação do domínio Dirichlet homogêneo
l41 = factory.addLine(p4, p41)
l42 = factory.addLine(p41, p42)          
l43 = factory.addLine(p42, p1)

# Linhas da casca esférica
inner_shell = factory.addCircleArc(p11, p1, p42)
outer_shell = factory.addCircleArc(p12, p1, p41)

# Criar o contorno da superfície
air_loop = factory.addCurveLoop([l11, inner_shell, l43])
magnetic_loop = factory.addCurveLoop([l12, outer_shell, l42, -inner_shell])
free_loop = factory.addCurveLoop([l13, l2, l3, l41, -outer_shell])

air_cavity = factory.addPlaneSurface([air_loop])
magnetic_shell = factory.addPlaneSurface([magnetic_loop])
free_space = factory.addPlaneSurface([free_loop])

# Refinamento: aplicar campos de distância para a casca esférica
gmsh.model.mesh.field.add("Distance", 1)
gmsh.model.mesh.field.setNumbers(1, "EdgesList", [inner_shell, outer_shell])  # Refinamento nos arcos da casca esférica

# Refinamento adicional para a linha l41
gmsh.model.mesh.field.add("Distance", 2)
gmsh.model.mesh.field.setNumbers(2, "EdgesList", [l41])

# Refinamento adicional para a linha l2
gmsh.model.mesh.field.add("Distance", 3)
gmsh.model.mesh.field.setNumbers(3, "EdgesList", [l2])

# Refinamento adicional para a linha l11
gmsh.model.mesh.field.add("Distance", 4)
gmsh.model.mesh.field.setNumbers(4, "EdgesList", [l11])

# Refinamento adicional para a linha l43
gmsh.model.mesh.field.add("Distance", 5)
gmsh.model.mesh.field.setNumbers(5, "EdgesList", [l43])

# Combinação de refinamentos
gmsh.model.mesh.field.add("Min", 6)
gmsh.model.mesh.field.setNumbers(6, "FieldsList", [1, 2, 3, 4, 5])

# Campo Threshold para controlar o refinamento
gmsh.model.mesh.field.add("Threshold", 7)
gmsh.model.mesh.field.setNumber(7, "InField", 6)
gmsh.model.mesh.field.setNumber(7, "SizeMin", min_size)  # Tamanho mínimo nas linhas e casca
gmsh.model.mesh.field.setNumber(7, "SizeMax", max_size)  # Tamanho máximo fora das regiões refinadas
gmsh.model.mesh.field.setNumber(7, "DistMin", 0.01)  # Distância mínima para aplicar o tamanho min_size
gmsh.model.mesh.field.setNumber(7, "DistMax", 0.05)  # Distância máxima para aplicar o tamanho max_size

# Aplicar o campo de malha combinado
gmsh.model.mesh.field.setAsBackgroundMesh(7)

# Definindo as curvas de contorno de Dirichlet (dim=1)
gmsh.model.addPhysicalGroup(dim=1, tags=[l41, l42, l43], tag=BOUNDARY[0]['tag'], name=BOUNDARY[0]['name'])
gmsh.model.addPhysicalGroup(dim=1, tags=[l2], tag=BOUNDARY[1]['tag'], name=BOUNDARY[1]['name'])

# Adicionar grupos físicos para Dim=2 (superfícies)
gmsh.model.addPhysicalGroup(dim=2, tags=[air_cavity], tag=MATERIAL[0]['tag'], name=MATERIAL[0]['name'])
gmsh.model.addPhysicalGroup(dim=2, tags=[magnetic_shell], tag=MATERIAL[1]['tag'], name=MATERIAL[1]['name'])
gmsh.model.addPhysicalGroup(dim=2, tags=[free_space], tag=MATERIAL[2]['tag'], name=MATERIAL[2]['name'])

# Sincronizar e gerar malha
factory.synchronize()
gmsh.model.mesh.generate(2)

# Opcional: visualizar na interface gráfica
gmsh.fltk.run()

# Finalizar
gmsh.finalize()