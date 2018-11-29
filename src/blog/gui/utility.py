__author__ = 'apple'

import queue

def get_queue():
    dicts = globals()
    return dicts["queue"]

def init_queue():
    gQueue = queue.Queue(0)
    dicts = globals()
    dicts["queue"] = gQueue