from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("cython_utils.pyx")
)
# By ZZBuAoYe
# python set_up.py build_ext --inplace