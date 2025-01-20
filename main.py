from duplicated import duplicate
from transcript import SearchTranscript
from sqlite import dataBase
from separate_transcribed import buscar_variantes
from classificacao import processar_variantes
from load_data import loadSequenciamento
from load_data import loadGenes

sequenciamento = loadGenes
genes = loadSequenciamento


#Retirar as duplicatas da coluna de genes do arquivo oriundo do sequenciamento
duplicate()

#Buscar transcritos canônicos
SearchTranscript()

#Criar banco de dados SQLite e importar a planilha
dataBase (sequenciamento, 'banco_de_dados.db')

#Filtrar a planilha pelos transcritos canônicos

buscar_variantes('banco_de_dados.db', 'genes.csv', 'variantes.csv')

# Classificar as variantes
processar_variantes('variantes.csv', coluna_variantes='Coding region change')


