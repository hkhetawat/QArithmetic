# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer

# Controlled operations

def cccx(ctrl,a,b,c):
    qc.reset(anc[0])
    qc.ccx(ctrl,a,anc[0])
    qc.ccx(b,anc[0],c)
    qc.ccx(ctrl,a,anc[0])
    qc.ccx(b,anc[0],c)

def csum(circ, ctrl, cin, a, b):
    circ.ccx(ctrl,a,b)
    circ.ccx(ctrl,cin,b)

def ccarry(circ, ctrl, cin, a, b, cout):
    cccx(ctrl, a, b, cout)
    circ.ccx(ctrl, a, b)
    cccx(ctrl, cin, b, cout)

def ccarry_dg(circ, ctrl, cin, a, b, cout):
    cccx(ctrl, cin, b, cout)
    circ.ccx(ctrl, a, b)
    cccx(ctrl, a, b, cout)

def c_adder(circ, ctrl, a, b, n):
    c = QuantumRegister(n)
    circ.add_register(c)
    for i in range(0, n-1):
        ccarry(circ, ctrl, c[i], a[i], b[i], c[i+1])
    ccarry(circ, ctrl, c[n-1], a[n-1], b[n-1], b[n])
    
    circ.ccx(ctrl, c[n-1],b[n-1])
    
    for i in range(n-2,-1,-1):
        ccarry_dg(circ, ctrl, c[i], a[i], b[i], c[i+1])
        csum(circ, ctrl, c[i], a[i], b[i])

def sub_qr(qr, x, y):
    sub = []
    for i in range (x, y+1):
        sub = sub + [(qr, i)]
    return sub        


def c_multiplier(circ, a, b, m, n):
    for i in range (0, n):
        c_adder(circ, a[i], b, sub_qr(m, i, n+i), n)




# Input N
N = 2

a = QuantumRegister(N)
b = QuantumRegister(N)
m = QuantumRegister(2*N)
anc = QuantumRegister(1)

cm = ClassicalRegister(2*N)

qc = QuantumCircuit(a, b, m, anc, cm)

# Input
# a =  3
qc.x(a[0])
qc.x(a[1])
# b = 3
qc.x(b[0])
qc.x(b[1])

c_multiplier(qc, a, b, m, N)

qc.measure(m, cm)

backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
