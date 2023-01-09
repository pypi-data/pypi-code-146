import unittest
import pyfaust as pf
from pyfaust.lazylinop import (LazyLinearOp, vstack, hstack, LazyLinearOp,
                               LazyLinearOperator, aslazylinearoperator)
import numpy.linalg as LA
import numpy as np

class TestLazyLinearOpFaust(unittest.TestCase):

    def setUp(self):
        self.lop = aslazylinearoperator(pf.rand(10, 15))
        self.lopA = self.lop.toarray()
        self.lop2 = aslazylinearoperator(pf.rand(self.lop.shape[0], self.lop.shape[1]))
        self.lop2A = self.lop2.toarray()
        self.lop3 = aslazylinearoperator(pf.rand(self.lop.shape[1], self.lop.shape[0]))
        self.lop3A = self.lop3.toarray()

    def test_shape(self):
        self.assertEqual(self.lop.shape, self.lopA.shape)

    def test_ndim(self):
        self.assertEqual(self.lop.ndim, 2)

    def test_transp(self):
        lopT = self.lop.T
        self.assertAlmostEqual(LA.norm(lopT.toarray()-self.lopA.T), 0)
        lopT = self.lop.transpose()
        self.assertAlmostEqual(LA.norm(lopT.toarray()-self.lopA.T), 0)
        self.assertEqual(self.lop.shape[0], lopT.shape[1])
        self.assertEqual(self.lop.shape[1], lopT.shape[0])

    def test_conj(self):
        lopC = self.lop.conj()
        self.assertAlmostEqual(LA.norm(lopC.toarray()-self.lopA.conj()), 0)

    def test_adjoint(self):
        lopH = self.lop.H
        self.assertAlmostEqual(LA.norm(lopH.toarray()-self.lopA.conj().T), 0)
        lopH = self.lop.getH()
        self.assertAlmostEqual(LA.norm(lopH.toarray()-self.lopA.conj().T), 0)
        self.assertEqual(self.lop.shape[0], lopH.shape[1])
        self.assertEqual(self.lop.shape[1], lopH.shape[0])

    def test_add(self):
        ladd = self.lop + self.lop2
        self.assertAlmostEqual(LA.norm(ladd.toarray()-(self.lopA+self.lop2A)),
                               0)
        M = np.random.rand(*self.lop.shape)
        ladd2 = self.lop + M
        self.assertTrue(isinstance(ladd2, LazyLinearOp))
        self.assertAlmostEqual(LA.norm(ladd2.toarray()-(self.lopA + M)),
                               0)
    def test_iadd(self):
        self.assertRaises(NotImplementedError, self.lop.__iadd__, self.lop2)

    def test_radd(self):
        M = np.random.rand(*self.lop.shape)
        ladd2 = M + self.lop
        self.assertTrue(isinstance(ladd2, LazyLinearOp))
        self.assertAlmostEqual(LA.norm(ladd2.toarray()-(M + self.lopA)), 0)

    def test_sub(self):
        lsub = self.lop - self.lop2
        self.assertAlmostEqual(LA.norm(lsub.toarray() - (self.lopA - self.lop2A)),
                               0)
        M = np.random.rand(*self.lop.shape)
        lsub2 = self.lop - M
        self.assertTrue(isinstance(lsub2, LazyLinearOp))
        self.assertAlmostEqual(LA.norm(lsub2.toarray() - (self.lopA - M)), 0)

    def test_rsub(self):
        M = np.random.rand(*self.lop.shape)
        lsub2 = M - self.lop
        self.assertTrue(isinstance(lsub2, LazyLinearOp))
        self.assertAlmostEqual(LA.norm(lsub2.toarray()-(M - self.lopA)), 0)

    def test_isub(self):
        self.assertRaises(NotImplementedError, self.lop.__isub__, self.lop2)

    def test_matmul_dot_matvec(self):
        from scipy.sparse import csr_matrix, issparse
        lmul = self.lop @ self.lop3
        self.assertTrue(pf.lazylinop.LazyLinearOp.isLazyLinearOp(lmul))
        self.assertAlmostEqual(LA.norm(lmul.toarray() - (self.lopA @ self.lop3A)),
                               0)
        lmul = self.lop.dot(self.lop3)
        self.assertTrue(pf.lazylinop.LazyLinearOp.isLazyLinearOp(lmul))
        self.assertAlmostEqual(LA.norm(lmul.toarray() - (self.lopA @ self.lop3A)),
                               0)
        M = np.random.rand(self.lop.shape[1], 15)
        lmul2 = self.lop @ M
        self.assertTrue(isinstance(lmul2, np.ndarray))
        self.assertAlmostEqual(LA.norm(lmul2 - (self.lopA @ M)),
                               0)

        if self.__class__ == TestLazyLinearOpFaust:
            lmul2 = self.lop @ csr_matrix(M)
            self.assertTrue(isinstance(lmul2, np.ndarray))
            self.assertAlmostEqual(LA.norm(lmul2 - (self.lop @ M)),
                                   0)

        lmul2 = self.lop.matvec(M[:,0])
        self.assertTrue(isinstance(lmul2, np.ndarray))
        self.assertAlmostEqual(LA.norm(lmul2 - (self.lopA @ M[:,0])),
                               0)

        S = csr_matrix(M)
        lmul3 = pf.lazylinop.aslazylinearoperator(S) @ S.T
        self.assertTrue(issparse(lmul3))
        self.assertAlmostEqual(LA.norm(lmul3 - (M @ M.T)),
                               0)

        # test multiplication of a sequence of matrices
        M = np.random.rand(2, 3, 4, self.lop.shape[1], 15)
        np.allclose(self.lop.toarray() @ M, self.lop.toarray() @ M)

    def test_rmatmul(self):
        M = np.random.rand(15, self.lop.shape[0])
        lmul2 = M @ self.lop
        self.assertTrue(isinstance(lmul2, np.ndarray))
        self.assertAlmostEqual(LA.norm(lmul2 - (M @ self.lopA)),
                               0)

    def test_imatmul(self):
        self.assertRaises(NotImplementedError, self.lop.__imatmul__, self.lop2)

    def test_mul(self):
        v = np.random.rand(self.lop.shape[1])
        lmul2 = self.lop * v
        self.assertTrue(isinstance(lmul2, np.ndarray))
        self.assertAlmostEqual(LA.norm(lmul2 - (self.lopA @ v)),
                               0)
        v = np.random.rand(self.lop.shape[1], 1)
        lmul2 = self.lop * v
        self.assertTrue(isinstance(lmul2, np.ndarray))
        self.assertAlmostEqual(LA.norm(lmul2 - (self.lopA @ v)),
                               0)

        s = np.random.rand(1, 1)[0, 0]
        lmul2 = self.lop * s
        self.assertTrue(isinstance(lmul2, LazyLinearOp))
        self.assertAlmostEqual(LA.norm(lmul2.toarray() - (self.lopA * s)),
                               0)

    def test_rmul(self):
        v = np.random.rand(self.lop.shape[0])
        lmul2 = v * self.lop
        self.assertTrue(isinstance(lmul2, np.ndarray))
        self.assertAlmostEqual(LA.norm(lmul2 - (v @ self.lopA)),
                               0)

        v = np.random.rand(1, self.lop.shape[0])
        lmul2 = v @ self.lop
        self.assertTrue(isinstance(lmul2, np.ndarray))
        self.assertAlmostEqual(LA.norm(lmul2 - (v @ self.lopA)),
                               0)

        s = np.random.rand(1, 1)[0, 0]
        self.assertTrue(np.isscalar(s))
        lmul2 = s * self.lop
        self.assertTrue(isinstance(lmul2, LazyLinearOp))
        self.assertAlmostEqual(LA.norm(lmul2.toarray() - (s * self.lopA)),
                               0)

    def test_concatenate(self):
        lcat = self.lop.concatenate(self.lop2, axis=0)
        self.assertAlmostEqual(LA.norm(lcat.toarray() - np.vstack((self.lopA,
                                                                   self.lop2A))),
                               0)
        self.assertEqual(lcat.shape[0], self.lop.shape[0] + self.lop2.shape[0])
        lcat = self.lop.concatenate(self.lop2, axis=1)
        self.assertAlmostEqual(LA.norm(lcat.toarray() - np.hstack((self.lopA,
                                                                   self.lop2A))),
                               0)
        self.assertEqual(lcat.shape[1], self.lop.shape[1] + self.lop2.shape[1])
        # auto concat
        lcat = self.lop.concatenate(self.lop, axis=0)
        self.assertAlmostEqual(LA.norm(lcat.toarray() - np.vstack((self.lopA,
                                                                   self.lopA))),
                               0)
        self.assertEqual(lcat.shape[0], self.lop.shape[0] + self.lop.shape[0])
        # using hstack and vstack
        #TODO: re-enable later (when LazyLinearOp will replace LazyLinearOp)
