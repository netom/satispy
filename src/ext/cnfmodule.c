#include <Python.h>

static PyObject *CnfError;

static PyObject * cnf_system(PyObject *self, PyObject *args)
{
    const char *command;
    int sts;

    if (!PyArg_ParseTuple(args, "s", &command)) {
        return NULL;
    }

    sts = system(command);
    return Py_BuildValue("i", sts);
}

static PyMethodDef CnfMethods[] = {
    {"system",  cnf_system, METH_VARARGS,
     "Execute a shell command."},
    {NULL, NULL, 0, NULL}        /* Sentinel */
};

PyMODINIT_FUNC initcnf(void)
{
    PyObject *m;

    m = Py_InitModule("cnf", CnfMethods);
    if (m == NULL)
        return;

    CnfError = PyErr_NewException("cnf.error", NULL, NULL);
    Py_INCREF(CnfError);
    PyModule_AddObject(m, "error", CnfError);
}
