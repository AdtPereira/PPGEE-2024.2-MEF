import gmsh

gmsh.initialize()

# Nome do modelo
gmsh.model.add("Malha Triangular Refinada Localmente")

# Dimensões do retângulo
width = 0.5
height = 0.5
ra = 0.1
rb = ra + 0.02205

# Tamanhos de malha
min_size = 0.01  # Tamanho mínimo perto das bordas verticais
max_size = 0.1   # Tamanho no restante do domínio

# Criação dos pontos
p1 = gmsh.model.geo.addPoint(0, 0, 0)  # Inferior esquerdo
p2 = gmsh.model.geo.addPoint(width, 0, 0)  # Inferior direito
p3 = gmsh.model.geo.addPoint(width, height, 0)  # Superior direito
p4 = gmsh.model.geo.addPoint(0, height, 0)  # Superior esquerdo

# Pontos da casca esférica
p11 = gmsh.model.geo.addPoint(ra, 0, 0)  
p12 = gmsh.model.geo.addPoint(rb, 0, 0)  
p41 = gmsh.model.geo.addPoint(0, rb, 0)  
p42 = gmsh.model.geo.addPoint(0, ra, 0)  

# Criação dos domínios Neumann Homogêneo Inferior
l11 = gmsh.model.geo.addLine(p1, p11)
l12 = gmsh.model.geo.addLine(p11, p12)
l13 = gmsh.model.geo.addLine(p12, p2)

# Criação do domínio Dirichlet não-homogêneo
l2 = gmsh.model.geo.addLine(p2, p3)  

# Superior
l3 = gmsh.model.geo.addLine(p3, p4)

# Criação do domínio Dirichlet homogêneo
l41 = gmsh.model.geo.addLine(p4, p41)
l42 = gmsh.model.geo.addLine(p41, p42)
l43 = gmsh.model.geo.addLine(p42, p1)

# Linhas da casca esférica
inner_shell = gmsh.model.geo.addCircleArc(p11, p1, p42)
outer_shell = gmsh.model.geo.addCircleArc(p12, p1, p41)

# Criar o contorno da superfície
air_loop = gmsh.model.geo.addCurveLoop([l11, inner_shell, l43])
magnetic_loop = gmsh.model.geo.addCurveLoop([l12, outer_shell, l42, -inner_shell])
free_loop = gmsh.model.geo.addCurveLoop([l13, l2, l3, l41, -outer_shell])

air_cavity = gmsh.model.geo.addPlaneSurface([air_loop])
magnetic_shell = gmsh.model.geo.addPlaneSurface([magnetic_loop])
free_space = gmsh.model.geo.addPlaneSurface([free_loop])

# Refinamento: aplicar campos de distância para as bordas verticais
gmsh.model.mesh.field.add("Distance", 1)
gmsh.model.mesh.field.setNumbers(1, "EdgesList", [l41])  # Refinamento para a lateral esquerda

gmsh.model.mesh.field.add("Distance", 2)
gmsh.model.mesh.field.setNumbers(2, "EdgesList", [l2])  # Refinamento para a lateral direita

# Combinação dos campos de distância
gmsh.model.mesh.field.add("Min", 3)
gmsh.model.mesh.field.setNumbers(3, "FieldsList", [1, 2])

# Refinamento baseado no campo combinado
gmsh.model.mesh.field.add("Threshold", 4)
gmsh.model.mesh.field.setNumber(4, "InField", 3)
gmsh.model.mesh.field.setNumber(4, "SizeMin", min_size)
gmsh.model.mesh.field.setNumber(4, "SizeMax", max_size)
gmsh.model.mesh.field.setNumber(4, "DistMin", 0.05)  # Refinamento próximo às bordas
gmsh.model.mesh.field.setNumber(4, "DistMax", 0.3)   # Transição para tamanho maior

# Aplicar o campo de malha
gmsh.model.mesh.field.setAsBackgroundMesh(4)

# Sincronizar e gerar malha
gmsh.model.geo.synchronize()
gmsh.model.mesh.generate(2)

# Exportar o arquivo
gmsh.write("malha_refinada_localmente.msh")

# Opcional: visualizar na interface gráfica
gmsh.fltk.run()

# Finalizar
gmsh.finalize()