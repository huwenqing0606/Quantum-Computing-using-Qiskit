# initialization
import numpy as np

# importing Qiskit
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, assemble, transpile

# import basic plot tools
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

# the demonstration of Deutsch-Jozsa Algorithm, including 
#   (1) the constant oracle
#   (2) the balanced oracle
#   (3) the Deiutsch-Jozsa circuit
def dj_demonstrate(n):

    # build the const oracle with X gate at the last (n+1) qubit
    const_oracle = QuantumCircuit(n+1)
    output = np.random.randint(2)
    if output == 1:
        const_oracle.x(n)
    const_oracle.draw(output='mpl')
    plt.show()

    # build the balanced oracle 
    balanced_oracle = QuantumCircuit(n+1)
    b_str = "101"
    # Place X-gates
    for qubit in range(len(b_str)):
        if b_str[qubit] == '1':
            balanced_oracle.x(qubit)
    balanced_oracle.draw(output='mpl')
    plt.show()
    # Use barrier as divider
    balanced_oracle.barrier()
    # Controlled-NOT gates
    for qubit in range(n):
        balanced_oracle.cx(qubit, n)
    balanced_oracle.barrier()
    balanced_oracle.draw(output='mpl')
    plt.show()
    # Place X-gates
    for qubit in range(len(b_str)):
        if b_str[qubit] == '1':
            balanced_oracle.x(qubit)
    # Show oracle
    balanced_oracle.draw(output='mpl')
    plt.show()

    # build the Deutsch-Jozsa circuit
    dj_circuit = QuantumCircuit(n+1, n)
    # Apply H-gates
    for qubit in range(n):
        dj_circuit.h(qubit)
    # Put qubit in state |->
    dj_circuit.x(n)
    dj_circuit.h(n)
    dj_circuit.draw(output='mpl')
    plt.show()
    # Add oracle
    dj_circuit += balanced_oracle
    dj_circuit.draw(output='mpl')
    plt.show()
    # Repeat H-gates
    for qubit in range(n):
        dj_circuit.h(qubit)
    dj_circuit.barrier()
    # Measure
    for i in range(n):
        dj_circuit.measure(i, i)
    # Display circuit
    dj_circuit.draw(output='mpl')
    plt.show()

    return dj_circuit

# the oracle gate for Deutsch-Jozsa Algorithm to detect difference: case='balanced' or 'constant'
def dj_oracle(case, n):
    # We need to make a QuantumCircuit object to return
    # This circuit has n+1 qubits: the size of the input,
    # plus one output qubit
    oracle_qc = QuantumCircuit(n+1)
    
    # First, let's deal with the case in which oracle is balanced
    if case == "balanced":
        # First generate a random number that tells us which CNOTs to
        # wrap in X-gates:
        b = np.random.randint(1,2**n)
        # Next, format 'b' as a binary string of length 'n', padded with zeros:
        b_str = format(b, '0'+str(n)+'b')
        # Next, we place the first X-gates. Each digit in our binary string 
        # corresponds to a qubit, if the digit is 0, we do nothing, if it's 1
        # we apply an X-gate to that qubit:
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)
        # Do the controlled-NOT gates for each qubit, using the output qubit 
        # as the target:
        for qubit in range(n):
            oracle_qc.cx(qubit, n)
        # Next, place the final X-gates
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                oracle_qc.x(qubit)

    # Case in which oracle is constant
    if case == "constant":
        # First decide what the fixed output of the oracle will be
        # (either always 0 or always 1)
        output = np.random.randint(2)
        if output == 1:
            oracle_qc.x(n)
    
    oracle_gate = oracle_qc.to_gate()
    oracle_gate.name = case+"_Oracle" # To show when we display the circuit
    return oracle_gate

# run the Deutsch-Jozsa circuit
def dj_algorithm(oracle, n):
    dj_circuit = QuantumCircuit(n+1, n)
    # Set up the output qubit:
    dj_circuit.x(n)
    dj_circuit.h(n)
    # And set up the input register:
    for qubit in range(n):
        dj_circuit.h(qubit)
    # Let's append the oracle gate to our circuit:
    dj_circuit.append(oracle, range(n+1))
    # Finally, perform the H-gates again and measure:
    for qubit in range(n):
        dj_circuit.h(qubit)
    
    for i in range(n):
        dj_circuit.measure(i, i)
    
    return dj_circuit


if __name__=='__main__':
    n = 3
    demonstrate = 1
    if demonstrate:
        dj_circuit = dj_demonstrate(n)
        # use local simulator
        aer_sim = Aer.get_backend('aer_simulator')
        shots = 1024
        qobj = assemble(dj_circuit, aer_sim)
        results = aer_sim.run(qobj).result()
        answer = results.get_counts()
        plot_histogram(answer)
        plt.show()
    else:
        oracle_gate = dj_oracle('balanced', n)
        dj_circuit = dj_algorithm(oracle_gate, n)
        dj_circuit.draw(output='mpl')
        plt.show()

        aer_sim = Aer.get_backend('aer_simulator')
        transpiled_dj_circuit = transpile(dj_circuit, aer_sim)
        qobj = assemble(transpiled_dj_circuit)
        results = aer_sim.run(qobj).result()
        answer = results.get_counts()
        plot_histogram(answer)
        plt.show()

    
