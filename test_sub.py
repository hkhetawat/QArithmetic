# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from QArithmetic import sub

# Input N
N = 4

a = QuantumRegister(N)
b = QuantumRegister(N+1)
c = QuantumRegister(N)

ca = ClassicalRegister(N)
cb = ClassicalRegister(N+1)
cc = ClassicalRegister(N)

qc = QuantumCircuit(a, b, c, ca, cb, cc)


# Input Superposition
# a =  1110
qc.x(a[1])
qc.x(a[2])
qc.x(a[3])
# b = 01011
qc.x(b[0])
qc.x(b[1])
qc.x(b[3])

sub(qc, a, b, c, N)

qc.measure(a, ca)
qc.measure(b, cb)
qc.measure(c, cc)

backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
