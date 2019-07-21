from app import app
import controllers

@app.route("/")
def hello():
    return "hello everybody!"

@app.route("/xrates")
def view_rates():
    return controllers.get_all_rates()