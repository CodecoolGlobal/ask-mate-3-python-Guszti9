import connection
import time


def filter_answers_by_question_id(question_id):
    all_answers = connection.read_from_dict_file('sample_data/answer.csv')
    filtered = [answer for answer in all_answers if answer['question_id'] == question_id]
    return filtered


def find_data_by_id(data_id, data_path):
    all_data = connection.read_from_dict_file(data_path)
    for data in all_data:
        if data['id'] == data_id:
            return data


def change_vote_number(vote, data_id, data_path, data_header):
    all_data = connection.read_from_dict_file(data_path)
    for data in all_data:
        if data['id'] == data_id:
            if vote == 'vote_up':
                data['vote_number'] = int(data['vote_number']) + 1
            elif vote == 'vote_down':
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


def sort_by(list_of_data, request_args):
    header_index = 1
    for category in ['sort_by_time', 'sort_by_views', 'sort_by_votes', 'sort_by_title', 'sort_by_message']:
        if category in request_args:
            is_descending = request_args.get('sorting_order') == 'descending'
            if category == 'sort_by_message' or category == 'sort_by_title':
                sortedlist = sorted(list_of_data, key=lambda i: str(i[connection.QUESTION_HEADER[header_index]].capitalize()), reverse=is_descending)
            else:
                sortedlist = sorted(list_of_data, key=lambda i: int(i[connection.QUESTION_HEADER[header_index]]), reverse=is_descending)
            return sortedlist
        header_index += 1
    return list_of_data


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
