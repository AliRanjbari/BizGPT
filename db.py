import psycopg2
import logging

logging.basicConfig(
    format='%(asctime)s %(levelname)s:%(message)s',
    level=logging.INFO)


class DB:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="qavanin",
            user="admin",
            password="12345"
        )
        self.cur = self.conn.cursor()
        self.__create_table()
       
        
    def __create_table(self):
        logging.info("DataBase: Creating data base if does not exists.")
        self.cur.execute('''
        CREATE TABLE IF NOT EXISTS approvals (
                        id SERIAL PRIMARY KEY,
                        text TEXT,
                        embedding FLOAT8[]  
            ) 
        ''')

        self.conn.commit()

    def add(self, id: int, text: str, embedding):
        logging.info(f"DataBase: Adding data with id {id}")
        insert_query = '''
            INSERT INTO approvals (id, text, embedding)
            VALUES (%d, %s, %s)
            '''
        self.cur.execute(insert_query, (id, text, embedding))
        self.conn.commit()