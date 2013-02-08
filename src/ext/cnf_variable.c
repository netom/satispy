#include <Python.h>
#include "structmember.h"

#include "cnf_variable.h"

void cnf_Variable_dealloc(Variable* self)
{
    Py_XDECREF(self->name);
    self->ob_type->tp_free((PyObject*)self);
}

PyObject * cnf_Variable_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    Variable *self;

    self = (Variable *)type->tp_alloc(type, 0);
    if (self != NULL) {
        self->name = PyString_FromString("");
        if (self->name == NULL) {
            Py_DECREF(self);
            return NULL;
        }

        self->inverted = 0;
    }

    return (PyObject *)self;
}

int cnf_Variable_init(Variable *self, PyObject *args, PyObject *kwds)
{
    PyObject *name=NULL, *tmp;

    char *kwlist[] = {"inverted", NULL};

    if (! PyArg_ParseTupleAndKeywords(args, kwds, "O|i", kwlist, &name, self->inverted)) {
        return -1;
    }

    if (name) {
        tmp = self->name;
        Py_INCREF(name);
        self->name = name;
        Py_XDECREF(tmp);
    }

    return 0;
}

PyObject* cnf_Variable_str(PyObject *self)
{
    Variable *v = (Variable *)self;

    return PyString_FromFormat("%s%s", v->inverted ? "-" : "", PyString_AsString(v->name));
}

PyObject* cnf_Variable_neg(PyObject* self)
{
    
    return NULL;
}

PyObject* cnf_Variable_and(PyObject* self, PyObject* other)
{
    return NULL;
}

PyObject* cnf_Variable_or(PyObject* self, PyObject* other)
{
    return NULL;
}

PyObject* cnf_Variable_xor(PyObject* self, PyObject* other)
{
    return NULL;
}

PyObject* cnf_Variable_rshift(PyObject* self, PyObject* other)
{
    return NULL;
}
