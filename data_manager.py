import connection

def filter_answers_by_question_id(question_id):
    all_answers = connection.read_from_dict_file('sample_data/answer.csv')
    filtered = [answer for answer in all_answers if answer['question_id'] == question_id]
    return filtered


def filter_question_by_question_id(question_id):
    return connection.read_from_dict_file('sample_data/question.csv')[int(question_id)-1]

