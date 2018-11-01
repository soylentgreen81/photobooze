import gphoto2 as gp
from os.path import join
from filelock import Timeout, FileLock


def take_picture(imagedir): 
    camera_lock = FileLock("camera.lock", timeout=15)
    with camera_lock:
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
        return file_path.name
