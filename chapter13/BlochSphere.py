from qiskit import Aer as qisAer
from qiskit import QuantumCircuit as QC
from qiskit import execute
from matplotlib import pyplot as plot
from qiskit.tools.visualization import plot_bloch_multivector as bloch_state_vector


quantum_circuit = QC(1, 1)
quantum_circuit.x(0)

simulator = qisAer.get_backend('statevector_simulator')
result = execute(quantum_circuit, backend=simulator).result()
statevector = result.get_statevector()
print('\n statevector is ', statevector)

bloch_state_vector(statevector)
plot.savefig("images/statevector.png")
plot.show()

simulator = qisAer.get_backend('unitary_simulator')
result = execute(quantum_circuit, backend=simulator).result()
unitary_matrix = result.get_unitary()
print('\nunitary matrix is \n', unitary_matrix)
