import os
from google.cloud import bigquery


credentials_path = "acessKey.json"
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credentials_path

client = bigquery.Client()
table_id = 'api-webscrapping.data.BBC_NEWS'

def send_to_bq(url, title, author, date, text):
    rows_to_insert = [
        {
            u'URL': url,
            u'TITLES': title,
            u'AUTHOR': author,
            u'DATE': date,
            u'TEXT': text
        }
    ]
    client.insert_rows_json(table_id, rows_to_insert)
