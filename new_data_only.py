import pandas as pd
from datetime import datetime, timedelta
import os

hoje = datetime.today().date()
ontem = hoje - timedelta(days=1)
hora = datetime.now().strftime("%H:%M:%S")

def get_new_data():
    print('get new data - starting ...')
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

    new_data_only = pd.concat([new_data, old_data], axis=0)
    new_data_only = new_data_only.merge(new_data, on='sequencial_id')
    new_data_only = new_data_only.drop_duplicates() 
    new_data_only = new_data_only.drop(columns='sequencial_id')
    new_data_only = new_data_only.drop_duplicates()
    new_data_only.to_csv('./data/new_data_only.csv', index=False, header=True, sep=';')
    print('New Data Only created')
    
        
    # apagando os arquivos em desuso
    try:
        os.remove("new_data.csv")
        os.remove("old_data.csv")
    except FileNotFoundError:
        print("O arquivo não foi encontrado.")
    
    return 


get_new_data()