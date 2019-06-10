# Timesheet Clockify

Script para transformar os dados do Clockify no formato da Timesheet do NEO Empresarial. Desenvolvido por LAB em 2019.1.

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

No Clockify, entrar em [Detailed Reports](https://clockify.me/reports/detailed). Selecionar o intervalo desejado. Confirmar se não há nenhuma entrada de dado sem tag (_cliente_). Exportar para __csv__ com o nome __clockify_report.csv__ na pasta do programa. Rodar o script com:

```
python main.py
```

O programa irá gerar um novo csv e um arquivo no formato do Excel que pode ser filtrado para facilitar o preenchimento da Timesheeto para os membros utilizando o Clockify.

## To-Do

- [ ] Integrar com API do Clockify. Baixar automaticamente o arquivo csv da semana;
- [ ] Fazer argumento para selecionar semana que deseja baixar;
- [ ] Fazer Excel para transferir automaticamente para timesheet;
- [ ] Integrar com BD do NEO;
- [ ] Calcular métricas (IEP, PREP);
- [ ] Integrar com metabase.