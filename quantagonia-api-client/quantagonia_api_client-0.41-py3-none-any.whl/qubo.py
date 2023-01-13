from __future__ import annotations

import os, os.path
from pydoc import classname
import readline
from unicodedata import numeric
from operator import itemgetter

THIS_SCRIPT = os.path.dirname(os.path.realpath(__file__))

from enum import Enum
from distutils.log import error, warn
from logging import warning
from pickletools import optimize
import sys
from typing import List, Dict, overload
import warnings
import re
import tempfile
import subprocess
import json
import copy
import gzip

try:
    from functools import singledispatchmethod
except:
    from singledispatchmethod import singledispatchmethod

import pyqubo as pq

from pulp import PulpSolverError
from quantagonia.enums import HybridSolverOptSenses

from quantagonia.runner import Runner
from quantagonia.runner_factory import RunnerFactory
from quantagonia.spec_builder import QUBOSpecBuilder

################################################################################
# Class definitions with singledispatch-declarations
################################################################################

class QuboVariable(object):

    def __init__(self, name : str, pos : int, initial=None, fixing=None):
        self.name = name
        self._pos = pos
        if initial and initial not in [0, 1]:
            warnings.warn(f"Initial variable value {initial} not binary. Ignore initial assignment.")
            initial=None
        if fixing and fixing not in [0, 1]:
            warnings.warn(f"Fixing variable value {fixing} not binary. Ignore fixing.")
            initial=None
        if initial and fixing and initial != fixing:
            warnings.warn("Initial != fixing, discard initial and use fixing")
            initial = fixing
        self.fixing = fixing
        self.__assignment = initial

    @property
    def assignment(self):
        return self.__assignment

    @assignment.setter
    def assignment(self, value):
        # check against fixing
        if self.fixing and self.fixing != value:
            error(f"Assigning {value} to {self.name} contradicts fixing {self.fixing}")
        self.__assignment = value

    def id(self):
        return self._pos

    def eval(self):
        if self.assignment is None:
            error("Variable " + self.name + " is still unassigned.")
        return self.assignment

    def __str__(self):
        return self.name

    def key(self):
        return str(self)

    @singledispatchmethod
    def __add__(self, other):
        return NotImplemented

    @singledispatchmethod
    def __sub__(self, other):
        return NotImplemented

    def __radd__(self, other : int | float) -> QuboExpression:
        q = QuboExpression()
        q += QuboTerm(other, [])
        q += self
        return q

    def __rsub__(self, other : int | float) -> QuboExpression:
        q = QuboExpression()
        q += QuboTerm(other, [])
        q -= self
        return q

    @singledispatchmethod
    def __mul__(self, other):
        return NotImplemented

    # other * var -> term
    def __rmul__(self, other : int | float) -> QuboTerm:
        return QuboTerm(other, [self])

class QuboTerm(object):

    def __init__(self, coefficient : float, vars : list):
        super().__init__()
        self.coefficient = coefficient

        # by convention, we only store the upper triangular part of the QUBO ->
        # need to sort the variables ascendingly by their IDs
        self.vars = self._unique_vars(vars)

    def _clone(self):
        return QuboTerm(self.coefficient, copy.copy(self.vars))

    def _join_vars(self, set0 : List[QuboVariable], set1 : List[QuboVariable]) -> List[QuboVariable]:
        return self._unique_vars([*set0, *set1])

    def _unique_vars(self, vars : List[QuboVariable]) -> List[QuboVariable]:
        joint = [(i.key(), i) for i in vars]
        joint = dict(joint)

        return sorted(list(joint.values()), key = lambda v : v.id())

    def key(self):
        return "_".join([str(v) for v in self.vars])

    def order(self):
        return len(self.vars)

    def checkIsQUBO(self):
        return (self.order() <= 2)

    def isValid(self):
        is_valid = self.checkIsQUBO()

        if len(self.vars) > 1:
            is_valid &= (self.vars[0].id() < self.vars[1].id())

        return is_valid

    def eval(self):
        # if term represents just the constant shift
        if self.order() == 0:
            return self.coefficient

        E = self.coefficient * self.vars[0].eval()

        for var in self.vars[1:]:
            E *= var.eval()

        return E

    def __add__(self, other : int | float | QuboTerm | QuboExpression) -> QuboExpression:
        q = QuboExpression()
        q += self
        q += other

        return q

    def __sub__(self, other : int | float | QuboTerm | QuboExpression) -> QuboExpression:
        q = QuboExpression()
        q += self
        q -= other

        return q

    def __radd__(self, other : int | float) -> QuboExpression:
        q = QuboExpression()
        q += QuboTerm(other, [])
        q += self
        return q

    def __rsub__(self, other : int | float) -> QuboExpression:
        q = QuboExpression()
        q += QuboTerm(other, [])
        q -= self
        return q

    @singledispatchmethod
    def __imul__(self, other):
        return NotImplemented

    @singledispatchmethod
    def __mul__(self, other):
        return NotImplemented

    def __rmul__(self, other : int | float):
        q = self._clone()
        q.coefficient *= other

        return q

    def __str__(self):
        s = ""
        if(self.coefficient >= 0):
            s += "+ "
        else:
            s += "- "

        s += str(abs(self.coefficient))

        if self.order() > 0:
            s += " * " + str(self.vars[0])
            for var in self.vars[1:]:
                s += " * " + str(var)

        return s

