from setuptools import find_packages, setup, Extension
from setuptools.command.install import install

import subprocess
import os

requirements=[
    "numpy",
    "setuptools"
]

class LibInstall(install):
    def run(self):
        command = "make"
        process = subprocess.Popen(command, shell=True, cwd='lib_src')
        process.wait()
        install.run(self)
        
packages = find_packages(".")

'''
lib_ext = Extension(
    'PLClib.PLClib',
    sources=['PLClib/PLC_lib_vec.cpp'],
    extra_compile_args = ['-fPIC'],
    target='PLClib'
    )
'''

setup(
    name='PLClib', 
    version='1.0',
    packages = packages,
    python_requires=">=3.7",
    include_package_data=True,
    package_data={'PLClib': ['PLC_lib_vec.so']},
    #ext_modules=[lib_ext],
    cmdclass={'install': LibInstall}
    )

