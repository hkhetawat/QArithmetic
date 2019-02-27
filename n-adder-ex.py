# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer

def full_adder(a, b, s, cin, cout):
    qc.ccx(a, b, cout)
    qc.ccx(a, cin, cout)
    qc.ccx(b, cin, cout)

    qc.cx(a,  s)
    qc.cx(b,  s)
    qc.cx(cin, s)

def n_adder(a, b, s, c, n):
    for i in range(0, n):
        full_adder(a[i], b[i], s[i], c[i], c[i+1])

# Input N
N = 4


a = QuantumRegister(N)
b = QuantumRegister(N)
s = QuantumRegister(N)
c = QuantumRegister(N + 1)

ca = ClassicalRegister(N)
cb = ClassicalRegister(N)
cs = ClassicalRegister(N)
cc = ClassicalRegister(N + 1)

qc = QuantumCircuit(a, b, s, c, ca, cb, cs, cc)


# Input Superposition
qc.x(a[3])
qc.x(a[2])
qc.x(a[1])
qc.x(b[3])
qc.x(b[1])
qc.x(b[0])

n_adder(a, b, s, c, N)

qc.measure(a, ca)
qc.measure(b, cb)
qc.measure(s, cs)
qc.measure(c, cc)

backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
