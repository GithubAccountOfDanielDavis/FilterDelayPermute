from distutils.core import setup, Extension
import numpy as np

# define the extension module
fdp_c_module = Extension('fdp_c', sources=['fdp_c.c'])

# run the setup
setup(
    ext_modules=[fdp_c_module],
    include_dirs=[np.get_include()]
)
