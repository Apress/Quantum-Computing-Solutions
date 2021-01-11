import pennylane as quantumDeepL
from pennylane import numpy as npython
from pennylane.optimize import GradientDescentOptimizer as GDOpt
dev = quantumDeepL.device('default.qubit', wires=2)
def FindAnsatz():
    quantumDeepL.Rot(0.3, 1.8, 5.4, wires=1)
    quantumDeepL.RX(-0.5, wires=0)
    quantumDeepL.RY( 0.5, wires=1)
    quantumDeepL.CNOT(wires=[0, 1])
@quantumDeepL.qnode(dev)
def FindCircuitX():
    FindAnsatz()
    return quantumDeepL.expval(quantumDeepL.PauliX(1))
@quantumDeepL.qnode(dev)
def FindCircuitY():
    FindAnsatz()
    return quantumDeepL.expval(quantumDeepL.PauliY(1))
def getCost(var):
    expX = FindCircuitX()
    expY = FindCircuitY()
    return (var[0] * expX + var[1] * expY) ** 2
optimizer = GDOpt(0.5)
variables = [0.3, 2.5]
variables_gd = [variables]
for i in range(20):
    variables = optimizer.step(getCost, variables)
    variables_gd.append(variables)
    print('Cost - step {:5d}: {: .7f} | Variable values: [{: .5f},{: .5f}]'
          .format(i+1, getCost(variables), variables[0], variables[1]) )