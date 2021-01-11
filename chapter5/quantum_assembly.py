import qiskit

class QASM_JobManager:

    def __init__(self):
      	self.data = []
        
    def createProgram(self,quantum,classical):
        qr = qiskit.QuantumRegister(quantum)
        cr = qiskit.ClassicalRegister(classical)
        program = qiskit.QuantumCircuit(qr, cr)
        return qr,cr,program
    
    def measure(self,program,qr,cr):
        program.measure(qr,cr)
            
    def getQASMBackend(self):
        backend = qiskit.BasicAer.get_backend('qasm_simulator')
        return backend
    
    def executeProgramOnQASM(self,program,backend):
        job = qiskit.execute( program, backend  )
        return job
        

jobManager = QASM_JobManager()

quantumRegister,classicalRegister,program = jobManager.createProgram(1,1)

jobManager.measure(program,quantumRegister,classicalRegister)


backend = jobManager.getQASMBackend()

print("The device name:",backend.name())


job = jobManager.executeProgramOnQASM(program,backend)

print( job.result().get_counts() )


