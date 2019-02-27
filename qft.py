from math import pi

# See https://en.wikipedia.org/wiki/Quantum_Fourier_transform#Circuit_implementation
# for a circuit diagram.

def qft(circ, q, n):
    # Iterate through the target.
    for i in range(1,n+1):
        # Apply the Hadamard gate to the target.
        circ.h(q[i-1])

        # Iterate through the control.
        for j in range(i+1,n+1):
            circ.cu1(2*pi/2**j, q[j-1], q[i-1])

# The inverse Fourier transform just uses a negative phase.
def iqft(circ, q, n):
    # Iterate through the target.
    for i in range(n,0,-1):
        # Iterate through the control.
        for j in range(n,i,-1):
            circ.cu1(-2*pi/2**j, q[j-1], q[i-1])

        # Apply the Hadamard gate to the target.
        circ.h(q[i-1])

