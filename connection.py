import csv

QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def read_from_dict_file(filename):
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        data_dict = list(reader)
        return data_dict


def write_to_dict_file(filename, data_to_write, fieldnames):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data_to_write)


def append_to_dict_file(filename, data_to_write, fieldnames):
    with open(filename, 'a', newline='') as csvfile:
        appender = csv.DictWriter(csvfile, fieldnames=fieldnames)
        appender.writerow(data_to_write)
