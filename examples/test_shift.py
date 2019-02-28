# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from QArithmetic import lshift, rshift

# Input N
n = 5

a = QuantumRegister(n)
b = QuantumRegister(n)

ca = ClassicalRegister(n)
cb = ClassicalRegister(n)

qc = QuantumCircuit(a, b, ca, cb)


# Input Superposition
# a =  11010
qc.x(a[1])
qc.x(a[3])
qc.x(a[4])
# b = 00011
qc.x(b[0])
qc.x(b[1])

# Left-shift |a>.
lshift(qc, a, n)
lshift(qc, a, n)
qc.measure(a, ca)

# Right-shift |b>.
rshift(qc, b, n)
rshift(qc, b, n)
qc.measure(b, cb)

# Simulate the circuit.
backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
