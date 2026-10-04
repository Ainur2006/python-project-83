import psycopg
from psycopg.rows import dict_row


class UrlsRepository:
    def __init__(self, db_url):
        self.db_url = db_url

    def get_connection(self):
        return psycopg.connect(self.db_url)

    def get_content(self):
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute('SELECT * FROM urls ORDER BY created_at DESC')
                return cur.fetchall()

    def find(self, id):
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute('SELECT * FROM urls WHERE id = %s', (id,))
                return cur.fetchone()

    def save(self, name):
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    """
                    INSERT INTO urls (name)
                    VALUES (%s)
                    ON CONFLICT (name) DO NOTHING
                    RETURNING id
                    """,
                    (name,),
                )
                url = cur.fetchone()
                if url:
                    return url["id"]
                cur.execute(
                    "SELECT id FROM urls WHERE name = %s",
                    (name,),
                )
                return cur.fetchone()["id"]