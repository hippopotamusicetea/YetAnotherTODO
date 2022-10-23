import logging

from flask import Flask
from flask_toastr import Toastr

f = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
logging.basicConfig(filename="log.txt", filemode="a", format=f, level=logging.DEBUG)

toastr = Toastr()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "butts"
    app.config["SQL_DATABASE_NAME"] = "todo_sql.db"
    app.config["TOASTR_POSITION_CLASS"] = "toast-top-center"
    app.config["TOASTR_OPACITY"] = False
    toastr.init_app(app)
    return app
