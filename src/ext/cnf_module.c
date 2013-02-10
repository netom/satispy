#include <Python.h>
#include "structmember.h"

#include "cnf_module.h"
#include "cnf_variable.h"
#include "cnf_cnf.h"

/****************************** Variable ******************************/

static PyNumberMethods Variable_NumberMethods = {
     .nb_negative = cnf_Variable_neg,
     .nb_rshift = cnf_Variable_rshift,
     .nb_and = cnf_Variable_and,
     .nb_xor = cnf_Variable_xor,
     .nb_or = cnf_Variable_or
};

static PyMemberDef Variable_members[] = {
    {"name", T_OBJECT_EX, offsetof(Variable, name), 0,
     "Variable name"},
    {"inverted", T_INT, offsetof(Variable, inverted), 0,
     "Marks if the variable is inverted in an expression"},
    {"number", T_INT, offsetof(Variable, number), 0,
     "Number of variable. Starts with 0."},
    {NULL}
};

static PyMethodDef Variable_methods[] = {
    {NULL}
};

PyTypeObject cnf_VariableType = {
    PyObject_HEAD_INIT(NULL)
    .tp_name = "cnf.Variable",
    .tp_basicsize = sizeof(Variable),
    .tp_dealloc = (destructor)cnf_Variable_dealloc,
    .tp_as_number = &Variable_NumberMethods,
    .tp_str = cnf_Variable_str,
    .tp_flags = Py_TPFLAGS_DEFAULT,
    .tp_doc = "Variable",
    .tp_methods = Variable_methods,
    .tp_members = Variable_members,
    .tp_init = (initproc)cnf_Variable_init,
    .tp_new = cnf_Variable_new,
};

/********************************* CNF ********************************/

static PyNumberMethods Cnf_NumberMethods = {
     .nb_negative = cnf_Cnf_neg,
     .nb_rshift = cnf_Cnf_rshift,
     .nb_and = cnf_Cnf_and,
     .nb_xor = cnf_Cnf_xor,
     .nb_or = cnf_Cnf_or,
     .nb_inplace_rshift = cnf_Cnf_inplace_rshift,
     .nb_inplace_and = cnf_Cnf_inplace_and,
     .nb_inplace_xor = cnf_Cnf_inplace_xor,
     .nb_inplace_or = cnf_Cnf_inplace_or
};

static PyMemberDef Cnf_members[] = {
    {NULL}
};

static PyMethodDef Cnf_methods[] = {
    {"getBuffer", cnf_Cnf_getBuffer, METH_NOARGS,
     "Returns the internal buffer as a python string"},
    {NULL}
};

PyTypeObject cnf_CnfType = {
    PyObject_HEAD_INIT(NULL)
    .tp_name      = "cnf.Cnf",
    .tp_basicsize = sizeof(Cnf),
    .tp_dealloc   = (destructor)cnf_Cnf_dealloc,
    .tp_as_number = &Cnf_NumberMethods,
    .tp_str       = cnf_Cnf_str,
    .tp_flags     = Py_TPFLAGS_DEFAULT,
    .tp_doc       = "Cnf expression",
    .tp_methods   = Cnf_methods,
    .tp_members   = Cnf_members,
    .tp_init      = (initproc)cnf_Cnf_init,
    .tp_new       = cnf_Cnf_new
};

static PyMethodDef cnf_methods[] = {
    {NULL}
};

/********************** Module initialization *************************/

PyMODINIT_FUNC initcnf(void) 
{
    PyObject* m;

    if (PyType_Ready(&cnf_VariableType) < 0) {
        return;
    }

    //Static variable
    //cnf_VariableType.tp_dict = PyDict_New();
    //PyDict_SetItemString(cnf_VariableType.tp_dict, "nextnumber", PyInt_FromLong(0));

    if (PyType_Ready(&cnf_CnfType) < 0) {
        return;
    }

    m = Py_InitModule3("cnf", cnf_methods,
                       "A mosule that provides fast CNF expression building tools");

    Py_INCREF(&cnf_VariableType);
    Py_INCREF(&cnf_CnfType);

    PyModule_AddObject(m, "Variable", (PyObject *)&cnf_VariableType);
    PyModule_AddObject(m, "Cnf", (PyObject *)&cnf_CnfType);
}
