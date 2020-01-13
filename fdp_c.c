#define PY_SSIZE_T_CLEAN
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <stdio.h>
#include <stdbool.h>
#include <stdint.h>
#include <string.h>
#include "Python.h"
#include <numpy/arrayobject.h>

static const uint16_t UNPERMUTE[256] = {
    121, 233, 122, 173, 140,  83,   1, 185, 194,   8,  28, 135,  94,
    195, 252,  17,  46, 199,  37,  21, 248, 222,  99, 160,  19,  35,
    115, 138,  96,  79,   9,  93, 142,  24, 183,  95, 131, 230,  51,
    164, 157, 110,  97, 170, 154,  44, 124, 166, 220, 180, 209, 104,
    234, 175, 207,  54,  84, 223, 218, 196,  59, 132, 146, 206, 153,
    88,   45,  47,  15,  71, 151, 250, 201,  68, 243,  38, 109, 123,
    113,   2, 182, 163,  81, 190,  53,  90,  36, 241, 221, 193,  78,
    189, 253, 101, 167, 106,  18,  31, 130, 239, 125,  60, 255, 238,
    56,  174, 251, 208,  66,  73, 188,  82,  98,  76,  69,  74, 240,
    4,   118, 111,  22, 246, 141, 158,  25, 100,  63,  58, 148, 229,
    236, 198,  85, 176, 203, 147,  14,  39, 145,  57, 120,  72, 134,
    52,   65, 171, 107, 143,  32, 235, 114, 237,  23, 159,  86, 112,
    156, 231,  70, 127, 225, 169,  87, 181,  29, 155, 200,   7, 117,
    217,  80, 186,  61, 102, 211, 172,  41,  50,  67, 254,  10,  43,
    144, 128,  30,   5,  89, 227, 249, 213,  33, 228, 161, 119, 150,
    168,  40, 152, 178,  16, 133,  49, 242, 224, 108, 126,   3, 215,
    27,  204, 245, 184, 210, 212, 244,  48, 187,  13, 219,  91,  55,
    197,  11,  34, 137,  64, 202, 216,   0, 191,  12, 139, 149, 177,
    192,  20, 205,  92, 179,  42, 105, 232,   6,  77, 165,  62,  75,
    116, 226, 162, 136, 103, 214,  26, 129, 247
};

static const uint16_t PERMUTE[256] = {
    228,   6,  79, 206, 117, 185, 242, 167,   9,  30, 180, 222, 230,
    217, 136,  68, 199,  15,  96,  24, 235,  19, 120, 152,  33, 124,
    253, 208,  10, 164, 184,  97, 148, 190, 223,  25,  86,  18,  75,
    137, 196, 176, 239, 181,  45,  66,  16,  67, 215, 201, 177,  38,
    143,  84,  55, 220, 104, 139, 127,  60, 101, 172, 245, 126, 225,
    144, 108, 178,  73, 114, 158,  69, 141, 109, 115, 246, 113, 243,
    90,   29, 170,  82, 111,   5,  56, 132, 154, 162,  65, 186,  85,
    219, 237,  31,  12,  35,  28,  42, 112,  22, 125,  93, 173, 251,
    51,  240,  95, 146, 204,  76,  41, 119, 155,  78, 150,  26, 247,
    168, 118, 193, 140,   0,   2,  77,  46, 100, 205, 159, 183, 254,
    98,   36,  61, 200, 142,  11, 250, 224,  27, 231,   4, 122,  32,
    147, 182, 138,  62, 135, 128, 232, 194,  70, 197,  64,  44, 165,
    156,  40, 123, 153,  23, 192, 249,  81,  39, 244,  47,  94, 195,
    161,  43, 145, 175,   3, 105,  53, 133, 233, 198, 238,  49, 163,
    80,   34, 211,   7, 171, 216, 110,  91,  83, 229, 234,  89,   8,
    13,   59, 221, 131,  17, 166,  72, 226, 134, 209, 236,  63,  54,
    107,  50, 212, 174, 213, 189, 252, 207, 227, 169,  58, 218,  48,
    88,   21,  57, 203, 160, 248, 187, 191, 129,  37, 157, 241,   1,
    52,  149, 130, 151, 103,  99, 116,  87, 202,  74, 214, 210, 121,
    255,  20, 188,  71, 106,  14,  92, 179, 102
};

static PyObject* encode (
        PyObject *self,
        PyObject *args,
        PyObject *kwargs
) {
    // Handle arguments
    Py_buffer secret;
    Py_ssize_t block_size = 512;
    Py_ssize_t iterations = 20;
    bool backwards_compatible = true;

    static char *kwarg_names[] = {
        "secret", "block_size", "iterations",
        "backwards_compatible", NULL
    };

    if (!PyArg_ParseTupleAndKeywords(
        args, kwargs, "s*|nnp",
        kwarg_names, &secret, &block_size,
        &iterations, &backwards_compatible
    )) return NULL;

    // Setup working variables
    uint16_t block_buffer[block_size];
    memset(
        block_buffer,
        0,
        block_size * sizeof(uint16_t)
    );

    void *s = secret.buf;
    uint16_t *b = block_buffer;
    if (backwards_compatible)
    {
        b += (block_size - secret.len);
        block_buffer[0] = UNPERMUTE[block_buffer[0]];
    }
    while (s < secret.buf + secret.len)
    {
        memcpy(b, s, sizeof(char));
        s++; b++;
    }
    uint16_t state = 0;

    // Perform algorithm
    for (int i = 0; i < iterations; i++)
    {
        for (int b = 0; b < block_size; b++)
        {
            // PERMUTE
            uint16_t permuted_echo = PERMUTE[block_buffer[b]];

            // FILTER
            state -= (state >> 4);
            state += (permuted_echo << 4);

            // DELAY
            block_buffer[b] = (state >> 3) & 0x00FF;
        }
    }

    // Return data as list
    PyObject *block_list = PyList_New(block_size);
    for (int b = 0; b < block_size; b++)
    {
        int index = (backwards_compatible)
            ? (secret.len + b) % block_size
            : b;
        PyObject *intObj = PyLong_FromUnsignedLong(
            (unsigned long) block_buffer[b]
        );
        if (PyList_SetItem(block_list, index, intObj) < 0)
        {
            return NULL;
        }
    }

    return Py_BuildValue("(IO)", state, block_list);
}

static PyMethodDef fdp_c_methods[] = {
    {"encode", (PyCFunction)encode, METH_VARARGS|METH_KEYWORDS},
    {NULL,  NULL}   /* sentinel */
};

static struct PyModuleDef fdp_c_definition = {
    PyModuleDef_HEAD_INIT,
    "fdp_c",
    "FilterDelayPermute variant written in C",
    -1,
    fdp_c_methods
};

PyMODINIT_FUNC PyInit_fdp_c (void)
{
    Py_Initialize();
    return PyModule_Create(&fdp_c_definition);
}
