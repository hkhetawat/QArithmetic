from math import pi
from qiskit import QuantumRegister
from qft import qft, iqft

# Define a controlled Toffoli gate
def cccx(circ,ctrl,a,b,c):
    circ.reset(anc[0])
    circ.ccx(ctrl,a,anc[0])
    circ.ccx(b,anc[0],c)
    circ.ccx(ctrl,a,anc[0])
    circ.ccx(b,anc[0],c)


# Define some functions for the adder.
def sum(circ, cin, a, b):
    circ.cx(a,b)
    circ.cx(cin,b)

def carry(circ, cin, a, b, cout):
    circ.ccx(a, b, cout)
    circ.cx(a, b)
    circ.ccx(cin, b, cout)

def carry_dg(circ, cin, a, b, cout):
    circ.ccx(cin, b, cout)
    circ.cx(a, b)
    circ.ccx(a, b, cout)

# Adder that takes |a>|b> to |a>|a+b>.
# |a> has length n.
# |b> has length n+1.
# Based on Vedral, Barenco, and Ekert (1996).
def add(circ, a, b, n):
    # Create a carry register of length n.
    c = QuantumRegister(n)
    circ.add_register(c)

    # Calculate all the carries except the last one.
    for i in range(0, n-1):
        carry(circ, c[i], a[i], b[i], c[i+1])

    # The last carry bit is the leftmost bit of the sum.
    carry(circ, c[n-1], a[n-1], b[n-1], b[n])

    # Calculate the second-to-leftmost bit of the sum.
    circ.cx(c[n-1],b[n-1])

    # Invert the carries and calculate the remaining sums.
    for i in range(n-2,-1,-1):
        carry_dg(circ, c[i], a[i], b[i], c[i+1])
        sum(circ, c[i], a[i], b[i])

# Adder that takes |a>|b>|0> to |a>|b>|a+b>.
# |a> has length n. 
# |b> has length n.
# |s> = |0> has length n+1.
def add_ex(circ, a, b, s, n):
    # Copy b to s.
    for i in range(0, n):
        circ.cx(b[i],s[i])

    # Add a and s.
    add(circ, a, s, n)

# Draper adder that takes |a>|b> to |a>|a+b>.
# |a> has length n.
# |b> has length n+1.
# https://arxiv.org/pdf/quant-ph/0008033.pdf
def add_draper(circ, a, b, n):
    # Take the QFT of "b."
    qft(circ, b, n)

    # Compute controlled-phases.
    # Iterate through the targets.
    for i in range(n,0,-1):
        # Iterate through the controls.
        for j in range(i,0,-1):
            circ.cu1(2*pi/2**(i-j+1), b[j-1], a[i-1])

    # Take the inverse QFT of "b."
    iqft(circ, b, n)

# Subtractor that takes |a>|b> to |a>|a-b>.
# |a> has length n.
# |b> has length n+1.
def sub(circ, a, b, n):
    # We add "a" to the 2's complement of "b."
    # First flip the bits of "b."
    circ.x(b)

    # Create a carry register of length n.
    c = QuantumRegister(n)
    circ.add_register(c)

    # Add 1 to the carry register, which adds 1 to b, negating it.
    circ.x(c[0])

    # Calculate all the carries except the last one.
    for i in range(0, n-1):
        carry(circ, c[i], a[i], b[i], c[i+1])

    # The last carry bit is the leftmost bit of the sum.
    carry(circ, c[n-1], a[n-1], b[n-1], b[n])

    # Calculate the second-to-leftmost bit of the sum.
    circ.cx(c[n-1],b[n-1])

    # Invert the carries and calculate the remaining sums.
    for i in range(n-2,-1,-1):
        carry_dg(circ, c[i], a[i], b[i], c[i+1])
        sum(circ, c[i], a[i], b[i])

    # Flip the carry to restore it to zero.
    circ.x(c[0])

# Subtractor that takes |a>|b>|0> to |a>|b>|a-b>.
# |a> has length n.
# |b> has length n.
# |s> = |0> has length n+1.
def sub_ex(circ, a, b, s, n):
    # Copy b to s.
    for i in range(0, n):
        circ.cx(b[i],s[i])

    # Subtract a and s.
    sub(circ, a, s, n)

# Multiplier that takes |a>|b>|0> to |a>|b>|a*b>.
# |a> has length n.
# |b> has length n.
# |s> = |0> has length 2n.
#def mult_ex(circ, a, b, s):

