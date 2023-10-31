from flask import Flask, request, render_template, redirect, url_for
from data import skills
import datetime
import platform

app = Flask(__name__)

@app.context_processor
def inject_global_data():
    global_data = {
        'u_agent': request.headers.get('User-Agent'),
        'OS': platform.system(),
        'time': datetime.datetime.now()
    }
    return global_data
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main")
def main():
    return render_template("main.html")


@app.route('/skill/')
@app.route('/skill/<int:idx>')
def skill(idx=None):
    if idx is not None:
        skill = skills[idx]
        return render_template("skill.html", skill=skill, skills=skills, idx=idx)
    else:
        return render_template("skills.html", skills=skills)



@app.route('/form', methods=["GET", "POST"])
def form():
    if request.method == "POST":
        gmail = request.form.get("gmail")
        message = request.form.get("message")

    else:
        gmail = request.args.get("gmail")
        message = request.args.get("message")

    return render_template("form.html", gmail=gmail, message=message)


if __name__ == '__main__':
    app.run(debug=True)