import csv
import requests
import re
from bs4 import BeautifulSoup
from load_data import loadGenes

base_url = "https://www.ncbi.nlm.nih.gov"

def SearchTranscript():
    # Carregar os genes e solicitar o nome da coluna para busca
    genes = loadGenes()
    coluna = input("Digite o nome da coluna que contém os genes: ")

    # Verificar se a coluna existe
    if coluna not in genes.columns:
        print(f"A coluna '{coluna}' não foi encontrada no arquivo.")
        return

    # Iterar sobre os genes e buscar os transcritos canônicos
    for index, row in genes.iterrows():
        gene_name = row[coluna]
        TRANSCRITO = None

        try:
            response = requests.get(f"{base_url}/clinvar/?term={gene_name}")
            response.raise_for_status()  

            soup = BeautifulSoup(response.text, 'html.parser')

            # Encontrando os transcritos canônicos na página
            transcript_seletor = soup.find_all('span', class_='ui-button-text wrap_balance')

            for span in transcript_seletor:
                transcript_text = span.get_text(separator="")
                match = re.search(r'NM_\d+\.\d+', transcript_text)
                if match:
                    TRANSCRITO = match.group(0)
                    break

        except Exception as err:
            print(f"Erro ao processar o gene {gene_name}: {err}")

        # Atualizar a coluna com o transcrito canônico encontrado
        genes.at[index, 'TRANSCRITO_CANONICO'] = TRANSCRITO if TRANSCRITO else "NM_ não encontrado"

    # Salvar o arquivo atualizado
    genes.to_csv("genes.csv", index=False)
    print("O processamento dos genes foi concluído e salvo no arquivo genes.csv.")
