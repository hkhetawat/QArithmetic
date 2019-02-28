# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from QArithmetic import cadd

# Input N
N = 4

a = QuantumRegister(N+1)
b = QuantumRegister(N+1)
c = QuantumRegister(1)

ca = ClassicalRegister(N+1)
cb = ClassicalRegister(N+1)
cc = ClassicalRegister(1)

qc = QuantumCircuit(a, b, c, ca, cb, cc)


# Input Superposition
# a =  01110
qc.x(a[1])
qc.x(a[2])
qc.x(a[3])
# b = 01011
qc.x(b[0])
qc.x(b[1])
qc.x(b[3])
# c = 0
#qc.x(c)

cadd(qc, c, a, b, N+1)

qc.measure(a, ca)
qc.measure(b, cb)
qc.measure(c, cc)

backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
