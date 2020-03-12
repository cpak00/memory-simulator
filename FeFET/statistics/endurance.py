import numpy as np

from core.collector import Collector
from util.tool import hamming_distance
from util.tool import bits2dtype

class EnduranceCollector(Collector):
    def __init__(self, bits, rows):
        super().__init__()
        self.content = np.zeros((rows, bits), dtype=bits2dtype(bits))
        return

    def collect_write(self, addr, data):
        last_row = int(self.get_data(addr))
        current_row = int(data)
        xor = str(bin(last_row ^ current_row))
        for index, value in enumerate(range(2, len(xor))[::-1]):
            if (xor[value] == '1'):
                self.content[addr, index] += 1
        return
    
    def collect_read(self, addr):
        return

    def _get_worst_row(self):
        index = np.argmax(self.content)
        row, bit = divmod(index, self.memory.bits)
        return row

    def result(self):
        return self.content[self._get_worst_row()]

    def clear(self):
        self.content[:] = 0

    pass
