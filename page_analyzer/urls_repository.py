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

    def find(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute('SELECT * FROM urls WHERE id = %s', (url_id,))
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

    def get_content_checks(self, url_id):
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    '''
                    SELECT * FROM url_checks
                    WHERE url_id = %s
                    ''',
                    (url_id,))
                return cur.fetchall()

    def save_checks(self, url_id, url_check_data):
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute(
                    '''
                    INSERT INTO url_checks (
                        url_id,
                        status_code,
                        h1,
                        title,
                        description
                        )
                    VALUES (%s, %s, %s, %s, %s)
                    ''',
                    (url_id, 
                     url_check_data['status_code'],
                     url_check_data['h1'],
                     url_check_data['title'],
                     url_check_data['description'],
                     )
                )

            conn.commit()

    def get_last_check(self):
        with self.get_connection() as conn:
            with conn.cursor(row_factory=dict_row) as cur:
                cur.execute('''
                            SELECT DISTINCT ON (u.id)
                            u.id, 
                            u.name,
                            uc.created_at AS last_check,
                            uc.status_code AS last_status_code
                            FROM urls AS u
                            LEFT JOIN url_checks AS uc
                            ON u.id = uc.url_id
                            ORDER BY u.id DESC
                            ''')
                return cur.fetchall()


    

