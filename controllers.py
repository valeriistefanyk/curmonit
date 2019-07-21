from flask import render_template, make_response

from models import ExRate

def get_all_rates():
    try:
        xrates = ExRate.select()
        return render_template("xrates.html", xrates = xrates)
    except Exception as ex:
        return make_response(str(ex), 500)