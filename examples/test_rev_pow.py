# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from qiskit.providers.aer import QasmSimulator
from QArithmetic import power

# Input N
N = 2
X = 2 # qc will take exponentially longer to compile with each increase

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

power(qc, a, b, m)

qc.measure(m, cm)

# Only 2 qubuts ^ 2 qubits would use 2^48Bytes~35TB in a statevector
# Thus MPS must be used here and if not configured correctly it may act unexpectedly
backend_sim = QasmSimulator(method='matrix_product_state')
print("started job")

job_sim = execute(qc, backend_sim, shots=20)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
# print(result_sim)
