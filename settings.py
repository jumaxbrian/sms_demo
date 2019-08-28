#defines all global variables
import collections

def init():
    global messages_queue
    messages_queue = collections.deque()

    global messages_dict
    messages_dict = dict()