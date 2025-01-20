import sqlite3
import pandas as pd

def buscar_variantes(banco_dados, arquivo_genes, output_file):
    """
    Busca variantes em um banco de dados com base nos genes fornecidos.

    Args:
        banco_dados (str): Caminho para o banco de dados SQLite.
        arquivo_genes (str): Caminho para o arquivo CSV contendo os genes.
        output_file (str): Caminho para o arquivo de saída com os resultados.
    """
    # Verificar se o arquivo_genes é válido
    if not isinstance(arquivo_genes, str):
        raise ValueError(f"O arquivo_genes deve ser um caminho de arquivo válido. Recebido: {type(arquivo_genes)}")

    # Ler os genes da coluna 'TRANSCRITO_CANONICO'
    try:
        variantes_procuradas = pd.read_csv(arquivo_genes)['TRANSCRITO_CANONICO'].dropna().tolist()
    except Exception as e:
        raise ValueError(f"Erro ao ler o arquivo CSV {arquivo_genes}: {e}")

    # Conectar ao banco de dados
    conn = sqlite3.connect(banco_dados)
    cur = conn.cursor()

    resultados = []
    for variante in variantes_procuradas:
        cur.execute('''
            SELECT * 
            FROM sequenciamento 
            WHERE `Coding region change` LIKE ?;
        ''', (f'%{variante}%',))
        resultados.extend(cur.fetchall())

    # Salvar os resultados em um arquivo CSV
    colunas = [desc[0] for desc in cur.description]
    pd.DataFrame(resultados, columns=colunas).to_csv(output_file, index=False)
    conn.close()

    print(f"Processamento concluído. Resultados salvos em: {output_file}")