class QuboExpression(object):

    def __init__(self):
        super().__init__()

        # hash -> (term with coefficient)
        self.terms = {}

    def _apply_addition(self, other, op_coefficient):

        if isinstance(other, int) or isinstance(other, float):
            constant = float(other)

            if self.constant is None:
                self.constant = op_coefficient * constant
            else:
                self.constant += op_coefficient * constant

            return self

        oother = other
        if isinstance(oother, QuboVariable):
            oother = QuboTerm(1, [oother])
        elif other.order() == 2:
            if other.vars[0].key() == other.vars[1].key():
                # simplify x0 * x0 -> x0
                oother = QuboTerm(1, [other.vars[0]])
                oother.coefficient = other.coefficient

        key = oother.key()
        if(key in self.terms):
            self.terms[key].coefficient += op_coefficient * oother.coefficient

            if(self.terms[key].coefficient == 0):
                del self.terms[key]
        else:
            self.terms[key] = oother
            self.terms[key].coefficient *= op_coefficient

        return self

    def _clone(self):
        q = QuboExpression()
        for k in self.terms:
            q.terms[k] = self.terms[k]._clone()

        return q

    ###
    # ADDITION + SUBTRACTION
    ###

    # join clones of term dictionaries
    def _join_terms(self, terms0 : Dict[str, QuboTerm], terms1 : Dict[str, QuboTerm], op_coefficient : float):
        joint_terms = {}
        for key, term in terms0.items():
            joint_terms[key] = term._clone()
        for k in terms1:
            if k in joint_terms:
                joint_terms[k].coefficient += op_coefficient * terms1[k].coefficient
            else:
                joint_terms[k] = terms1[k]._clone()

        return joint_terms

    # join second dictionary into first
    def _i_join_terms(self, terms0 : Dict[str, QuboTerm], terms1 : Dict[str, QuboTerm], op_coefficient : float):
        for k in terms1:
            if k in terms0:
                terms0[k].coefficient += op_coefficient * terms1[k].coefficient
            else:
                terms0[k] = terms1[k]._clone()

        return terms0

    @singledispatchmethod
    def __iadd__(self, other):
        return NotImplemented

    @singledispatchmethod
    def __isub__(self, other):
        return NotImplemented

    def __add__(self, other : int | float | QuboVariable | QuboTerm | QuboExpression):
        q = self._clone()
        return q.__iadd__(other)

    def __sub__(self, other : int | float | QuboVariable | QuboTerm | QuboExpression):
        q = self._clone()
        return q.__isub__(other)

    def __radd__(self, other : int | float) -> QuboExpression:
        q = QuboExpression()
        q += QuboTerm(other, [])
        q += self
        return q

    def __rsub__(self, other : int | float) -> QuboExpression:
        q = QuboExpression()
        q += QuboTerm(other, [])
        q -= self
        return q

    @singledispatchmethod
    def __imul__(self, other):
        return NotImplemented

    def __mul__(self, other : int | float | QuboVariable | QuboTerm | QuboExpression):
        q = self._clone()
        q *= other
        return q

    def __rmul__(self, other : int | float):
        q = self._clone()
        for _, term in q.terms.items():
            term *= other
        return q

    # Python 3.10: other: QuboTerm | QuboVariable
    def eval(self, shift = 0):
        E = shift

        for term in self.terms:
            E += self.terms[term].eval()

        return E

    def isValid(self):
        is_valid = True

        for _, term in self.terms.items():
            is_valid &= term.isValid()

        return is_valid

    def __str__(self):
        s = " ".join([str(self.terms[t]) for t in self.terms])

        return s

