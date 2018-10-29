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

import gphoto2cffi as gp
from os import listdir
from os.path import join

import threading

booze = Flask(__name__, static_folder="static", template_folder="templates")

imagedir = "/home/alarm/images/"

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
    data = [ 
            {'pictureurl': '/pictures/'+p} 
            for p in listdir(imagedir)
    ]
    return jsonify(data)
    
@booze.route("/pictures/<filename>")
def getPicture(filename):
    image = join(imagedir, filename)
    return send_file(image, mimetype="image/jpeg")

@booze.route("/pictures", methods=["POST"])
def postPicture():
    cam = gp.Camera()
    image_data = cam.capture(to_camera_storage = False)
    # to_camera_storage = True gibt nen "File-Object"???
    # sonst bytes
    filename = image_data.name # Blind dem Quelltext von gphoto2-cffi entnommen
    with open(join(imagedir, filename), 'wb') as f:
        f.write(image_data.get_data()) # Blind dem Quelltext von gphoto2-cffi entnommen
    return jsonify({'pictureurl':'/pictures/' + filename})

if __name__ == "__main__":
    booze.run (  host="0.0.0.0", port = "8000", debug = "True" )
