# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from QArithmetic import square

# Input N
N = 3

a = QuantumRegister(N)
b = QuantumRegister(2*N)

cb = ClassicalRegister(2*N)

qc = QuantumCircuit(a, b, cb)

# Input
# a = 111 = 7
qc.x(a[0])
qc.x(a[1])
qc.x(a[2])

square(qc, a, b)

qc.measure(b, cb)

backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))