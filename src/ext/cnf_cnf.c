#include <Python.h>

#include "cnf_module.h"
#include "cnf_cnf.h"

#include <stdio.h>

int64_t init_variables   = 64;
int64_t init_max_clauses = 1; // MUST BE at least 1, assumed by variable

PyObject * cnf_Cnf_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    Cnf *self;
    self = (Cnf *)type->tp_alloc(type, 0);
    return (PyObject *)self;
}

int cnf_Cnf_init(Cnf *self, PyObject *args, PyObject *kwds)
{
    self->variables = init_variables;
    self->max_clauses = init_max_clauses;
    self->clauses = 0;
    self->buf = (int64_t *)PyMem_Malloc(self->variables/4*self->max_clauses);
    if (self->buf == NULL) {
        PyErr_SetString(PyExc_MemoryError, "Out of memory.");
        Py_DECREF(self);
        return -1;
    }
    memset(self->buf, 0, self->variables/4*self->max_clauses);
    return 0;
}

void cnf_Cnf_dealloc(Cnf* self)
{
    PyMem_Free(self->buf);
    self->ob_type->tp_free((PyObject*)self);
}

PyObject *cnf_Cnf_str(PyObject *self)
{
    PyErr_SetString(PyExc_NotImplementedError, "Not implemented yet.");
    return NULL;
}

PyObject * cnf_Cnf_neg(PyObject* self)
{
    PyErr_SetString(PyExc_NotImplementedError, "Not implemented yet.");
    return NULL;
}

PyObject * cnf_Cnf_and(PyObject* self, PyObject* other)
{
    PyErr_SetString(PyExc_NotImplementedError, "Not implemented yet.");
    return NULL;
}

PyObject * cnf_Cnf_or(PyObject* self, PyObject* other)
{
    PyErr_SetString(PyExc_NotImplementedError, "Not implemented yet.");
    return NULL;
}

PyObject * cnf_Cnf_xor(PyObject* self, PyObject* other)
{
    PyErr_SetString(PyExc_NotImplementedError, "Not implemented yet.");
    return NULL;
}

PyObject * cnf_Cnf_rshift(PyObject* self, PyObject* other)
{
    PyErr_SetString(PyExc_NotImplementedError, "Not implemented yet.");
    return NULL;
}

PyObject * cnf_Cnf_inplace_and(PyObject* self, PyObject* other)
{
    PyErr_SetString(PyExc_NotImplementedError, "Not implemented yet.");
    return NULL;
}

PyObject * cnf_Cnf_inplace_or(PyObject* self, PyObject* other)
{
    PyErr_SetString(PyExc_NotImplementedError, "Not implemented yet.");
    return NULL;
}

PyObject * cnf_Cnf_inplace_xor(PyObject* self, PyObject* other)
{
    PyErr_SetString(PyExc_NotImplementedError, "Not implemented yet.");
    return NULL;
}

PyObject * cnf_Cnf_inplace_rshift(PyObject* self, PyObject* other)
{
    PyErr_SetString(PyExc_NotImplementedError, "Not implemented yet.");
    return NULL;
}

PyObject *cnf_Cnf_getBuffer(PyObject *self, PyObject *args)
{
    Cnf *me = (Cnf *)self;
    return PyString_FromStringAndSize((char *)me->buf, me->variables/8*me->clauses);
}
