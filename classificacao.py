import csv
import requests
import re
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor

base_url = "https://www.ncbi.nlm.nih.gov"

def processar_variantes(arquivo_csv, coluna_variantes):
    if coluna_variantes is None:
        raise ValueError("O nome da coluna contendo as variantes deve ser fornecido.")

    def classificacaoVariantes(variante):
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
            type_element = soup.select_one('#id_first > div > dl > dd:nth-child(4) > p > font > span:nth-child(1)')
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

    # Abrir o arquivo original e carregar as variantes
    with open(arquivo_csv, "r", encoding="utf-8", errors="replace") as f:
        reader = csv.DictReader(f)
        if coluna_variantes not in reader.fieldnames:
            raise ValueError(f"A coluna '{coluna_variantes}' não foi encontrada no arquivo.")
        variantes = [{"variante": row[coluna_variantes]} for row in reader]
        campo_extra = reader.fieldnames + ["rs", "classificacao", "tipo", "consequencia", "erro"]  # Novos campos a serem adicionados

    # Processar as variantes com ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=10) as executor:
        results = list(executor.map(classificacaoVariantes, variantes))

    # Abrir o arquivo original para atualizar as colunas com os novos dados
    with open(arquivo_csv, "r+", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

        # Atualizar os nomes dos campos para incluir os novos campos
        campo_extra = reader.fieldnames + ["variante", "rs", "classificacao", "tipo", "consequencia", "erro"]

        # Adicionar os resultados ao arquivo original
        for i, row in enumerate(rows):
            result = results[i]
            row.update(result)  # Atualizar a linha com os dados da classificação

        # Reposicionar o cursor no início do arquivo e escrever as linhas com as novas colunas
        f.seek(0)
        writer = csv.DictWriter(f, fieldnames=campo_extra)
        writer.writeheader()  # Escrever o cabeçalho
        writer.writerows(rows)  # Escrever as linhas com os novos dados
        f.truncate()  # Garantir que o arquivo seja truncado no novo tamanho

    print("Processamento concluído. Resultados salvos no arquivo original.")
