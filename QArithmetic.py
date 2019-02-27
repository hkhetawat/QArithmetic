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
# |c> is an ancilla of all zeros of length n.
def add(circ, a, b, c, n):
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
# |s> has length n+1.
# |c> is an ancilla of all zeros of length n.
def add_ex(circ, a, b, s, c, n):
    # Copy b to s.
    for i in range(0, n):
        circ.cx(b[i],s[i])

    # Add a and s.
    add(circ, a, s, c, n)

# Subtrator that takes |a>|b> to |a>|a-b>.
# |a> has length n.
# |b> has length n+1.
# |c> is an ancilla of all zeros of length n.
def sub(circ, a, b, c, n):
    # We add "a" to the 2's complement of "b."
    # First flip the bits of "b."
    circ.x(b)

    # Now carry in 1, so we're adding 1 to b, which negates it.
    circ.x(c[0])

    # Now add them.
    add(circ, a, b, c, n)

    # Flip the carry to restore it to zero.
    circ.x(c[0])

