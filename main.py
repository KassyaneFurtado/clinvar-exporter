import csv
import requests
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

base_url = "https://www.ncbi.nlm.nih.gov"

def fetch_and_parse(variante):
    variante_name = variante["variante"]
    try:
        response = requests.get(f"{base_url}/clinvar/?term={variante_name}")
        response.raise_for_status()

        soup = BeautifulSoup(response.text, features="html.parser")

        classificacao = "-"
        rs = "-"
        tipo = "-"
        consequencia = "-"

        # Verifica se a variante tem o rs
        if response.history:
            rs_element = soup.select_one('.litvar')
            if rs_element:
                rs_text = rs_element.get('id')
                match = re.search(r'litvar_(\d+)', rs_text)
                if match:
                    rs = f"rs_{match.group(1)}"
        else:
            rs_element = soup.select_one("#feat_variation_title")
            if rs_element:
                rs = rs_element.text.strip()

        # Verifica a classificação da variante
        classificacao_element = soup.select_one(
            '#germline-somatic-info > div.germline-info > div.germline-section > div:nth-child(2) > div.single-item-value'
        )
        if classificacao_element:
            classificacao = classificacao_element.text.replace("\n", " ").strip()

        # Procura pelo tipo da variante
        type_element = soup.select_one('#id_first > div > dl > dd:nth-child(4) > p > span:nth-child(1)')
        if type_element:
            tipo = type_element.text.strip()

        # Verifica a consequência Molecular
        consequence_element = soup.select_one('#id_first > div > dl > dd.margin-top > table > tbody > tr:nth-child(1) > td:nth-child(3)')
        if consequence_element:
            consequencia = consequence_element.text.strip()

        return {
            "variante": variante_name,
            "rs": rs,
            "classificacao": classificacao,
            "tipo": tipo,
            "consequencia": consequencia
        }
    except Exception as e:
        return {
            "variante": variante_name,
            "erro": str(e)
        }

with open("variantes.csv", "r") as f:
    reader = csv.DictReader(f)
    variantes = [{"variante": row["variante"]} for row in reader]

with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_and_parse, variantes))

output_fields = ["variante", "rs", "classificacao", "tipo", "consequencia", "erro"]
with open("saida.csv", "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=output_fields)
    writer.writeheader()
    writer.writerows(results)

print("Processing complete. Results saved to saida.csv")