# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from QArithmetic import div

# Input n
n = 2

p = QuantumRegister(2*n)
d = QuantumRegister(2*n)
q = QuantumRegister(n)

cp = ClassicalRegister(2*n)
cd = ClassicalRegister(2*n)
cq = ClassicalRegister(n)

qc = QuantumCircuit(p,d,q,cp,cd,cq)


# Input Superposition
# p = 0011
qc.x(p[0])
qc.x(p[1])
# d = 1000
qc.x(d[3])

div(qc, p, d, q, n)

qc.measure(p, cp)
qc.measure(d, cd)
qc.measure(q, cq)

backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
