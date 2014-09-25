from satispy import Variable
from satispy.solver import Minisat

v1 = Variable('v1')
v2 = Variable('v2')
v3 = Variable('v3')

exp = v1 & v2 | v3

solver = Minisat()

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
