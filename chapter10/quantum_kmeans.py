import matplotlib.pyplot as plot
import pandas as pand
from qiskit import QuantumRegister, ClassicalRegister
from qiskit import QuantumCircuit
from qiskit import Aer, execute
from numpy import pi

figure, axis = plot.subplots()
axis.set(xlabel='Feature 1', ylabel='Feature 2')


data_input = pand.read_csv('kmeans_input.csv',
    usecols=['Feature 1', 'Feature 2', 'Class'])


isRed = data_input['Class'] == 'Red'
isGreen = data_input['Class'] == 'Green'
isBlack = data_input['Class'] == 'Black'

# Filter data
redData = data_input[isRed].drop(['Class'], axis=1)
greenData = data_input[isGreen].drop(['Class'], axis=1)
blackData = data_input[isBlack].drop(['Class'], axis=1)


y_p = 0.141
x_p = -0.161

xgc = sum(redData['Feature 1']) / len(redData['Feature 1'])
xbc = sum(greenData['Feature 1']) / len(greenData['Feature 1'])
xkc = sum(blackData['Feature 1']) / len(blackData['Feature 1'])

# Finding the y-coords of the centroids
ygc = sum(redData['Feature 2']) / len(redData['Feature 2'])
ybc = sum(greenData['Feature 2']) / len(greenData['Feature 2'])
ykc = sum(blackData['Feature 2']) / len(blackData['Feature 2'])

# Plotting the centroids
plot.plot(xgc, ygc, 'rx')
plot.plot(xbc, ybc, 'gx')
plot.plot(xkc, ykc, 'kx')


plot.plot(x_p, y_p, 'bo')

# Setting the axis ranges
plot.axis([-1, 1, -1, 1])

plot.show()

# Calculating theta and phi values
phi_list = [((x + 1) * pi / 2) for x in [x_p, xgc, xbc, xkc]]
theta_list = [((x + 1) * pi / 2) for x in [y_p, ygc, ybc, ykc]]

quantumregister = QuantumRegister(3, 'quantumregister')


classicregister = ClassicalRegister(1, 'classicregister')

quantum_circuit = QuantumCircuit(quantumregister, classicregister, name='qc')


backend = Aer.get_backend('qasm_simulator')


quantum_results_list = []


for i in range(1, 4):
    quantum_circuit.h(quantumregister[2])

   
    quantum_circuit.u3(theta_list[0], phi_list[0], 0, quantumregister[0])           
    quantum_circuit.u3(theta_list[i], phi_list[i], 0, quantumregister[1]) 

    quantum_circuit.cswap(quantumregister[2], quantumregister[0], quantumregister[1])
    quantum_circuit.h(quantumregister[2])

    quantum_circuit.measure(quantumregister[2], classicregister[0])

    quantum_circuit.reset(quantumregister)

    job = execute(quantum_circuit, backend=backend, shots=1024)
    result = job.result().get_counts(quantum_circuit)
    quantum_results_list.append(result['1'])

print(quantum_results_list)



class_list = ['Red', 'Green', 'Black']


quantum_p_class = class_list[quantum_results_list.index(min(quantum_results_list))]


distances_list = [((x_p - i[0])**2 + (y_p - i[1])**2)**0.5 for i in [(xgc, ygc), (xbc, ybc), (xkc, ykc)]]
classical_p_class = class_list[distances_list.index(min(distances_list))]

print("""using quantumdistance algorithm,
 the new data point is related to the""", quantum_p_class, 
 'class.\n')
print('Euclidean distances are listed: ', distances_list, '\n')
print("""based on euclidean distance calculations,
 the new data point is related to the""", classical_p_class, 
 'class.')