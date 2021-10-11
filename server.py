from flask import Flask, render_template, request
import connection

app = Flask(__name__)


@app.route("/")
def hello():
    return


@app.route("/list")
def list():
    list_of_data = connection.read_from_dict_file("sample_data/question.csv")
    print(list_of_data)
    return render_template("list.html", data=list_of_data)


if __name__ == "__main__":
    app.run()
