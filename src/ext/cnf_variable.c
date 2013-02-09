#include <Python.h>
#include "structmember.h"

#include "cnf_variable.h"

long nextnumber;

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
    }

    return (PyObject *)self;
}

int cnf_Variable_init(Variable *self, PyObject *args, PyObject *kwds)
{
    PyObject *name=NULL, *tmp;

    self->inverted = 0;

    if (! PyArg_ParseTuple(args, "O|i", &name, &self->inverted)) {
        return -1;
    }

    // TODO: inverted must be 1 or 0

    if (name) {
        tmp = self->name;
        Py_INCREF(name);
        self->name = name;
        Py_XDECREF(tmp);
    }

    self->number = nextnumber++;

    return 0;
}

void cnf_Variable_dealloc(Variable* self)
{
    Py_XDECREF(self->name);
    self->ob_type->tp_free((PyObject*)self);
}

PyObject* cnf_Variable_str(PyObject *self)
{
    Variable *v = (Variable *)self;

    return PyString_FromFormat("%s%s", v->inverted ? "-" : "", PyString_AsString(v->name));
}

PyObject* cnf_Variable_neg(PyObject* self)
{
    Variable *v = (Variable *)self;
    PyObject *args = PyTuple_Pack(2, v->name, PyInt_FromLong(1 - v->inverted));

    Variable *new = (Variable *)cnf_Variable_new(self->ob_type, args, NULL);
    cnf_Variable_init(new, args, NULL);

    return new;
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
