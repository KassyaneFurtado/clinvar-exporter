import pandas as pd
from load_data import loadSequenciamento

def duplicate():
    # Carregar o arquivo usando a função loadSequenciamento
    df = loadSequenciamento()

    # Solicitar ao usuário o nome da coluna para remoção de duplicatas
    coluna = input("Digite o nome da coluna para remover duplicatas: ")

    # Verificar se a coluna existe no DataFrame
    if coluna not in df.columns:
        print(f"A coluna '{coluna}' não foi encontrada.")
        return

    # Remover duplicatas e manter apenas a coluna especificada
    df_sem_duplicatas = df[[coluna]].drop_duplicates()

    # Garantir que há dados antes de salvar
    if df_sem_duplicatas.empty:
        print("Nenhum dado encontrado após a remoção de duplicatas.")
    else:
        # Salvar o arquivo somente se houver dados
        df_sem_duplicatas.to_csv("genes.csv", index=False)
        print(f"A planilha 'genes.csv' foi criada com os valores únicos da coluna '{coluna}'.")
