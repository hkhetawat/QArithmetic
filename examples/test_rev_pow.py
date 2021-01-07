# Import the Qiskit SDK
from numpy.lib.function_base import copy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from qiskit.providers.aer import QasmSimulator
from QArithmetic import full_qr, power
from copy import copy

from qiskit.tools.visualization import circuit_drawer

# Input N
N = 2
X = 2 # qc will take exponentially longer to compile with each increase

a = QuantumRegister(N)
b = QuantumRegister(X)
m = QuantumRegister(N*(pow(2,X)-1))

ca = ClassicalRegister(N)
cm = ClassicalRegister(N*(pow(2,X)-1))

qc = QuantumCircuit(a, b, m, cm, ca)

# Input
# a = 11 = 3
qc.x(a[0])
qc.x(a[1])
# b= 11 = 3
qc.x(b[0])
qc.x(b[1])

power(qc, a, b, m)

qc.measure(m, cm)
qc.measure(a, ca)

backend_sim = Aer.get_backend('qasm_simulator')
print("started job")

job_sim = execute(qc, backend_sim, shots=1)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))