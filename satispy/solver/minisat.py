from satispy.exception import SATSolverMissing
from satispy.io import DimacsCnf
from satispy import Variable
from satispy import Solution

import shutil
import subprocess

import os
import tempfile

class Minisat(object):
    PATH = 'minisat'

    def __init__(self, path=PATH, args=['-verb=0']):
        self.path = path
        self.args = args

    def available(self):
        return shutil.which(self.path)

    def solve(self, cnf):
        path = self.available()

        if not path:
            raise SATSolverMissing(self.path) 

        with tempfile.NamedTemporaryFile(mode='r', delete_on_close=False) as outfile, \
             tempfile.NamedTemporaryFile(mode='w', delete_on_close=False) as infile:

            io = DimacsCnf()
            infile.write(io.tostring(cnf))
            infile.close()

            process = subprocess.Popen(
                [path] + self.args + [infile.name, outfile.name],
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,

            )

            process.communicate()

            s = Solution()

            if process.returncode == 10:
                s.success = True
            elif process.returncode == 20:
                s.success = False
                return s
            else:
                raise SATSolverFailed('Sat solver exit code unknown.')

            lines = outfile.readlines()

            for line in lines:
                if line[0] not in "-0123456789":
                    # "SAT", "UNSAT", or junk
                    continue
                varz = line.split(" ")[:-1]
                for v in varz:
                    v = v.strip()
                    value = v[0] != '-'
                    v = v.lstrip('-')
                    vo = io.varobj(v)
                    s.varmap[vo] = value

        return s
