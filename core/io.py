import numpy as np

from core.operation import SingleOperation, TYPE


class IO(object):
    '''
    IO module to control write and read
    '''
    def __init__(self):
        self.content = []
        self.cursor = 0
        return

    
    def load_npy(self, filename):
        self.content = np.load(filename)

    def save_npy(self, filename):
        np.save(filename, self.content)


    def restart_io(self):
        self.cursor = 0


    def pop(self):
        if (self.cursor >= len(self.content)):
            return None
        
        single_io = self.content[self.cursor] # get a i/o operation
        self.cursor += 1
        op = SingleOperation(single_io)

        return op

    
    def push_write(self, addr, data):
        self.content.append([TYPE.write, addr, data])
        return


    def push_read(self, addr):
        self.content.append([TYPE.read, addr, None])
        return
        
    pass