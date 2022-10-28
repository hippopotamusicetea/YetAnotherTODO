
import logging

from flask import Flask
from flask_toastr import Toastr
from flask_cors import CORS

f = "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
logging.basicConfig(filename="log.txt", filemode="a", format=f, level=logging.DEBUG)

toastr = Toastr()


# if os.os.getenv("DB") == "sql":


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "a_really_secret_key"
    app.config["SQL_DATABASE_NAME"] = "todo_sql.db"
    app.config["TOASTR_POSITION_CLASS"] = "toast-top-center"
    app.config["TOASTR_OPACITY"] = False
    with app.app_context():
        toastr.init_app(app)
        CORS(app)
        return app
