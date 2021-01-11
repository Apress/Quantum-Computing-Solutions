import renom_q.ml.quantum_svm
quantum_svm = renom_q.ml.quantum_svm.QSVM()
xval = [[3, 4], [5, 6], [7, 9], [8, 6]]
yval = [1, -1, 1, -1]
quantum_svm.plot_graph(xval, yval)