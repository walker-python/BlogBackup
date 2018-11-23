__author__ = 'apple'

import Queue

def get_queue():
    dicts = globals()
    return dicts["queue"]

def init_queue():
    gQueue = Queue.Queue(0)
    dicts = globals()
    dicts["queue"] = gQueue