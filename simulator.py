from core.memory import GeneralMemory
from core.io import IO
from FeFET.statistics.endurance import EnduranceCollector
from FeFET.statistics.energy import EnergyCollector

from util.tool import batchIO_write

import numpy as np

class Simulator(object):
    def __init__(self, bits, rows):
        # collector
        self.endurance = EnduranceCollector(bits = bits, rows = rows)
        self.energy = EnergyCollector(bits = bits, rows = rows)
        collectors = [self.endurance, self.energy]
        self.mm = GeneralMemory(bits, rows, collectors)
        self.io = IO()
        return

    def load_batch_write(self, filename):
        raw_data = np.load(filename)
        self.io = batchIO_write(raw_data)
        return

    def run(self):
        while (True):
            op = self.io.pop()
            if (op is None):
                break

            self.mm.write_float(op.addr, op.data)

    def result(self):
        results = {"endurance": self.endurance.result(),
                "energy": self.energy.result()}
        return results
    pass


if __name__ == '__main__':
    sim = Simulator(64, 10)
    sim.load_batch_write('data.npy')
    sim.run()
    print(sim.result())

    print('=== completed ===')