#!/usr/bin/env python3
from flask import (
        abort,
        Flask,
        jsonify,
        render_template,
        Response,
        stream_with_context,
        send_file
        )

import gphoto2 as gp
import os


booze = Flask(__name__, static_folder="static", template_folder="templates")

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
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))
    print('Capturing image')
    file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE))
    print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
    target = os.path.join('/tmp', file_path.name)
    print('Copying image to', target)
    camera_file = gp.check_result(gp.gp_camera_file_get(
            camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
    gp.check_result(gp.gp_file_save(camera_file, target))
    gp.check_result(gp.gp_camera_exit(camera))
    return send_file(target, mimetype='image/jpeg')


if __name__ == "__main__":
    booze.run (  host="0.0.0.0", port = "8000", debug = "True" )
