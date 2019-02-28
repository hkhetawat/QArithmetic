# QArithmetic
Arithmetic library for IBM Qiskit

This is our great, awesome, extremely impressive, daunting, inspiring arithmetic library

List of operations implemented:

# Bit-wise operations

Controlled Toffoli gate 

Source: O. Scott, Nathan & Dueck, G.W.. (2008). Pairwise decomposition of toffoli gates in a quantum circuit. 231-236. 10.1145/1366110.1366168. 


Logical AND (qc, a, b, c, N);qc->quantum circuit, a->input1, b->input2, c->output, N->bit-string length


Logical OR (qc, a, b, c, N);qc->quantum circuit, a->input1, b->input2, c->output, N->bit-string length

Logical XOR (qc, a, b, c, N);qc->quantum circuit, a->input1, b->input2, c->output, N->bit-string length

Logical NOT (qc, a, c, N)

Shift right

Shift left

# Arithmetic operations

QFT-based add (Draper adder)

Ripple carry add

QFT-based sub

Ripple carry sub

Sub-and-swap

Multiply

Divide

