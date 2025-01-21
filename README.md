# Clinvar Exporter

O **Clinvar Exporter** é um software de código aberto projetado para buscar a classificação de variantes genéticas obtidas através de dados de Sequenciamento de Nova Geração (NGS). Seu principal objetivo é fornecer uma ferramenta gratuita e eficiente para auxiliar na análise de variantes genéticas, integrando-se a bancos de dados renomados, como o ClinVar.

## Índice

- [Sobre o Projeto](#sobre-o-projeto)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Como Executar o Projeto](#como-executar-o-projeto)
- [Como Contribuir](#como-contribuir)
- [Licença](#licença)
- [Contato](#contato)

## Sobre o Projeto

Variantes genéticas são alterações na sequência do DNA que podem afetar a funcionalidade das proteínas codificadas pelos genes. Essas alterações podem resultar em proteínas não funcionais, reduzir sua atividade ou, em alguns casos, não causar impactos aparentes.

A classificação dessas variantes, baseada em sua patogenicidade, é fundamental para compreender sua relevância clínica. Ferramentas como o ClinVar são cruciais nesse processo, fornecendo uma base de dados consolidada para apoiar análises e decisões clínicas.

## Como Executar o Projeto

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/KassyaneFurtado/clinvar_exporter.git

2. **Crie um ambiente virtual e ative-o:**


    ```bash
   python3 -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate

3. **Instale as dependências:**

    ```bash
    pip install -r requirements.txt

4. **Execute o script principal:**

    ```bash
    python main.py