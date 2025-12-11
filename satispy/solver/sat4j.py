from satispy.io import DimacsCnf
from satispy import Variable
from satispy import Solution

from subprocess import call
from tempfile import NamedTemporaryFile

class Sat4j(object):
    COMMAND = 'sat4j %s > %s'

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

        outfile.close()

        return s
