#include <Python.h>
#include "structmember.h"

#include "cnf_variable.h"
#include "cnf_cnf.h"

/****************************** Variable ******************************/

static PyNumberMethods Variable_NumberMethods = {
     0, /*nb_add*/
     0, /*nb_subtract*/
     0, /*nb_multiply*/
     0, /*nb_divide*/
     0, /*nb_remainder*/
     0, /*nb_divmod*/
     0, /*nb_power*/
     cnf_Variable_neg, /*nb_negative*/
     0, /*nb_positive*/
     0, /*nb_absolute*/
     0, /*nb_nonzero, Used by PyObject_IsTrue */
     0, /*nb_invert*/
     0, /*nb_lshift*/
     cnf_Variable_rshift, /*nb_rshift*/
     cnf_Variable_and, /*nb_and*/
     cnf_Variable_xor, /*nb_xor*/
     cnf_Variable_or, /*nb_or*/
     0, /*nb_coerce, Used by the coerce() function */
     0, /*nb_int*/
     0, /*nb_long*/
     0, /*nb_float*/
     0, /*nb_oct*/
     0, /*nb_hex*/

     /* Added in release 2.0 */
     0, /*nb_inplace_add*/
     0, /*nb_inplace_subtract*/
     0, /*nb_inplace_multiply*/
     0, /*nb_inplace_divide*/
     0, /*nb_inplace_remainder*/
     0, /*nb_inplace_power*/
     0, /*nb_inplace_lshift*/
     0, /*nb_inplace_rshift*/
     0, /*nb_inplace_and*/
     0, /*nb_inplace_xor*/
     0, /*nb_inplace_or*/

     /* Added in release 2.2 */
     0, /*nb_floor_divide*/
     0, /*nb_true_divide*/
     0, /*nb_inplace_floor_divide*/
     0, /*nb_inplace_true_divide*/

     /* Added in release 2.5 */
     0, /*nb_index*/
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

static PyTypeObject cnf_VariableType = {
    PyObject_HEAD_INIT(NULL)
    0,                         /*ob_size*/
    "cnf.Variable",            /*tp_name*/
    sizeof(Variable),/*tp_basicsize*/
    0,                         /*tp_itemsize*/
    (destructor)cnf_Variable_dealloc, /*tp_dealloc*/
    0,                         /*tp_print*/
    0,                         /*tp_getattr*/
    0,                         /*tp_setattr*/
    0,                         /*tp_compare*/
    0,                         /*tp_repr*/
    &Variable_NumberMethods,   /*tp_as_number*/
    0,                         /*tp_as_sequence*/
    0,                         /*tp_as_mapping*/
    0,                         /*tp_hash */
    0,                         /*tp_call*/
    cnf_Variable_str,          /*tp_str*/
    0,                         /*tp_getattro*/
    0,                         /*tp_setattro*/
    0,                         /*tp_as_buffer*/
    Py_TPFLAGS_DEFAULT,        /*tp_flags*/
    "Variable",                /*tp_doc */
    0,		                   /*tp_traverse */
    0,   	                   /*tp_clear */
    0,	                       /*tp_richcompare */
    0,	                       /*tp_weaklistoffset */
    0,	                       /*tp_iter */
    0,	                       /*tp_iternext */
    Variable_methods,          /*tp_methods */
    Variable_members,          /*tp_members */
    0,                         /*tp_getset */
    0,                         /*tp_base */
    0,                         /*tp_dict */
    0,                         /*tp_descr_get */
    0,                         /*tp_descr_set */
    0,                         /*tp_dictoffset */
    (initproc)cnf_Variable_init,/*tp_init */
    0,                         /*tp_alloc */
    cnf_Variable_new,          /*tp_new */
};

/********************************* CNF ********************************/

static PyNumberMethods Cnf_NumberMethods = {
     0, /*nb_add*/
     0, /*nb_subtract*/
     0, /*nb_multiply*/
     0, /*nb_divide*/
     0, /*nb_remainder*/
     0, /*nb_divmod*/
     0, /*nb_power*/
     cnf_Cnf_neg, /*nb_negative*/
     0, /*nb_positive*/
     0, /*nb_absolute*/
     0, /*nb_nonzero, Used by PyObject_IsTrue */
     0, /*nb_invert*/
     0, /*nb_lshift*/
     cnf_Cnf_rshift, /*nb_rshift*/
     cnf_Cnf_and, /*nb_and*/
     cnf_Cnf_xor, /*nb_xor*/
     cnf_Cnf_or, /*nb_or*/
     0, /*nb_coerce, Used by the coerce() function */
     0, /*nb_int*/
     0, /*nb_long*/
     0, /*nb_float*/
     0, /*nb_oct*/
     0, /*nb_hex*/

     /* Added in release 2.0 */
     0, /*nb_inplace_add*/
     0, /*nb_inplace_subtract*/
     0, /*nb_inplace_multiply*/
     0, /*nb_inplace_divide*/
     0, /*nb_inplace_remainder*/
     0, /*nb_inplace_power*/
     0, /*nb_inplace_lshift*/
     cnf_Cnf_inplace_rshift, /*nb_inplace_rshift*/
     cnf_Cnf_inplace_and, /*nb_inplace_and*/
     cnf_Cnf_inplace_xor, /*nb_inplace_xor*/
     cnf_Cnf_inplace_or, /*nb_inplace_or*/

     /* Added in release 2.2 */
     0, /*nb_floor_divide*/
     0, /*nb_true_divide*/
     0, /*nb_inplace_floor_divide*/
     0, /*nb_inplace_true_divide*/

     /* Added in release 2.5 */
     0, /*nb_index*/
};

static PyMemberDef Cnf_members[] = {
    {NULL}
};

static PyMethodDef Cnf_methods[] = {
    {NULL}
};

static PyTypeObject cnf_CnfType = {
    PyObject_HEAD_INIT(NULL)
    .tp_name      = "cnf.Cnf",                 /*tp_name*/
    .tp_basicsize = sizeof(Cnf),               /*tp_basicsize*/
    .tp_dealloc   = (destructor)cnf_Cnf_dealloc,/*tp_dealloc*/
    .tp_as_number = &Cnf_NumberMethods,        /*tp_as_number*/
    .tp_str       = cnf_Cnf_str,               /*tp_str*/
    .tp_flags     = Py_TPFLAGS_DEFAULT,        /*tp_flags*/
    .tp_doc       = "Cnf expression",          /* tp_doc */
    .tp_methods   = Cnf_methods,               /*tp_methods */
    .tp_members   = Cnf_members,               /*tp_members */
    .tp_init      = (initproc)cnf_Cnf_init,    /*tp_init */
    .tp_new       = cnf_Cnf_new               /*tp_new */
};

static PyMethodDef cnf_methods[] = {
    {NULL}  /* Sentinel */
};

/********************** Module initialization *************************/

PyMODINIT_FUNC initcnf(void) 
{
    PyObject* m;

    cnf_VariableType.tp_new = PyType_GenericNew;
    if (PyType_Ready(&cnf_VariableType) < 0) {
        return;
    }

    //cnf_VariableType.tp_dict = PyDict_New();
    //PyDict_SetItemString(cnf_VariableType.tp_dict, "nextnumber", PyInt_FromLong(0));

    cnf_CnfType.tp_new = PyType_GenericNew;
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
