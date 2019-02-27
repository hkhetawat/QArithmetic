# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer

# Define some functions for the adder.
def sum(cin, a, b):
    qc.cx(a,b)
    qc.cx(cin,b)

def carry(cin, a, b, cout):
    qc.ccx(a, b, cout)
    qc.cx(a, b)
    qc.ccx(cin, b, cout)

def carry_dg(cin, a, b, cout):
    qc.ccx(cin, b, cout)
    qc.cx(a, b)
    qc.ccx(a, b, cout)

# Define the adder.
def n_adder(a, b, c, n):
    # Calculate all the carries except the last one.
    for i in range(0, n-1):
        carry(c[i], a[i], b[i], c[i+1])

    # The last carry bit is the leftmost bit of the sum.
    carry(c[n-1], a[n-1], b[n-1], b[n])

    # Calculate the second-to-leftmost bit of the sum.
    qc.cx(c[n-1],b[n-1])

    # Invert the carries and calculate the remaining sums.
    for i in range(n-2,-1,-1):
        print(i)
        carry_dg(c[i], a[i], b[i], c[i+1])
        sum(c[i], a[i], b[i])

# Input N
N = 4

a = QuantumRegister(N)
b = QuantumRegister(N+1)
c = QuantumRegister(N)

ca = ClassicalRegister(N)
cb = ClassicalRegister(N+1)
cc = ClassicalRegister(N)

qc = QuantumCircuit(a, b, c, ca, cb, cc)


# Input Superposition
# a =  1110
qc.x(a[1])
qc.x(a[2])
qc.x(a[3])
# b = 01011
qc.x(b[0])
qc.x(b[1])
qc.x(b[3])

n_adder(a, b, c, N)

qc.measure(a, ca)
qc.measure(b, cb)
qc.measure(c, cc)

backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
