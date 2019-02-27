# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from QArithmetic import add_ex

# Input N
N = 4

a = QuantumRegister(N)
b = QuantumRegister(N)
s = QuantumRegister(N+1)
c = QuantumRegister(N)

ca = ClassicalRegister(N)
cb = ClassicalRegister(N)
cs = ClassicalRegister(N+1)
cc = ClassicalRegister(N)

qc = QuantumCircuit(a, b, s, c, ca, cb, cs, cc)


# Input Superposition
# a =  1110
qc.x(a[1])
qc.x(a[2])
qc.x(a[3])
# b = 1011
qc.x(b[0])
qc.x(b[1])
qc.x(b[3])

add_ex(qc, a, b, s, c, N)

qc.measure(a, ca)
qc.measure(b, cb)
qc.measure(s, cs)
qc.measure(c, cc)

backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
