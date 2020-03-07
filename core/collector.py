from abc import ABCMeta, abstractclassmethod
class Collector(object):
    '''
    Base class of statistics collector
    '''
    __metaclass__ = ABCMeta

    def __init__(self):
        self.memory = None
        return

    def bind(self, mm):
        '''
        bind with memory
        '''
        self.memory = mm
        return

    def get_data(self, addr):
        '''
        get data from memory without collect
        '''
        return self.memory.content[addr]
    
    @abstractclassmethod
    def collect_write(cls, addr, data):
        return

    @abstractclassmethod
    def collect_read(cls, addr):
        return
    pass
