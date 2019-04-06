#!/usr/bin/env python3
from flask import (
    abort,
    Flask,
    jsonify,
    render_template,
    Response,
    request,
    stream_with_context,
    send_file,
    current_app,
    url_for
    )

from os import listdir
from os.path import join
from imageutil import create_thumbs


booze = Flask(__name__, static_folder="static", template_folder="templates")
booze.config.from_object('settings')

def format_image_name(name):
    return {
            'full': url_for('get_picture',size='full', filename=name),
            'scaled': url_for('get_picture',size='scaled', filename=name),
            'thumb': url_for('get_picture', size='thumb', filename=name)
    }


@booze.route("/", methods = ["GET"])
def index():
    return render_template("index.html")


@booze.route("/api/v1/pictures", methods=["GET"])
def get_pictures():
    imagedir = current_app.config['IMAGE_FOLDER']
    data = [ 
        format_image_name(name)
        for name in listdir(imagedir)
    ]
    return jsonify(data)


@booze.route("/api/v1/pictures/<size>/<filename>")
def get_picture(size, filename):
    if size == 'thumb':
        folder = current_app.config['THUMB_FOLDER']
    elif size == 'scaled':
        folder = current_app.config['SCALED_FOLDER']
    else:
        folder = current_app.config['IMAGE_FOLDER'] 
    image = join(folder, filename)
    return send_file(image, mimetype="image/jpeg")


@booze.route("/api/v1/pictures", methods=["POST"])
def post_picture():
    image_folder = current_app.config['IMAGE_FOLDER']
    scaled_folder = current_app.config['SCALED_FOLDER']
    thumb_folder = current_app.config['THUMB_FOLDER']
    camera_func = current_app.config['CAMERA_FUNCTION']
    current_app.logger.info('Taking a picture...')
    image_name = camera_func(image_folder)
    create_thumbs(image_name, image_folder, scaled_folder, thumb_folder)   
    return jsonify(format_image_name(image_name))


if __name__ == "__main__":
    booze.run (  host="0.0.0.0", port = "8000", debug = "True" )
