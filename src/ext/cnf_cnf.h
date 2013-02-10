#ifndef CNF_CNF_H
#define CNF_CNF_H

#include <inttypes.h>

typedef struct {
    PyObject_HEAD
    int64_t *buf;
    int64_t variables;
    int64_t clauses;
    int64_t max_clauses;
} Cnf;

extern int64_t init_variables;
extern int64_t init_max_clauses;

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

PyObject *cnf_Cnf_getBuffer(PyObject *self, PyObject *args);

#endif
//CNF_CNF_H
