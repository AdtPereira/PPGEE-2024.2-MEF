import os
import nbformat
from nbconvert import HTMLExporter
import shutil

# Diretório atual onde o código está sendo executado
current_dir = os.getcwd()

# Diretório final para os arquivos HTML
final_dir = os.path.join(current_dir, 'html')
os.makedirs(final_dir, exist_ok=True)  # Certifica-se de que a pasta 'html' existe

def convert_notebooks_to_html(root_directory):
    # Percorre todos os arquivos e subpastas do diretório raiz
    for root, _, files in os.walk(root_directory):
        for file in files:
            if file.endswith('.ipynb') and not file.startswith('convert_to_html'):
                notebook_path = os.path.join(root, file)
                print(f'Convertendo {notebook_path} para HTML...')
                
                # Configurando o exportador para HTML com imagens incorporadas
                html_exporter = HTMLExporter()
                html_exporter.exclude_input = False  # Inclui as células de entrada
                html_exporter.embed_images = True  # Incorpora as imagens no HTML como base64
                
                # Lendo e convertendo o notebook usando nbformat
                with open(notebook_path, 'r', encoding='utf-8') as nb_file:
                    notebook_content = nbformat.read(nb_file, as_version=4)  # Carrega o notebook como um NotebookNode
                    body, _ = html_exporter.from_notebook_node(notebook_content)
                    
                    # Salvando o arquivo HTML no diretório temporário de saída
                    html_filename = file.replace('.ipynb', '.html')
                    temp_output_path = os.path.join(root, html_filename)
                    with open(temp_output_path, 'w', encoding='utf-8') as html_file:
                        html_file.write(body)
                    print(f'{html_filename} salvo temporariamente em {root}.')

                    # Movendo o arquivo HTML gerado para a pasta "html"
                    final_output_path = os.path.join(final_dir, html_filename)
                    shutil.move(temp_output_path, final_output_path)
                    print(f'{html_filename} movido para a pasta {final_dir}.')

# Executa a conversão para cada notebook na pasta raiz e suas subpastas
convert_notebooks_to_html(current_dir)
