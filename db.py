import time
import psycopg2


class Database:
    def __init__(self, database_url) -> None:
        self.con = psycopg2.connect(database_url)
        self.cur = self.con.cursor()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.con.close()

    def create_table(self):
        q = """
        CREATE TABLE IF NOT EXISTS books (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            description TEXT NOT NULL,
            rating INT NOT NULL,
            price FLOAT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.cur.execute(q)
        self.con.commit()

    def truncate_table(self):
        q = """
        TRUNCATE TABLE books
        """
        self.cur.execute(q)
        self.con.commit()

    def insert_quote(self, book):
        q = """
        INSERT INTO books (name, description, rating, price) VALUES (%s, %s, %s, %s)
        """
        self.cur.execute(q, (book['name'], book['description'], book['rating'], book['price']))
        self.con.commit()
