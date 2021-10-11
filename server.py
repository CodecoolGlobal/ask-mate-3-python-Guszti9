from flask import Flask, render_template, request
import connection

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
    question_data = connection.read_from_dict_file('sample_data/question.csv')[int(question_id)-1]
    answers = []
    all_answer_data = connection.read_from_dict_file('sample_data/answer.csv')
    for data in all_answer_data:
        if data['question_id'] == question_id:
            answers.append(data['message'])
    return render_template("question_page.html", question_data=question_data, answers=answers)


if __name__ == "__main__":
    app.run()
