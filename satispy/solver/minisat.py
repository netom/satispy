from satispy.io import DimacsCnf
from satispy import Variable
from satispy import Solution

import sys
import os
from subprocess import Popen, TimeoutExpired
from tempfile import NamedTemporaryFile
from signal import SIGTERM

class Minisat(object):
    COMMAND = 'minisat %s %s > ' + \
        ('NUL' if sys.platform == 'win32' else '/dev/null')

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
