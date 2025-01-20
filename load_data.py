from pandas import read_excel
from pandas import read_csv

def loadSequenciamento():
    return read_excel("sequenciamento.xlsx")

def loadGenes():
    return read_csv("genes.csv")

def loadVariants():
    return read_csv('variantes.csv')

