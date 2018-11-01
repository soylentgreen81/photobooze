#!/usr/bin/env python3
from flask import (
        abort,
        Flask,
        jsonify,
        render_template,
        Response,
        stream_with_context,
        send_file,
        current_app,
        url_for
        )

import gphoto2 as gp
from os import listdir
from os.path import join

from filelock import Timeout, FileLock

booze = Flask(__name__, static_folder="static", template_folder="templates")
booze.config.from_object('settings')

@booze.route("/", methods = ["GET"])
def index():
    return render_template("index.html")


@booze.route("/api/v1/pictures", methods = ["GET"])
def getPictures():
    imagedir = current_app.config['IMAGE_FOLDER']
    data = [ 
        {'pictureurl': url_for('getPicture',filename= p)} 
        for p in listdir(imagedir)
    ]
    return jsonify(data)
    
@booze.route("/api/v1/pictures/<filename>")
def getPicture(filename):
    image = join(current_app.config['IMAGE_FOLDER'], filename)
    return send_file(image, mimetype="image/jpeg")



@booze.route("/api/v1/pictures", methods=["POST"])
def postPicture():
    imagedir = current_app.config['IMAGE_FOLDER']
    cameraLock = FileLock("camera.lock", timeout=15)
    with cameraLock: 
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
        return jsonify({'pictureurl': url_for('getPicture',filename=file_path.name)})

if __name__ == "__main__":
    booze.run (  host="0.0.0.0", port = "8000", debug = "True" )
