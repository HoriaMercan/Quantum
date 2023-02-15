'''
    Thisd is a simple circuit that performs remainder division
    
    The circuit contains 5 registers:
        - n and d, each with bits bits
        - q and r each with bits bits (which are initially all 0)
        - anc with 3 bits (used in computation, not important)
'''

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, AncillaRegister
import matplotlib.pyplot as plt
from math import pi
import gates

from qiskit_ibm_runtime import Estimator, Session
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.circuit.random import random_circuit

from qiskit.primitives import Sampler

sampler = Sampler()

regs = gates.RegisterUtils
ds = gates.DefiniteStates
'''
    If you want your own api key, register at:
    https://quantum-computing.ibm.com and run
    QiskitRuntimeService.save_account(channel="ibm_quantum", token="API_TOKEN")
    or use the commented line (once), with my token
'''
# QiskitRuntimeService.save_account(channel="ibm_quantum", token="1df855214acba333a1a1b8475d93d571dce92f0104fee8e25d3616afe112e342ed32f0f4a4517f2e893ce574eb265f007e9dd5b86cbb49a8217912a0eb582de2")


service = QiskitRuntimeService()

'''
    Change it to whatever suits your needs
'''
bits = 4

'''
    Declare Quantum Registers
    and classical register used for measurement
'''
n = QuantumRegister(bits)
d = QuantumRegister(bits)
r = QuantumRegister(bits)
q = QuantumRegister(bits)
anc = QuantumRegister(3)

cl = ClassicalRegister(bits)


'''
    Remainder theorem
    |n\ |d\ |0\ |0\ |000\ => |n\ |d\ |n%d\ |n/d\ |***\ 
'''
rth = gates.QFTArithmetic.QFTRemainderTheorem(bits)

circuit = QuantumCircuit(n,d,r,q,anc,cl)

gates.init_reg(circuit, n, ds.binary(9, bits=bits))
gates.init_reg(circuit, d, ds.binary(3, bits=bits))

circuit.append(rth, regs.join(n,d,r,q,anc))
#circuit.append(ipadd.inverse(), regs.join(d, r, anc[2:]))
#circuit.append(leftshift, regs.join(r, anc[0:2]))
#circuit.append(leftshift, regs.join(r, anc[0:2]))


'''
    Measure the r: remainder-register
    You can also measure q: quotient-register with: 
    |-------
    | ....
    |  circuit.measure(r[i], cl[i])
    |
'''
circuit.barrier()
for i in range(bits):
    circuit.measure(q[i], cl[i])



'''
    Run sampler and output results
'''
job = sampler.run(circuit)
result = job.result()

circuit.draw("mpl", filename='pics/rth.qg.png')
print(f">>> Quasi-distribution: {result.quasi_dists[0]}")

'''
For plotting:
    D = result.quasi_dists[0]

    plt.bar(range(len(D)), list(D.values()), align='center')
    plt.xticks(range(len(D)), list(D.keys()))
    # # for python 2.x:
    # plt.bar(range(len(D)), D.values(), align='center')  # python 2.x
    # plt.xticks(range(len(D)), D.keys())  # in python 2.x

    plt.show()
'''