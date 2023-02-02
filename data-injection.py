import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta

hoje = datetime.today().date()
ontem = hoje - timedelta(days=1)
hora = datetime.now().strftime("%H:%M:%S")

conn = psycopg2.connect(
    database='dbTeste', user='postgres', host='localhost', port='5432', password='3002'
)
conn.autocommit = True
cursor = conn.cursor()

sql = f""" copy dw.reclamacoes FROM 'C:/Projetos/AMERIC~1/data/DATA-{hoje}.CSV' DELIMITER ';' CSV HEADER ENCODING 'UTF8' QUOTE '\"' ESCAPE '''';"""


cursor.execute(sql)
