import cirq

qbit = cirq.GridQubit(0, 0)


quantum_circuit = cirq.Circuit.from_ops(
    cirq.X(qbit)**0.5,  
    cirq.measure(qbit, key='m')
)
print("Quantum Circuit:", quantum_circuit)
quantum_simulator = cirq.Simulator()
results = quantum_simulator.run(quantum_circuit, repetitions=20)
print("Results ",results)
