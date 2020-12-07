# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from qiskit.providers.aer import QasmSimulator
from QArithmetic import reversible_pow

from qiskit.tools.visualization import circuit_drawer
import matplotlib.pyplot as plt

# Input N
N = 2
X = 2 # keep this to two

a = QuantumRegister(N)
b = QuantumRegister(X)
m = QuantumRegister(N*(pow(2,X+1)))

cm = ClassicalRegister(N*(pow(2,X+1)))

qc = QuantumCircuit(a, b, m, cm)

# Input
# a = 010 = 2
qc.x(a[0])
qc.x(a[1])
# b= 010 = 2
qc.x(b[0])
qc.x(b[1])

reversible_pow(qc, a, b, m)

qc.measure(m, cm)
# circuit_drawer(qc, output="mpl", interactive=True, scale=1.0, filename='test', fold=-1).show()
# circuit_drawer(qc, output="text", interactive=True, scale=1.0, filename='test3', fold=-1)

# backend_sim = Aer.get_backend('unitary_simulator')
# backend_sim = StatevectorSimulator(precision='single', method="automatic", max_memory_mb=12288)
backend_sim = QasmSimulator(method='matrix_product_state', precision='single')
print("started job")
job_sim = execute(qc, backend_sim, shots=1024)
# job_sim.wait_for_final_state(wait=5)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
# print(result_sim)
