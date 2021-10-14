import connection
import time


def filter_answers_by_question_id(question_id):
    all_answers = connection.read_from_dict_file('sample_data/answer.csv')
    filtered = [answer for answer in all_answers if answer['question_id'] == question_id]
    return filtered


def find_data_by_id(id, data_path):
    all_data = connection.read_from_dict_file(data_path)
    for data in all_data:
        if data['id'] == id:
            return data


def change_vote_number(up_or_downvote, id, data_path, data_header):
    all_data = connection.read_from_dict_file(data_path)
    for data in all_data:
        if data['id'] == id:
            if up_or_downvote == 'vote_up':
                data['vote_number'] = int(data['vote_number']) + 1
            elif up_or_downvote == 'vote_down':
                data['vote_number'] = int(data['vote_number']) - 1
            break
    connection.write_to_dict_file(data_path, all_data, data_header)


def increase_view_number(question_id):
    all_questions = connection.read_from_dict_file(connection.QUESTIONS_FILE_PATH)
    for question in all_questions:
        if question['id'] == question_id:
            question['view_number'] = int(question['view_number']) + 1
            break
    connection.write_to_dict_file(connection.QUESTIONS_FILE_PATH, all_questions, connection.QUESTION_HEADER)


def sorting(is_descending, sorted_by='submission_time'):
    list_of_data = connection.read_from_dict_file(connection.QUESTIONS_FILE_PATH)
    if sorted_by == 'title' or sorted_by == 'message':
        return sorted(list_of_data, key=lambda i: str(i[sorted_by].capitalize()), reverse=is_descending)
    else:
        return sorted(list_of_data, key=lambda i: int(i[sorted_by]), reverse=is_descending)


def initialize_question(title, message, image=''):
    all_question = connection.read_from_dict_file(connection.QUESTIONS_FILE_PATH)
    max_id = max(item['id'] for item in all_question)
    new_question = {
        'id': int(max_id) + 1,
        'submission_time': int(time.time()),
        'view_number': 0,
        'vote_number': 0,
        'title': title,
        'message': message,
        'image': image
    }
    return new_question


def initialize_answer(question_id, message, image=''):
    all_answers = connection.read_from_dict_file(connection.ANSWERS_FILE_PATH)
    max_id = max(item['id'] for item in all_answers)
    new_answer = {
        'id': str(int(max_id) + 1),
        'submission_time': int(time.time()),
        'vote_number': 0,
        'question_id': question_id,
        'message': message,
        'image': image
    }
    return new_answer
