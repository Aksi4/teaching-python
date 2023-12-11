from flask import request, render_template
from app.misc.data import skills


from . import misc_bp

@misc_bp.route('/appeal', methods=["GET", "POST"])
def appeal():
    if request.method == "POST":
        gmail = request.form.get("gmail")
        message = request.form.get("message")
    else:
        gmail = request.args.get("gmail")
        message = request.args.get("message")

    return render_template("appeal.html", gmail=gmail, message=message)



@misc_bp.route('/skill/')
@misc_bp.route('/skill/<int:idx>')
def skill(idx=None):
    if idx is not None:
        skill = skills[idx]
        return render_template("skill.html", skill=skill, skills=skills, idx=idx)
    else:
        return render_template("skills.html", skills=skills)








