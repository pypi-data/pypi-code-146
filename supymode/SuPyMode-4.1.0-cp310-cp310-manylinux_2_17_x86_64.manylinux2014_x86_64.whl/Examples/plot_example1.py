"""
2x2 Coupler
===========
"""

# %%
# Importing the package dependencies: FiberFusing, PyOptik [optional]
from FiberFusing import Geometry, Circle, BackGround
from SuPyMode.Solver import SuPySolver
from PyOptik import ExpData

# %%
# Generating the fiber structure
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Here we make use of the FiberFusing to generate a fiber structure that we use
# as the cladding. The refractive index of the strcture is defined using PyOptik.
index = ExpData('FusedSilica').GetRI(1.55e-6)

air = BackGround(index=1)

clad = Circle(position=(0, 0), radius=62.5, index=index)

# %%
# Creating the geometry rasterization
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# The cladding being defined we create the cores that are distributed at
# each (virtual) center of the cladding.
# All the components: air -- cladding -- cores, are inputed into a geometry class
# that will generate the mesh which will be used in the finit-difference matrix.
cores = [Circle(position=clad.center, radius=4.1, index=index + 0.005)]

geometry = Geometry(background=air,
                    clad=clad,
                    cores=cores,
                    x_bound='auto',
                    y_bound='auto',
                    n_x=60,
                    n_y=60,
                    index_scrambling=1e-6)

_ = geometry.plot().show()

# %%
# We here create the solver class and generate the superset which
# will contains the supermodes to be computed.
solver = SuPySolver(geometry=geometry, tolerance=1e-8, max_iter=10000)

solver.init_superset(wavelength=1.55, n_step=500, itr_i=1.0, itr_f=0.05)


# %%
# We now add supermodes for different type of attributes such as boundaries.
# By default the solver assume no boundaries in the system.
_ = solver.add_modes(sorting='field',
                     boundaries={'right': 'zero', 'left': 'zero', 'top': 'zero', 'bottom': 'zero'},
                     n_computed_mode=8,
                     n_sorted_mode=4)

# %%
# The modes are now computed [can take a few minutes], the modes are concatenated
# in a superset class that we can access with the get_set() function. This class
# can be used to analyse the data
superset = solver.get_set()

# %%
# Field computation: :math:`E_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(type='field', itr_list=[1.0, 0.05]).show()

# %%
# After mode visualization we can name them for an easier further analyze.
# This step is, however, not mandatory.
_ = superset.name_supermodes('LP01', 'LP02', 'LP11_v', 'LP11_h')

# %%
# Effective index: :math:`n^{eff}_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(type='index').show()

# %%
# Modal coupling: :math:`C_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(type='coupling').show()

# %%
# Adiabatic criterion: :math:`\tilde{C}_{i,j}`
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
_ = superset.plot(type='adiabatic').show()
