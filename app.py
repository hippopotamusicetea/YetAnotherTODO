"""
TODO Implement Priority Specific Identifiers on Cards
TODO Implement further sql queries such as getting all of priority, searching by due date
TODO Implement due dates, entered dates etc
TODO Fix stupid bottom bar
TODO Add summary at top using bulma level layout
TODO Implement Flet frontend instead of using flask - probably keep flask too though as alternative
https://flet.dev/docs/guides/python/mobile-support#standalone-mobile-package-for-flet-app
TODO Add category filters
TODO Change priorities to integers but render using todos for high/med/low
"""

import os
from threading import Timer

from flask import render_template, request, redirect, flash, url_for

from crud import SQLTasks
from src import create_app
from src.net import start_browser

app = create_app()
sql = SQLTasks(app.config["SQL_DATABASE_NAME"])


def start():
    # The reloader has not yet run - open the browser
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        url = "http://127.0.0.1:5000"
        Timer(2, function=start_browser, args=(url,)).start()

    # Otherwise, continue as normal
    app.run(host="0.0.0.0", port=5000, debug=True)


@app.route("/", methods=["GET", "POST"])
def index():
    rows = sql.get_todo_list()
    if request.method == "POST":
        todo_dict = request.form.to_dict()
        name = request.form["name"]
        sql.create_todo(todo_dict)
        flash({"title": "", "message": f"Todo '{name}' added!"}, "success")
        return redirect("/")
    return render_template("main.html", todos=rows)


@app.route("/update/<int:todo_id>", methods=["POST"])
def update(todo_id):
    print(f"edit request: todo_id = {todo_id}")
    if request.method == "POST":
        return redirect(url_for("index"))
    return redirect(url_for("index"))


@app.route("/complete", methods=["POST"])
def complete():
    if request.method == "POST":
        todo_id = request.form["record-id"]
        name = request.form["name"]
        sql.complete_todo(todo_id)
        flash({"title": "", "message": f"Todo '{name}' completed!"}, "success")
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route("/delete", methods=["POST"])
def delete():
    if request.method == "POST":
        todo_id = request.form["record-id"]
        name = request.form["name"]
        sql.delete_todo(todo_id)
        flash({"title": "", "message": f"Todo '{name}' deleted!"}, "success")
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route("/query", methods=["POST"])
def priority():
    if request.method == "POST":
        if request.form.get("high") == "high":
            rows = sql.query_priority("High")
            return render_template("main.html", todos=rows, filter="High")
        elif request.form.get("medium") == "medium":
            rows = sql.query_priority("Medium")
            return render_template("main.html", todos=rows, filter="Medium")
        elif request.form.get("low") == "low":
            rows = sql.query_priority("Low")
            return render_template("main.html", todos=rows, filter="Low")
        elif request.form.get("all") == "all":
            return redirect(url_for("index"))
    return redirect(url_for("index"))


@app.before_first_request
def check_table():
    sql.create_table()
    sql.load_queries()


if __name__ == "__main__":
    start()
