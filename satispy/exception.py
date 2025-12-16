class SATException(Exception):
    pass

class SATSolverFailed(SATException):
    pass

class SATUnsatisfiable(SATException):
    pass

class SATSolverMissing(SATException):
    pass
