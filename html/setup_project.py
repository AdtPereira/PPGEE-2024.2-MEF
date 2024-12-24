import sys
import numpy as np
import import_ipynb
from scipy.sparse.linalg import spsolve

# Adicionar caminho ao diretório raiz do projeto
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Importação dos módulos do projeto
try:
    from pre_processing import domain, read_mesh
    from fem_processing import matrices_assembly
    from fem_processing import boundary_conditions
    from fem_processing import sources
    from pos_processing import graph_results
    print("Modules imports were successful!")
except ModuleNotFoundError as e:
    print(f"Module not found: {e}")
except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
