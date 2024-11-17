import csv
import requests
import re
from bs4 import BeautifulSoup

base_url = "https://www.ncbi.nlm.nih.gov"

genes_file = "genes.csv"

with open(genes_file) as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        gene_name = row['GENE']
        
        try:
            response = requests.get(f"{base_url}/clinvar/?term={gene_name}")
            response.raise_for_status()

            soup = BeautifulSoup(response.text, 'html.parser')

            transcrito_seletor = soup.select_one('.ui-button-text.wrap_balance')

            transcrito_canonico = None

            for transcrito in transcrito_seletor:
                transcrito_text = transcrito_seletor.get_text(separator="")

                match = re.search(r'NM_\d+\.\d+', transcrito_text)

                if match:
                    transcrito_canonico = match.group(0)
                    print(f"Gene: {gene_name} - Transcrito canônico: {transcrito_canonico}")
                    break

            
            if not transcrito_canonico:
                print(f"Gene: {gene_name} - Código NM_ não encontrado nos transcritos.")
        
        except requests.exceptions.HTTPError as http_err:
            print(f"Erro HTTP para o gene {gene_name}: {http_err}")
        except Exception as err:
            print(f"Erro ao processar o gene {gene_name}: {err}")

