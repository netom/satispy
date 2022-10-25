from satispy.io import DimacsCnf
from satispy import Variable
from satispy import Solution

from os import devnull
import sys
import os
from subprocess import Popen, TimeoutExpired
from tempfile import NamedTemporaryFile
from signal import SIGTERM

class Minisat(object):
    COMMAND = 'minisat -verb=0 %s %s > ' + devnull

    def __init__(self, command=COMMAND, timeout=None):
        self.command = command
        self.timeout = timeout

    def solve(self, cnf):
        s = Solution()

        infile = NamedTemporaryFile(mode='w')
        outfile = NamedTemporaryFile(mode='r')

        io = DimacsCnf()
        infile.write(io.tostring(cnf))
        infile.flush()

        try:
            ret = Popen(self.command % (infile.name, outfile.name), shell=True,
                        start_new_session=True)
            ret.wait(timeout=self.timeout)
        except TimeoutExpired as e:
            print(e)
            os.killpg(os.getpgid(ret.pid), SIGTERM)
            raise e

        infile.close()

        if ret.returncode != 10:
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
