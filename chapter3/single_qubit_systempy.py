import numpy as nump
import scipy as scip
import scipy.linalg

Zero_state = nump.array([[1.0],
                 [0.0]])
One_state = nump.array([[0.0],
                [1.0]])
                
                
NormalizeQuantumState = lambda quantum_state: quantum_state / scip.linalg.norm(quantum_state)

Plus_State = NormalizeQuantumState(Zero_state + One_state)

print("normalized quantum state of",Zero_state, "+", One_state,"is", Plus_State)