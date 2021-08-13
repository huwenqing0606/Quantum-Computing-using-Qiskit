import numpy as np
from numpy import pi
# importing Qiskit
from qiskit import QuantumCircuit, transpile, assemble, Aer, IBMQ
from qiskit.providers.ibmq import least_busy
from qiskit.tools.monitor import job_monitor
# import basic plot tools
from qiskit.visualization import plot_histogram, plot_bloch_multivector
import matplotlib.pyplot as plt

def QFourier_demonstrate():
    
    qc = QuantumCircuit(3)

    # Encode the state 5
    qc.x(0)
    qc.x(2)
    qc.draw(output='mpl')
    plt.show()

    qc.h(2)
    qc.draw(output='mpl')
    plt.show()

    qc.cp(pi/2, 1, 2) # CROT from qubit 1 to qubit 2
    qc.draw(output='mpl')
    plt.show()

    qc.cp(pi/4, 0, 2) # CROT from qubit 2 to qubit 0
    qc.draw(output='mpl')
    plt.show()

    qc.h(1)
    qc.cp(pi/2, 0, 1) # CROT from qubit 0 to qubit 1
    qc.h(0)
    qc.draw(output='mpl')
    plt.show()

    qc.swap(0,2)
    qc.draw(output='mpl')   
    plt.show()

    return qc


if __name__=='__main__':

    demonstrate=1
    if demonstrate:
        qc=QFourier_demonstrate()
    else:
        qc=None

    sim = Aer.get_backend("aer_simulator")
    qc.save_statevector()
    statevector = sim.run(qc).result().get_statevector()
    plot_bloch_multivector(statevector)
    plt.show()


