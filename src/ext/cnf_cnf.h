typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
} Cnf;

void cnf_Cnf_dealloc(Cnf* self);
PyObject *cnf_Cnf_new(PyTypeObject *type, PyObject *args, PyObject *kwds);
int cnf_Cnf_init(Cnf *self, PyObject *args, PyObject *kwds);

PyObject *cnf_Cnf_str(PyObject *self);

PyObject *cnf_Cnf_neg(PyObject* self);
PyObject *cnf_Cnf_and(PyObject* self, PyObject* other);
PyObject *cnf_Cnf_or(PyObject* self, PyObject* other);
PyObject *cnf_Cnf_xor(PyObject* self, PyObject* other);
PyObject *cnf_Cnf_rshift(PyObject* self, PyObject* other);

PyObject *cnf_Cnf_inplace_and(PyObject* self, PyObject* other);
PyObject *cnf_Cnf_inplace_or(PyObject* self, PyObject* other);
PyObject *cnf_Cnf_inplace_xor(PyObject* self, PyObject* other);
PyObject *cnf_Cnf_inplace_rshift(PyObject* self, PyObject* other);
