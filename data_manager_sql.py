from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import time
import connection_sql


@connection_sql.connection_handler
def add_question(cursor, title, message, image):
    query = f"""
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
        VALUES (CURRENT_TIMESTAMP, 0, 0, '{title}', '{message}', '{image}')"""
    cursor.execute(query)

