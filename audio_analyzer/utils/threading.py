import threading
from functools import reduce
import time

def run_thread_with_lock(lock, func):
    if lock.locked(): return lock

    def target():
        lock.acquire()
        func()
        lock.release()

    threading.Thread(target=target).start()

    return lock

def wait(*locks):
    def locked():
        return reduce(lambda a, b: a or b, (lock.locked() for lock in locks))

    while locked():
        time.sleep(0.1)
