from math import pi

# Quantum Fourier transform of |q>, of length n.
# See Fig. 3 of Khosropour et al. (2011) for a circuit diagram.
def qft(circ, q, n):
    # Iterate through the target.
    for i in range(n,0,-1):
        # Apply the Hadamard gate to the target.
        circ.h(q[i-1])

        # Iterate through the control.
        for j in range(i-1,0,-1):
            circ.cu1(2*pi/2**(i-j+1), q[j-1], q[i-1])

# Inverse Fourier transform of |q>, of length n.
def iqft(circ, q, n):
    # Iterate through the target.
    for i in range(1,n+1):
        # Iterate through the control.
        for j in range(1,i):
            # The inverse Fourier transform just uses a negative phase.
            circ.cu1(-2*pi/2**(i-j+1), q[j-1], q[i-1])

        # Apply the Hadamard gate to the target.
        circ.h(q[i-1])

# Controlled-controlled phase gate with phase theta.
# a and b are the controls, and c is the target.
def ccu1(circ, theta, a, b, c):
    circ.cu1(theta/2, b, c)
    circ.cx(a, b)
    circ.cu1(-theta/2, b, c)
    circ.cx(a, b)
    circ.cu1(theta/2, a, c)

# Quantum Fourier transform of q, controlled by p.
def cqft(circ, p, q, n):
    # All the operators are controlled by p.

    # Iterate through the target.
    for i in range(n,0,-1):
        # Apply the Hadamard gate to the target.
        circ.ch(p, q[i-1])

        # Iterate through the control.
        for j in range(i-1,0,-1):
            ccu1(circ, 2*pi/2**(i-j+1), p, q[j-1], q[i-1])

# Inverse quantum Fourier transform of p, controlled by p.
def ciqft(circ, p, q, n):
    # Iterate through the target.
    for i in range(1,n+1):
        # Iterate through the control.
        for j in range(1,i):
            ccu1(circ, -2*pi/2**(i-j+1), p, q[j-1], q[i-1])

        # Apply the Hadamard gate to the target.
        circ.ch(p, q[i-1])