################################################################################
# Single-dispatch implementations
# -> move overloaded methods in global namespace to avoid having forward declarations
################################################################################

###
## QuboVariable - add
###

@QuboVariable.__add__.register
def _(self, other : int) -> QuboExpression:
    q = QuboExpression()
    q += QuboTerm(1.0, [self])
    q += QuboTerm(float(other), [])

    return q

@QuboVariable.__add__.register
def _(self, other : float) -> QuboExpression:
    q = QuboExpression()
    q += QuboTerm(1.0, [self])
    q += QuboTerm(other, [])

    return q

@QuboVariable.__add__.register
def _(self, other : QuboVariable) -> QuboExpression:
    q = QuboExpression()
    q += QuboTerm(1.0, [self])
    q += QuboTerm(1.0, [other])

    return q

@QuboVariable.__add__.register
def _(self, other : QuboTerm) -> QuboExpression:
    q = QuboExpression()
    q += QuboTerm(1.0, [self])
    q += other

    return q

@QuboVariable.__add__.register
def _(self, other : QuboExpression) -> QuboExpression:
    q = QuboExpression()
    q += QuboTerm(1.0, [self])
    q += other

    return q

###
## QuboVariable - sub
###

@QuboVariable.__sub__.register
def _(self, other : int) -> QuboExpression:
    q = QuboExpression()
    q += QuboTerm(1.0, [self])
    q -= QuboTerm(float(other), [])

    return q

@QuboVariable.__sub__.register
def _(self, other : float) -> QuboExpression:
    q = QuboExpression()
    q += QuboTerm(1.0, [self])
    q -= QuboTerm(other, [])

    return q

@QuboVariable.__sub__.register
def _(self, other : QuboVariable) -> QuboExpression:
    q = QuboExpression()
    q += QuboTerm(1.0, [self])
    q -= QuboTerm(1.0, [other])

    return q

@QuboVariable.__sub__.register
def _(self, other : QuboTerm) -> QuboExpression:
    q = QuboExpression()
    q += QuboTerm(1.0, [self])
    q -= other

    return q

@QuboVariable.__sub__.register
def _(self, other : QuboExpression) -> QuboExpression:
    q = QuboExpression()
    q += QuboTerm(1.0, [self])
    q -= other

    return q

###
## QuboVariable - mul
###

@QuboVariable.__mul__.register
def _(self, other : int) -> QuboTerm:
    return QuboTerm(float(other), [self])

@QuboVariable.__mul__.register
def _(self, other : float) -> QuboTerm:
    return QuboTerm(other, [self])

@QuboVariable.__mul__.register
def _(self, other : QuboVariable) -> QuboTerm:
    return QuboTerm(1.0, [self, other])

@QuboVariable.__mul__.register
def _(self, other : QuboTerm) -> QuboExpression:
    q = other._clone()
    q *= QuboTerm(1.0, [self])

    return q

@QuboVariable.__mul__.register
def _(self, other : QuboExpression) -> QuboExpression:
    q = other._clone()
    q *= QuboTerm(1.0, [self])

    return q

###
## QuboTerm - imul
###

@QuboTerm.__imul__.register
def _(self, other : int) -> QuboTerm:
    self.coefficient *= other
    return self

@QuboTerm.__imul__.register
def _(self, other : float) -> QuboTerm:
    self.coefficient *= other
    return self

