import numpy as np

from core.collector import Collector
from util.tool import hamming_distance
from util.tool import bits2dtype

class EnergyCollector(Collector):
    def __init__(self, bits, rows):
        super().__init__()
        self.content = 0
        return

    def collect_write(self, addr, data):
        last_row = int(self.memory.bitline)
        current_row = int(data)
        xor = (last_row ^ current_row) & current_row # 0 -> 1 charge
        self.content += hamming_distance(xor)
        return
    
    def collect_read(self, addr):
        last_row = int(self.memory.bitline)
        current_row = int(self.get_data(addr))
        xor = (last_row ^ current_row) & current_row # 0 -> 1 charge
        self.content += hamming_distance(xor)

    def result(self):
        return self.content
    pass
