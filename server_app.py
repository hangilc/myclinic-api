import datetime
from typing import Dict

from flask import Flask, request, jsonify, send_file
from flask.json import JSONEncoder
import impl
import model
from db_session import Session
from sqlalchemy import create_engine, event
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
import json
import signal
import sys
from werkzeug.serving import run_with_reloader
from werkzeug.debug import DebuggedApplication
import re
import traceback
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
# db_user = os.environ["MYCLINIC_DB_USER"]
# db_pass = os.environ["MYCLINIC_DB_PASS"]
# engine = create_engine(f"mysql+pymysql://{db_user}:{db_pass}@localhost/myclinic?charset=utf8&raw", echo=False)
# Session = sessionmaker(bind=engine)


class AppJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        elif isinstance(obj, datetime.date):
            return obj.strftime("%Y-%m-%d")
        elif hasattr(obj, "to_dict"):
            return obj.to_dict()
        else:
            return super().default(obj)


app.json_encoder = AppJsonEncoder


def cvt_to_int(src):
    return int(src)


def cvt_to_float(src):
    return float(src)


def cvt_to_str(src):
    return src


def cvt_to_date(src):
    if src == "0000-00-00":
        return src
    else:
        return datetime.datetime.strptime(src, "%Y-%m-%d")


def cvt_to_datetime(src):
    return datetime.datetime.strptime(src, "%Y-%m-%d %H:%M:%S")


def confirm_int(value):
    if not isinstance(value, int):
        raise Exception("int expected")
    return value


def confirm_str(value):
    if not isinstance(value, str):
        raise Exception("string expected")
    return value


def confirm_float(value):
    if not isinstance(value, float):
        raise Exception("float expected")
    return value


class ImplementationError(Exception):
    code = 500

    def __init__(self, message):
        self.message = message

    def to_dict(self):
        return {"message": self.message}


def pascal_to_hyphen(name):
    return re.sub(r'(?<!^)(?=[A-Z0-9])', '-', name).lower()


@app.errorhandler(ImplementationError)
def handle_implementation_error(error):
    print("ERROR:", error)
    traceback.print_exc()
    response = jsonify(error.to_dict())
    response.status_code = error.code
    return response


last_practice_log = None
practice_log_clients = []


@app.route("/practice-log")
def ws_practice_log_handler():
    global practice_log_clients
    if request.environ.get("wsgi.websocket"):
        ws = request.environ["wsgi.websocket"]
        practice_log_clients.append(ws)
        print("practice-log-clients (added)", practice_log_clients)
        global last_practice_log
        if not last_practice_log:
            session = Session()
            try:
                last_created = impl.find_todays_last_practice_log(session)
                if last_created:
                    last_practice_log = json.dumps(last_created.to_dict())
            finally:
                session.close()
        while True:
            message = ws.receive()
            if message is None:
                break
            if last_practice_log:
                ws.send(last_practice_log)
        practice_log_clients.remove(ws)
        print("practice-log-clients (removed)", practice_log_clients)
    return ""


last_hotline_log = None
hotline_clients = []


def _hotline_created_log(hotline: model.Hotline) -> Dict:
    return {"kind": "hotline-created", "body": json.dumps({"created": hotline.to_dict()})}


@app.route("/hotline")
def ws_hotline_handler():
    global hotline_clients
    if request.environ.get("wsgi.websocket"):
        ws = request.environ["wsgi.websocket"]
        hotline_clients.append(ws)
        print("hotline-clients (added)", hotline_clients)
        global last_hotline_log
        if not last_hotline_log:
            session = Session()
            try:
                last_created = impl.find_todays_last_hotline(session)
                if last_created:
                    last_hotline_log = _hotline_created_log(last_created)
            finally:
                session.close()
        while True:
            message = ws.receive()
            if message is None:
                break
            if last_hotline_log:
                ws.send(last_hotline_log)
        hotline_clients.remove(ws)
        print("hotline-clients (removed)", hotline_clients)
    return ""


remote_reception_servers = []
remote_reception_clients = []


