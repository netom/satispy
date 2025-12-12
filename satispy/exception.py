class SATException(Exception):
    pass

class SATUnsatisfiable(SATException):
    pass

class SATSolverMissing(SATException):
    pass
