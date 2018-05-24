from distutils.core import setup
from Cython.Build import cythonize

setup(
    name = 'upload',
    ext_modules = cythonize('upload.pyx'),
)
