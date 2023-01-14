#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 17 22:55:29 2022

@author: krzysztof
"""

import unittest
import numpy as np
import math
import salto

class TestAxis(unittest.TestCase):

    def test_axis(self):
        
        A = np.array([-10, 2])
        B = np.array([5, 18])
        C = np.array([-6, 15])
        
        new_axis = salto.axis(A, B)
        
        C_scalar_projection = new_axis(C)
        
        assert math.isclose(C_scalar_projection, 1.253892, abs_tol=0.00001)
        
    def test_different_vector_sisze(self):
        
        A = np.array([-10, 2, 3])
        B = np.array([5, 18])
        
        with self.assertRaises(ValueError) as context:
            salto.axis(A, B)
            

if __name__ == "__main__":
     unittest.main()

