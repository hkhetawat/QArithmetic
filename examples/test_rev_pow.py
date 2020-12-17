# Import the Qiskit SDK
from numpy.lib.function_base import copy
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, IBMQ
from qiskit import execute, Aer
from qiskit.providers.aer import QasmSimulator
from QArithmetic import full_qr, power
from copy import copy

from qiskit.tools.visualization import circuit_drawer

# Input N
N = 2
X = 2 # qc will take exponentially longer to compile with each increase

a = QuantumRegister(N)
b = QuantumRegister(X)
m = QuantumRegister(N*(pow(2,X)-1))

ca = ClassicalRegister(N)
cm = ClassicalRegister(N*(pow(2,X)-1))

qc = QuantumCircuit(a, b, m, cm, ca)
# b = full_qr(b) + full_qr(b)

# Input
# a = 11 = 3
qc.x(a[0])
qc.x(a[1])
# b= 11 = 3
qc.x(b[0])
qc.x(b[1])

power(qc, a, b, m)

# qc = qc.decompose()
# qc = qc.reverse_ops()

qc.measure(m, cm)
qc.measure(a, ca)

circuit_drawer(qc, output="text", interactive=True, scale=1.0, filename='test3', fold=-1)
# Only 2 qubuts ^ 2 qubits would use 2^48Bytes~35TB in a statevector
# Thus MPS must be used here and if not configured correctly it may act unexpectedly
provider = IBMQ.load_account()
backend_sim = provider.backends.ibmq_qasm_simulator
# backend_sim = QasmSimulator(method='extended_stabilizer',precision="single", max_memory_mb=int(pow(2,33.5)))
print("started job")

job_sim = execute(qc, backend_sim, shots=20)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
