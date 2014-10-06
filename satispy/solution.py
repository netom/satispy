class Solution(object):
    def __init__(self, success=False, error=False, varmap={}):
        self.success = success
        self.error = error
        self.varmap = varmap

    def __getitem__(self, i):
        return self.varmap[i]