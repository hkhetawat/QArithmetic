# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
from QArithmetic import lshift_fourier
from qiskit.tools.visualization import circuit_drawer
from qft import qft, iqft

# Input N
N = 3

a = QuantumRegister(N)

ca = ClassicalRegister(N)

qc = QuantumCircuit(a, ca)

# Input
# a = 010 = 2
# qc.x(a[0])
qc.x(a[1])
# qc.x(a[2])

qft(qc, a, len(a))
lshift_fourier(qc, a)
iqft(qc, a, len(a))

qc.measure(a, ca)

circuit_drawer(qc, output="text", interactive=True, scale=1.0, filename='test4', fold=-1)
backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))

# from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
# from numpy import pi

# qreg_q = QuantumRegister(3, 'q')

# circuit = QuantumCircuit(qreg_q)

# circuit.x(qreg_q[1])
# circuit.h(qreg_q[2])
# circuit.cp(pi/2, qreg_q[2], qreg_q[1])
# circuit.cp(pi/4, qreg_q[2], qreg_q[0])
# circuit.h(qreg_q[1])
# circuit.cp(pi/2, qreg_q[1], qreg_q[0])
# circuit.h(qreg_q[0])
# circuit.h(qreg_q[1])
# circuit.cp(pi/2, qreg_q[1], qreg_q[2])
# circuit.h(qreg_q[1])
# circuit.h(qreg_q[2])
# circuit.cz(qreg_q[2], qreg_q[1])
# circuit.h(qreg_q[2])

# gate srswap a, b {
#   cx a, b;
#   h a;
#   t a;
#   tdg b;
#   h a;
#   h b;
#   cx a, b;
#   h a;
#   h b;
#   tdg a;
#   h a;
#   cx a, b;
#   sdg a;
#   s b;
# }



# OPENQASM 2.0;
# include "qelib1.inc";
# gate srswap a, b {
#   cx a, b;
#   h a;
#   t a;
#   tdg b;
#   h a;
#   h b;
#   cx a, b;
#   h a;
#   h b;
#   tdg a;
#   h a;
#   cx a, b;
#   sdg a;
#   s b;
# }

# qreg q[3];

# x q[0];
# h q[2];
# cp(pi/2) q[1],q[2];
# cp(pi/4) q[0],q[2];
# h q[1];
# cp(pi/2) q[0],q[1];
# h q[0];
# h q[0];
# cp(-pi/2) q[0],q[1];
# h q[1];
# cp(pi/2) q[1],q[2];
# h q[1];
# h q[2];
# cp(pi) q[2],q[1];
# cp(pi/2) q[0],q[1];
# h q[2];
# cp(pi/4) q[0],q[2];
# cp(pi/2) q[0],q[1];
# h q[0];
# p(pi) q[0];
# barrier q[0],q[1],q[2];
# h q[0];


# h q[0];
# h q[1];
# csx q[0],q[1];
# csx q[0],q[1];
# csx q[0],q[1];
# cp(pi/2) q[1],q[2];
# cp(-pi/4) q[0],q[2];
# csx q[0],q[1];
# h q[2];
# h q[1];
# cz q[2],q[1];


# circuit.x(qreg_q[1])
# circuit.h(qreg_q[2])
# circuit.cp(pi/2, qreg_q[1], qreg_q[2])
# circuit.x(qreg_q[0])
# circuit.cp(pi/4, qreg_q[0], qreg_q[2])
# circuit.h(qreg_q[1])
# circuit.cp(pi/2, qreg_q[0], qreg_q[1])
# circuit.h(qreg_q[0])
# circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2])
# circuit.h(qreg_q[0])
# circuit.h(qreg_q[1])
# circuit.csx(qreg_q[0], qreg_q[1])
# circuit.csx(qreg_q[0], qreg_q[1])
# circuit.csx(qreg_q[0], qreg_q[1])
# circuit.cp(pi/2, qreg_q[1], qreg_q[2])
# circuit.cp(-pi/4, qreg_q[0], qreg_q[2])
# circuit.csx(qreg_q[0], qreg_q[1])
# circuit.h(qreg_q[2])
# circuit.h(qreg_q[1])
# circuit.cz(qreg_q[2], qreg_q[1])
# circuit.h(qreg_q[2])
# circuit.cp(pi/4, qreg_q[0], qreg_q[2])
# circuit.cp(pi/4, qreg_q[0], qreg_q[2])
# circuit.cp(pi/2, qreg_q[0], qreg_q[1])
# circuit.h(qreg_q[0])
# circuit.h(qreg_q[1])
# circuit.cz(qreg_q[1], qreg_q[0])
# circuit.h(qreg_q[1])
# circuit.barrier(qreg_q[0], qreg_q[1], qreg_q[2])
# circuit.h(qreg_q[0])
# circuit.cp(-pi/2, qreg_q[0], qreg_q[1])
# circuit.h(qreg_q[1])
# circuit.cp(-pi/4, qreg_q[0], qreg_q[2])
# circuit.cp(-pi/2, qreg_q[1], qreg_q[2])
# circuit.h(qreg_q[2])


# circuit.h(qreg_q[0])
# circuit.h(qreg_q[1])
# circuit.csx(qreg_q[0], qreg_q[1])
# circuit.csx(qreg_q[0], qreg_q[1])
# circuit.csx(qreg_q[0], qreg_q[1])
# circuit.cp(pi/2, qreg_q[1], qreg_q[2])
# circuit.cp(-pi/4, qreg_q[0], qreg_q[2])
# circuit.csx(qreg_q[0], qreg_q[1])
# circuit.h(qreg_q[2])
# circuit.h(qreg_q[1])
# circuit.cz(qreg_q[2], qreg_q[1])
# circuit.h(qreg_q[2])
# circuit.cp(pi/4, qreg_q[0], qreg_q[2])
# circuit.cp(pi/4, qreg_q[0], qreg_q[2])
# circuit.cp(pi/2, qreg_q[0], qreg_q[1])
# circuit.h(qreg_q[0])
# circuit.h(qreg_q[1])
# circuit.cz(qreg_q[1], qreg_q[0])
# circuit.h(qreg_q[0])
# circuit.h(qreg_q[1])
# circuit.cp(-pi/2, qreg_q[0], qreg_q[1])
# circuit.cp(-3*pi/4, qreg_q[0], qreg_q[2])
# circuit.h(qreg_q[0])