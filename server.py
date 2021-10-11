from flask import Flask, render_template, request
import connection

app = Flask(__name__)


@app.route("/")
def hello():
    return


@app.route("/list")
def list_questions():
    list_of_data = connection.read_from_dict_file("sample_data/question.csv")
    print(list_of_data)
    return render_template("list.html", data=list_of_data)


@app.route("question/<question_id>")
def display_question(question_id):
    question_data = {}
    answers = []
    return render_template("question_page.html", question_data=question_data, answers=answers)


if __name__ == "__main__":
    app.run()
