from camera import take_picture

from filelock import Timeout, FileLock

def _test():
    lock = FileLock('test.lock', timeout=0)
    with lock:
        print(take_picture('/tmp'))


def test():
    try:
        _test()
    except Timeout:
        print('no no no')


test()
