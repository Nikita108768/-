from flask import *
from random import *
from db_scripts import *
import os


Folder = os.getcwd() 

def start_value():
    session["quest_counter"] = 0
    session["quiz_number"] = -1
    session["true_answer"] = 0

def index():
    if request.method == 'GET':
        start_value()
        quiz_names = get_quiz_names()      
        return render_template("start.html",list = quiz_names)
    else:
        session["quiz_number"] = int(request.form.get("quiz_select"))
        return redirect(url_for('quest'))

def quest():
    next_q = get_question_after(session["quest_counter"],session["quiz_number"])
    session["quest_counter"] += 1

    if request.method == "POST":
        _id = request.form.get("q_id")
        print(_id)
        answer = request.form.get("otveti")
        print(check_answer(_id,answer))   
        if check_answer(_id,answer):
            session["true_answer"] += 1

    if next_q == None:
        return redirect(url_for('finish'))

    q_id = next_q[0]
    question = next_q[1]
    answer_list = [ next_q[2],next_q[3],next_q[4],next_q[5]]
    shuffle(answer_list)

    return render_template("test.html", question = question,q_id = q_id, answer_list = answer_list)

def finish():
    all_quiz = get_quiz_names()
    for quiz in all_quiz:
        name = ""
        if quiz[0] == session["quiz_number"]:
            name = quiz[1]
            break

    return render_template ("result.html",
                                          true_answer = session["true_answer"],
                                          name = name,
                                          total_question = session["quest_counter"] -1)

app = Flask(__name__,template_folder = Folder,static_folder = Folder)

app.add_url_rule('/', 'index', index, methods = ["POST","GET"])   
app.add_url_rule('/quest', 'quest', quest, methods =["POST","GET"])   
app.add_url_rule('/finish', 'finish', finish)   

app.config['SECRET_KEY'] = "ГГ_топ"

if __name__ == "__main__":
    app.run(host = "0.0.0.0")