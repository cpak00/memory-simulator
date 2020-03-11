from core.memory import GeneralMemory
from FeFET.statistics.endurance import EnduranceCollector
from FeFET.statistics.energy import EnergyCollector

from util.tool import batchIO_write

import numpy as np

data = np.asarray([[1, 2, 3, 4], [4, 3, 2, 1], [1, 1, 1, 1], [2, 2, 2, 2], [3.0, 3.0, 3.0, 3.0]], dtype=np.float64)
print(data.shape)
np.save('data.npy', data)
io = batchIO_write(data)

print(io.pop().addr)

endurance = EnduranceCollector(bits = 64, rows = 10)
energy = EnergyCollector(bits = 64, rows = 10)

collectors = [endurance, energy]
mm = GeneralMemory(bits = 64, rows = 10, collectors=collectors)
mm.write_float(1, 1.0)
mm.write_float(2, 2.0)
mm.write_float(1, 2.0)
mm.write_float(1, 0.0)
mm.write_float(1, 3.0)
print(mm.read_float(1))

print(endurance.result())
print(energy.result())