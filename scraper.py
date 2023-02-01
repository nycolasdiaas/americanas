# Web Scraping Reclame Aqui - Americanas
# Feito por Nycolas Dias

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup
import re
from datetime import datetime, timedelta
import os

# Requisitando página inicial
options = Options()
# options.add_argument('--headless')
options.add_argument('window-size=400,600')
links= []
lista_reclamacoes = []
url_base = 'https://www.reclameaqui.com.br'
errorlist = []
new_data = []

def ultima_pag():
    navegador = webdriver.Chrome(options=options)
    sleep(1)
    navegador.get('https://www.reclameaqui.com.br/empresa/sou-energy/lista-reclamacoes/')
    sleep(1)
    s = BeautifulSoup(navegador.page_source, 'html.parser')
    ult_pag = s.find('div', class_='sc-1sm4sxr-3 eejODo').find('ul', class_='sc-jhGUec eGyFMq').find_all('li')
    ult_pag = int(ult_pag[-2].text)
    return ult_pag

def main(x):
    url = f'https://www.reclameaqui.com.br/empresa/americanas-com-loja-online/lista-reclamacoes/?pagina={x}' 
    links = []
    # Pegando os dados do site e todas as reclamacoes da pagina
    navegador = webdriver.Chrome(options=options)
    sleep(2)
    navegador.get(url)
    sleep(2)
    page_content = navegador.page_source
    site = BeautifulSoup(page_content, 'html.parser')
    
   
    urls = site.findAll('div', attrs={'class': 'sc-1pe7b5t-0 bJdtis'}) # Conjunto com LINKS da pag

    for i in urls:
        link_req = url_base +i.find('a')['href']
        links.append(link_req)   
    
    for link in links:
        sleep(2)
        navegador.get(link)
        sleep(2)
        # print(navegador)
        soup = BeautifulSoup(navegador.page_source, 'html.parser')
        titulo_reclamacao = soup.find('h1', attrs={'class': 'lzlu7c-3 berwWw'}).text
        localizacao = soup.find('span', attrs={'data-testid': 'complaint-location'}).text
        data_criacao = soup.find('span', attrs={'data-testid': 'complaint-creation-date'}).text
        id_reclamacao = soup.find('span', attrs={'data-testid': 'complaint-id'}).text
        id_reclamacao = ''.join(re.findall('[0-9]{9}', id_reclamacao)) # RETIRANDO A PALAVRA 'ID'
        status_reclamacao = soup.find('div', attrs={'data-testid': 'complaint-status'}).text
        try:
            compraria_novamente = soup.find('div', attrs={'data-testid': 'complaint-deal-again'}).text
            nota_atendimento = soup.find('div', attrs={'class': 'uh4o7z-3 ceUcTc'}).text
            consideracao_final_consumidor = soup.find('p', attrs={'class': 'sc-1o3atjt-4 JkSWX'}).text
             
        except:
            compraria_novamente = ''
            nota_atendimento = ''
            consideracao_final_consumidor = ''
            
        reclamacao = {
            'TITULO': titulo_reclamacao.upper(),
            'LOCALIZACAO': localizacao.upper(),
            'DATA_CRIACAO': data_criacao.upper(),
            'ID_RECLAMACAO': id_reclamacao.upper(),
            'STATUS': status_reclamacao.upper(),
            'COMPRARIA_NOVAMENTE': compraria_novamente.upper(),
            'NOTA_ATENDIMENTO': nota_atendimento.upper(),
            'CONSIDERACAO_FINAL_CONSUMIDOR': consideracao_final_consumidor.upper(),
            'REFERENCIA': 'AMERICANAS'
        }

        lista_reclamacoes.append(reclamacao)
    return lista_reclamacoes

def get_new_data():
    old_data = pd.read_csv(f'./data/data-{ontem}.csv', sep=';')
    new_data = pd.read_csv(f'./data/data-{hoje}.csv', sep=';')


    data_e = old_data['DATA_CRIACAO']
    titulo_e = old_data['TITULO']
    data_c = new_data['DATA_CRIACAO']
    titulo_c = new_data['TITULO']

    day = datetime.today().date().day

    seq_id_e = (data_e + ' - ' + titulo_e)
    old_data['sequencial_id'] = seq_id_e
    old_data = old_data.drop_duplicates()
    old_data.to_csv('old_data.csv', index=False)
    #----------------------------------------------------------------
    seq_id_c = (data_e + ' - ' + titulo_e)
    new_data['sequencial_id'] = seq_id_c
    new_data = new_data.drop_duplicates()
    new_data.to_csv('new_data.csv',index=False)

    old_data = pd.read_csv(f'old_data.csv')
    new_data = pd.read_csv(f'new_data.csv')

    new_data_only = pd.merge(new_data, old_data, how='outer')
    new_data_only = new_data_only.drop_duplicates() 
    new_data_only = new_data_only.drop(columns='sequencial_id')
    new_data_only = new_data_only.drop_duplicates()
    new_data_only.to_csv('./data/new_data_only.csv', index=False)
    print('New Data Only created')


    # apagando os arquivos em desuso
    try:
        os.remove("new_data.csv")
        os.remove("old_data.csv")
    except FileNotFoundError:
        print("O arquivo não foi encontrado.")

    return

try: 
    hoje = datetime.today().date()
    ontem = hoje - timedelta(days=1)
    hora = datetime.now().strftime("%H:%M:%S")
    
    # PAGINAÇÃO DAS 10 ULTIMAS PAGINAS, MAIS OU MENOS DADOS DE 1 DIA
    for x in range(1,11): 
        main(x)
        print(f"Estamos na página {x}")
        
    df = pd.DataFrame(lista_reclamacoes) # Dados novos coletados pelo script de web scraping
    print(f"Salvando ...")
    df.to_csv(f'.\data\data-{hoje}.csv', index=False, sep=';') 
    
    sleep(3) # Aguardando ...
    
    print(f"Pegando somente os novos dados")
    get_new_data()
    
except Exception as e:
    errorlist.append(f'{e} em {hoje}')
    f = open('logs_error.txt', 'a')
    f.write(str(errorlist))
    f.close()
finally:
    print(f'Done. {hora}')