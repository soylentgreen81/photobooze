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

import threading

booze = Flask(__name__, static_folder="static", template_folder="templates")

imagedir = "/home/alarm/images/"

cameraSemaphore = threading.Semaphore(1)

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

@booze.route("/pictures", methods = ["GET"])
def getPictures():
    data = []
    for root, dirs, files in os.walk(imagedir):
        for filename in files:
            data.append({'pictureurl':'/pictures/' + filename})
    return jsonify(data)
    
@booze.route("/pictures/<filename>")
def getPicture(filename):
    image = os.path.join(imagedir, filename)
    return send_file(image, mimetype="image/jpeg")

@booze.route("/pictures", methods=["POST"])
def postPicture():
    with cameraSemaphore:
        camera = gp.check_result(gp.gp_camera_new())
        gp.check_result(gp.gp_camera_init(camera))
        print('Capturing image')
        file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE))
        print('Camera file path: {0}/{1}'.format(file_path.folder, file_path.name))
        target = os.path.join(imagedir, file_path.name)
        print('Copying image to', target)
        camera_file = gp.check_result(gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
        gp.check_result(gp.gp_file_save(camera_file, target))
        gp.check_result(gp.gp_camera_exit(camera))
        return jsonify({'pictureurl':'/pictures/' + file_path.name})


if __name__ == "__main__":
    booze.run (  host="0.0.0.0", port = "8000", debug = "True" )
