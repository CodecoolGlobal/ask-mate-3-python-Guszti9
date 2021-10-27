from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import connection_sql


@connection_sql.connection_handler
def add_question(cursor, title, message, image):
    query = """
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
        VALUES (CURRENT_TIMESTAMP, -1, 0, %(title)s, %(message)s, %(image)s)"""
    cursor.execute(query, {'title': title, 'message': message, 'image': 'images/' + image})
    query = """
            SELECT id
            FROM question
            WHERE view_number = -1"""
    cursor.execute(query)
    return cursor.fetchone()


@connection_sql.connection_handler
def edit_question(cursor, question_id, title, message, image):
    if image:
        query = """
            UPDATE question
            SET title = %(title)s, message = %(message)s, image = %(image)s
            WHERE id = %(question_id)s"""
        cursor.execute(query, {'title': title, 'message': message, 'image': 'images/' + image, 'question_id': question_id})
    else:
        query = """
            UPDATE question
            SET title = %(title)s, message = %(message)s
            WHERE id = %(question_id)s"""
        cursor.execute(query, {'title': title, 'message': message, 'question_id': question_id})


@connection_sql.connection_handler
def delete_question(cursor, question_id):
    query = """
        DELETE FROM question
        WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@connection_sql.connection_handler
def get_question_by_id(cursor, question_id):
    query = """
        SELECT *
        FROM question
        WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
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
def change_question_vote_number(cursor, question_id, vote):
    if vote == 'vote_up':
        query = """
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE id = %(question_id)s"""
    else:
        query = """
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@connection_sql.connection_handler
def increase_view_number(cursor, question_id):
    query = """
    UPDATE question
    SET view_number = view_number + 1
    WHERE id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})


@connection_sql.connection_handler
def get_answer_by_id(cursor, answer_id):
    query = """
        SELECT *
        FROM answer
        WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()


@connection_sql.connection_handler
def get_answers(cursor, question_id):
    query = """
        SELECT *
        FROM answer
        WHERE question_id = %(question_id)s
        ORDER BY submission_time"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@connection_sql.connection_handler
def add_new_answer(cursor, question_id, message, image=''):
    query = """
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES (CURRENT_TIMESTAMP, 0, %(question_id)s, %(message)s, %(image)s)"""
    cursor.execute(query, {'question_id': question_id, 'message': message, 'image': 'images/' + image})


@connection_sql.connection_handler
def change_answers_vote_number(cursor, vote, answer_id):
    if vote == 'vote_up':
        query = """
        UPDATE answer
        SET vote_number = vote_number + 1
        WHERE id = %(answer_id)s"""
    else:
        query = """
        UPDATE answer
        SET vote_number = vote_number - 1
        WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})


@connection_sql.connection_handler
def delete_answer(cursor, answer_id):
    query = """
        DELETE FROM answer
        WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})


@connection_sql.connection_handler
def edit_answer(cursor, answer_id, message, image):
    if image:
        query = f"""
            UPDATE answer
            SET message = %(message)s, image = %(image)s
            WHERE id = %(answer_id)s"""
        cursor.execute(query, {'message': message, 'image': 'images/' + image, 'answer_id': answer_id})
    else:
        query = f"""
            UPDATE answer
            SET message = %(message)s
            WHERE id = %(answer_id)s"""
        cursor.execute(query, {'message': message, 'answer_id': answer_id})


@connection_sql.connection_handler
def search_question(cursor, search_word):
    query = """
    SELECT *
    FROM question, answer
    WHERE title ILIKE %s
    OR question.message ILIKE %s
    OR answer.message ILIKE %s"""
    args = ['%' + search_word + '%'] * 3
    cursor.execute(query, args)
    return cursor.fetchall()
