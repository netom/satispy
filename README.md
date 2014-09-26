SATisPy
=======

Satispy is a Python library that aims to be an interface to various
SAT (boolean satisfiability) solver applications.

Supported solvers:

 * [MiniSAT](http://minisat.se/) (Linux)
 * [Lingeling](http://fmv.jku.at/lingeling/) (Linux, Cygwin)

Support for other solvers should be fairly easy as long as they accept the
[DIMACS CNF SAT format](http://www.satcompetition.org/2009/format-benchmarks2009.html).

Installing
----------

You can grab the current version from pypi:

    $ sudo pip install satispy

Or you can download a copy from https://github.com/netom/satispy, and
runs

    $ sudo ./setup.py install

in the directory of the project.

If you want to develop on the library, use:

	$ ./setup.py develop

You can run the tests found in the test folder by running run_tests.py.

How it works
------------

You need a SAT solver and numpy to be installed on your machine for this to work.

Let's see an example:

    from satispy import Variable, Cnf
    from satispy.solver import Minisat
    
    v1 = Variable('v1')
    v2 = Variable('v2')
    v3 = Variable('v3')
    
    exp = v1 & v2 | v3
    
    solver = Minisat()
    
    solution = solver.solve(exp)
    
    if solution.success:
        print "Found a solution:"
        print v1, solution[v1]
        print v2, solution[v2]
        print v3, solution[v3]
    else:
        print "The expression cannot be satisfied"

This program tries to satisfy the boolean expression

v1 & v2 | v3

You can make this true by assigning true to all variables for example,
but there are other solutions too. This program finds a single arbitrary
solution.

First, the program imports the various classes so we can build an expression
and try to solve it.

Every expression is in CNF form, but we don't have to enter the expression
in it. The Cnf class takes care of the proper arranging of the boolean
terms.

Expressions can be built by creating variables and gluing them together
arbitrarily with boolean operators:

* NOT: - (unary)
* AND: &
* OR:  |
* XOR: ^
* IMPLICATION >>

The solver class Minisat is used to solve the formula.

Note: the Minisat class creates two temporary files, so it needs write
access to the system's temporary directory

The returned solution can be checked by reading the "success" boolean
flag.

Then, the solution can be queried for variable assignments by using it
like a dictionary. Note that Variable objects are used, not strings.

(This very example can be found in the examples directory)
