from flask import Flask, render_template, request

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

@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'POST':
        max_id = max(item['id'] for item in all_answers)
        answer = {}
        answer['id'] = max_id + 1
        answer['submission_time'] = time.time()
        answer['vote_number'] = 0
        answer['question_id'] = question_id
        answer['message'] = request.form['message']
        answer['image'] = ''

    return render_template("post-answer.html", question= , answers= )


if __name__ == "__main__":
    app.run()
