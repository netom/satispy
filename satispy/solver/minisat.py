from satispy.io import DimacsCnf
from satispy import Variable
from satispy import Solution

from os import devnull
from subprocess import call
from tempfile import NamedTemporaryFile

class Minisat(object):
    COMMAND = 'minisat -verb=0 %s %s > ' + devnull

    def __init__(self, command=COMMAND):
        self.command = command

    def solve(self, cnf):
        s = Solution()

        infile = NamedTemporaryFile(mode='w')
        outfile = NamedTemporaryFile(mode='r')

        io = DimacsCnf()
        infile.write(io.tostring(cnf))
        infile.flush()

        ret = call(self.command % (infile.name, outfile.name), shell=True)

        infile.close()

        if ret != 10:
            return s

        s.success = False

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
