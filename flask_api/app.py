from flask import Flask, request, jsonify
from prometheus_client import make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
from flask_prometheus_metrics import register_metrics

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "This is my first API call!"


@app.route("/post", methods=["POST"])
def testpost():
    input_json = request.get_json(force=True)
    dictToReturn = {"text": input_json["text"]}
    return jsonify(dictToReturn)


# provide app's version and deploy environment/config name to set a gauge metric
register_metrics(app, app_version="v0.1.2", app_config="staging")

# Plug metrics WSGI app to your main app with dispatcher
dispatcher = DispatcherMiddleware(app.wsgi_app, {"/metrics": make_wsgi_app()})

run_simple(hostname="0.0.0.0", port=5000, application=dispatcher)
