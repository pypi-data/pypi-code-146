"""
Init for qnn
"""
# pylint: disable=redefined-builtin
from .measure import expval,ProbsMeasure,QuantumMeasure,\
    DensityMatrixFromQstate,VN_Entropy,Mutal_Info,Hermitian_expval,MeasurePauliSum,VarMeasure,Purity
from .quantumlayer import NoiseQuantumLayer,QuantumLayer,\
    QuantumLayerMultiProcess,QuantumLayerV2,grad
from .template import CSWAPcircuit,IQPEmbeddingCircuits,\
    AmplitudeEmbeddingCircuit,AngleEmbeddingCircuit,\
        RotCircuit,BasicEmbeddingCircuit,CRotCircuit,CCZ,Controlled_Hadamard,\
           StronglyEntanglingTemplate, BasicEntanglerTemplate,RandomTemplate,SimplifiedTwoDesignTemplate
from . import pqc, qae, qdrl, qgan, qlinear, qcnn, qvc, utils, svm, qp
from .opt import SPSA, QNG, insert_pauli_for_mt, get_metric_tensor
from .qembed import Quantum_Embedding
