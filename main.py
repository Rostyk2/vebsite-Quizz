from flask import Flask, render_template, redirect, url_for, request, session
from quizz.squel import SQLManager

app = Flask(__name__)
app.secret_key = "Fri201000"

@app.route("/")
def index():
    manager = SQLManager("kahoot_3.db")
    quizzes = manager.select_quizzes()
    return render_template("index.html", quizzes=quizzes)

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if len(username) > 20:
            return "Нікнейм повинен містити не більше 20 символів"
        elif len(password) > 8:
            return "Пароль повинен містити не більше 8 символів"

        session["username"] = username
        session["password"] = password
        return redirect(url_for("home"))
    return render_template("register.html")

@app.route("/home")
def home():
    manager = SQLManager("kahoot_3.db")
    quizzes = manager.select_quizzes()
    return render_template("home.html", username=session.get("username"), quizzes=quizzes)

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio.html')

@app.route('/rules')
def rules():
    return render_template('rules.html')

@app.route('/info')
def information():
    return render_template('information.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route("/quizzes/<int:quizz_id>")
def start_quizz(quizz_id):
    manager = SQLManager("kahoot_3.db")
    questions = manager.select_questions(quizz_id)
    session["questions"] = questions
    session["cur_question"] = 0
    session["true_answer"] = 0
    return redirect(url_for('show_question', quizz_id=quizz_id))

@app.route("/quizzes/<int:quizz_id>/question")
def show_question(quizz_id):
    cur_question = session.get("cur_question", 0)
    questions = session.get("questions", [])
    if cur_question < len(questions):
        question = questions[cur_question]
        manager = SQLManager("kahoot_3.db")
        answers = manager.select_answer(question[0])
        session["answers"] = answers
        return render_template('question_page.html', answers=answers, question=question, quizz_id=quizz_id)
    else:
        return redirect(url_for("result_quizz", quizz_id=quizz_id))


@app.route("/quizzes/<int:quizz_id>/answer", methods=["POST"])
def answer_func(quizz_id):
    answer_id = int(request.form.get("answer"))
    cur_question = session.get("cur_question", 0)
    questions = session.get("questions", [])
    answers = session.get("answers", [])

    correct_answer = answer_id

    if correct_answer:
        session["true_answer"] = session.get("true_answer", 0) + 1

    session["cur_question"] = cur_question + 1

    return redirect(url_for("show_question", quizz_id=quizz_id))

@app.route("/quizzes/<int:quizz_id>/result")
def result_quizz(quizz_id):
    true_answers = session.get("true_answer", 0)
    return render_template("result.html", true_answer=true_answers, quizz_id=quizz_id)

if __name__ == "__main__":
    app.run(debug=True)
