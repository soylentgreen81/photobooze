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

from os import listdir
from os.path import join

booze = Flask(__name__, static_folder="static", template_folder="templates")
booze.config.from_object('settings')


@booze.route("/", methods = ["GET"])
def index():
    return render_template("index.html")


@booze.route("/api/v1/pictures", methods=["GET"])
def get_pictures():
    imagedir = current_app.config['IMAGE_FOLDER']
    data = [ 
        {'pictureurl': url_for('get_picture', filename= p)}
        for p in listdir(imagedir)
    ]
    return jsonify(data)


@booze.route("/api/v1/pictures/<filename>")
def get_picture(filename):
    image = join(current_app.config['IMAGE_FOLDER'], filename)
    return send_file(image, mimetype="image/jpeg")


@booze.route("/api/v1/pictures", methods=["POST"])
def post_picture():
    imagedir = current_app.config['IMAGE_FOLDER']
    camera_func = current_app.config['CAMERA_FUNCTION']
    image_name = camera_func(imagedir)
    return jsonify({'pictureurl': url_for('get_picture', filename=image_name)})


if __name__ == "__main__":
    booze.run (  host="0.0.0.0", port = "8000", debug = "True" )
