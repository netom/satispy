typedef struct {
    PyObject_HEAD
    PyObject *name;
    long inverted;
    long number;
} Variable;

PyObject* cnf_Variable_new(PyTypeObject *type, PyObject *args, PyObject *kwds);

int cnf_Variable_init(Variable *self, PyObject *args, PyObject *kwds);

void cnf_Variable_dealloc(Variable* self);

PyObject* cnf_Variable_str(PyObject *self);

PyObject* cnf_Variable_neg(PyObject* self);
PyObject* cnf_Variable_and(PyObject* self, PyObject* other);
PyObject* cnf_Variable_or(PyObject* self, PyObject* other);
PyObject* cnf_Variable_xor(PyObject* self, PyObject* other);
PyObject* cnf_Variable_rshift(PyObject* self, PyObject* other);
