import numpy as np

class TYPE(object):
    write = 1
    read = 0
    pass

class SingleOperation(object):
    def __init__(self, single_io):
        self.ctrl = single_io[0]
        self.addr = single_io[1]
        self.data = single_io[2]
        return
    pass