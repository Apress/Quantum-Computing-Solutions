from qiskit import IBMQ as Quantum_Simulator
from qiskit import QuantumRegister as QReg
from qiskit import ClassicalRegister as CReg
from qiskit import QuantumCircuit
from qiskit import Aer
from qiskit import *
from qiskit.tools.monitor import job_monitor as tools_monitor
from qiskit.tools.visualization import plot_histogram
from matplotlib import pyplot as plot



def create_circuit():
    qr = QReg(4)
    cr = CReg(4)

    circuit = QuantumCircuit(qr, cr)

    circuit.h(qr[0])  
    circuit.cx(qr[0], qr[1])  
    circuit.cx(qr[1], qr[2])  

    circuit.measure(qr, cr)  

    return circuit


def execute_simulator(circuit, shots=1024):
    print('\n executing the qasm simulator...\n')

    simulator = Aer.get_backend('qasm_simulator')
    result = execute(circuit, backend=simulator, shots=shots).result()

    return result


def execute_machine(circuit, device_name='ibmq_essex', shots=1024):
    print('\nexecuting on the {}...\n'.format(device_name))

    Quantum_Simulator.load_account()

    provider = Quantum_Simulator.get_provider('ibm-q')
    device = provider.get_backend(device_name)

    job = execute(circuit, backend=device, shots=shots)
    tools_monitor(job)

    return job.result()


def create_circuit_diagram(circuit, title=''):
    circuit.draw(output='mpl')
    plot.title(title)
    plot.savefig("images/qe_circ.png")
    plot.show()


def create_results(circuit, result, title=''):
    counts = result.get_counts(circuit)
    print(counts)
    plot_histogram(counts)
    plot.title(title)
    plot.savefig("images/qe_res.png")
    plot.show()


if __name__ == '__main__':

    circ = create_circuit()

    res = execute_simulator(circ)


    create_circuit_diagram(circ, '4 quantum bits based qauntum entaglement circuit')
    create_results(circ, res, '4 quantum bits based qauntum entaglement')
