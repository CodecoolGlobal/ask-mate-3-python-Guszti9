from flask import Flask, render_template, request, redirect, url_for
import data_manager
import connection
import time

app = Flask(__name__)


@app.route("/")
def hello():
    return 'Hello World!'


@app.route("/list", methods=['GET', 'POST'])
def list_questions():
    list_of_data = connection.read_from_dict_file("sample_data/question.csv")
    if request.method == 'GET':
        print('meafao')
        if request.form[]
            print('keke')
    return render_template("list.html", data=list_of_data)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        all_question = connection.read_from_dict_file("sample_data/question.csv")
        max_id = max(item['id'] for item in all_question)
        new_question = {
            'id': int(max_id) + 1,
            'submission_time': int(time.time()),
            'view_number': 0,
            'vote_number': 0,
            'title': request.form['title'],
            'message': request.form['message']
        }
        connection.append_to_dict_file("sample_data/question.csv", new_question, connection.QUESTION_HEADER)
        return redirect('/list')
    return render_template("add-edit-question.html")


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    questions = connection.read_from_dict_file('sample_data/question.csv')
    question_index = int(question_id) - 1
    if request.method == 'POST':
        questions[question_index]['title'] = request.form['title']
        questions[question_index]['message'] = request.form['message']
        connection.write_to_dict_file("sample_data/question.csv", questions, connection.QUESTION_HEADER)
        return redirect(f"/question/{question_id}")

    return render_template("add-edit-question.html", question_data=questions[question_index])


@app.route("/question/<question_id>")
def display_question(question_id):
    question_data = data_manager.find_question_by_question_id(question_id)
    answers = data_manager.filter_answers_by_question_id(question_id)
    return render_template("question_page.html", question_data=question_data, answers=answers)


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def post_answer(question_id):
    all_answers = connection.read_from_dict_file('sample_data/answer.csv')
    answers_to_the_question = data_manager.filter_answers_by_question_id(question_id)
    question = data_manager.find_question_by_question_id(question_id)
    if request.method == 'POST':
        answer = {}
        max_id = max(item['id'] for item in all_answers)
        answer['id'] = str(int(max_id) + 1)
        answer['submission_time'] = int(time.time())
        answer['vote_number'] = 0
        answer['question_id'] = question_id
        answer['message'] = request.form['message']
        answer['image'] = ''

        connection.append_to_dict_file('sample_data/answer.csv', answer, ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image'])
        return redirect(url_for('display_question', question_id=question_id))
    return render_template("post-answer.html", question=question, answers=answers_to_the_question )


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    all_answers = connection.read_from_dict_file('sample_data/answer.csv')
    answer_to_delete = data_manager.filter_answer_by_answer_id(answer_id)
    all_answers.remove(answer_to_delete)
    connection.write_to_dict_file('sample_data/answer.csv', all_answers, ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image'])

    question_id = answer_to_delete['question_id']
    return redirect(url_for('display_question', question_id=question_id))


if __name__ == "__main__":
    app.run()

