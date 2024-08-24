import psycopg2
import logging
from os import getenv
from embedding import Embedding
import numpy as np

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class DB:
    def __init__(self, embedding: Embedding):
        self.embedding = embedding
        self.conn = psycopg2.connect(
            host=getenv("DB_HOST"),
            database=getenv("DB_DATABASE"),
            user=getenv("DB_USER"),
            password=getenv("DB_PASSWORD")
        )
        self.cur = self.conn.cursor()
        self.__create_table()
       
        
    def __create_table(self):
        logging.info("DataBase: Creating data base if does not exists.")
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS approvals (
                        id NUMERIC PRIMARY KEY,
                        text TEXT,
                        embedding BYTEA  
            ) 
        ''')

        self.conn.commit()


    def fetch_all(self):
        query = "SELECT * FROM approvals"
        self.cur.execute(query)
        rows = self.cur.fetchall()

        for row in rows:
            id, text, embedding_binary = row
            if embedding_binary:
                embedding_array = np.frombuffer(embedding_binary, dtype=np.float64)
                yield (id, text, embedding_array)
            else:
                continue
            

    def add(self, id: int, text: str):
        text_embedding = self.embedding.get_embedding(text).tobytes()
        logging.info(f"DataBase: Adding data with id {id}")
        insert_query = '''
                INSERT INTO approvals (id, text, embedding)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
                '''
        try:
            self.cur.execute(insert_query, (id, text, psycopg2.Binary(text_embedding)))
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.exception("DataBase: can't add entity")


    def close_connection(self):
        self.con.close()
        self.cur.close()