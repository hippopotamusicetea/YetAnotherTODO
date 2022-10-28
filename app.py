"""

TODO Implement Flet frontend instead of using flask - probably keep flask too though as alternative
https://flet.dev/docs/guides/python/mobile-support#standalone-mobile-package-for-flet-app
TODO Change priorities to integers but render using todos for high/med/low
TODO Implement sorting newest/oldest/alphabetically
TODO Implement the ADHD style daily/monthly/yearly style of todo list
Handle sql/sqla/peeww via env['DB']
Remember to add production server and set env

"""

import os
from threading import Timer
import datetime
from flask import render_template, request, redirect, flash, url_for, g

from src import create_app
from src.net import start_browser
from src.crud import SQLTasks
from src.db import get_db

app = create_app()
sql = SQLTasks()
categories = ["Work", "Home", "Other"]
priorities = ["High", "Medium", "Low"]


def start():
    # The reloader has not yet run - open the browser
    if not os.environ.get("WERKZEUG_RUN_MAIN"):
        url = "http://127.0.0.1:5000"
        Timer(1, function=start_browser, args=(url,)).start()

    # Otherwise, continue as normal
    app.run(host="0.0.0.0", port=5000, debug=True)


def header_items(conn):
    time_sum = sql.get_times(conn)[0]
    todo_total = sql.get_todo_num(conn)[0]
    return todo_total, time_sum


def get_task_children(conn, todo_id):
    rows = sql.get_children(conn, todo_id)
    child_list = []
    for r in rows:
        print(f"child row data:")
        for b in r:
            print(b)
        child = {
            "id": r["id"],
            "subtask": r["subtask"],
            "completion_time": r["completion_time"],
            "complete": r["complete"],
        }
        child_list.append(child)
    return child_list


def get_child_dict(conn, rows):
    child_dict = {}
    for r in rows:
        todo_id = r["id"]
        child_dict[todo_id] = get_task_children(conn, todo_id)
        return child_dict


@app.route("/", methods=["GET"])
def index():
    conn = get_db()
    with conn as c:
        rows = sql.get_todo_list(c)
        child_dict = get_child_dict(c, rows)
        todo_total, time_sum = header_items(c)
        return render_template(
            "main.html",
            todos=rows,
            categories=categories,
            todo_total=todo_total,
            time=time_sum,
            child_dict=child_dict,
        )


@app.route("/task", methods=["POST"])
def add_task():
    conn = get_db()
    if request.method == "POST":
        todo_dict = request.form.to_dict()
        name = request.form["name"]
        sql.create_todo(conn, todo_dict)
        flash({"title": "", "message": f"Todo '{name}' added!"}, "success")
        return redirect(url_for("index"))


@app.route("/subtask", methods=["POST"])
def add_subtask():
    conn = get_db()
    if request.method == "POST":
        subtask_dict = request.form.to_dict()
        sql.create_subtask(conn, subtask_dict)
        flash(
            {"title": "", "message": f"Subtask added to {subtask_dict['name']}"},
            "success",
        )
        return redirect(url_for("index"))
    return redirect(url_for("index"))


@app.route("/update", methods=["POST"])
def update():
    if request.method == "POST":
        return redirect(url_for("index"))
    return redirect(url_for("index"))


@app.route("/complete", methods=["POST"])
def complete():
    if request.method == "POST":
        conn = get_db()
        todo_id = request.form["record-id"]
        name = request.form["name"]
        sql.complete_todo(conn, todo_id)
        flash({"title": "", "message": f"Todo '{name}' completed!"}, "success")
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route("/delete", methods=["POST"])
def delete():
    if request.method == "POST":
        conn = get_db()
        todo_id = request.form["record-id"]
        name = request.form["name"]
        sql.delete_todo(conn, todo_id)
        flash({"title": "", "message": f"Todo '{name}' deleted!"}, "success")
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route("/subtask_complete", methods=["POST"])
def subtask_complete():
    if request.method == "POST":
        conn = get_db()
        subtask_id = request.form["subtask-id"]
        for x in request.form:
            print(x)
        sql.complete_subtask(conn, subtask_id)
        flash({"title": "", "message": f"Subtask completed!"}, "success")
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route("/subtask_delete", methods=["POST"])
def subtask_delete():
    if request.method == "POST":
        conn = get_db()
        subtask_id = request.form["subtask-id"]
        sql.delete_subtask(conn, subtask_id)
        flash({"title": "", "message": f"Subtask deleted!"}, "success")
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))


