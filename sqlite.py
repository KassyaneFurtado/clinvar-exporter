import sqlite3
import pandas as pd
from load_data import loadSequenciamento

def dataBase(planilha, banco_dados):
    """
    Função para criar um banco de dados SQLite a partir de uma planilha.
    
    Args:
        planilha (str): Caminho para a planilha CSV.
        banco_dados (str): Nome do arquivo do banco de dados SQLite.
    """
    # Conectar ao banco de dados SQLite (será criado se não existir)
    conn = sqlite3.connect(banco_dados)
    cursor = conn.cursor()

    # Criar ou substituir a tabela sequenciamento
    cursor.execute("DROP TABLE IF EXISTS sequenciamento")

    # Importar o arquivo CSV usando pandas
    try:
        planilha = loadSequenciamento()
        planilha.to_sql('sequenciamento', conn, if_exists='replace', index=False)
    except Exception as e:
        print(f"Erro ao carregar a planilha: {e}")
        conn.close()
        return

    # Exibir as tabelas disponíveis no banco de dados
    try:
        resultado = pd.read_sql("SELECT name FROM sqlite_master WHERE type='table';", conn)
        print("Tabelas no banco de dados:")
        print(resultado)
    except Exception as e:
        print(f"Erro ao consultar tabelas no banco de dados: {e}")
    finally:
        # Fechar a conexão com o banco de dados
        conn.close()

