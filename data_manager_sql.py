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


@connection_sql.connection_handler
def increase_view_number(cursor, question_id):
    query = f"""
    UPDATE question
    SET view_number = view_number + 1
    WHERE id = {question_id}"""
    cursor.execute(query)


@connection_sql.connection_handler
def get_answer_by_id(cursor, answer_id):
    query = f"""
        SELECT *
        FROM answer
        WHERE id = {answer_id}"""
    cursor.execute(query)
    return cursor.fetchone()

@connection_sql.connection_handler
def get_answers(cursor, question_id):
    query = f"""
        SELECT *
        FROM answer
        WHERE question_id = {question_id}
        ORDER BY submission_time"""
    cursor.execute(query)
    return cursor.fetchall()


@connection_sql.connection_handler
def change_answers_vote_number(cursor, vote, answer_id):
    if vote == 'vote_up':
        query = f"""
        UPDATE answer
        SET vote_number = vote_number + 1
        WHERE id = {answer_id}"""
    elif vote == 'vote_down':
        query = f"""
        UPDATE answer
        SET vote_number = vote_number - 1
        WHERE id = {answer_id}"""
    cursor.execute(query)