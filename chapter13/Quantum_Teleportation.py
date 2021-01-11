

from qiskit import QuantumCircuit as QC
from qiskit import IBMQ as Quantum_Simulator
from qiskit import Aer as Quantum_AER
from qiskit import execute
import matplotlib.pyplot as plot
from qiskit.tools.monitor import job_monitor as tools_monitor
from qiskit.tools.visualization import plot_histogram as histogram


def create_circuit():
    circ = QC(4, 4)

    circ.x(0)
    circ.barrier()

    circ.h(1)
    circ.cx(1, 2)
    circ.cx(0, 1)
    circ.h(0)
    circ.barrier()

    circ.measure(0, 0)
    circ.measure(1, 1)
    circ.barrier()

    circ.cx(1, 3)
    circ.cz(0, 3)
    circ.barrier()

    circ.measure(2, 2)

    return circ


def execute_simulator(circ, shots=1024):
    print('\nexecute the qasm simulator...\n')

    sim = Quantum_AER.get_backend('qasm_simulator')
    result = execute(circ, backend=sim, shots=shots).result()

    return result


def execute_machine(circ, device_name='ibmq_essex', shots=1024):
    print('\nexecuting on {}...\n'.format(device_name))

    Quantum_Simulator.load_account()

    provider = Quantum_Simulator.get_provider('ibm-q')
    device = provider.get_backend(device_name)

    job = execute(circ, backend=device, shots=shots)
    tools_monitor(job)

    return job.result()


def create_circuit_diagram(circ, title=''):
    circ.draw(output='mpl')
    plot.title(title)
    plot.savefig("images/qt_circ.png")
    plot.show()


def create_results_plot(result, title=''):
    counts = result.get_counts()
    print('\ncounts are : {}\n'.format(counts))
    histogram(counts)
    plot.title(title)
    plot.savefig("images/qt_res.png")
    plot.show()


if __name__ == '__main__':
    circ = create_circuit()

    create_circuit_diagram(circ, ' quantum teleportation circuit')

    result = execute_simulator(circ)
    

    create_results_plot(result, ' quantum teleportation output')
