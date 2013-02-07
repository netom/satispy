#include <Python.h>

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
} cnf_VariableObject;

static PyTypeObject cnf_VariableType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "cnf.Variable",            /*tp_name*/
    sizeof(cnf_VariableObject),/*tp_basicsize*/
    0,                         /*tp_itemsize*/
    0,                         /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,        /*tp_flags*/
    "Variable",                /* tp_doc */
};

typedef struct {
    PyObject_HEAD
    /* Type-specific fields go here. */
} cnf_CnfObject;

static PyTypeObject cnf_CnfType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "cnf.Cnf",                 /*tp_name*/
    sizeof(cnf_CnfObject),     /*tp_basicsize*/
    0,                         /*tp_itemsize*/
    0,                         /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    0,                         /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    0,                         /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,        /*tp_flags*/
    "Cnf expression",          /* tp_doc */
};

static PyMethodDef cnf_methods[] = {
    {NULL}  /* Sentinel */
};

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
#define PyMODINIT_FUNC void
#endif

PyMODINIT_FUNC initcnf(void) 
{
    PyObject* m;

    cnf_VariableType.tp_new = PyType_GenericNew;
    cnf_CnfType.tp_new = PyType_GenericNew;

    if (PyType_Ready(&cnf_VariableType) < 0) {
        return;
    }

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
