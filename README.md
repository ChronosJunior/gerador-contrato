# gerador-contrato

## 1. Siga o passo a passo do tutorial [Desenvolver no Google Workspace](https://developers.google.com/workspace/guides/get-started?hl=pt-br) para criar autenticação OAuth e baixar o arquivo `credentials.json`

## 2. Baixe o repositório para sua máquina:

    git clone https://github.com/ChronosJunior/gerador-contrato.git
    cd gerador-contrato

## 3. Crie um arquivo '.env' e configure as variáveis FILE_NAME e DIR_NAME seguindo o exemplo (substitua os valores com <> pelos valores reais. Exemplo: <nome_pasta> -> pasta_x):

    FILE_NAME=<nome_arquivo>
    DIR_NAME=<nome_pasta>

## 4. Instale os pré-requisito:

    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## 5. Execute

    python3 main.py