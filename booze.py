#!/usr/bin/env python3
from flask import (
        abort,
        Flask,
        jsonify,
        render_template,
        Response,
        stream_with_context
        )

import gphoto2 as gp


booze = Flask(__name__)

def preview_stream():
    # init gphoto2 here
    gphoto = "Hallo Welt"
    while True:
        yield gphoto


@booze.route("/", methods = ["GET"])
def index():
    return render_template("index.html")

@booze.route("/preview", methods = ["GET"])
def preview():
    return abort(404)
    return Response(response=stream_with_context(preview_stream()), mimetype="text/plain")

@booze.route("/click")
def click():
    return abort(404)




if __name__ == "__main__":
    booze.run ( host = "localhost", port = "8000", debug = "True" )
