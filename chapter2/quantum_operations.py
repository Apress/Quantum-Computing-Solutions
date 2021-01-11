import numpy as nump

def multi_quantum_state(*args):
    ret = nump.array([[1.0]])
    for q in args:
        ret = nump.kron(ret, q)
    return ret

zero_quantum_state = nump.array([[1.0],
                       [0.0]])
one_quantum_state = nump.array([[0.0],
                      [1.0]])

Hadmard_quantum_gate = 1.0 / 2**0.5 * nump.array([[1, 1],
                             [1, -1]])
    
new_quantum_state = nump.dot(Hadmard_quantum_gate, zero_quantum_state)
print("dot product : Hadmard quantum gate and zero  quantumstate",new_quantum_state)

SWAP_quantum_gate = nump.array([[1,0,0,0],
                      [0,0,1,0],
                      [0,1,0,0],
                      [0,0,0,1]])
    
t0_quantum_state = multi_quantum_state(zero_quantum_state, one_quantum_state)
t1_quantum_state = nump.dot(SWAP_quantum_gate, t0_quantum_state)
print("SWAP Quantum  Gate - T1 Quantum state",t1_quantum_state)

Identity_quantum_gate = nump.eye(2)
t0_quantum_state = multi_quantum_state(zero_quantum_state, one_quantum_state)
t1_quantum_state = nump.dot(multi_quantum_state(Hadmard_quantum_gate, Identity_quantum_gate), t0_quantum_state)
print("Multi Quantum State of H Quantum gate and I Quantum gate",t1_quantum_state)