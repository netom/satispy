from satispy.exception import SATSolverMissing
from satispy.io import DimacsCnf
from satispy import Variable
from satispy import Solution

import shutil
import subprocess

import os
import tempfile

class IntelSatSolver(object):
    PATH = 'intel_sat_solver_static'

    def __init__(self, path=PATH, args=[]):
        self.path = path
        self.args = args

    def available(self):
        return shutil.which(self.path)

    def solve(self, cnf):
        path = self.available()

        if not path:
            raise SATSolverMissing(self.path) 

        # For some reason, The Intel SAT solver can't read from stdin properly.
        io = DimacsCnf()
        infile = tempfile.NamedTemporaryFile(mode='w')
        infile.write(io.tostring(cnf))
        infile.flush()

        process = subprocess.Popen(
            [path, infile.name] + self.args,
            stdout=subprocess.PIPE,
        )

        s = Solution()
        s.success = False

        stdout_data, stderr_data = process.communicate()

        infile.close()

        if process.returncode not in [10, 20]:
            return s

        lines = stdout_data.decode('utf-8').split('\n')

        for line in lines:
            if line[0:2] == 'c ':
                continue
            if line[0:13] == 's SATISFIABLE':
                s.success = True
                continue
            if line[0:2] == 'v ':
                varz = line.split(" ")[1:-1]
                for v in varz:
                    v = v.strip()
                    value = v[0] != '-'
                    v = v.lstrip('-')
                    vo = io.varobj(v)
                    s.varmap[vo] = value

        return s
