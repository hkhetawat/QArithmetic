# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from QArithmetic import square
from qiskit.tools.visualization import circuit_drawer

# Input N
N = 3

a = QuantumRegister(2*N)

ca = ClassicalRegister(2*N)

qc = QuantumCircuit(a, ca)

# Input
# a = 010 = 2
# qc.x(a[0])
qc.x(a[2])

square(qc, a)

qc.measure(a, ca)

circuit_drawer(qc, output="text", interactive=True, scale=1.0, filename='test3', fold=-1)
backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))

# from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
# from numpy import pi

# qreg_q = QuantumRegister(3, 'q')

# circuit = QuantumCircuit(qreg_q)

# circuit.x(qreg_q[0])
# circuit.h(qreg_q[0])
# circuit.cp(pi/2, qreg_q[0], qreg_q[1])
# circuit.h(qreg_q[1])
# circuit.barrier(qreg_q[1], qreg_q[0], qreg_q[2])
# circuit.h(qreg_q[0])
# circuit.cp(pi, qreg_q[0], qreg_q[1])
# circuit.cx(qreg_q[0], qreg_q[2])
# circuit.h(qreg_q[0])
# circuit.cp(pi/2, qreg_q[2], qreg_q[0])
# circuit.h(qreg_q[1])
# circuit.cx(qreg_q[1], qreg_q[2])
# circuit.h(qreg_q[1])
# circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2])
# circuit.h(qreg_q[1])
# circuit.cp(pi/2, qreg_q[0], qreg_q[1])
# circuit.h(qreg_q[0])