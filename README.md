# NewTimesheet
Script para receber os dados semanais do clockify e coloca-los em uma planilha excel.
O script faz a integração dos dados ja armazenados com os novos dados que são recebios a cada script. Desta forma, o arquivo excel se torna uma base de dados dos horarios trabalhados pelos membros do NEO.

O script faz as referências nescessárias e armazena os horários realizados da mesma atividade, colocando os dados em mesmas linhas mas em colunas diferentes.

Script realizado por LDB em 2019.2


## Como usar

Caso você já tenha o programa baixado e com as dependências instaladas pule para a seção [Rodando Script](#rodando-script). Caso contrario, siga os passos da seção [Instalando](#instalando).

### Instalando
Primeiro, baixar os arquivos desse repositório. Manualmente ou se tiver o gitlab configurado com:
```
git clone https://gitlab.com/NEOsons/timesheet-clockify.git 
```
Abrir um terminal na pasta do programa e instalar as dependências com:

```
pip install -r requirements.txt
```
Ou se tiver pipenv:
```
pipenv shell
pipenv sync
```
### Rodando script

O script automaticamente pega os dados referente ao intervalo de segunda a domingo da semana anterior. O nescessário é apenas executa o script com:

```
python NewTimesheet.py
```

O programa irá gerar um novo arquivo no formato do Excel que será a base de dados da timesheet do semestre.

