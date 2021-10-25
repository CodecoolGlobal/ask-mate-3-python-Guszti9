import csv
import os
from werkzeug.utils import secure_filename

QUESTION_HEADER = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADER = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
QUESTIONS_FILE_PATH = 'sample_data/question.csv'
ANSWERS_FILE_PATH = 'sample_data/answer.csv'

UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'png', 'jpg'}


def read_from_dict_file(filename):
    with open(filename, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        data_dict = list(reader)
        return data_dict


def write_to_dict_file(filename, data_to_write, fieldnames):
    with open(filename, 'w', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in data_to_write:
            writer.writerow(row)


def append_to_dict_file(filename, data_to_write, fieldnames):
    with open(filename, 'a', newline='') as csv_file:
        appender = csv.DictWriter(csv_file, fieldnames=fieldnames)
        appender.writerow(data_to_write)


def upload_image(image):
    if '.' in image.filename and image.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS:
        filename = secure_filename(image.filename)
        image.save(os.path.join(UPLOAD_FOLDER, filename))


def delete_image(image_name):
    os.remove(os.path.join(UPLOAD_FOLDER, image_name))
