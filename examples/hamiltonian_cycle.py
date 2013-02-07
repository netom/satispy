# Naive implementation of Hamilton-cycle searching in a graph
#
# Based on the following paper:
#
# Formalizing Dangerous SAT Encodings
# Alexander Hertel, Philipp Hertel, and Alasdair Urquhart
# Department of Computer Science,
# University of Toronto, Toronto ON M5S 3G4, Canada,
# [ahertel][philipp][urquhart]@cs.toronto.edu

from satispy import Variable, Cnf
from satispy.solver import Minisat

import networkx as nx

N = 6
M = 6

g = nx.grid_2d_graph(N, M)

lennodes = len(g.nodes())
gnodes = g.nodes()

exp = Cnf()

# Variables
# We create a variable for every node that
# marks the position of that node in the path
print "Creating variables..."
varz = {}
for n in gnodes:
    varz[n] = []
    for i in xrange(lennodes):
        # n, m, position
        varz[n].append(Variable("%d_%d_%d" % (n[0], n[1], i)))

# Total (X)
print "Creating total clauses..."
for i in gnodes:
    c = Cnf()
    for j in xrange(lennodes):
        c |= varz[i][j]
    exp &= c

# Onto
print "Creating onto clauses..."
for j in xrange(lennodes):
    c = Cnf()
    for i in gnodes:
        c |= varz[i][j]
    exp &= c

# 1-1 (X)
print "Creating 1-1 calues..."
for j in xrange(lennodes):
    print j
    for i1 in gnodes:
        for i2 in gnodes:
            if i1 != i2:
                exp &= -varz[i1][j] | -varz[i2][j]

# Fn
print "Creating Fn calues..."
for i in xrange(lennodes):
    print i
    for j1 in gnodes:
        for j2 in gnodes:
            if i1 != i2:
                exp &= -varz[i][j1] | -varz[i][j2]

# Edge
print "Adding edge clauses..."
for j in xrange(lennodes):
    print j
    for i in gnodes:
        for k in gnodes:
            if i != k and k not in g.neighbors(i):
                exp &= -varz[i][j] | -varz[k][(j+1) % lennodes]
            
# Enabling minisat to write to stdout
solver = Minisat('minisat %s %s')

print "Solving..."
solution = solver.solve(exp)

if not solution.success:
    print "There is no Hamilton cycle in the graph."
    exit()

print "Extracting solution..."
path = []
for n in g.nodes():
    nodepos = -1
    for j in xrange(lennodes):
        if solution[varz[n][j]]:
            nodepos = j
            break
    path.append((nodepos, n))

path.sort()

for n in path:
    print n[0], n[1]
