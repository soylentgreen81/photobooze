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
from os import listdir
from os.path import join

import threading

booze = Flask(__name__, static_folder="static", template_folder="templates")

imagedir = "/home/alarm/images/"

cameraSemaphore = threading.Semaphore(1)


@booze.route("/", methods = ["GET"])
def index():
    return render_template("index.html")


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
    with cameraSemaphore: 
        camera = gp.check_result(gp.gp_camera_new())
        gp.check_result(gp.gp_camera_init(camera))
        config = gp.check_result(gp.gp_camera_get_config(camera))
        capture_target = gp.check_result(gp.gp_widget_get_child_by_name(config, 'capturetarget'))
        value = gp.check_result(gp.gp_widget_get_choice(capture_target, 1))
        gp.check_result(gp.gp_widget_set_value(capture_target, value))
        gp.check_result(gp.gp_camera_set_config(camera, config))
        file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE))
        target = join(imagedir, file_path.name)
        camera_file = gp.check_result(gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
        gp.check_result(gp.gp_file_save(camera_file, target))
        gp.check_result(gp.gp_camera_exit(camera))
        return jsonify({'pictureurl':'/pictures/' + file_path.name})

if __name__ == "__main__":
    booze.run (  host="0.0.0.0", port = "8000", debug = "True" )
