import psycopg2

from entities import Event
from config import pSQL_adress, pSQL_db_name, pSQL_password, pSQL_username

# Connection to postgreSQL server and create table if not exists:
with psycopg2.connect(host=pSQL_adress, database=pSQL_db_name,
        user=pSQL_username, password=pSQL_password) as connection:
    connection.autocommit = True 
    with connection.cursor() as cursor:
        cursor.execute("""
                SELECT version();
                """)
        print("Server version: " + str(cursor.fetchone()))

        cursor.execute("""
                CREATE TABLE IF NOT EXISTS events(
                id INT PRIMARY KEY,
                title VARCHAR(100) DEFAULT 'NO_TITLE',
                event_date DATE, 
                date_added DATE 
                )
                """)


