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
logs = []


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
            
        
        # print(data_criacao)
        formato_data = "%d/%m/%Y ÀS %H:%M"
        data_criacao = datetime.strptime(data_criacao, formato_data) # ETL pra converter pra timestamp
        data_criacao = str(data_criacao).replace('ÀS', '').strip()
        # print(data_criacao)
        
        reclamacao = {
            'titulo': titulo_reclamacao.upper(),
            'localizacao': localizacao.upper(),
            'data_criacao': data_criacao.upper(),
            'id_reclamacao': id_reclamacao.upper(),
            'status': status_reclamacao.upper(),
            'compraria_novamente': compraria_novamente.upper(),
            'nota_atendimento': nota_atendimento.upper(),
            'consideracao_final_consumidor': consideracao_final_consumidor.upper(),
            'referencia': 'AMERICANAS'
        }

        lista_reclamacoes.append(reclamacao)
    return lista_reclamacoes


try: 
    hoje = datetime.today().date()
    ontem = hoje - timedelta(days=1)
    hora = datetime.now().strftime("%H:%M:%S")
    
    # PAGINAÇÃO DAS 10 ULTIMAS PAGINAS, MAIS OU MENOS DADOS DE 1 DIA
    for x in range(1,10): 
        main(x)
        print(f"Estamos na página {x}")
        
    df = pd.DataFrame(lista_reclamacoes) # Dados novos coletados pelo script de web scraping
    print(f"Salvando ...")
    df.to_csv(f'./data/data-{hoje}.csv', index=False, sep=';', header=True)     
except Exception as e:
    msg_erro = '\n'+'='*60 +'\n'+f'{e} em {hoje} as {hora}\n' + '='*60+'\n'
    f = open('./logs/logs_error.txt', 'a')
    f.write(''.join(msg_erro))
    f.close()
    print(''.join(msg_erro))
finally:
    msg = '\n'+'='*60 +'\n'+f'O script rodou {hoje} as {hora} e foram coletados {len(df)} registros.\n'+'='*60+'\n'
    print(msg)
    f = open('./logs/logs.txt', 'a')
    f.write(''.join(msg))
    f.close()
    print(''.join(logs))