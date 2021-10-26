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


@connection_sql.connection_handler
def edit_question(cursor, question_id, title, message, image):
    if image:
        query = f"""
            UPDATE question
            SET title = '{title}', message = '{message}', image = '{image}'
            WHERE id = {question_id}"""
    else:
        query = f"""
            UPDATE question
            SET title = '{title}', message = '{message}'
            WHERE id = {question_id}"""
    cursor.execute(query)


@connection_sql.connection_handler
def get_question_by_id(cursor, question_id):
    query = f"""
        SELECT *
        FROM question
        WHERE id = {question_id}"""
    cursor.execute(query)
    return cursor.fetchone()


@connection_sql.connection_handler
def get_questions(cursor, order_by='submission_time', order='desc'):
    query = f"""
        SELECT *
        FROM question
        ORDER BY {order_by} {order}"""
    cursor.execute(query)
    return cursor.fetchall()
