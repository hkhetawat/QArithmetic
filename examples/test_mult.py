# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from QArithmetic import mult

# Input N
N = 2

a = QuantumRegister(N)
b = QuantumRegister(N)
m = QuantumRegister(2*N)

cm = ClassicalRegister(2*N)

qc = QuantumCircuit(a, b, m, cm)

# Input
# a = 010 = 2
qc.x(a[0])
qc.x(a[1])
# b = 011 = 3
qc.x(b[0])
qc.x(b[1])

mult(qc, a, b, m, N)

qc.measure(m, cm)

backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
