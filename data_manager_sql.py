from psycopg2 import sql
from psycopg2.extras import RealDictCursor

import connection_sql
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg'}


@connection_sql.connection_handler
def add_question(cursor, title, message, image):
    query = f"""
        INSERT INTO question (submission_time, view_number, vote_number, title, message, image)
        VALUES (CURRENT_TIMESTAMP, -1, 0, '{title}', '{message}', '{image}')"""
    cursor.execute(query)
    query = """
        SELECT id
        FROM question
        WHERE view_number = -1"""
    cursor.execute(query)
    return cursor.fetchone()


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
def delete_question(cursor, question_id):
    query = f"""
        DELETE FROM question
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
def change_question_vote_number(cursor, question_id, vote):
    if vote == 'vote_up':
        query = f"""
        UPDATE question
        SET vote_number = vote_number + 1
        WHERE id = {question_id}"""
    elif vote == 'vote_down':
        query = f"""
        UPDATE question
        SET vote_number = vote_number - 1
        WHERE id = {question_id}"""
    cursor.execute(query)


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
def add_new_answer(cursor, question_id, message, image=''):
    query = f"""
        INSERT INTO answer (submission_time, vote_number, question_id, message, image)
        VALUES (CURRENT_TIMESTAMP, 0, '{question_id}', '{message}', '{image}')"""
    cursor.execute(query)


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


@connection_sql.connection_handler
def delete_answer(cursor, answer_id):
    query = f"""
        DELETE FROM answer
        WHERE id = {answer_id}"""
    cursor.execute(query)


@connection_sql.connection_handler
def get_comments_by_question_id(cursor, question_id):
    query = """
        SELECT message, submission_time
        FROM comment
        WHERE question_id = %(question_id)s
        """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@connection_sql.connection_handler
def add_comments_to_question(cursor, question_id, message):
    query = """
        INSERT INTO comment (question_id, message, submission_time, edited_count)
        VALUES (%(question_id)s, %(message)s, CURRENT_TIMESTAMP, 0)
        """
    cursor.execute(query, {'question_id': question_id, 'message': message})


def upload_image(image):
    if '.' in image.filename and image.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        filename = secure_filename(image.filename)
        image.save(os.path.join(UPLOAD_FOLDER, filename))


def delete_image(image_name):
    os.remove(os.path.join(UPLOAD_FOLDER, image_name))
