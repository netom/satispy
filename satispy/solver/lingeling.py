from satispy.exception import SATSolverMissing
from satispy.io import DimacsCnf
from satispy import Variable
from satispy import Solution

import shutil
import subprocess

class Lingeling(object):
    PATH = 'lingeling'

    def __init__(self, path=PATH, args=['-q']):
        self.path = path
        self.args = args

    def available(self):
        return shutil.which(self.path)

    def solve(self, cnf):
        path = self.available()

        if not path:
            raise SATSolverMissing(self.path) 

        process = subprocess.Popen(
            [path] + self.args,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
        )

        io = DimacsCnf()
        stdout_data, _ = process.communicate(io.tostring(cnf).encode())

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