@app.route("/query", methods=["POST"])
def query():
    if request.method == "POST":
        conn = get_db()
        todo_total, time_sum = header_items(conn)
        if request.form.get("high") == "high":
            rows = sql.query_priority(conn, "High")
            child_dict = get_child_dict(conn, rows)
            return render_template(
                "main.html",
                todos=rows,
                filter="High",
                categories=categories,
                todo_total=todo_total,
                time=time_sum,
                child_dict=child_dict
            )
        elif request.form.get("medium") == "medium":
            rows = sql.query_priority(conn, "Medium")
            child_dict = get_child_dict(conn, rows)
            return render_template(
                "main.html",
                todos=rows,
                filter="Medium",
                categories=categories,
                todo_total=todo_total,
                time=time_sum,
                child_dict=child_dict
            )
        elif request.form.get("low") == "low":
            rows = sql.query_priority(conn, "Low")
            child_dict = get_child_dict(conn, rows)
            return render_template(
                "main.html",
                todos=rows,
                filter="Low",
                categories=categories,
                todo_total=todo_total,
                time=time_sum,
                child_dict=child_dict
            )
        elif request.form.get("all") == "all":
            return redirect(url_for("index"))
        elif request.form.get("over-week") == "over-week":
            rows = sql.get_overdue_week(conn)
            child_dict = get_child_dict(conn, rows)
            return render_template(
                "main.html",
                todos=rows,
                filter="On List Over One Week",
                categories=categories,
                todo_total=todo_total,
                time=time_sum,
                child_dict=child_dict
            )
        elif request.form.get("due-week") == "due-week":
            rows = sql.get_due_in_week(conn)
            child_dict = get_child_dict(conn, rows)
            return render_template(
                "main.html",
                todos=rows,
                filter="Due in next week",
                categories=categories,
                todo_total=todo_total,
                time=time_sum,
                child_dict=child_dict
            )
        # convert others to similar pattern
        elif request.form.get("category-query") in categories:
            category = request.form["category-query"]
            rows = sql.get_category(conn, category)
            child_dict = get_child_dict(conn, rows)
            return render_template(
                "main.html",
                todos=rows,
                filter=category,
                categories=categories,
                todo_total=todo_total,
                time=time_sum,
                child_dict=child_dict
            )
        elif request.form.get("complete") == "1":
            current_status = request.form["complete"]
            print(f"current {current_status}")
            rows = sql.get_status(conn, current_status)
            child_dict = get_child_dict(conn, rows)
            return render_template(
                "main.html",
                todos=rows,
                filter="Complete",
                categories=categories,
                todo_total=todo_total,
                time=time_sum,
                child_dict=child_dict
            )
        elif request.form.get("incomplete") == "0":
            current_status = request.form["incomplete"]
            rows = sql.get_status(conn, current_status)
            child_dict = get_child_dict(conn, rows)
            return render_template(
                "main.html",
                todos=rows,
                filter="Incomplete",
                categories=categories,
                todo_total=todo_total,
                time=time_sum,
                child_dict=child_dict
            )

    return redirect(url_for("index"))


@app.before_first_request
def check_table():
    conn = get_db()
    sql.create_table(conn)


@app.template_filter('formatdatetime')
def format_datetime(value):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    f = "%d/%m/%Y"

    if value is None:
        return ""
    else:
        d = datetime.datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
    return d.strftime(f)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


if __name__ == "__main__":
    start()
