"""
References
----------

Local optimization:
    - Unconstrained minimization
        1. Hooke-Jeeves method
            1961. R.Hooke, T.A.Jeeves.
            ``Direct Search'' Solution of Numerical and Statistical Problems.
            doi:10.1145/321062.321069
        2. CG (a nonlinear conjugate gradient algorithm by Polak and Ribiere)
            2006. J.Nocedal, S.J.Wright. Numerical Optimization. P.120-122.
        3. BFGS (method of Broyden, Fletcher, Goldfarb, and Shanno)
            2006. J.Nocedal, S.J.Wright. Numerical Optimization. P.136.
        4. Newton-CG (truncated Newton method)
            2006. J.Nocedal, S.J.Wright. Numerical Optimization. P.168.
        5. The dog-leg trust-region algorithm.
            2006. J.Nocedal, S.J.Wright. Numerical Optimization.
        6. The Newton conjugate gradient trust-region algorithm
            2006. J.Nocedal, S.J.Wright. Numerical Optimization.
        7. The Newton GLTR trust-region algorithm
            1999. N.I.M.Gould et al.
            Solving The Trust-Region Subproblem Using The Lanczos Method.

            2018. F.Lenders, C.Kirches, A.Potschka.
            Trlib. A Vector-Free Implementation Of The GLTR Method
            For Iterative Solution Of The Trust Region Problem.

    - Bound-Constrained minimization
        1. Nelder-Mead
            1965. J.A.Nelder, R.Mead.
            A Simplex Method For Function Minimization.
        2. L-BFGS-B algorithm
            1995. R.H.Byrd et al.
            A Limited Memory Algorithm For Bound Constrained Optimization.

            1997. C.Zhu et al.
            Algorithm 778. L-BFGS-B. Fortran Subroutines
            For Large-Scale Bound Constarined Optimization.
        3. Powell’s method
            1964. M.J.D.Powell.
            An Efficient Method For Finding The Minimum Of A Function
            Of Several Variables Without Calculating Derivatives.

            2007. W.H.Press et al.
            Numerical Recipes. The Art Of Scientific Computing.
        4. A truncated Newton algorithm
            2006. J.Nocedal, S.J.Wright. Numerical Optimization. P.168.

            1984. S.G.Nash.
            Newton-Type Minimization Via The Lanczos Method.


    - Constrained Minimization.
        1. The Constrained Optimization BY Linear Approximation (COBYLA)
            1998. M.J.D.Powell.
            Direct Search Algorithms For Optimization Calculations.

            2007. M.J.D.Powell.
            A View Of Algorithms For Optimization Without Derivatives.
        2. Sequential Least Squares Programming (SLSQP)
            1988. D.Kraft.
            A Software Package For Sequential Quadratic Programming.
        3. A trust-region algorithm for constrained optimization
            2006. J.Nocedal, S.J.Wright. Numerical Optimization. P.549.

            1998. M.Lalee, J.Nocedal, T.Plantenga.
            On The Implementation Of An Algorithm
            For Large-Scale Equality Constrained Optimization.

            1999. R.H.Byrd, M.E.Hribar, J.Nocedal.
            An Interior Point Algorithm For Large-Scale Nonlinear Programming.

Global optimization:
    1. Radial Movement Optimization
        2014. R.Rahmani, R.Yusof.
        A New Simple, Fast And Efficient Algorithm
        For Global Optimization Over Continuous Search-Space Problems.
        Radial Movement Optimization.

    2. Differential Evolution
        1997. R.Storn, K.Price.
        Differential Evolution –
        A Simple And Efficient Heuristic
        For Global Optimization Over Continuous Spaces
        doi:10.1023/a:1008202821328


"""


from .hj import HookeJeeves
from .pca import PrincipalComponentAnalysis
from .pso import ParticleSwarmOptimization
from .rmo import RadialMovementOptimization
