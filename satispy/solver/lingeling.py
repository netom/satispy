from satispy.io import DimacsCnf
from satispy import Variable
from satispy import Solution

from subprocess import *
import tempfile

import time
import os

class Lingeling(object):
    COMMAND = 'lingeling %s'

    def __init__(self, command=COMMAND):
        self.command = command

    def solve(self, cnf):
        s = Solution()

        # NamedTemporaryFile doesn't work on Windows, see https://stackoverflow.com/questions/15169101/how-to-create-a-temporary-file-that-can-be-read-by-a-subprocess
        infile, infilename = tempfile.mkstemp(suffix="cnf")

        try:
            io = DimacsCnf()
            os.write(infile, io.tostring(cnf))
            os.close(infile)

            try:
                cmd = self.command % (infilename.replace("\\","/"))
                check_output(cmd, stderr=STDOUT, shell=True)
            # Lingeling and most SAT-solvers use a non-zero return code, which in most POSIX command indicates an error.
            # That's why python raises an exception, but here it's expected
            except CalledProcessError as call:
                if call.returncode != 10 and call.returncode != 20:
                    s.error = call.output
                    return s
        finally:
            os.remove(infilename)

        if call.returncode != 10:
            return s

        s.success = True

        for line in call.output.split("\n"):
            # Solution line example: v 1 -2 3 -4 5 6 0
            if len(line) > 0 and line[0] == 'v':
                varz = line.split(" ")[1:-1]
                for v in varz:
                    v = v.strip()
                    value = v[0] != '-'
                    v = v.lstrip('-')
                    vo = io.varobj(v)
                    s.varmap[vo] = value

        return s
