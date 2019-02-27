# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer

def full_adder(a, b, cin, cout):
    qc.ccx(a, b, cout)
    qc.ccx(a, cin, cout)
    qc.ccx(b, cin, cout)

    qc.cx(a,  b)
    qc.cx(cin, b)

def n_adder(a, b, c, n):
    for i in range(0, n):
        full_adder(a[i], b[i], c[i], c[i+1])

# Input N
N = 1


a = QuantumRegister(N)
b = QuantumRegister(N)
c = QuantumRegister(N + 1)

ca = ClassicalRegister(N)
cb = ClassicalRegister(N)
cc = ClassicalRegister(N + 1)

qc = QuantumCircuit(a, b, c, ca, cb, cc)


# Input Superposition
qc.h(a)
qc.h(b)
qc.h(c[0])


n_adder(a, b, c, N)

qc.measure(a, ca)
qc.measure(b, cb)
qc.measure(c, cc)

backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
