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


        classificacao = "Não tem classificação"
        rs = "Não tem rs"


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

        
        classificacao_element = soup.select_one(
            "#germline-somatic-info > div.germline-info > div.germline-section > div:nth-child(2) > div.single-item-value"
        )
        if classificacao_element:
            classificacao = classificacao_element.text.replace("\n", " ").strip()

        return {
            "variante": variante_name,
            "rs": rs,
            "classificacao": classificacao
        }
    except Exception as e:
        return {
            "variante": variante_name,
            "err": str(e)
        }


with open("variantesD.csv", "r") as f:
    reader = csv.DictReader(f)
    variantes = [{"variante": row["variante"]} for row in reader]


with ThreadPoolExecutor(max_workers=5) as executor:
    results = list(executor.map(fetch_and_parse, variantes))


output_fields = ["variante", "rs", "classificacao", "err"]
with open("saida.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=output_fields)
    writer.writeheader()
    writer.writerows(results)

print("Processing complete. Results saved to saida.csv")
