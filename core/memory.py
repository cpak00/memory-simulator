import numpy as np
from core.parser import DataParser
from core.collector import Collector
from util.tool import bits2dtype

from config import config

class GeneralMemory(object):
    '''
    GeneralMemory(bits = n, rows = m) \n
    number of bits is how many bits in a row \n
    number of rows is how many rows in this memory \n
    total n * m bits
    '''
    def __init__(self, bits, rows, collectors = []):
        # create content of memory
        self.dtype = bits2dtype(bits)

        self.content = np.zeros(rows, dtype=self.dtype)
        self.bits = bits
        # charge bitline
        self.bitline = 0
        # bind data parser with memory
        self.parser = DataParser(bits)
        # bind data collector with memory
        self.collectors = collectors
        for collector in collectors:
            if isinstance(collector, Collector):
                collector.bind(self)
            else:
                raise Exception('collector must inherited from core.Collector')
        return

    def write_raw(self, addr, data):
        '''
        write_raw(addr, data): write data -> memory[addr]
        '''
        for c in self.collectors:
            c.collect_write(addr, data)
        self.bitline = data
        self.content[addr] = data

        if ('write_log' in config and config['write_log']):
            print('write with data: %s => addr: %s' % (hex(data), addr))
        return

    def write_float(self, addr, data):
        '''
        write_float(addr, data): write data -> memory[addr]
        '''
        self.write_raw(addr, self.parser.float2hex(data))

    def read_raw(self, addr):
        '''
        read_raw(addr): read addr -> data
        '''
        for c in self.collectors:
            c.collect_read(addr)
        data = self.content[addr]
        self.bitline = data

        if ('read_log' in config and config['read_log']):
            print('read from addr: %s => data: %s' % (addr, hex(data)))
        return data

    def read_float(self, addr):
        '''
        read_float(addr): read addr -> data
        '''
        return self.parser.hex2float(self.read_raw(addr))

    pass
