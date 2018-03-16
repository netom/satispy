class Solution(object):
    def __init__(self, success=False, error=False, varmap=None):
        self.success = success
        self.error = error
        if varmap is None:
            varmap = {}
        self.varmap = varmap

    def __getitem__(self, i):
        return self.varmap[i]
