import threading

def run_thread_with_lock(lock, func):
    if lock.locked(): return lock

    def target():
        lock.acquire()
        func()
        lock.release()

    threading.Thread(target=target).start()

    return lock
