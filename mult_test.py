# Import the Qiskit SDK
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit import execute, Aer
def cccx(ctrl,a,b,c):
    qc.reset(anc[0])
    qc.ccx(ctrl,a,anc[0])
    qc.ccx(b,anc[0],c)
    qc.ccx(ctrl,a,anc[0])
    qc.ccx(b,anc[0],c)

def control_full_adder(ctrl, a, b, s, cin, cout):
    cccx(ctrl,a, b, cout)
    cccx(ctrl,a, cin, cout)
    cccx(ctrl,b, cin, cout)

    qc.ccx(ctrl, a,  s)
    qc.ccx(ctrl, b,  s)
    qc.ccx(ctrl, cin, s)

def control_n_adder(ctrl, a, b, s, c, n):
    for i in range(0, n):
        control_full_adder(ctrl[0], a[i], b[i], s[i], c[i], c[i+1])



# Input N
N = 3
anc = QuantumRegister(1)


temp = QuantumRegister(1)
a = QuantumRegister(N)
b = QuantumRegister(N)
s = QuantumRegister(N)
c = QuantumRegister(N + 1)


ca = ClassicalRegister(N)
cb = ClassicalRegister(N)
cs = ClassicalRegister(N)
cc = ClassicalRegister(N + 1)

qc = QuantumCircuit(a, b, s, c, ca, cb, cs, cc,temp)
qc.add_register(anc)

# Input Superposition
#qc.x(a[3])
qc.x(a[2])
qc.x(a[1])
#qc.x(b[3])
qc.x(b[1])
qc.x(b[0])
qc.x(temp[0])

control_n_adder(temp, a, b, s, c, N)

qc.measure(a, ca)
qc.measure(b, cb)
qc.measure(s, cs)
qc.measure(c, cc)

backend_sim = Aer.get_backend('qasm_simulator')
job_sim = execute(qc, backend_sim)
result_sim = job_sim.result()

print(result_sim.get_counts(qc))
