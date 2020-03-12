from core.coder import Coder
from util.tool import cycle_right_shifting

import numpy as np

class WeightBasedCompareCoder(Coder):
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

            cost_energy = self.mm.parser.hamming(bitline ^ current_row)
            if cost_energy <= (self.mm.bits / 4):
                self.shifting_content[addr] = self.shifting
                return current_row
            else:
                last_raw = int(self.mm.read_raw(addr))
                piecewise = [4] * (self.mm.bits // 4)

                weight_current = np.argmax(self.weight(current_row, piecewise))
                weight_last = np.argmax(self.weight(last_raw, piecewise))

                self.shifting = weight_last * 4
                self.shifting_content[addr] = self.shifting
                current_row = self.mm.parser.bcs_r(current_row, (weight_last - weight_current) * 4)
                return current_row
            

    def decode(self, addr, raw):
        shifting = self.shifting_content[addr]
        return self.mm.parser.bcs_l(raw, shifting)
        return raw

    def weight(self, data, piecewise):
        result = [0] * len(piecewise)
        l = self.mm.parser.int2bitsarray(data)
        piecewise = np.asarray([0] + piecewise, dtype=int).cumsum()
        for i in range(1, len(piecewise)):
            result[i-1] = np.sum(l[piecewise[i-1]:piecewise[i]])

        return result
    
    pass