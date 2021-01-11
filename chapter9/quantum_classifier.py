
import qclassify

from qclassify.preprocessing import *
from qclassify.encoding_circ import *
from qclassify.qclassifier import QClassifier as QuantumClassifier
from qclassify.proc_circ import *
from qclassify.postprocessing import *

encoding_opts={
                'preprocessing':id_func,        
                'encoding_circ':x_product,      
        }





process_opts={
                'proc_circ':layer_xz,   
                'postprocessing':{
                        'quantum':measure_top, 
                        'classical':prob_one, 
                }
        }






quantum_bits = [0, 1] 
classify_opts = {
                'encoder_options':encoding_opts,
                'proc_options':process_opts,
        }
qCircuit = QuantumClassifier(quantum_bits, classify_opts)





circuit_values = [1, 1] 
params = [2.0672044712460114,          1.3311348339721203] 

quantum_circuit_prog = qCircuit.circuit(circuit_values, params) 

print(quantum_circuit_prog)





