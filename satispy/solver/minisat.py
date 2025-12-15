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
        if os.path.exists('/dev/stdin') and os.path.exists('/dev/stdout'):
            stdin = '/dev/stdin'
        elif 'isreserved' in dir(os.path) and os.path.isreserved('CON'):
            stdin = 'CON'
        else:
            raise RuntimeError('No standard input/output devices (/dev/std*, CON) could be found.')

        self.path = path
        self.args = args + [stdin]

    def available(self):
        return shutil.which(self.path)

    def solve(self, cnf):
        path = self.available()

        if not path:
            raise SATSolverMissing(self.path) 

        outfile = tempfile.NamedTemporaryFile(mode='r')

        process = subprocess.Popen(
            [path] + self.args + [outfile.name],
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
        )

        io = DimacsCnf()
        # TODO: have to be able to handle large inputs and outputs
        _, stderr_data = process.communicate(io.tostring(cnf).encode())

        s = Solution()
        s.success = False

        if process.returncode not in [10]:
            return s

        lines = outfile.readlines()

        for line in lines:
            if line[0:3] == 'SAT':
                s.success = True
                continue
            varz = line.split(" ")[:-1]
            for v in varz:
                v = v.strip()
                value = v[0] != '-'
                v = v.lstrip('-')
                vo = io.varobj(v)
                s.varmap[vo] = value

        outfile.close()

        return s
