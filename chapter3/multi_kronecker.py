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


three_quantum_states = nump.kron(nump.kron(zero_quantum_state, one_quantum_state), one_quantum_state)
print("three  quantum states -kronecker",three_quantum_states)



#multi_quantum_states = multi_quantum_state(zero_quantum_state, one_quantum_state, one_quantum_state, 
                        # one_quantum_state, zero_quantum_state, one_quantum_state)

#print("multi quantum states",multi_quantum_states)
#print("multi quantumstates shape",multi_quantum_states.shape)