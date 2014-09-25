# This is the example from the README, but modified to show how to use a solver (in this case lingeling) compiled in CYGWIN

from satispy import Variable
from satispy.solver import Lingeling

# Windows-style CYGWIN path here
CYGWIN_PATH="C:\\cygwin64\\"
# Single command if the solver is in your PATH, otherwise UNIX path here
SOLVER="lingeling.exe"

v1 = Variable('v1')
v2 = Variable('v2')
v3 = Variable('v3')

exp = v1 & v2 | v3

solver = Lingeling(command=CYGWIN_PATH + "bin\\bash.exe --login -c \"" + SOLVER + " %s\"")

solution = solver.solve(exp)

if solution.error != False:
    print "Error:"
    print solution.error
elif solution.success:
    print "Found a solution:"
    print v1, solution[v1]
    print v2, solution[v2]
    print v3, solution[v3]
else:
    print "The expression cannot be satisfied"
