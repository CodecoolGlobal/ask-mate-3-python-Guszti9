import connection


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


def change_answers_vote_number(up_or_downvote, answer_id, all_answers):
    for answer in all_answers:
        if answer['id'] == answer_id:
            if up_or_downvote == 'up':
                changed_vote_number = int(answer['vote_number']) + 1
                answer['vote_number'] = changed_vote_number
            elif up_or_downvote == 'down':
                changed_vote_number = int(answer['vote_number']) - 1
            answer['vote_number'] = changed_vote_number
            break
