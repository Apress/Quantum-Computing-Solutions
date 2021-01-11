

import pennylane as qnnL
from pennylane import numpy as numcal
from pennylane.optimize import AdamOptimizer as AdamO

try:
    device = qnnL.device('strawberryfields.fock', wires=1, cutoff_dim=10)    
except:
    print("please install the package strawberryfields")


def GetQNNLayer(varr):
    """ One layer of the quantum neural network
    """
    qnnL.Rotation(varr[0], wires=0)
    qnnL.Squeezing(varr[1], 0., wires=0)
    qnnL.Rotation(varr[2], wires=0)

    qnnL.Displacement(varr[3], 0., wires=0)

    qnnL.Kerr(varr[4], wires=0)


@qnnL.qnode(device)
def GetQNN(vars, xcoor=None):
    """ Returns The quantum neural network 
    """

    qnnL.Displacement(xcoor, 0., wires=0)

    for var in vars:
        GetQNNLayer(var)

    return qnnL.expval.X(0)


def GetQNNSquareLoss(labelValues, predictionValues):
    """ Get the Square loss function
    """
    lossValue = 0
    for label, prediction in zip(labelValues, predictionValues):
        lossValue = lossValue + (label - prediction) ** 2
    lossValue = lossValue / len(labelValues)

    return lossValue


def GetQNNCost(variables, featureValues, labelValues):
    """ Minimizing Cost function 
    """
    
    predictions = [GetQNN(variables, xcoor=x) for x in featureValues]
    
    return GetQNNSquareLoss(labelValues, predictions)

sincurvevalues = numcal.loadtxt("sin_curve_values.txt")
xcoordinate= sincurvevalues[:, 0]
ycoordinate = sincurvevalues[:, 1]

numcal.random.seed(0)
layer_recount = 4
variable_initial = 0.05 * numcal.random.randn(layer_recount, 5)

optimizer = AdamO(0.01, beta1=0.9, beta2=0.999)


variable = variable_initial

for iteration in range(500):
    var_cost = optimizer.step(lambda v: GetQNNCost(v, xcoordinate, ycoordinate), variable)
    
    print("Iteration value: {:5d} | Cost is: {:0.7f} ".format(iteration + 1, GetQNNCost(var_cost, xcoordinate, ycoordinate)))
