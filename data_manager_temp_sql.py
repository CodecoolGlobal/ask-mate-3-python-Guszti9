import time
import connection_temp_sql
from typing import List, Dict
from psycopg2 import sql
from psycopg2.extras import RealDictCursor


@connection_temp_sql.connection_handler
def get_questions(cursor, order_by='submission_time', order='desc'):
    query = f"""
        SELECT *
        FROM question
        ORDER BY {order_by} {order}"""
    cursor.execute(query)
    return cursor.fetchall()
