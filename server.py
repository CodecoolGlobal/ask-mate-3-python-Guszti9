from flask import Flask, render_template, request, redirect, url_for, session
from bonus_questions import SAMPLE_QUESTIONS
from markupsafe import Markup
import data_manager_sql
import util


app = Flask(__name__)
app.secret_key = 'powerpuffprogrammers'
app.config['UPLOAD_FOLDER'] = util.UPLOAD_FOLDER


@app.route("/")
def home():
    data = data_manager_sql.get_questions()
    loop_range = 5 if len(data) > 5 else len(data)
    if request.args.get('search'):
        search_phrase = request.args.get("search")
        question_data = data_manager_sql.search_question(request.args.get('search'))
        loop_range = 5 if len(question_data) > 5 else len(question_data)
        answer_data = data_manager_sql.search_answer(request.args.get('search'))
        for dictionary in question_data:
            util.marking(dictionary, search_phrase)
        for dictionary in answer_data:
            dictionary['a_message'] = dictionary['a_message'].casefold()
            dictionary['a_message'] = Markup(dictionary['a_message'].replace(search_phrase, f"<mark>{search_phrase}</mark>"))
            util.marking(dictionary, search_phrase)
        return render_template("index.html", data=question_data, answer_data=answer_data, loop_range=loop_range)
    return render_template("index.html", data=data, loop_range=loop_range)


@app.route("/list")
def list_questions():
    data = data_manager_sql.get_questions()
    if request.args.get('order_by'):
        return render_template("list.html", data=data_manager_sql.get_questions(request.args.get('order_by'), request.args.get('sorting_order')))
    return render_template("list.html", data=data)


@app.route("/question/<question_id>")
def display_question(question_id):
    data_manager_sql.increase_view_number(question_id)
    question_data = data_manager_sql.get_question_by_id(question_id)
    answers_data = data_manager_sql.get_answers(question_id)
    comment_data = {'question': data_manager_sql.get_comments_by_question_id(question_id)}
    tags = data_manager_sql.get_tags(question_id)
    for answer in answers_data:
        comment_data[answer['id']] = data_manager_sql.get_comments_by_answer_id(answer['id'])
    return render_template("question_page.html", question_data=question_data, answers=answers_data, comments=comment_data, tags=tags)


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    user_id = session['id']
    if request.method == 'POST':
        util.upload_image(request.files['image'])
        question_id = data_manager_sql.add_question(request.form['title'], request.form['message'], user_id, request.files['image'].filename)['id']
        return redirect(f'/question/{question_id}')
    return render_template("add-edit-question.html")


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'POST':
        user_id = data_manager_sql.get_question_by_id(question_id)['user_id']
        if session['id'] == user_id:
            data_manager_sql.edit_question(question_id, request.form['title'], request.form['message'], request.files['image'].filename)
            if request.files['image']:
                util.upload_image(request.files['image'])
            return redirect(f"/question/{question_id}")

    return render_template("add-edit-question.html", question_data=data_manager_sql.get_question_by_id(question_id))


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    user_id = data_manager_sql.get_question_by_id(question_id)['user_id']
    if session['id'] == user_id:
        data_manager_sql.delete_question(question_id)
        data_manager_sql.delete_tag_if_not_in_question_tag()
    return redirect('/list')


@app.route("/question/<question_id>/<vote>")
def vote_question(question_id, vote):
    data_manager_sql.change_question_vote_number(question_id, vote)
    data_manager_sql.change_reputation_by_question(question_id, vote)
    return redirect('/list')


@app.route("/bonus-questions")
def bonus_questions():
    return render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def post_answer(question_id):
    if 'username' in session:
        username = session['username']
        user_id = data_manager_sql.get_user_id_by_user_name(username)['user_id']
        if request.method == 'POST':
            util.upload_image(request.files['image'])
            data_manager_sql.add_new_answer(question_id, request.form['message'], user_id, request.files['image'].filename)
            return redirect(url_for('display_question', question_id=question_id))
    return render_template("add-edit-answer.html", question=data_manager_sql.get_question_by_id(question_id),
                           answers=data_manager_sql.get_answers(question_id), answer=False)


@app.route("/answer/<answer_id>/edit", methods=['GET', 'POST'])
def edit_answer(answer_id):
    if 'username' in session:
        answer_to_edit = data_manager_sql.get_answer_by_id(answer_id)
        question_id = answer_to_edit['question_id']
        if request.method == 'POST':
            data_manager_sql.edit_answer(answer_id, request.form['message'], request.files['image'].filename)
            if request.files['image']:
                util.upload_image(request.files['image'])
            return redirect(url_for('display_question', question_id=question_id))
    return render_template('add-edit-answer.html', answer=answer_to_edit, question=data_manager_sql.get_question_by_id(question_id))