#        lcat = vstack((self.lop, self.lop2, self.lop))
#        self.assertAlmostEqual(LA.norm(lcat.toarray() - np.vstack((self.lopA,
#                                                                   self.lop2A,
#                                                                  self.lopA))),
#                               0)
#        self.assertEqual(lcat.shape[0], 2 * self.lop.shape[0] + self.lop2.shape[0])
#        lcat = hstack((self.lop, self.lop2, self.lopA))
#        self.assertAlmostEqual(LA.norm(lcat.toarray() - np.hstack((self.lopA,
#                                                                   self.lop2A,
#                                                                  self.lopA))),
#                               0)
#        self.assertEqual(lcat.shape[1], 2 * self.lop.shape[1] + self.lop2.shape[1])



    def test_chain_ops(self):
        lchain = self.lop + self.lop2
        lchain = lchain @ self.lop3
        lchain = 2 * lchain * 3
        self.assertTrue(np.allclose(lchain.toarray(), 6 * (self.lopA + self.lop2A) @ self.lop3A))
        lchain = lchain.concatenate(self.lop3, axis=0)
        mat_ref = np.vstack(((2 * (self.lopA + self.lop2A) @ self.lop3A * 3),
                             self.lop3A))
        self.assertAlmostEqual(LA.norm(lchain.toarray() - mat_ref),
                               0)

    def test_get_item(self):
        n1 = self.lop.shape[0]//2
        n2 = self.lop.shape[1]//2
        lslice = self.lop[3:n1, 3:n2]
        lsliceA = self.lopA[3:n1, 3:n2]
        self.assertAlmostEqual(LA.norm(lslice.toarray()-lsliceA), 0)

    def test_real(self):
        cF = pf.rand(self.lop.shape[0], self.lop.shape[1], field='complex')
        lcF = LazyLinearOp.create_from_op(cF)
        lcF = lcF.real
        self.assertAlmostEqual(LA.norm(lcF.toarray()-cF.real.toarray()), 0)

    def test_imag(self):
        cF = pf.rand(self.lop.shape[0], self.lop.shape[1], field='complex')
        lcF = LazyLinearOp.create_from_op(cF)
        lcF = lcF.imag
        self.assertAlmostEqual(LA.norm(lcF.toarray()-cF.imag.toarray()), 0)

    def test_aslazylinop(self):
        from pyfaust.lazylinop import aslazylinearoperator
        cF = pf.rand(self.lop.shape[0], self.lop.shape[1], field='complex')
        #TODO: re-enable later (when LazyLinearOp will replace LazyLinearOp)
