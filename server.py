from flask import Flask, render_template, request, redirect, url_for
from markupsafe import Markup
import data_manager_sql
import util


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = util.UPLOAD_FOLDER


@app.route("/")
def home():
    data = data_manager_sql.get_questions()
    loop_range = 5 if len(data) > 5 else len(data)
    return render_template("index.html", data=data, loop_range=loop_range)


@app.route("/list")
def list_questions():
    data = data_manager_sql.get_questions()
    if request.args.get('order_by'):
        return render_template("list.html", data=data_manager_sql.get_questions(request.args.get('order_by'), request.args.get('sorting_order')))
    if request.args.get('search'):
        search_phrase = request.args.get("search")
        question_data = data_manager_sql.search_question(request.args.get('search'))
        answer_data = data_manager_sql.search_answer(request.args.get('search'))
        for dictionary in question_data:
            dictionary['message'] = dictionary['message'].casefold()
            dictionary['message'] = Markup(dictionary['message'].replace(search_phrase, f"<mark>{search_phrase}</mark>"))
            dictionary['title'] = dictionary['title'].casefold()
            dictionary['title'] = Markup(dictionary['title'].replace(search_phrase, f"<mark>{search_phrase}</mark>"))
        for dictionary in answer_data:
            dictionary['amessage'] = dictionary['amessage'].casefold()
            dictionary['amessage'] = Markup(dictionary['amessage'].replace(search_phrase, f"<mark>{search_phrase}</mark>"))
            dictionary['message'] = dictionary['message'].casefold()
            dictionary['message'] = Markup(dictionary['message'].replace(search_phrase, f"<mark>{search_phrase}</mark>"))
            dictionary['title'] = dictionary['title'].casefold()
            dictionary['title'] = Markup(dictionary['title'].replace(search_phrase, f"<mark>{search_phrase}</mark>"))
        return render_template("list.html", data=question_data, answer_data=answer_data)
    return render_template("list.html", data=data)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'POST':
        util.upload_image(request.files['image'])
        question_id = data_manager_sql.add_question(request.form['title'], request.form['message'], request.files['image'].filename)['id']
        return redirect(f'/question/{question_id}')
    return render_template("add-edit-question.html")


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        data_manager_sql.edit_question(question_id, request.form['title'], request.form['message'], request.files['image'].filename)
        if request.files['image']:
            util.upload_image(request.files['image'])
        return redirect(f"/question/{question_id}")

    return render_template("add-edit-question.html", question_data=data_manager_sql.get_question_by_id(question_id))


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    data_manager_sql.delete_question(question_id)
    return redirect('/list')


@app.route("/question/<question_id>/<vote>")
def vote_question(question_id, vote):
    data_manager_sql.change_question_vote_number(question_id, vote)
    return redirect('/list')


@app.route("/question/<question_id>")
def display_question(question_id):
    data_manager_sql.increase_view_number(question_id)
    question_data = data_manager_sql.get_question_by_id(question_id)
    answers_data = data_manager_sql.get_answers(question_id)
    comment_data = {'question': data_manager_sql.get_comments_by_question_id(question_id)}
    for answer in answers_data:
        comment_data[answer['id']] = data_manager_sql.get_comments_by_answer_id(answer['id'])
    return render_template("question_page.html", question_data=question_data, answers=answers_data, comments=comment_data)


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def post_answer(question_id):
    if request.method == 'POST':
        util.upload_image(request.files['image'])
        data_manager_sql.add_new_answer(question_id, request.form['message'], request.files['image'].filename)
        return redirect(url_for('display_question', question_id=question_id))
    return render_template("add-edit-answer.html", question=data_manager_sql.get_question_by_id(question_id),
                           answers=data_manager_sql.get_answers(question_id), answer=False)


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    answer_to_delete = data_manager_sql.get_answer_by_id(answer_id)
    if answer_to_delete['image']:
        util.delete_image(answer_to_delete['image'])
    data_manager_sql.delete_answer(answer_id)
    question_id = answer_to_delete['question_id']
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/answer/<answer_id>/<vote>")
def vote_answer(answer_id, vote):
    answer_to_vote = data_manager_sql.get_answer_by_id(answer_id)
    data_manager_sql.change_answers_vote_number(vote, answer_id)
    question_id = answer_to_vote['question_id']
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/question/<question_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'POST':
        data_manager_sql.add_comments_to_question(question_id, request.form['message'])
        return redirect(url_for('display_question', question_id=question_id))
    return render_template("add-edit-comment.html")


@app.route("/answer/<answer_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    if request.method == 'POST':
        data_manager_sql.add_comments_to_answer(answer_id, request.form['message'])
        question_id = data_manager_sql.get_answer_by_id(answer_id)['question_id']
        return redirect(url_for('display_question', question_id=question_id))
    return render_template("add-edit-comment.html")


@app.route("/comment/<comment_id>/edit", methods=['GET', 'POST'])
def edit_comment(comment_id):
    comment = data_manager_sql.get_comment(comment_id)
    if request.method == 'POST':
        data_manager_sql.edit_comments(comment_id, request.form['message'])
        if comment['question_id']:
            question_id = comment['question_id']
        else:
            question_id = data_manager_sql.get_answer_by_id(comment['answer_id'])['question_id']
        return redirect(url_for('display_question', question_id=question_id))
    return render_template("add-edit-comment.html", comment_data=comment)


@app.route("/comments/<comment_id>/delete")
def delete_comment(comment_id):
    comment = data_manager_sql.get_comment(comment_id)
    if comment['question_id']:
        question_id = comment['question_id']
    else:
        question_id = data_manager_sql.get_answer_by_id(comment['answer_id'])['question_id']
    data_manager_sql.delete_comments(comment_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/answer/<answer_id>/edit", methods=['GET', 'POST'])
def edit_answer(answer_id):
    answer_to_edit = data_manager_sql.get_answer_by_id(answer_id)
    question_id = answer_to_edit['question_id']
    if request.method == 'POST':
        data_manager_sql.edit_answer(answer_id, request.form['message'], request.files['image'].filename)
        if request.files['image']:
            util.upload_image(request.files['image'])
        return redirect(url_for('display_question', question_id=question_id))
    return render_template('add-edit-answer.html', answer=answer_to_edit, question=data_manager_sql.get_question_by_id(question_id))


@app.route("/question/<question_id>/new-tag", methods=['GET', 'POST'])
def add_tag(question_id):
    if request.method == 'POST':
        if request.form["postId"] == "2":
            data_manager_sql.add_tag(question_id, request.form['new-tag'])
        else:
            data_manager_sql.add_question_tag(int(question_id), int(request.form.get('select-tag')))
    tags = data_manager_sql.get_tags(question_id)
    non_added_tags = data_manager_sql.get_non_added_tags_for_question(tags, question_id)
    question_data = data_manager_sql.get_question_by_id(question_id)
    return render_template("add-tag.html", tags=tags, question_data=question_data, non_added_tags=non_added_tags)


if __name__ == "__main__":
    app.run(debug=True)