@QuboTerm.__imul__.register
def _(self, other : QuboVariable) -> QuboTerm:
    return self.__imul__(QuboTerm(1.0, [other]))

@QuboTerm.__imul__.register
def _(self, other : QuboTerm) -> QuboTerm:
    self.coefficient *= other.coefficient
    self.vars = self._join_vars(self.vars, other.vars)

    if self.order() > 2:
        raise Exception("Only QuboTerms with order <= 2 are supported.")

    return self

###
## QuboTerm - mul
###

@QuboTerm.__mul__.register
def _(self, other : int) -> QuboTerm:
    q = self._clone()
    q *= other
    return q

@QuboTerm.__mul__.register
def _(self, other : float) -> QuboTerm:
    q = self._clone()
    q *= other
    return q

@QuboTerm.__mul__.register
def _(self, other : QuboVariable) -> QuboTerm:
    q = self._clone()
    q *= other
    return q

@QuboTerm.__mul__.register
def _(self, other : QuboTerm) -> QuboTerm:
    q = self._clone()
    q *= other
    return q

@QuboTerm.__mul__.register
def _(self, other : QuboExpression) -> QuboExpression:
    q = other._clone()
    q *= self
    return q

###
## QuboExpression - iadd
###

@QuboExpression.__iadd__.register
def _(self, other : int) -> QuboExpression:
    if "" in self.terms:
        self.terms[""].coefficient += other
    else:
        self.terms[""] = QuboTerm(float(other), [])
    return self

@QuboExpression.__iadd__.register
def _(self, other : float) -> QuboExpression:
    if "" in self.terms:
        self.terms[""].coefficient += other
    else:
        self.terms[""] = QuboTerm(float(other), [])
    return self

@QuboExpression.__iadd__.register
def _(self, other : QuboVariable) -> QuboExpression:
    return self.__iadd__(QuboTerm(1.0, [other]))

@QuboExpression.__iadd__.register
def _(self, other : QuboTerm) -> QuboExpression:
    q = QuboExpression()
    q.terms[other.key()] = other

    return self.__iadd__(q)

@QuboExpression.__iadd__.register
def _(self, other : QuboExpression) -> QuboExpression:
    self.terms = self._i_join_terms(self.terms, other.terms, 1.0)
    return self

###
## QuboExpression - isub
###

@QuboExpression.__isub__.register
def _(self, other : int) -> QuboExpression:
    return self.__iadd__(-1.0 * other)

@QuboExpression.__isub__.register
def _(self, other : float) -> QuboExpression:
    return self.__iadd__(-1.0 * other)

@QuboExpression.__isub__.register
def _(self, other : QuboVariable) -> QuboExpression:
    return self.__isub__(QuboTerm(1.0, [other]))

@QuboExpression.__isub__.register
def _(self, other : QuboTerm) -> QuboExpression:
    q = QuboExpression()
    q.terms[other.key()] = other._clone()
    q.terms[other.key()].coefficient *= -1.0

    return self.__iadd__(q)

@QuboExpression.__isub__.register
def _(self, other : QuboExpression) -> QuboExpression:
    self.terms = self._i_join_terms(self.terms, other.terms, -1.0)
    return self

###
## QuboExpression - imul
###

@QuboExpression.__imul__.register
def _(self, other : int) -> QuboExpression:
    for _, term in self.terms.items():
        term *= other
    return self

@QuboExpression.__imul__.register
def _(self, other : float) -> QuboExpression:
    for _, term in self.terms.items():
        term *= other
    return self

@QuboExpression.__imul__.register
def _(self, other : QuboTerm) -> QuboExpression:
    for _, term in self.terms.items():
        term *= other
    return self

@QuboExpression.__imul__.register
def _(self, other : QuboVariable) -> QuboExpression:
    for _, term in self.terms.items():
        term *= other
    return self

@QuboExpression.__imul__.register
def _(self, other : QuboExpression) -> QuboExpression:
    q = QuboExpression()
    for _, s_term in self.terms.items():
        for _, o_term in other.terms.items():
            q += s_term * o_term

    self.terms = q.terms
    return self

