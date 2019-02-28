# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer


def bitwise_and(qc, a, b, c, N):
    for i in range(0, N):
        qc.ccx(a[i], b[i], c[i])

def bitwise_or(qc, a, b, c, N):
    for i in range(0, N):
        qc.ccx(a[i], b[i], c[i])
        qc.cx(a[i], c[i])
        qc.cx(b[i], c[i])

def bitwise_xor(qc, a, b, c, N):
    for i in range(0, N):
        qc.cx(a[i], c[i])
        qc.cx(b[i], c[i])

def bitwise_not(qc, a, c, N):
    for i in range(0, N):
        qc.cx(a[i], c[i])
        qc.x(c[i])

# Input N
N = 4

a = QuantumRegister(N)
b = QuantumRegister(N)
c = QuantumRegister(N)

ca = ClassicalRegister(N)
cb = ClassicalRegister(N)
cc = ClassicalRegister(N)

qc = QuantumCircuit(a, b, c, ca, cb, cc)


# Input Superposition
# a =  1110
qc.x(a[1])
qc.x(a[3])
# b = 1011
qc.x(b[0])
qc.x(b[1])
qc.x(b[3])

bitwise_not(qc, a, c, N)

qc.measure(a, ca)
qc.measure(b, cb)
qc.measure(c, cc)

backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
