from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

def convert_html_to_pdf_with_chrome():
    # Diretório para os arquivos HTML e PDF
    base_dir = os.getcwd()
    html_dir = os.path.join(base_dir, "html")
    output_dir = os.path.join(base_dir, "pdfs")
    
    # Verifica e cria a pasta 'pdfs' se ela não existir
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Pasta 'pdfs' criada em: {output_dir}")
    else:
        print(f"Pasta de saída: {output_dir}")
    
    # Configuração do Chrome para salvar como PDF
    chrome_options = Options()
    chrome_options.add_argument('--kiosk-printing')
    
    # Configurações de preferências para salvar o PDF na pasta correta
    prefs = {
        "savefile.default_directory": output_dir,
        "printing.print_preview_sticky_settings.appState": '{"recentDestinations":[{"id":"Save as PDF","origin":"local"}],"selectedDestinationId":"Save as PDF","version":2}',
        "download.default_directory": output_dir,
        "download.prompt_for_download": False
    }
    chrome_options.add_experimental_option("prefs", prefs)
    
    # Inicializa o driver do Chrome sem modo headless
    driver = webdriver.Chrome(options=chrome_options)
    
    # Lista todos os arquivos HTML na pasta 'html'
    html_files = [os.path.join(html_dir, file) for file in os.listdir(html_dir) if file.endswith('.html')]
    
    if not html_files:
        print("Nenhum arquivo HTML encontrado no diretório.")
        driver.quit()
        return
    
    # Abre e imprime cada arquivo HTML como PDF com o nome correspondente
    for html_file in html_files:
        driver.get("file:///" + html_file)
        time.sleep(2)  # Aguarda o carregamento completo
        
        # Define o nome do arquivo PDF baseado no nome do HTML original
        pdf_file_name = os.path.basename(html_file).replace('.html', '.pdf')
        pdf_file_path = os.path.join(output_dir, pdf_file_name)
        
        # Executa o comando de impressão
        driver.execute_script('window.print();')
        print(f"Solicitação para salvar '{pdf_file_path}' como PDF enviada.")
        time.sleep(1)  # Aumenta o tempo de espera para garantir a geração do PDF
    
    # Fecha o navegador
    driver.quit()

# Exemplo de uso
convert_html_to_pdf_with_chrome()
