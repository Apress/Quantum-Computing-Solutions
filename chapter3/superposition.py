import numpy as nump

zero_quantum_state = nump.array([[1.0],
                       [0.0]])
one_quantum_state = nump.array([[0.0],
                      [1.0]])

quantum_amp1 = 1.0 / 2**0.5
quantum_amp2 = 1.0 / 2**0.5
superposition_quantum_state = quantum_amp1 * zero_quantum_state + quantum_amp2 * one_quantum_state
print("superposition of", zero_quantum_state, " and ", one_quantum_state," is ",superposition_quantum_state)

