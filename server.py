from flask import Flask, render_template, request, redirect, url_for
import data_manager
import connection
import time

app = Flask(__name__)


@app.route("/")
def hello():
    return 'Hello World!'


@app.route("/list")
def list_questions():
    list_of_data = connection.read_from_dict_file("sample_data/question.csv")
    print(list_of_data)
    return render_template("list.html", data=list_of_data)


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


if __name__ == "__main__":
    app.run()
