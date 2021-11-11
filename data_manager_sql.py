import connection_sql


# QUERY'S FOR QUESTIONS


@connection_sql.connection_handler
def add_question(cursor, title, message, user_id, image=''):
    query = """
                INSERT INTO question (submission_time, view_number, vote_number, title, message, image, user_id)
                VALUES (CURRENT_TIMESTAMP, -1, 0, %(title)s, %(message)s, %(image)s, %(user_id)s)"""
    cursor.execute(query, {'title': title, 'message': message, 'user_id': user_id, 'image': image})
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
        cursor.execute(query, {'title': title, 'message': message, 'image': image, 'question_id': question_id})
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
def search_question(cursor, search_word):
    query = """
    SELECT *
    FROM question
    WHERE title ILIKE %s
    OR question.message ILIKE %s"""
    args = ['%' + search_word + '%'] * 2
    cursor.execute(query, args)
    return cursor.fetchall()


@connection_sql.connection_handler
def get_question_by_id(cursor, question_id):
    query = """
        SELECT question.id, to_char(submission_time, 'YYYY-MM-DD HH24:MI') AS submission_time, view_number, vote_number, title, message, image, users.username AS username, user_id
        FROM question, users
        WHERE question.id = %(question_id)s
        AND users.id = question.user_id;"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchone()


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
def get_questions(cursor, order_by='submission_time', order='desc'):
    query = f"""
        SELECT id, to_char(submission_time, 'YYYY-MM-DD HH24:MI') AS submission_time, view_number, vote_number, title, message, image
        FROM question
        ORDER BY {order_by} {order}"""
    cursor.execute(query)
    return cursor.fetchall()


@connection_sql.connection_handler
def get_questions_by_user_id(cursor, user_id):
    query = """
        SELECT id, to_char(submission_time, 'YYYY-MM-DD HH24:MI') AS submission_time, view_number, vote_number, title, message, image
        FROM question
        WHERE user_id = %(user_id)s
    """
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


# QUERY'S FOR ANSWER


@connection_sql.connection_handler
def add_new_answer(cursor, question_id, message, user_id, image=''):
    query = """
                INSERT INTO answer (submission_time, vote_number, question_id, message, image, user_id)
                VALUES (CURRENT_TIMESTAMP, 0, %(question_id)s, %(message)s, %(image)s, %(user_id)s)"""
    cursor.execute(query, {'question_id': question_id, 'message': message, 'image': image, 'user_id': user_id})


@connection_sql.connection_handler
def edit_answer(cursor, answer_id, message, image):
    if image:
        query = f"""
            UPDATE answer
            SET message = %(message)s, image = %(image)s
            WHERE id = %(answer_id)s"""
        cursor.execute(query, {'message': message, 'image': image, 'answer_id': answer_id})
    else:
        query = f"""
            UPDATE answer
            SET message = %(message)s
            WHERE id = %(answer_id)s"""
        cursor.execute(query, {'message': message, 'answer_id': answer_id})


@connection_sql.connection_handler
def delete_answer(cursor, answer_id):
    query = """
        DELETE FROM answer
        WHERE id = %(answer_id)s"""
    cursor.execute(query, {'answer_id': answer_id})


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
def search_answer(cursor, search_word):
    query = """
    SELECT question.id, question.submission_time, question.title, question.message, question.image, question.vote_number, question.view_number, answer.message AS a_message
    FROM question
    JOIN answer ON question.id = answer.question_id
    WHERE answer.message ILIKE %s"""
    args = ['%' + search_word + '%']
    cursor.execute(query, args)
    return cursor.fetchall()


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
        SELECT answer.id, submission_time, vote_number, question_id, message, image, user_id, users.username AS username, accepted
        FROM answer, users
        WHERE question_id = %(question_id)s
        AND user_id = users.id
        ORDER BY submission_time"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@connection_sql.connection_handler
def get_answers_by_user_id(cursor, user_id):
    query = """
        SELECT answer.id, submission_time, vote_number, question_id, message, image
        from answer
        where user_id = %(user_id)s
    """
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchall()


@connection_sql.connection_handler
def accept_refuse_answer(cursor, answer_id, acceptance_value):
    if acceptance_value == 'accept':
        query = """
            UPDATE answer
            SET accepted = 1
            WHERE answer.id = %(answer_id)s;"""
    elif acceptance_value == "refuse":
        query = """
                    UPDATE answer
                    SET accepted = -1
                    WHERE answer.id = %(answer_id)s;"""
    cursor.execute(query, {'answer_id': answer_id})

# QUERY'S FOR COMMENT


@connection_sql.connection_handler
def add_comments_to_question(cursor, question_id, message, user_id):
    query = """
        INSERT INTO comment (question_id, message, submission_time, edited_count, user_id)
        VALUES (%(question_id)s, %(message)s, CURRENT_TIMESTAMP, 0, %(user_id)s)
        """
    cursor.execute(query, {'question_id': question_id, 'message': message, 'user_id': user_id})


@connection_sql.connection_handler
def add_comments_to_answer(cursor, answer_id, message, user_id):
    query = """
        INSERT INTO comment (answer_id, message, submission_time, edited_count, user_id)
        VALUES (%(answer_id)s, %(message)s, CURRENT_TIMESTAMP, 0, %(user_id)s)
        """
    cursor.execute(query, {'answer_id': answer_id, 'message': message, 'user_id': user_id})


@connection_sql.connection_handler
def edit_comments(cursor, comment_id, message):
    query = """
        UPDATE comment
        SET message = %(message)s, submission_time = CURRENT_TIMESTAMP, edited_count = edited_count + 1
        WHERE id = %(comment_id)s
        """
    cursor.execute(query, {'comment_id': comment_id, 'message': message})


@connection_sql.connection_handler
def delete_comments(cursor, comment_id):
    query = """
        DELETE FROM comment
        WHERE id = %(comment_id)s
        """
    cursor.execute(query, {'comment_id': comment_id})


@connection_sql.connection_handler
def get_comments_by_question_id(cursor, question_id):
    query = """
        SELECT id, message, to_char(submission_time, 'YYYY-MM-DD HH24:MI') AS submission_time, edited_count, user_id
        FROM comment
        WHERE question_id = %(question_id)s
        """
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@connection_sql.connection_handler
def get_comments_by_answer_id(cursor, answer_id):
    query = """
        SELECT id, message, to_char(submission_time, 'YYYY-MM-DD HH24:MI') AS submission_time, edited_count, user_id
        FROM comment
        WHERE answer_id = %(answer_id)s
        """
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchall()


@connection_sql.connection_handler
def get_comment(cursor, comment_id):
    query = """
        SELECT message, question_id, answer_id, user_id
        FROM comment
        WHERE id = %(comment_id)s
        """
    cursor.execute(query, {'comment_id': comment_id})
    return cursor.fetchone()


@connection_sql.connection_handler
def get_comments_by_user_id(curses, user_id):
    query = """
        SELECT
            message,
            (case when c.question_id is null
            THEN
                (select a.question_id
                from answer a
                where a.id = c.answer_id)
            ELSE c.question_id END)
            as question_id,
            answer_id
        FROM comment c
        WHERE user_id = %(user_id)s
    """
    curses.execute(query, {'user_id': user_id})
    return curses.fetchall()


# QUERY'S FOR TAG


@connection_sql.connection_handler
def add_question_tag(cursor, question_id, tag_id):
    query = """
    INSERT INTO question_tag (question_id, tag_id)
    VALUES (%(question_id)s, %(tag_id)s)"""
    cursor.execute(query, {'question_id': question_id, 'tag_id': tag_id})


@connection_sql.connection_handler
def add_tag(cursor, question_id, tag_name):
    query = """
    INSERT INTO tag (name)
    VALUES (%(tag_name)s)
    RETURNING id """
    cursor.execute(query, {'tag_name': tag_name})
    tag_id = cursor.fetchone()['id']
    query = """
    INSERT INTO question_tag (question_id, tag_id)
    VALUES (%(question_id)s, %(tag_id)s)"""
    cursor.execute(query, {'question_id': question_id, 'tag_id': tag_id})


@connection_sql.connection_handler
def delete_question_tag(cursor, tag_id):
    query = """
        DELETE FROM question_tag
        WHERE tag_id = %(tag_id)s
        """
    cursor.execute(query, {'tag_id': tag_id})


@connection_sql.connection_handler
def delete_tag_if_not_in_question_tag(cursor):
    query = """
    DELETE FROM tag
    WHERE id NOT IN (SELECT tag_id FROM question_tag)
    """
    cursor.execute(query)


@connection_sql.connection_handler
def get_tags(cursor, question_id):
    query = """
    SELECT tag_id, name from question_tag
    inner join tag t on t.id = question_tag.tag_id
    WHERE question_id = %(question_id)s"""
    cursor.execute(query, {'question_id': question_id})
    return cursor.fetchall()


@connection_sql.connection_handler
def get_non_added_tags_for_question(cursor, added_tags, question_id):
    query = """
        SELECT id, name from tag
        WHERE name NOT IN (SELECT name from tag
        inner join question_tag q on q.tag_id = tag.id
        WHERE question_id = %(question_id)s)"""
    cursor.execute(query, {'added_tags': added_tags, 'question_id': question_id})
    return cursor.fetchall()


# QUERY'S FOR USERS


@connection_sql.connection_handler
def registration(cursor, username, password, image=''):
    query = """
    INSERT INTO users (username, password, reputation, registration_date, avatar)
    VALUES (%(username)s, %(password)s, 0, CURRENT_TIMESTAMP, %(image)s);"""
    cursor.execute(query, {'username': username, 'password': password, 'image': image})


@connection_sql.connection_handler
def change_reputation_by_question(cursor, question_id, vote):
    if vote == 'vote_up':
        query = """
        UPDATE users
        SET reputation = reputation + 5
        FROM question
        WHERE question.id = %(question_id)s 
        AND question.user_id = users.id;
        """
    else:
        query = """
                UPDATE users
                SET reputation = reputation - 2
                FROM question
                WHERE question.id = %(question_id)s 
                AND question.user_id = users.id;
                """
    cursor.execute(query, {'question_id': question_id})


@connection_sql.connection_handler
def change_reputation_by_answer(cursor, answer_id, vote):
    if vote == 'vote_up':
        query = """
        UPDATE users
        SET reputation = reputation + 10
        FROM answer
        WHERE answer.id = %(answer_id)s 
        AND answer.user_id = users.id;
        """
    else:
        query = """
                UPDATE users
                SET reputation = reputation - 2
                FROM answer
                WHERE answer.id = %(answer_id)s 
                AND answer.user_id = users.id;
                """
    cursor.execute(query, {'answer_id': answer_id})


@connection_sql.connection_handler
def change_reputation_by_accepted_answer(cursor, answer_id):
    if get_acceptance_value(answer_id) == 0:
        query = """
        UPDATE users
        SET reputation = reputation + 15
        FROM answer
        WHERE answer.id = %(answer_id)s
        AND answer.user_id = users.id;
        """
    else:
        query = """
                UPDATE users
                SET reputation = reputation - 15
                FROM answer
                WHERE answer.id = %(answer_id)s
                AND answer.user_id = users.id;
                """
    cursor.execute(query, {'answer_id': answer_id})


@connection_sql.connection_handler
def get_usernames(cursor):
    query = """
    SELECT username
    FROM users
    GROUP BY username;"""
    cursor.execute(query)
    usernames = [row["username"] for row in cursor.fetchall()]
    return usernames


@connection_sql.connection_handler
def get_user_password(cursor, username):
    query = """
    SELECT password
    FROM users
    WHERE username = %(username)s;"""
    cursor.execute(query, {'username': username})
    hashed_password = [row["password"] for row in cursor.fetchall()]
    return hashed_password[0]


@connection_sql.connection_handler
def get_users(cursor):
    query = """
        SELECT
            id,
            username,
            reputation,
            registration_date,
            (select count(*) from question where user_id = users.id) as number_of_asked_questions,
            (select count(*) from answer where user_id = users.id) as number_of_answers,
            (select count(*) from comment where user_id = users.id) as number_of_comments
        FROM users
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection_sql.connection_handler
def get_user(cursor, user_id):
    query = """
        SELECT 
            *,
            (select count(*) from question where %(user_id)s = user_id) as number_of_asked_questions,
            (select count(*) from answer where %(user_id)s = user_id) as number_of_answers,
            (select count(*) from comment where %(user_id)s = user_id) as number_of_comments
        FROM users
        WHERE id = %(user_id)s
    """
    cursor.execute(query, {'user_id': user_id})
    return cursor.fetchone()


# PLUS QUERY'S


@connection_sql.connection_handler
def get_tags_and_number_of_question(cursor):
    query = """
    SELECT name, COUNT(question_id) as number_of_questions
    FROM tag
    INNER JOIN question_tag qt
    ON tag.id = qt.tag_id
    GROUP BY name
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection_sql.connection_handler
def get_user_id_by_user_name(cursor, username):
    query = """
    SELECT id AS user_id
    FROM users
    WHERE username = %(username)s"""
    cursor.execute(query, {'username': username})
    return cursor.fetchone()


@connection_sql.connection_handler
def get_acceptance_value(cursor, answer_id):
    query = """
    SELECT accepted
    FROM answer
    WHERE id = %(answer_id)s;
    """
    cursor.execute(query, {'answer_id': answer_id})
    return cursor.fetchone()