################################################################################
################################################################################
################################################################################

class QuboModel(object):

    def __init__(self, sense : HybridSolverOptSenses = HybridSolverOptSenses.MAXIMIZE):

        self.vars = {}
        self.objective = QuboExpression()
        self.__sense = sense

        # for future use
        self.sos1 = []
        self.sos2 = []

        self._pos_ctr = 0

    @property
    def sense(self):
        return self.__sense

    @sense.setter
    def sense(self, sense : HybridSolverOptSenses):
        if isinstance(sense, HybridSolverOptSenses):
            self.__sense = sense
        else:
            raise RuntimeError(f"Try to set invalid optimization sense: {sense}")

    def addSOS1(self, vars : list):
        warnings.warn("SOS1 constraints are currently not supported in QUBOs")
        self.sos1.append(vars)

    def addSOS2(self, vars : list):
        warnings.warn("SOS2 constraints are currently not supported in QUBOs")
        self.sos2.append(vars)

    def addVariable(self, name : str, initial=None, fixing=None, disable_warnings=False):
        if(name in self.vars):
            if(not disable_warnings):
                warnings.warn("Variable " + name + " already in QUBO...")

            return self.vars[name]

        self.vars[name] = QuboVariable(name, self._pos_ctr, initial, fixing)
        self._pos_ctr += 1

        return self.vars[name]

    def variable(self, name : str):
        return self.vars[name]

    def eval(self):
        return self.objective.eval()

    def isValid(self):

        # check that all terms are in the upper triangle and that they
        # have been reduced in the right way

        return self.objective.isValid()

    def writeQUBO(self, path : str):

        shift = 0.0
        num_shift = 0
        if "" in self.objective.terms:
            num_shift = 1
            shift = self.objective.terms[""].coefficient

        # check that all terms are in the upper triangular part
        if not self.isValid():
            raise Exception("QUBO invalid - check that all terms are in the upper triangular part of Q.")

        # prepare sorted (by row) COO triplets
        triplets = []
        for key in self.objective.terms:
            if key == "":
                continue

            term = self.objective.terms[key]

            if(term.order() == 1):
                triplets.append((term.vars[0].id(), term.vars[0].id(), term.coefficient))

            # By convention, we only store the upper triangular part of the matrix, but it
            # is mirrored into the lower triangular part inside the QUBO solver - hence in
            # order to maintain the optimum, we have to divide the coefficients of
            # off-diagonal entries by 2
            if(term.order() == 2):
                triplets.append((term.vars[0].id(), term.vars[1].id(), 0.5 * term.coefficient))

        triplets.sort(key=itemgetter(0,1))

        with open(path, 'w') as f:

            f.write(self.sense.value + "\n")
            f.write("1\n")
            f.write("1.0\n")

            f.write(f"{shift}\n")

            # create sparse matrix from terms in objective
            f.write(f"{len(self.vars)} {len(self.objective.terms) - num_shift}\n")
            for t in triplets:
                f.write(f"{t[0]} {t[1]} {t[2]}\n")

            # add fixings
            for var in self.vars.values():
                if var.fixing:
                    f.write(f"f {var.id()} {var.fixing}\n")

    def get_nnz_upper_triangle(self):
        """
        Get the number of nonzeros for the upper triangle matrix.
        This corresponds to the number of terms in the objective function, excluding the shift.
        """

        # do we have a shift?
        if "" in self.objective.terms:
            return len(self.objective.terms) - 1
        else:
            return len(self.objective.terms)

    def get_nnz_full_matrix(self):
        """
        Compute number of nonzeros of the full matrix.
        Instead of using an attribute for the nonzeros, we simply compute them on demand.
        """
        # first, get nnz of the upper triangle matrix, this is only the number of terms in the objective
        upper_triangle_nnz = self.get_nnz_upper_triangle()
        # count linear terms to compute nnz of full matrix
        linear_terms = 0
        for term in self.objective.terms.values():
            if term.order() == 1:
                linear_terms += 1
        full_matrix_nnz = 2*upper_triangle_nnz - linear_terms

        return full_matrix_nnz

    @classmethod
    def readQUBO(cls, path : str):

        if path.endswith(".gz"):
            with gzip.open(path, 'rt') as f:
                qubo = cls._readQuboFile(f)
        else:
            with open(path, 'r') as f:
                qubo = cls._readQuboFile(f)

        return qubo


    @classmethod
    def _readQuboFile(cls, f):

        # check if sense is specified in first line
        first_line = f.readline().strip()
        if first_line in [sense.value for sense in HybridSolverOptSenses]:
            sense = HybridSolverOptSenses(first_line)
            num_terms = int(f.readline().strip())
        else:
            sense = HybridSolverOptSenses.MAXIMIZE # default
            num_terms = int(first_line)
        if num_terms != 1:
            raise Exception("Aggregated QUBOs are not supported...")
        weight = float(f.readline().strip())
        if weight != 1.0:
            raise Exception("Weighted QUBOs are not supported...")
        shift = float(f.readline().strip())

        nnz_string = f.readline().strip().split(" ")
        num_vars = int(nnz_string[0])
        num_nnz = int(nnz_string[1])

        # create variables
        qubo = QuboModel(sense)

        if shift != 0:
            qubo.objective += shift

        vars = []
        for ix in range(0, num_vars):
            vars.append(qubo.addVariable(f"x_{ix}"))

        # create terms
        term_ctr = 0
        check_symmetry = False
        lower_terms = []
        for line in f:
            split = line.split(" ")
            ix_i = int(split[0])
            ix_j = int(split[1])
            entry = float(split[2])

            if ix_i == ix_j:
                qubo.objective += entry * vars[ix_i]
            elif ix_i > ix_j:
                raise Exception("Invalid .qubo file, only upper triangular matrix can be stored")
            else:
                # since we only store the upper triangular matrix, we need to
                # make the entries in the lower triangular matrix explicit
                # through doubling the coefficient
                qubo.objective += 2.0 * entry * vars[ix_i] * vars[ix_j]

            term_ctr += 1


        if term_ctr != num_nnz:
            raise Exception("Invalid .qubo files, float of NNZ specified does not match NZ entries!")

        return qubo

    def __str__(self):
        return str(self.objective)

    def _solvePrep(self):

        # temporary folder for the QUBO problem
        tmp_path = tempfile.mkdtemp()
        tmp_problem = os.path.join(tmp_path, "pyclient.qubo")

        # convert problem into QUBO format (i.e. a matrix)
        self.writeQUBO(tmp_problem)

        return tmp_problem

    def _solveParse(self, solution):

        # parse solution, store assignments in variables
        sol_string_splitted = solution.split("\n")

        for var in self.vars:
            self.vars[var].assignment = int(sol_string_splitted[self.vars[var].id()])

    async def solveAsync(self, specs : dict, runner : Runner):

        tmp_problem = self._solvePrep()
        res = await runner.solveAsync(tmp_problem, specs)

        self._solveParse(res['solution_file'])

        # return (optimal) objective
        return self.eval()

    def solve(self, specs : dict, runner : Runner):

        tmp_problem = self._solvePrep()
        res = runner.solve(tmp_problem, specs)

        self._solveParse(res['solution_file'])

        # return (optimal) objective
        return self.eval()

    def __str__(self):
        return str(self.objective)

    #######
    # PYQUBO Compatibility Layer
    #######
    def fromPyQuboModel(self, model : pq.Model, constants : dict = {}):
        self.vars = {}
        self.objective = QuboExpression()
        self._pos_ctr = 0

        # guarantees that we only have terms of oders {1, 2}
        qmodel, shift = model.to_qubo(feed_dict=constants)

        # create objective from QUBO model
        for term in qmodel:
            if(term[0] == term[1]):
                # unary term
                v = self.addVariable(term[0], disable_warnings=True)
                self.objective += QuboTerm(qmodel[term], [v])
            else:
                # pairwise term
                v0 = self.addVariable(term[0], disable_warnings=True)
                v1 = self.addVariable(term[1], disable_warnings=True)
                self.objective += QuboTerm(qmodel[term], [v0, v1])

        if shift != 0:
            self.objective += shift
