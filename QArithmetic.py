from math import pi
from qiskit import QuantumRegister, QuantumCircuit, AncillaRegister
from qft import qft, iqft, cqft, ciqft, ccu1
from qiskit.circuit.library import SXdgGate

################################################################################
# Bitwise Operators
################################################################################

# bit-wise operations
def bitwise_and(qc, a, b, c, N):
    for i in range(0, N):
        qc.ccx(a[i], b[i], c[i])

def bitwise_or(qc, a, b, c, N):
    for i in range(0, N):
        qc.ccx(a[i], b[i], c[i])
        qc.cx(a[i], c[i])
        qc.cx(b[i], c[i])

def bitwise_xor(qc, a, b, c, N):
    for i in range(0, N):
        qc.cx(a[i], c[i])
        qc.cx(b[i], c[i])

def bitwise_not(qc, a, c, N):
    for i in range(0, N):
        qc.cx(a[i], c[i])
        qc.x(c[i])

# Cyclically left-shifts a binary string "a" of length n.
# If "a" is zero-padded, equivalent to multiplying "a" by 2.
def lshift(circ, a, n=-1):
    # Init n if it was not
    if n == -1:
        n = len(a)

    # Iterate through pairs and do swaps.
    for i in range(n,1,-1):
        circ.swap(a[i-1],a[i-2])

# Cyclically left-shifts a binary string "a" of length n, controlled by c.
# If "a" is zero-padded, equivalent to multiplying "a" by 2, if and only if c.
def c_lshift(circ, c, a, n=-1):
    # Init n if it was not
    if n == -1:
        n = len(a)

    # Iterate through pairs and do swaps.
    for i in range(n,1,-1):
        circ.cswap(c, a[i-1],a[i-2])

# Cyclically right-shifts a binary string "a" of length n.
# If "a" is zero-padded, equivalent to dividing "a" by 2.
def rshift(circ, a, n=-1):
    # Init n if it was not
    if n == -1:
        n = len(a)

    # Iterate through pairs and do swaps.
    for i in range(n-1):
        circ.swap(a[i],a[i+1])

# Cyclically right-shifts a binary string "a" of length n, controlled by c.
# If "a" is zero-padded, equivalent to dividing "a" by 2, if and only if c.
def c_rshift(circ, c, a, n=-1):
    # Init n if it was not
    if n == -1:
        n = len(a)
    
    # Iterate through pairs and do swaps.
    for i in range(n,1,-1):
        circ.cswap(c, a[i-1],a[i-2])

################################################################################
# Addition Circuits
################################################################################

# Define some functions for the ripple adder.
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

# Draper adder that takes |a>|b> to |a>|a+b>.
# |a> has length x and is less than or equal to n
# |b> has length n+1 (left padded with a zero).
# https://arxiv.org/pdf/quant-ph/0008033.pdf
def add(circ, a, b, n):
    # move n forward by one to account for overflow
    n += 1

    # Take the QFT.
    qft(circ, b, n)

    # Compute controlled-phases.
    # Iterate through the targets.
    for i in range(n,0,-1):
        # Iterate through the controls.
        for j in range(i,0,-1):
            # If the qubit a[j-1] exists run cu1, if not assume the qubit is 0 and never existed
            if len(a) - 1 >= j - 1:
                circ.cu1(2*pi/2**(i-j+1), a[j-1], b[i-1])

    # Take the inverse QFT.
    iqft(circ, b, n)

# Draper adder that takes |a>|b> to |a>|a+b>, controlled on |c>.
# |a> has length x and is less than or equal to n
# |b> has length n+1 (left padded with a zero).
# |c> is a single qubit that's the control.
def cadd(circ, c, a, b, n):
    # move n forward by one to account for overflow
    n += 1

    # Take the QFT.
    cqft(circ, c, b, n)

    # Compute controlled-phases.
    # Iterate through the targets.
    for i in range(n,0,-1):
        # Iterate through the controls.
        for j in range(i,0,-1):
            # If the qubit a[j-1] exists run ccu, if not assume the qubit is 0 and never existed
            if len(a) - 1 >= j - 1:
                ccu1(circ, 2*pi/2**(i-j+1), c, a[j-1], b[i-1])

    # Take the inverse QFT.
    ciqft(circ, c, b, n)

