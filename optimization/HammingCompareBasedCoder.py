from core.coder import Coder
from util.tool import cycle_right_shifting

import numpy as np

class HammingCompareBasedCoder(Coder):
    def __init__(self, shift_per_write=4, compare_time=10):
        self.shifting = 0
        self.compare_flag = 0
        self.shift_per_write = shift_per_write
        self.compare_time = compare_time
        self.shifting_content = np.zeros((0), dtype=int)
        return

    def bind(self, mm):
        super().bind(mm)
        self.shifting_content = np.zeros(self.mm.rows, dtype=int)

    def encode(self, addr, raw):
        current_row = int(self.mm.parser.bcs_r(raw, self.shifting))
        if (self.compare_flag < self.compare_time):
            self.compare_flag += 1
            self.shifting_content[addr] = self.shifting
            return current_row
        else:
            self.compare_flag = 0

            bitline = int(self.mm.bitline)
            last_raw = int(self.mm.read_raw(addr))        
            compare_row = int(self.mm.parser.bcs_r(current_row, self.shift_per_write))
            cost_current = self.cost(current_row, bitline, last_raw)
            cost_compare = self.cost(compare_row, bitline, last_raw)
            if cost_current <= cost_compare:
                raw = current_row
            else:
                self.shifting = (self.shifting + self.shift_per_write) % 32
                raw = compare_row

            self.shifting_content[addr] = self.shifting
            return raw

    def decode(self, addr, raw):
        shifting = self.shifting_content[addr]
        return self.mm.parser.bcs_l(raw, shifting)
        return raw

    def cost(self, data, bitline, last_row):
        '''
        calculate cost formula
        '''
        return self.mm.parser.hamming(data ^ last_row)
    
    pass