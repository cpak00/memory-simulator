import numpy as np
from core.parser import DataParser
from core.collector import Collector
from core.coder import Coder
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
        self.rows = rows
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
        # default coder
        self.coder = Coder()
        return

    def bind_coder(self, coder):
        self.coder = coder
        self.coder.bind(self)
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

    def write(self, addr, data):
        data = self.coder.encode(addr, data);
        self.write_raw(addr, data)

    def write_float(self, addr, data):
        '''
        write_float(addr, data): write data -> memory[addr]
        '''
        self.write(addr, self.parser.float2hex(data))

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

    def read(self, addr):
        data = self.read_raw(addr)
        return self.coder.decode(addr, data)

    def read_float(self, addr):
        '''
        read_float(addr): read addr -> data
        '''
        return self.parser.hex2float(self.read(addr))

    def clear(self):
        self.content[:] = 0
        return

    pass
