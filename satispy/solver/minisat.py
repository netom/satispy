from satispy.io import DimacsCnf
from satispy import Variable
from satispy import Solution

from subprocess import call
from tempfile import NamedTemporaryFile

class Minisat(object):
    COMMAND = 'minisat %s %s > /dev/null'

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

        s.success = True

        lines = outfile.readlines()[1:]

        for line in lines:
            varz = line.split(" ")[:-1]
            for v in varz:
                v = v.strip()
                value = v[0] != '-'
                v = v.lstrip('-')
                vo = io.varobj(v)
                s.varmap[vo] = value

        # Close deletes the tmp files
        outfile.close()

        return s
