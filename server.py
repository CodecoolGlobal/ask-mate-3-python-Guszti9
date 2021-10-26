from flask import Flask, render_template, request, redirect, url_for
import data_manager
import connection
import data_manager_sql
from datetime import datetime

import data_manager_sql

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = connection.UPLOAD_FOLDER


@app.template_filter('datetime')
def datetime_format(unix_timestamp):
    return datetime.utcfromtimestamp(int(unix_timestamp)).strftime('%Y-%m-%d %H:%M')


@app.route("/")
def hello():
    return redirect('/list')


@app.route("/list")
def list_questions():
    data = data_manager_sql.get_questions()
    if request.args.get('order_by'):
        return render_template("list.html", data=data_manager_sql.get_questions(request.args.get('order_by'), request.args.get('sorting_order')))
    return render_template("list.html", data=data)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        connection.upload_image(request.files['image'])
        data_manager_sql.add_question(request.form['title'], request.form['message'], request.files['image'].filename)
        return redirect('/list')
    return render_template("add-edit-question.html")


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        data_manager_sql.edit_question(question_id, request.form['title'], request.form['message'], request.files['image'].filename)
        if request.files['image']:
            connection.upload_image(request.files['image'])
        return redirect(f"/question/{question_id}")

    return render_template("add-edit-question.html", question_data=data_manager_sql.get_question_by_id(question_id))


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    questions = connection.read_from_dict_file(connection.QUESTIONS_FILE_PATH)
    data = []
    for question in questions:
        if question['id'] != question_id:
            data.append(question)
        if question['id'] == question_id and question['image']:
            connection.delete_image(question['image'])
    connection.write_to_dict_file(connection.QUESTIONS_FILE_PATH, data, connection.QUESTION_HEADER)
    return redirect('/list')


@app.route("/question/<question_id>/<vote>")
def vote_question(question_id, vote):
    data_manager.change_vote_number(vote, question_id, connection.QUESTIONS_FILE_PATH, connection.QUESTION_HEADER)
    return redirect('/list')


@app.route("/question/<question_id>")
def display_question(question_id):
    data_manager.increase_view_number(question_id)
    answers = data_manager.filter_answers_by_question_id(question_id)
    return render_template("question_page.html", question_data=data_manager_sql.get_question_by_id(question_id), answers=answers)


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def post_answer(question_id):
    answers_to_the_question = data_manager.filter_answers_by_question_id(question_id)
    question = data_manager.find_data_by_id(question_id, connection.QUESTIONS_FILE_PATH)
    if request.method == 'POST':
        answer = data_manager.initialize_answer(question_id, request.form['message'], request.files['image'].filename)
        connection.append_to_dict_file(connection.ANSWERS_FILE_PATH, answer, connection.ANSWER_HEADER)
        connection.upload_image(request.files['image'])
        return redirect(url_for('display_question', question_id=question_id))
    return render_template("post-answer.html", question=question, answers=answers_to_the_question)


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    all_answers = connection.read_from_dict_file(connection.ANSWERS_FILE_PATH)
    answer_to_delete = data_manager.find_data_by_id(answer_id, connection.ANSWERS_FILE_PATH)
    if answer_to_delete['image']:
        connection.delete_image(answer_to_delete['image'])
    all_answers.remove(answer_to_delete)
    connection.write_to_dict_file(connection.ANSWERS_FILE_PATH, all_answers, connection.ANSWER_HEADER)
    question_id = answer_to_delete['question_id']
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/answer/<answer_id>/<vote>")
def vote_answer(answer_id, vote):
    data_manager.change_vote_number(vote, answer_id, connection.ANSWERS_FILE_PATH, connection.ANSWER_HEADER)
    answer_to_vote = data_manager.find_data_by_id(answer_id, connection.ANSWERS_FILE_PATH)
    question_id = answer_to_vote['question_id']
    return redirect(url_for('display_question', question_id=question_id))


if __name__ == "__main__":
    app.run()
