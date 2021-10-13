import connection
import time


def filter_answers_by_question_id(question_id):
    all_answers = connection.read_from_dict_file('sample_data/answer.csv')
    filtered = [answer for answer in all_answers if answer['question_id'] == question_id]
    return filtered


def find_question_by_question_id(question_id):
    all_question = connection.read_from_dict_file('sample_data/question.csv')
    for question in all_question:
        if question['id'] == question_id:
            question_by_id = question
            break
    return question_by_id


def find_answer_by_answer_id(answer_id):
    all_answers = connection.read_from_dict_file('sample_data/answer.csv')
    for answer in all_answers:
        if answer['id'] == answer_id:
            filtered_answer = answer
    return filtered_answer


def change_answers_vote_number(up_or_downvote, answer_id):
    all_answers = connection.read_from_dict_file(connection.ANSWERS_FILE_PATH)
    for answer in all_answers:
        if answer['id'] == answer_id:
            if up_or_downvote == 'vote_up':
                changed_vote_number = int(answer['vote_number']) + 1
                answer['vote_number'] = changed_vote_number
            elif up_or_downvote == 'vote_down':
                changed_vote_number = int(answer['vote_number']) - 1
            answer['vote_number'] = changed_vote_number
            break
    connection.write_to_dict_file(connection.ANSWERS_FILE_PATH, all_answers, connection.ANSWER_HEADER)


def increase_view_number(question_id):
    all_questions = connection.read_from_dict_file(connection.QUESTIONS_FILE_PATH)
    for question in all_questions:
        if question['id'] == question_id:
            increased_view_number = int(question['vote_number']) + 1
            question['vote_number'] = increased_view_number
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