@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    if 'username' in session:
        answer_to_delete = data_manager_sql.get_answer_by_id(answer_id)
        if answer_to_delete['image']:
            util.delete_image(answer_to_delete['image'])
        data_manager_sql.delete_answer(answer_id)
        question_id = answer_to_delete['question_id']
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/answer/<answer_id>/<vote>")
def vote_answer(answer_id, vote):
    if 'username' in session:
        answer_to_vote = data_manager_sql.get_answer_by_id(answer_id)
        data_manager_sql.change_answers_vote_number(vote, answer_id)
        data_manager_sql.change_reputation_by_answer(answer_id, vote)
        question_id = answer_to_vote['question_id']
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/answer_acceptance/<answer_id>/<acceptance_value>")
def accept_refuse_answer(answer_id, acceptance_value):
    question_id = data_manager_sql.get_answer_by_id(answer_id)['question_id']
    data_manager_sql.accept_refuse_answer(answer_id, acceptance_value)
    data_manager_sql.change_reputation_by_accepted_answer(answer_id)
    return redirect(url_for("display_question", question_id=question_id))


@app.route("/question/<question_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_question(question_id):
    if request.method == 'POST':
        if 'username' in session:
            user_id = data_manager_sql.get_user_id_by_user_name(session['username'])['user_id']
            data_manager_sql.add_comments_to_question(question_id, request.form['message'], user_id)
            return redirect(url_for('display_question', question_id=question_id))
    return render_template("add-edit-comment.html")


@app.route("/answer/<answer_id>/new-comment", methods=['GET', 'POST'])
def add_comment_to_answer(answer_id):
    if request.method == 'POST':
        if 'username' in session:
            user_id = data_manager_sql.get_user_id_by_user_name(session['username'])['user_id']
            data_manager_sql.add_comments_to_answer(answer_id, request.form['message'], user_id)
            question_id = data_manager_sql.get_answer_by_id(answer_id)['question_id']
            return redirect(url_for('display_question', question_id=question_id))
    return render_template("add-edit-comment.html")


@app.route("/comment/<comment_id>/edit", methods=['GET', 'POST'])
def edit_comment(comment_id):
    if 'username' in session:
        user_id = data_manager_sql.get_user_id_by_user_name(session['username'])['user_id']
        comment = data_manager_sql.get_comment(comment_id)
        if request.method == 'POST':
            if user_id == comment['user_id']:
                data_manager_sql.edit_comments(comment_id, request.form['message'])
                if comment['question_id']:
                    question_id = comment['question_id']
                else:
                    question_id = data_manager_sql.get_answer_by_id(comment['answer_id'])['question_id']
                return redirect(url_for('display_question', question_id=question_id))
    return render_template("add-edit-comment.html", comment_data=comment)


@app.route("/comments/<comment_id>/delete")
def delete_comment(comment_id):
    if 'username' in session:
        user_id = data_manager_sql.get_user_id_by_user_name(session['username'])['user_id']
        comment = data_manager_sql.get_comment(comment_id)
        if user_id == comment['user_id']:
            if comment['question_id']:
                question_id = comment['question_id']
            else:
                question_id = data_manager_sql.get_answer_by_id(comment['answer_id'])['question_id']
            data_manager_sql.delete_comments(comment_id)
    return redirect(url_for('display_question', question_id=question_id))


@app.route("/tag_page")
def tag_page():
    return render_template("tag_page.html", tags_and_questions=data_manager_sql.get_tags_and_number_of_question())


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


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag(question_id, tag_id):
    data_manager_sql.delete_question_tag(tag_id)
    data_manager_sql.delete_tag_if_not_in_question_tag()
    question_data = data_manager_sql.get_question_by_id(question_id)
    return redirect(url_for('display_question', question_id=question_data['id']))


@app.route("/registration", methods=['GET', 'POST'])
def registration():
    information = ''
    if request.method == 'POST':
        if request.form['password'] == request.form['check_password']:
            username = request.form['username']
            password = request.form['password']
            hashed_password = util.hash_password(password)
            data_manager_sql.registration(username, hashed_password)
            return redirect('/')
        else:
            information = 'Passwords does not match!'
    return render_template('registration.html', info=information)


@app.route("/login", methods=['GET', 'POST'])
def login():
    logininfo = ''
    usernames = data_manager_sql.get_usernames()
    if request.method == 'POST':
        if request.form['username'] in usernames:
            username = request.form['username']
            password = request.form['password']
            if util.verify_password(password, data_manager_sql.get_user_password(username)):
                session['username'] = username
                session['id'] = data_manager_sql.get_user_id_by_user_name(username)['user_id']
                return redirect("/")
            else:
                logininfo = 'Invalid login attempt!'
    return render_template('login.html', logininfo=logininfo)


@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('id', None)
    return redirect("/")


@app.route("/users")
def list_users():
    if session and 'username' in session:
        users = data_manager_sql.get_users()
        return render_template("users-list.html", users=users)


@app.route("/user/<user_id>")
def display_user(user_id):
    user = data_manager_sql.get_user(user_id)
    questions = data_manager_sql.get_questions_by_user_id(user_id)
    answers = data_manager_sql.get_answers_by_user_id(user_id)
    comments = data_manager_sql.get_comments_by_user_id(user_id)
    return render_template("user.html", user=user, questions=questions, answers=answers, comments=comments)


if __name__ == "__main__":
    app.run(debug=True)
