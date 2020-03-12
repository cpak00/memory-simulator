import numpy as np

from core.collector import Collector
from util.tool import hamming_distance
from util.tool import bits2dtype

from config import config

class EnergyCollector(Collector):
    def __init__(self, bits, rows):
        super().__init__()
        self.content_read = 0
        self.content_write = 0
        return

    def collect_write(self, addr, data):
        last_row = int(self.memory.bitline)
        current_row = int(data)
        xor = (last_row ^ current_row) & current_row # 0 -> 1 charge
        self.content_write += hamming_distance(xor)
        return
    
    def collect_read(self, addr):
        last_row = int(self.memory.bitline)
        current_row = int(self.get_data(addr))
        xor = (last_row ^ current_row) & current_row # 0 -> 1 charge
        self.content_read += hamming_distance(xor)
        return

    def result(self):
        return self.content_write * config['write energy'] + self.content_read * config['read energy']

    def clear(self):
        self.cotent = 0
        return

    pass