# Adder that takes |a>|b> to |a>|a+b>.
# |a> has length n.
# |b> has length n+1.
# Based on Vedral, Barenco, and Ekert (1996).
def add_ripple(circ, a, b, n):
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
def add_ripple_ex(circ, a, b, s, n):
    # Copy b to s.
    for i in range(0, n):
        circ.cx(b[i],s[i])

    # Add a and s.
    add_ripple(circ, a, s, n)


################################################################################
# Subtraction Circuits
################################################################################

# Subtractor that takes |a>|b> to |a>|a-b>.
# |a> has length n+1 (left padded with a zero).
# |b> has length n+1 (left padded with a zero).
def sub(circ, a, b, n):
    # Flip the bits of a.
    circ.x(a)

    # Add it to b.
    add(circ, a, b, n - 1)

    # Flip the bits of the result. This yields the sum.
    circ.x(b)

    # Flip back the bits of a.
    circ.x(a)

# Subtractor that takes |a>|b> to |a-b>|b>.
# |a> has length n+1 (left padded with a zero).
# |b> has length n+1 (left padded with a zero).
def sub_swap(circ, a, b, n):
    # Flip the bits of a.
    circ.x(a)

    # Add it to b.
    add(circ, b, a, n - 1)

    # Flip the bits of the result. This yields the sum.
    circ.x(a)

# Subtractor that takes |a>|b> to |a>|a-b>.
# |a> has length n.
# |b> has length n+1.
def sub_ripple(circ, a, b, n):
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
def sub_ripple_ex(circ, a, b, s, n):
    # Copy b to s.
    for i in range(0, n):
        circ.cx(b[i],s[i])

    # Subtract a and s.
    sub_ripple(circ, a, s, n)

################################################################################
# Multiplication Circuit
################################################################################

# Controlled operations

# Take a subset of a quantum register from index x to y, inclusive.
def sub_qr(qr, x, y): # may also be able to use qbit_argument_conversion
    sub = []
    for i in range (x, y+1):
        sub = sub + [(qr[i])]
    return sub

def full_qr(qr):
    return sub_qr(qr, 0, len(qr) - 1)

# Computes the product c=a*b.
# a has length n.
# b has length n.
# c has length 2n.
def mult(circ, a, b, c, n):
    for i in range (0, n):
        cadd(circ, a[i], b, sub_qr(c, i, n+i), n)

# Computes the product c=a*b if and only if control.
# a has length n.
# b has length n.
# control has length 1.
# c has length 2n.
def cmult(circ, control, a, b, c, n):
    qa = QuantumRegister(len(a))
    qb = QuantumRegister(len(b))
    qc = QuantumRegister(len(c))
    tempCircuit = QuantumCircuit(qa, qb, qc)
    mult(tempCircuit, qa, qb, qc, n)
    tempCircuit = tempCircuit.control(1) #Add Decomposition after pull request inclusion #5446 on terra
    print("Remember To Decompose after release >0.16.1")
    circ.compose(tempCircuit, qubits=full_qr(control) + full_qr(a) + full_qr(b) + full_qr(c), inplace=True)

################################################################################
# Division Circuit
################################################################################

# Divider that takes |p>|d>|q>.
# |p> is length 2n and has n zeros on the left: 0 ... 0 p_n ... p_1.
# |d> has length 2n and has n zeros on the right: d_2n ... d_{n+1) 0 ... 0.
# |q> has length n and is initially all zeros.
# At the end of the algorithm, |q> will contain the quotient of p/d, and the
# left n qubits of |p> will contain the remainder of p/d.
def div(circ, p, d, q, n):
    # Calculate each bit of the quotient and remainder.
    for i in range(n,0,-1):
        # Left shift |p>, which multiplies it by 2.
        lshift(circ, p, 2*n)

        # Subtract |d> from |p>.
        sub_swap(circ, p, d, 2*n)

        # If |p> is positive, indicated by its most significant bit being 0,
        # the (i-1)th bit of the quotient is 1.
        circ.x(p[2*n-1])
        circ.cx(p[2*n-1], q[i-1])
        circ.x(p[2*n-1])

        # If |p> is negative, indicated by the (i-1)th bit of |q> being 0, add D back
        # to P.
        circ.x(q[i-1])
        cadd(circ, q[i-1], d, p, 2*n - 1)
        circ.x(q[i-1])

