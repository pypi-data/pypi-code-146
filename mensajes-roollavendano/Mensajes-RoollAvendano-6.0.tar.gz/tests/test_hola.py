import unittest
import numpy as np

from mensajes.hola.saludo import generar_array

class PruebasHola(unittest.TestCase):
    def test_generar_array(self):
        ## usamos la propia funcion de numopy en vez del clasico assert
        np.testing.assert_array_equal(
            np.array([0,1,2,3,4,5]),
            generar_array(6)
        )




