# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from QArithmetic import qft, iqft

# Input N
N = 4

a = QuantumRegister(N)

ca = ClassicalRegister(N)

qc = QuantumCircuit(a, ca)


# Input Superposition
# a =  0110
qc.x(a[1])
qc.x(a[2])

qft(qc, a, N)
iqft(qc, a, N)

qc.measure(a, ca)

backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
