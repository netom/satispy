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

        # I tried using stdin, but it looks like the Intel SAT solver can't
        # read from stdin properly.
        with tempfile.NamedTemporaryFile(mode='w', delete_on_close=False) as infile:
            io = DimacsCnf()
            infile.write(io.tostring(cnf))
            infile.close()

            process = subprocess.Popen(
                [path, infile.name] + self.args,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
            )

            stdout_data, _ = process.communicate()

            s = Solution()

            if process.returncode == 10:
                s.success = True
            elif process.returncode == 20:
                s.success = False
                return s
            else:
                raise SATSolverFailed('Sat solver exit code unknown.')

            lines = stdout_data.decode('utf-8').split('\n')

            for line in lines:
                if line[0:2] == 'v ':
                    varz = line.split(" ")[1:-1]
                    for v in varz:
                        v = v.strip()
                        value = v[0] != '-'
                        v = v.lstrip('-')
                        vo = io.varobj(v)
                        s.varmap[vo] = value

        return s
