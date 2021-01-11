import pennylane as quantumPenny
from pennylane import numpy as nump
from pennylane.optimize import  NesterovMomentumOptimizer as NMO

device = quantumPenny.device('default.qubit', wires=2)


def CalcAngles(xval):

    beta0_val = 2 * nump.arcsin(nump.sqrt(xval[1]) ** 2 / nump.sqrt(xval[0] ** 2 + xval[1] ** 2 + 1e-12) )
    beta1_val = 2 * nump.arcsin(nump.sqrt(xval[3]) ** 2 / nump.sqrt(xval[2] ** 2 + xval[3] ** 2 + 1e-12) )
    beta2_val = 2 * nump.arcsin(nump.sqrt(xval[2] ** 2 + xval[3] ** 2) / nump.sqrt(xval[0] ** 2 + xval[1] ** 2 + xval[2] ** 2 + xval[3] ** 2))

    return nump.array([beta2_val, -beta1_val / 2, beta1_val / 2, -beta0_val / 2, beta0_val / 2])


def CalcState(arr):

    quantumPenny.RY(arr[0], wires=0)

    quantumPenny.CNOT(wires=[0, 1])
    quantumPenny.RY(arr[1], wires=1)
    quantumPenny.CNOT(wires=[0, 1])
    quantumPenny.RY(arr[2], wires=1)

    quantumPenny.PauliX(wires=0)
    quantumPenny.CNOT(wires=[0, 1])
    quantumPenny.RY(arr[3], wires=1)
    quantumPenny.CNOT(wires=[0, 1])
    quantumPenny.RY(arr[4], wires=1)
    quantumPenny.PauliX(wires=0)


def CalcLayer(Warr):

    quantumPenny.Rot(Warr[0, 0], Warr[0, 1], Warr[0, 2], wires=0)
    quantumPenny.Rot(Warr[1, 0], Warr[1, 1], Warr[1, 2], wires=1)

    quantumPenny.CNOT(wires=[0, 1])
    

@quantumPenny.qnode(device)
def FindCircuit(weight, angle=None):

    CalcState(angle)
    
    for W in weight:
        CalcLayer(W)

    return quantumPenny.expval(quantumPenny.PauliZ(0))


def GetVariationalClassifier(var, angle=None):

    weight = var[0]
    bias_val = var[1]

    return FindCircuit(weight, angle=angle) + bias_val


def CalcSquareLoss(label, prediction):
    loss_val = 0
    for l, p in zip(label, prediction):
        loss_val = loss_val + (l - p) ** 2
    loss_val = loss_val / len(label)

    return loss_val


def CalcAccuracy(label, prediction):

    loss_val = 0
    for l, p in zip(label, prediction):
        if abs(l - p) < 1e-5:
            loss_val = loss_val + 1
    loss_val = loss_val / len(label)

    return loss_val


def CalcCost(weight, feature, label):

    prediction = [GetVariationalClassifier(weight, angle=f) for f in feature]

    return CalcSquareLoss(label, prediction)


data_iris_flowers = nump.loadtxt("iris_flower_data.txt")
XVal = data_iris_flowers[:, 0:2]

pad = 0.3 * nump.ones((len(XVal), 1))
XPad = nump.c_[nump.c_[XVal, pad], nump.zeros((len(XVal), 1)) ] 

norm = nump.sqrt(nump.sum(XPad ** 2, -1))
X_norm = (XPad.T / norm).T  

ftrs = nump.array([CalcAngles(x) for x in X_norm])   

YVal = data_iris_flowers[:, -1]

nump.random.seed(0)
num_data = len(YVal)
num_train = int(0.75 * num_data)
index = nump.random.permutation(range(num_data))
feats_train = ftrs[index[:num_train]]
YValT = YVal[index[:num_train]]
ftrs_val = ftrs[index[num_train:]]
Y_val = YVal[index[num_train:]]

quantumbits = 2
layers = 6
varinit = (0.01 * nump.random.randn(layers, quantumbits, 3), 0.0)

opt = NMO(0.01)
batsize = 5

var = varinit
for it in range(50):

    bat_index = nump.random.randint(0, num_train, (batsize, ))
    features_train_batch = feats_train[bat_index]
    Ytrainbat = YValT[bat_index]
    var = opt.step(lambda v: CalcCost(v, features_train_batch, Ytrainbat), var)

    predict_train = [nump.sign(GetVariationalClassifier(var, angle=f)) for f in feats_train]
    predict_val = [nump.sign(GetVariationalClassifier(var, angle=f)) for f in ftrs_val]

    accuracy_train = CalcAccuracy(YValT, predict_train)
    accuracy_val = CalcAccuracy(Y_val, predict_val)

    print("it value: {:5d} | Cost Features: {:0.7f} | Accuracy training: {:0.7f} | Accuracy for validation: {:0.7f} "
          "".format(it+1, CalcCost(var, ftrs, YVal), accuracy_train, accuracy_val))
