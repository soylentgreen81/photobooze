#!/usr/bin/env python3
from flask import (
    abort,
    Flask,
    jsonify,
    redirect,
    render_template,
    Response,
    request,
    stream_with_context,
    send_file,
    current_app,
    url_for
    )
from flask_socketio import SocketIO, send
from os import listdir
from os.path import join
from imageutil import create_thumbs
from filelock import Timeout, FileLock
import threading
import asyncio
import eventlet

booze = Flask(__name__, static_folder="static", template_folder="templates")
booze.config.from_object('settings')

socketio = SocketIO(booze, async_mode='eventlet')

countdown_lock = FileLock("countdown.lock", timeout=0) 
eventlet.monkey_patch()

def socket_test():
    for x in range(0, 5):
        socketio.emit('random', {"r":x})

def photo_trigger():
    with countdown_lock.acquire(timeout=1):
        socketio.emit('working', {})
        for t in range(3,-1,-1):
            print(t)
            socketio.emit('timer',{"time": t})
            socketio.sleep(1)
        socketio.emit('processing',{})
        socketio.sleep(0.3)
        image_folder = current_app.config['IMAGE_FOLDER']
        scaled_folder = current_app.config['SCALED_FOLDER']
        thumb_folder = current_app.config['THUMB_FOLDER']
        camera_func = current_app.config['CAMERA_FUNCTION']
        current_app.logger.info('Taking a picture...')
        try:    
            image_name = camera_func(image_folder)
            create_thumbs(image_name, image_folder, scaled_folder, thumb_folder)
            result = format_image_name(image_name)
            socketio.emit('result', result)
            socketio.sleep(0)
            #print(result)
            return result
        except:
            socketio.emit('error','Ein Fehler ist aufgetreten')
            socketio.sleep(0)
            raise

def format_image_name(name):
    return {
            'full': url_for('get_picture',size='full', filename=name),
            'src': url_for('get_picture',size='scaled', filename=name),
            'thumbnail': url_for('get_picture', size='thumb', filename=name),
            'w' : 1920,
            'h' : 1280
    }


@booze.route("/", methods = ["GET"])
def index():
    return render_template("gallery.html")

@booze.route("/gallery")
def gallery():
    return render_template('gallery.html')

@booze.route("/kiosk")
def kiosk():
    return render_template("kiosk.html")

@booze.route("/slideshow")
def slideshow():
    return render_template('slideshow.html')


@booze.route("/api/v1/pictures", methods=["GET"])
def get_pictures():
    imagedir = current_app.config['IMAGE_FOLDER']
    data = [ 
        format_image_name(name)
        for name in sorted(listdir(imagedir))
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
    try:
        result = photo_trigger()
        return jsonify(result)
    except Timeout:
        return abort(409)

@booze.route("/api/v1/trigger", methods=["GET"])
def send_trigger():
    try:
        print("Rest API call")
        result = photo_trigger()
        return "==^..^=="
    except Timeout:
        return "==X..X=="

@socketio.on("connect")
def socket_connect():
    print('client da')

@socketio.on("random")
def socket_trigger(trigger):
    socket_test()

@socketio.on("trigger")
def socket_trigger(trigger):
    print("trigger---socket")
    try:
        photo_trigger()
    except Timeout:
        return abort(409)

############### CAPTIVE PORTAL ##################
@booze.route("/generate_204")
def cp_generate_204():
    # Android
    return Response(
            response=None,
            status=200,
            headers=None,
            mimetype="text/html",
            content_type="text/html",
            direct_passthrough=False
            )

@booze.route("/gen_204")
def cp_gen_204():
    # Android
    return redirect (
            location=url_for("gallery"),
            code=302,
            Response=None
            )

@booze.route("/hotspot-detect.html")
def cp_hotspot_detect():
    # Apple
    return redirect(
            location=url_for("gallery"),
            code=302,
            Response=None
            )

if __name__ == "__main__":
    socketio.run (booze,  host="0.0.0.0", port = 80, debug = False )
