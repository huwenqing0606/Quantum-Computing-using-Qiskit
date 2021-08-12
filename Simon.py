# importing Qiskit
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, transpile, assemble

# import basic plot tools
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# construct the oracle function for Simon's algorithm
# case of 2 qubits and the secret string b='11' 
def Simon_oracle_11(b):
    b_str=str(b)
    n=len(b_str)
    oracle_qc = QuantumCircuit(2*n)
    # using CNOT gates, create a copy of input in the first register
    for qubit in range(n):
        oracle_qc.cx(qubit, n+qubit)
    # separate the copy part and the XOR part visually
    oracle_qc.barrier()
    # the XOR part for b='11'
    oracle_qc.cx(0,3)
    oracle_qc.cx(1,2)

    return oracle_qc

# Calculate the dot product of the results
def bdotz(b, z):
    accum = 0
    for i in range(len(b)):
        accum += int(b[i]) * int(z[i])
    return (accum % 2)
    
if __name__=='__main__':
    # Implement the circuit for Simon's algorithm
    # n=2 and b='11'
    b='11'
    n=len(b)
    Simon_circuit = QuantumCircuit(2*n, n)
    # Apply Hadamard gates before querying the oracle
    Simon_circuit.h(range(n))
    # Apply barrier for visual separation
    Simon_circuit.barrier()
    # Apply the Simon oracle for b='11'
    Simon_circuit += Simon_oracle_11(b)  
    # Apply barrier for visual separation
    Simon_circuit.barrier()
    # Apply Hadamard gates to the input register
    Simon_circuit.h(range(n))
    # Measure qubits
    Simon_circuit.measure(range(n), range(n))
    Simon_circuit.draw(output='mpl')
    plt.show()

    # use local simulator
    aer_sim = Aer.get_backend('aer_simulator')
    shots = 1024
    qobj = assemble(Simon_circuit, shots=shots)
    results = aer_sim.run(qobj).result()
    counts = results.get_counts()
    plot_histogram(counts)
    plt.show()
    
    # check b\cdot z=0 for all outputs z
    for z in counts:
        print('{}.{} = {} (mod 2)'.format(b, z, bdotz(b,z)) )
