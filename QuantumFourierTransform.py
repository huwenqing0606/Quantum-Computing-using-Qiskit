import numpy as np
from numpy import pi
# importing Qiskit
from qiskit import QuantumCircuit, transpile, assemble, Aer, IBMQ
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
# import basic plot tools
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import matplotlib.pyplot as plt

# demonstrate a simple 4 qubit Quantum Fourier Transform circuit
def QFourier_demonstrate(qc_init):
    
    qc = QuantumCircuit(4)

    qc += qc_init
    qc.barrier()
    qc.draw(output='mpl')
    plt.show()

    qc.h(0)
    qc.barrier()
    qc.draw(output='mpl')
    plt.show()

    qc.cp(pi/2, 0, 1) # CROT from qubit 0 to qubit 1
    qc.barrier()
    qc.draw(output='mpl')
    plt.show()

    qc.cp(pi/4, 0, 2) # CROT from qubit 0 to qubit 2
    qc.cp(pi/8, 0, 3) # CROT from qubit 0 to qubit 3
    qc.barrier()
    qc.draw(output='mpl')
    plt.show()

    qc.h(1)
    qc.cp(pi/2, 1, 2) # CROT from qubit 1 to qubit 2
    qc.cp(pi/4, 1, 3) # CROT from qubit 1 to qubit 3
    qc.h(2)
    qc.cp(pi/2, 2, 3) # CROT from qubit 2 to qubit 3
    qc.h(3)
    qc.barrier()
    qc.draw(output='mpl')
    plt.show()

    qc.swap(0,3)
    qc.swap(1,2)
    qc.draw(output='mpl')   
    plt.show()

    return qc


# recursively build the sequence of H and CROT gates for QFT circuit
def QFourier_H_CROT(circuit, k, n):
    if k==n:
        return circuit
    circuit.h(k)
    for target_qubit in range(k+1, n):
        circuit.cp(pi/2**(target_qubit-k), k, target_qubit)
    circuit.barrier()

    QFourier_H_CROT(circuit, k+1, n)


# the swap gate of Quantum Fourier Transform 
def QFourier_swap(circuit, n):
    for qubit in range(n//2):
        circuit.swap(qubit, n-qubit-1)
    return circuit


if __name__=='__main__':

    demonstrate = 0
    if demonstrate:
        # Encode the initial state
        qc_init = QuantumCircuit(4)
        qc_init.x(0)
        qc_init.x(2)
        # build the Quantum Fourier Transform circuit for demonstration
        qc=QFourier_demonstrate(qc_init)
    else:
        # n is number of registers, j is the initial state in [0, 2**n-1]
        n = 7
        j = 135
        if (j<0 or j>2**n):
            print('j out of range: 0 to 2**n\n')
        # turn j into binary, highest power of 2 on right
        init_state = bin(j)[2:].zfill(n)[::-1]
        # Encode the initial state
        qc_init = QuantumCircuit(n)
        for qubit in range(n):
            if init_state[qubit]=='1':
                qc_init.x(qubit)
        qc_init.barrier()
        qc_init.draw(output='mpl')
        plt.show()
        # build the Quantum Fourier Transform circuit for demonstration
        qc = qc_init.copy()
        # add the H and CROT gates
        QFourier_H_CROT(qc, 0, n)
        qc.draw(output='mpl')
        plt.show()
        # add the swap gate
        QFourier_swap(qc, n)
        qc.draw(output='mpl')
        plt.show()

        
    # start plotting the change of basis in Quantum Fourier Transform
    sim = Aer.get_backend("aer_simulator")
    # the original basis
    qc_init.save_statevector()
    statevector = sim.run(qc_init).result().get_statevector()
    plot_bloch_multivector(statevector)
    plt.show()
    # the transformed basis
    qc.save_statevector()
    statevector = sim.run(qc).result().get_statevector()
    plot_bloch_multivector(statevector)
    plt.show()


