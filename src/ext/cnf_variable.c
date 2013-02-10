#include <Python.h>
#include "structmember.h"

#include "cnf_module.h"
#include "cnf_variable.h"
#include "cnf_cnf.h"

int64_t nextnumber;

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

    if (self->inverted != 0 && self->inverted != 1) {
        PyErr_SetString(PyExc_ValueError, "Parameter 'inverted' must be either 0 or 1.");
        return -1;
    }

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
    Variable *me = (Variable *)self;
    return PyString_FromFormat("%s%s", me->inverted ? "-" : "", PyString_AsString(me->name));
}

PyObject* cnf_Variable_neg(PyObject* self)
{
    Variable *me = (Variable *)self;
    PyObject *args = PyTuple_Pack(2, me->name, PyInt_FromLong(1 - me->inverted));
    return PyObject_CallObject((PyObject *) &cnf_VariableType, args);
}

PyObject* cnf_Variable_and(PyObject* self, PyObject* other)
{
    if (other->ob_type == &cnf_VariableType) {
        Cnf *cnf = (Cnf *)PyObject_CallObject((PyObject *) &cnf_CnfType, NULL);
        return (PyObject *)cnf;
    } else if (other->ob_type == &cnf_CnfType) {
        return cnf_Cnf_and(other, self);
    } else {
        PyErr_SetString(
            PyExc_TypeError,
            "Only Variable and Cnf types can be mixed in an expression"
        );
        return NULL;
    }
}

PyObject* cnf_Variable_or(PyObject* self, PyObject* other)
{
    if (other->ob_type == &cnf_VariableType) {
        Variable *me = (Variable *)self;
        Variable *ot = (Variable *)other;
        Cnf *cnf = (Cnf *)PyObject_CallObject((PyObject *) &cnf_CnfType, NULL);
        // TODO: variable numbers
        // TODO: cnf->ensureSize(N, M)
        // TODO: cnf->setVariable(clause, var) (inline? macro?)
        cnf->clauses = 1;
        return (PyObject *)cnf;
    } else if (other->ob_type == &cnf_CnfType) {
        return cnf_Cnf_or(other, self);
    } else {
        PyErr_SetString(
            PyExc_TypeError,
            "Only Variable and Cnf types can be mixed in an expression"
        );
        return NULL;
    }
}

PyObject* cnf_Variable_xor(PyObject* self, PyObject* other)
{
    if (other->ob_type == &cnf_VariableType) {
        Cnf *cnf = (Cnf *)PyObject_CallObject((PyObject *) &cnf_CnfType, NULL);
        return (PyObject *)cnf;
    } else if (other->ob_type == &cnf_CnfType) {
        return cnf_Cnf_xor(other, self);
    } else {
        PyErr_SetString(
            PyExc_TypeError,
            "Only Variable and Cnf types can be mixed in an expression"
        );
        return NULL;
    }
}

PyObject* cnf_Variable_rshift(PyObject* self, PyObject* other)
{
    if (other->ob_type == &cnf_VariableType) {
        Cnf *cnf = (Cnf *)PyObject_CallObject((PyObject *) &cnf_CnfType, NULL);
        return (PyObject *)cnf;
    } else if (other->ob_type == &cnf_CnfType) {
        return cnf_Cnf_rshift(other, self);
    } else {
        PyErr_SetString(
            PyExc_TypeError,
            "Only Variable and Cnf types can be mixed in an expression"
        );
        return NULL;
    }
}
