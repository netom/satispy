from satispy.exception import SATException

class Solution(object):
    def __init__(self, success=False, error=False, varmap=None):
        self.success = success
        self.error = error
        if varmap is None:
            varmap = {}
        self.varmap = varmap

    def __getitem__(self, i):
        if not self.success:
            raise SATException("Unsuccessful solution")
        return self.varmap[i]