################################################################################
# Expontential Circuit
################################################################################

# square that takes |a> |b>
# |a> is length n and is a unsigned integer
# |b> is length 2n and has 2n zeros, after execution b = a^2
def square(circ, a, b, n=-1):
    if n == -1:
        n = len(a)
    
    # First Addition
    circ.cx(a[0], b[0])
    for i in range(1, n):
        circ.ccx(a[0], a[i], b[i])
    
    # Custom Addition Circuit For Each Qubit of A
    for k in range(1, n):
        # modifying qubits
        d = b[k:n+k+1]
        qft(circ, d, n+1) #Technically the first few QFT could be refactored to use less gates due to guaranteed controls

        # Compute controlled-phases.
        # Iterate through the targets.
        for i in range(n+1,0,-1):
            # Iterate through the controls.
            for j in range(i,0,-1):
                if len(a) - 1 < j - 1:
                    pass # skip over non existent qubits
                elif k == j - 1: # Cannot control twice
                    circ.cu1(2*pi/2**(i-j+1), a[j-1], d[i-1])
                else:
                    ccu1(circ, 2*pi/2**(i-j+1), a[k], a[j-1], d[i-1])
        
        iqft(circ, d, n+1)
                





# a has length n
# b has length v
# finalOut has length n*((2^v)-1), for safety
def power(circ, a, b, finalOut): #Because this is reversible/gate friendly memory blooms to say the least
    # Track Number of Qubits
    n = len(a)
    v = len(b)

    # Left 0 pad a, to satisfy multiplication function arguments
    aPad = AncillaRegister(n * (pow(2, v) - 3)) # Unsure of where to Anciallas these
    circ.add_register(aPad)
    padAList = full_qr(aPad)
    aList = full_qr(a)
    a = aList + padAList

    # Create a register d for mults and init with state 1
    d = AncillaRegister(n) # Unsure of where to Anciallas these
    circ.add_register(d)

    # Create a register for tracking the output of cmult to the end
    ancOut = AncillaRegister(n*2) # Unsure of where to Anciallas these
    circ.add_register(ancOut)

    # Left 0 pad finalOut to provide safety to the final multiplication
    if (len(a) * 2) - len(finalOut) > 0:
        foPad = AncillaRegister((len(a) * 2) - len(finalOut))
        circ.add_register(foPad)
        padFoList = full_qr(foPad)
        foList = full_qr(finalOut)
        finalOut = foList + padFoList
    
    # Create zero bits
    num_recycle = (2 * n * (pow(2, v) - 2)) - (n * pow(2, v)) # 24
    permaZeros = []
    if num_recycle > 0:
        permaZeros = AncillaRegister(num_recycle) #8
        circ.add_register(permaZeros)
        permaZeros = full_qr(permaZeros)

    # Instead of MULT copy bits over
    if v >= 1:
        for i in range(n):
            circ.ccx(b[0], a[i], d[i])
        circ.x(b[0])
        circ.cx(b[0], d[0])
        circ.x(b[0])
    
    # iterate through every qubit of b
    for i in range(1,v): # for every bit of b 
        for j in range(pow(2, i)):
            # run multiplication operation if and only if b is 1
            bonus = permaZeros[:2*len(d) - len(ancOut)]
            cmult(circ, [b[i]], a[:len(d)], d, full_qr(ancOut) + bonus, len(d))

            # if the multiplication was not run copy the qubits so they are not destroyed when creating new register
            circ.x(b[i])
            for qub in range(0,len(d)):
                circ.ccx(b[i], d[qub], ancOut[qub])
            circ.x(b[i])

            # Move the output to the input for next function and double the qubit length
            d = ancOut

            if i == v - 1 and j == pow(2, i) - 2:
                # this is the second to last step send qubiits to output
                ancOut = finalOut
            elif not (i == v - 1 and j == pow(2, i) - 1):
                # if this is not the very last step
                # create a new output register of twice the length and register it
                ancOut = AncillaRegister(len(d) + n) # Should label permazero bits
                circ.add_register(ancOut)