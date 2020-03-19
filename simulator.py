from core.memory import GeneralMemory
from core.io import IO
from FeFET.statistics.endurance import EnduranceCollector
from FeFET.statistics.energy import EnergyCollector

from core.coder import Coder
from optimization.HammingCompareBasedCoder import HammingCompareBasedCoder
from optimization.OrderedCompareBasedCoder import OrderedCompareBasedCoder
from optimization.WeightBasedCompareCoder import WeightBasedCompareCoder
from optimization.AdvancedOrderedCoder import AdvancedOrderedCoder

from util.tool import batchIO_write

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

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

    def reset(self):
        self.io.restart_io()
        self.mm.clear()
        self.endurance.clear()
        self.energy.clear()

    def result(self):
        results = {"endurance": self.endurance.result(),
                "energy": self.energy.result()}
        return results
    
    pass


if __name__ == '__main__':
    sim = Simulator(32, 6000)
    sim.load_batch_write('data.npy')
    
    '''
    sim.mm.bind_coder(Coder())
    sim.reset()
    sim.run()
    print('=== completed code===')
    plt.figure()
    sns.heatmap(sim.endurance.content, cmap=plt.cm.viridis)
    plt.title('energy: %s, endurance: %s' % (sim.result()['energy'], max(sim.result()['endurance'])))
    plt.savefig('NoneCoder.png')
    
    sim.mm.bind_coder(HammingCompareBasedCoder(4, 1000))
    sim.reset()
    sim.run()
    print('=== completed hamming===')
    plt.figure()
    sns.heatmap(sim.endurance.content, cmap=plt.cm.viridis)
    plt.title('energy: %s, endurance: %s' % (sim.result()['energy'], max(sim.result()['endurance'])))
    plt.savefig('HammingCompareBasedCoder.png')
    '''
    '''
    sim.mm.bind_coder(OrderedCompareBasedCoder())
    sim.reset()
    sim.run()
    print('=== completed code===')
    plt.figure()
    sns.heatmap(sim.endurance.content, cmap=plt.cm.viridis)
    plt.title('energy: %s, endurance: %s' % (sim.result()['energy'], max(sim.result()['endurance'])))
    plt.savefig('OrderedCompareBasedCoder.png')
    

    sim.mm.bind_coder(WeightBasedCompareCoder())
    sim.reset()
    sim.run()
    print('=== completed code===')
    plt.figure()
    sns.heatmap(sim.endurance.content, cmap=plt.cm.viridis)
    plt.title('energy: %s, endurance: %s' % (sim.result()['energy'], max(sim.result()['endurance'])))
    plt.savefig('WeightBasedCompareCoder.png')
    '''
    sim.mm.bind_coder(AdvancedOrderedCoder())
    sim.reset()
    sim.run()
    print('=== completed code===')
    plt.figure()
    sns.heatmap(sim.endurance.content, cmap=plt.cm.viridis)
    plt.title('energy: %s, endurance: %s' % (sim.result()['energy'], max(sim.result()['endurance'])))
    plt.savefig('AdvancedOrderedCoder.png')