@app.route("/remote/reception/server")
def ws_remote_reception_server():
    global remote_reception_servers
    global remote_reception_clients
    if request.environ.get("wsgi.websocket"):
        ws = request.environ["wsgi.websocket"]
        print("reception server added")
        remote_reception_servers.append(ws)
        while True:
            message = ws.receive()
            if message is None:
                break
            print("reception server event: " + message)
            for client in remote_reception_clients:
                client.send(message)
        remote_reception_servers.remove(ws)
        print("reception server removed")
        return ""


@app.route("/remote/reception/client")
def ws_remote_reception_client():
    global remote_reception_servers
    global remote_reception_clients
    if request.environ.get("wsgi.websocket"):
        ws = request.environ["wsgi.websocket"]
        print("reception client added")
        remote_reception_clients.append(ws)
        while True:
            message = ws.receive()
            if message is None:
                break
            print("reception client command: " + message)
            for server in remote_reception_servers:
                server.send(message)
        remote_reception_clients.remove(ws)
        print("reception client removed")
        return ""


def run_server():
    global app
    app = DebuggedApplication(app)
    server = WSGIServer(
        ('0.0.0.0', 28080),
        app,
        handler_class=WebSocketHandler
    )
    server.serve_forever()


def datetime_to_sqldatetime(d: datetime.datetime) -> str:
    return d.strftime("%Y-%m-%d %H:%M:%S")


def now_as_sqldatetime() -> str:
    return datetime_to_sqldatetime(datetime.datetime.now())


class MyclinicContext:
    def __init__(self):
        self.new = []
        self.dirty = []
        self.deleted = []
        self.practice_logs = []
        self.hotline_logs = []
        self.is_before_logs = True


@event.listens_for(Session, "after_flush")
def handle_after_flush(session, ctx):
    print("after flush", session.new, session.dirty, session.deleted)
    if session.myclinic.is_before_logs:
        session.myclinic.new.extend(session.new)
        session.myclinic.dirty.extend(session.dirty)
        session.myclinic.deleted.extend(session.deleted)


def enter_myclinic_logs(session):
    print("enter (enter_myclinic_logs)")
    session.myclinic.is_before_logs = False
    for m in session.myclinic.new:
        if type(m).__name__ == "Hotline":
            session.myclinic.hotline_logs.append(_hotline_created_log(m))
        else:
            plog = model.PracticeLog(
                serial_id=None,
                kind=pascal_to_hyphen(type(m).__name__) + "-created",
                created_at=now_as_sqldatetime(),
                body=json.dumps({"created": m.to_dict()})
            )
            session.add(plog)
            session.myclinic.practice_logs.append(plog)
    for m in session.myclinic.dirty:
        plog = model.PracticeLog(
            serial_id=None,
            kind=pascal_to_hyphen(type(m).__name__) + "-updated",
            created_at=now_as_sqldatetime(),
            body=json.dumps({"updated": m.to_dict(), "prev": None})
        )
        session.add(plog)
        session.myclinic.practice_logs.append(plog)
    for m in session.myclinic.deleted:
        plog = model.PracticeLog(
            serial_id=None,
            kind=pascal_to_hyphen(type(m).__name__) + "-deleted",
            created_at=now_as_sqldatetime(),
            body=json.dumps({"deleted": m.to_dict()})
        )
        session.add(plog)
        session.myclinic.practice_logs.append(plog)


def emit_myclinic_logs(session):
    global last_hotline_log
    global last_practice_log
    print("enter handle_myclinic_logs")
    for log in session.myclinic.practice_logs:
        log = json.dumps(log.to_dict())
        print("practice-log", log)
        for c in practice_log_clients:
            c.send(log)
            last_practice_log = log
    for log in session.myclinic.hotline_logs:
        log = json.dumps(log)
        print("hotline-log", log)
        for c in hotline_clients:
            c.send(log)
            last_hotline_log = log


import server_routes


def run():
    server_routes.init_routes()
    signal.signal(signal.SIGINT, lambda signum, _: sys.exit(0))
    run_with_reloader(run_server)
