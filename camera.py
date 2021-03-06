from datetime import datetime
import gphoto2 as gp
from os.path import join
from filelock import Timeout, FileLock
import asyncio

def take_picture(imagedir): 
    camera = gp.check_result(gp.gp_camera_new())
    gp.check_result(gp.gp_camera_init(camera))
    config = gp.check_result(gp.gp_camera_get_config(camera))
    capture_target = gp.check_result(gp.gp_widget_get_child_by_name(config, 'capturetarget'))
    value = gp.check_result(gp.gp_widget_get_choice(capture_target, 1))
    gp.check_result(gp.gp_widget_set_value(capture_target, value))
    gp.check_result(gp.gp_camera_set_config(camera, config))
    file_path = gp.check_result(gp.gp_camera_capture(camera, gp.GP_CAPTURE_IMAGE))
    file_name = datetime.now().strftime('%y%m%d-%H%M%S-%f') + file_path.name
    target = join(imagedir, file_name)
    camera_file = gp.check_result(gp.gp_camera_file_get(camera, file_path.folder, file_path.name, gp.GP_FILE_TYPE_NORMAL))
    gp.check_result(gp.gp_file_save(camera_file, target))
    gp.check_result(gp.gp_camera_exit(camera))
    return file_name

async def take_picture_async(imagedir):
    executor = asyncio.get_event_loop().run_in_executor
    future = executor(None, take_picture, imagedir)
    await future
    return future.result()
