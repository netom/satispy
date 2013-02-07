#!/usr/bin/env python

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

import copy
import unittest

from satispy import *
from satispy.io import *
from satispy.solver import *

class VariableTest(unittest.TestCase):
    def testVariable(self):
        v = Variable("name")
        self.assertEqual("name", str(v))
        self.assertEqual("-name", str(-v))

    def testEqualits(self):
        v1 = Variable("v1")
        v2 = Variable("v1")

        self.assertEqual(v1,v1)
        self.assertEqual(v1,v2)
        self.assertEqual(v1,copy.deepcopy(v1))

        self.assertNotEqual(v1,-v1)

    def testHash(self):
        v1 = Variable("v1")
        v2 = Variable("v1")

        self.assertEqual(hash(v1),hash(v1))
        self.assertEqual(hash(v1),hash(v2))

        # Yes, this is guaranteed in this case
        self.assertNotEqual(hash(v1),hash(-v1))

    def testDataStructures(self):
        v1 = Variable("v1")
        v2 = Variable("v1")

        # Set
        s = set([v1,v2])

        self.assertEqual(1,len(s))

        # Dictionary
        d = {}

        d[v1] = "first"
        d[v2] = "second"

        self.assertEqual("second", d[v1])
        self.assertEqual("second", d[v2])

        # Frozenset
        fs = frozenset([v1,v2])

        self.assertEqual(1,len(s))

        fs1 = frozenset([v1])
        fs2 = frozenset([v2])
        self.assertEqual(fs1,fs2)

        # This property is used in the CNF class
        self.assertEqual(hash(fs1),hash(fs2))

    def testOrdering(self):
        v1 = Variable("v1")
        v2 = Variable("v2")

        self.assertTrue(v1 < v2)
        self.assertTrue(v1 <= v2)
        self.assertTrue(v2 > v1)
        self.assertTrue(v2 >= v1)
        self.assertFalse(v1 > v2)
        self.assertFalse(v1 >= v2)
        self.assertFalse(v2 < v1)
        self.assertFalse(v2 <= v1)

class CnfTest(unittest.TestCase):
    def testAnd(self):
        v1 = Variable("v1")
        v2 = Variable("v2")
        cnf = v1 & v2
        self.assertEqual(set([frozenset([v1]),frozenset([v2])]), set(cnf.dis))

    def testOr(self):
        v1 = Variable("v1")
        v2 = Variable("v2")
        v3 = Variable("v3")
        v4 = Variable("v4")

        cnf1 = v1 | v2

        self.assertEqual(set([frozenset([v1,v2])]), set(cnf1.dis))

        cnf2 = cnf1 | v3

        self.assertEqual(set([frozenset([v1,v2,v3])]), set(cnf2.dis))

        # Test empty CNF or
        cnf = Cnf()
        cnf |= v1

        self.assertEqual(set([frozenset([v1])]), set(cnf.dis))

    def testCreateFrom(self):
        v1 = Variable("v1")
        self.assertEqual(set([frozenset([v1])]), set(Cnf.create_from(v1).dis))

    def testMixed(self):
        v1 = Variable("v1")
        v2 = Variable("v2")
        v3 = Variable("v3")
        v4 = Variable("v4")

        self.assertEqual(
            set([
                frozenset([v1,v2]),
                frozenset([v3])
            ]),
            set(((v1 | v2) & v3).dis)
        )

        # Distribution
        self.assertEqual(
            set([
                frozenset([v1,v3]),
                frozenset([v2,v3])
            ]),
            set(((v1 & v2) | v3).dis)
        )

        # Double distribution
        self.assertEqual(
            set([
                frozenset([v1,v3]),
                frozenset([v1,v4]),
                frozenset([v2,v3]),
                frozenset([v2,v4])
            ]),
            set(((v1 & v2) | (v3 & v4)).dis)
        )

    def testNegation(self):
        v1 = Variable("v1")
        v2 = Variable("v2")
        v3 = Variable("v3")

        self.assertEqual(
            set([frozenset([-v1])]),
            set((-Cnf.create_from(v1)).dis)
        )

    def testXor(self):
        v1 = Variable("v1")
        v2 = Variable("v2")

        cnf = v1 ^ v2

        self.assertEqual(
            set([
                frozenset([v1,v2]),
                frozenset([-v1,-v2])
            ]),
            set(cnf.dis)
        )

    def testImplication(self):
        v1 = Variable("v1")
        v2 = Variable("v2")

        self.assertEqual(
            set([frozenset([-v1,v2])]),
            set((v1 >> v2).dis)
        )

class DimacsTest(unittest.TestCase):
    def testDimacs(self):
        v1 = Variable("v1")
        v2 = Variable("v2")
        v3 = Variable("v3")
        v4 = Variable("v4")

        cnf1 = (v1 | v2) & (-v3 | v4) & (-v1 | v3 | -v4)

        io = DimacsCnf()

        s = io.tostring(cnf1)

        # Must be true because of Variable ordering, and
        # the guarantee of numbering during IO
        self.assertEqual(io.varname(v1), '1')
        self.assertEqual(io.varname(v2), '2')
        self.assertEqual(io.varname(v3), '3')
        self.assertEqual(io.varname(v4), '4')
        self.assertEqual(io.varobj('1'), v1)
        self.assertEqual(io.varobj('2'), v2)
        self.assertEqual(io.varobj('3'), v3)
        self.assertEqual(io.varobj('4'), v4)

        cnf2 = io.fromstring(s)

        # Must be true due to io conventions
        self.assertEqual(io.varname(v1), '1')
        self.assertEqual(io.varname(v2), '2')
        self.assertEqual(io.varname(v3), '3')
        self.assertEqual(io.varname(v4), '4')
        self.assertEqual(io.varobj('1'), v1)
        self.assertEqual(io.varobj('2'), v2)
        self.assertEqual(io.varobj('3'), v3)
        self.assertEqual(io.varobj('4'), v4)

        # The frozenset is deterministic, so this will be ture
        # if everything else is OK
        self.assertEqual(cnf1, cnf2)

class MinisatTest(unittest.TestCase):

    def testSolution(self):
        v1 = Variable("v1")
        v2 = Variable("v2")
        v3 = Variable("v3")
        v4 = Variable("v4")

        cnf = (v1 | v2) & (-v3 | v4) & (-v1 | v3 | -v4)
        #  v1, -v2, -v3, -v4
        #  v1, -v2,  v3,  v4
        #  v1,  v2, -v3, -v4
        #  v1,  v2,  v3,  v4
        # -v1,  v2, -v3, -v4
        # -v1,  v2, -v3,  v4
        # -v1,  v2,  v3,  v4

        solver = Minisat()

        sol = solver.solve(cnf)

        self.assertTrue(
            (sol[v1],sol[v2], sol[v3], sol[v4])
            in
            [
                (True,  False, False, False),
                (True,  False, True,  True ),
                (True,  True,  False, False),
                (True,  True,  True,  True ),
                (False, True,  False, False),
                (False, True,  False, True ),
                (False, True,  True,  True )
            ]
        )


if __name__ == "__main__":
    unittest.main()