#        lcF = aslazylinearoperator(cF)
#        self.assertTrue(pf.lazylinop.LazyLinearOp.isLazyLinearOp(lcF))
#        self.assertEqual(cF.shape, lcF.shape)

class TestLazyLinearOpFFTFunc(TestLazyLinearOpFaust):

    def setUp(self):
        from scipy.fft import fft, ifft
        # axis = 0 to be consistent with LazyLinearOp.toarray() which applies
        # fft on columns of the matrix, not on the rows (axis=1)
        self.lop = LazyLinearOperator((8, 8), matmat=lambda x: fft(x, axis=0),
                                      rmatmat=lambda x: 8 * ifft(x, axis=0))
        self.lopA = self.lop.toarray()
        self.lop2 = aslazylinearoperator(pf.rand(self.lop.shape[0], self.lop.shape[1]))
        self.lop2A = self.lop2.toarray()
        self.lop3 = aslazylinearoperator(pf.rand(self.lop.shape[1], self.lop.shape[0]))
        self.lop3A = self.lop3.toarray()

class TestLazyLinearOpFaustKron(TestLazyLinearOpFaust):

    def setUp(self):
        from pyfaust.lazylinop import kron as lkron
        lop_A = aslazylinearoperator(pf.rand(10, 15))
        lop_B = aslazylinearoperator(pf.rand(10, 15))
        self.lop = lkron(lop_A, lop_B)
        self.lopA = self.lop.toarray()
        self.lop2 = aslazylinearoperator(pf.rand(*self.lop.shape))
        self.lop2A = self.lop2.toarray()
        self.lop3 = aslazylinearoperator(pf.rand(self.lop.shape[1], 10))
        self.lop3A = self.lop3.toarray()

