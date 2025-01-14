import csv
import requests
import re
from bs4 import BeautifulSoup

base_url = "https://www.ncbi.nlm.nih.gov"
genes_file = "genes.csv"
output_file = "transcritos.csv"


with open(genes_file) as file:
    reader = csv.DictReader(file)
    
    with open(output_file, mode="a", newline="") as out_file:
        writer = csv.writer(out_file)

        for row in reader:
            gene_name = row['GENE']
            transcrito_canonico = None

            try:
                response = requests.get(f"{base_url}/clinvar/?term={gene_name}")
                response.raise_for_status()  

                soup = BeautifulSoup(response.text, 'html.parser')

                # Encontrando os transcritos canonicos na página
                transcrito_seletor = soup.find_all('span', class_='ui-button-text wrap_balance')

                for span in transcrito_seletor:
                    if span:
                        transcrito_text = span.get_text(separator="")
                        match = re.search(r'NM_\d+\.\d+', transcrito_text)
                        if match:
                            transcrito_canonico = match.group(0)
                            break

            except Exception as err:
                print(f"Erro ao processar o gene {gene_name}: {err}")

            
            if transcrito_canonico:
                writer.writerow([gene_name, transcrito_canonico])
            else:
                writer.writerow([gene_name, "NM_ não encontrado"])

print("Processamento concluído.")