class TestLazyLinearOpEye(TestLazyLinearOpFaust):

    def setUp(self):
        from pyfaust.lazylinop import eye
        self.lop = eye(8, 12)
        self.lopA = self.lop.toarray()
        self.lop2 = eye(*self.lop.shape, k=2)
        self.lop2A = self.lop2.toarray()
        self.lop3 = eye(self.lop.shape[1], self.lop.shape[0], k=-2)
        self.lop3A = self.lop3.toarray()

class TestLazyLinearOpDiag(TestLazyLinearOpFaust):

    def setUp(self):
        from pyfaust.lazylinop import diag
        v = np.random.rand(10)
        self.lop = diag(v, k=2)
        self.lopA = self.lop.toarray()
        self.lop2 = diag(v, k=-2)
        self.lop2A = self.lop2.toarray()
        self.lop3 = diag(v, k=2)
        self.lop3A = self.lop3.toarray()

class TestLazyLinearOpBlkDiag(TestLazyLinearOpFaust):

    def setUp(self):
        from pyfaust.lazylinop import block_diag
        from scipy.linalg import block_diag as sblock_diag
        from pyfaust import rand
        A = rand(12, 14)
        B = rand(13, 15)
        C = rand(14, 16)
        self.lop = block_diag(A, B, C)
        self.lopA = sblock_diag(A.toarray(), B.toarray(), C.toarray())
        self.lop2 = block_diag(A+A, B+B, C+C)
        self.lop2A = sblock_diag(2 * A.toarray(), 2 * B.toarray(), 2 * C.toarray())
        self.lop3 = block_diag(C.T, B.T, A.T)
        self.lop3A = sblock_diag(C.T.toarray(), B.T.toarray(), A.T.toarray())

class TestLazyLinearOpSum(TestLazyLinearOpFaust):

    def setUp(self):
        from pyfaust.lazylinop import sum
        from pyfaust import rand
        A = rand(12, 14)
        B = rand(12, 14)
        C = rand(12, 14)
        self.lop = sum(A, B, C)
        self.lopA = np.add.reduce([A.toarray(), B.toarray(), C.toarray()])
        self.lop2 = sum(A+A, B+B, C+C)
        self.lop2A = np.add.reduce([2 * A.toarray(), 2 * B.toarray(), 2 * C.toarray()])
        self.lop3 = sum(C.T, B.T, A.T)
        self.lop3A = np.add.reduce([C.T.toarray(), B.T.toarray(), A.T.toarray()])

if '__main__' == __name__:
    unittest.main()
