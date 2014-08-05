from setuptools import setup, find_packages

setup(
    name='SimpleSolidPy',
    version='0.0.2',
    description='Python interface to for declarative geometry',
    author='Dwight Hubbard',
    author_email='d@d-h.us',
    url='https://github.com/dhubbard/SimpleSolidPy',
    py_modules=['SimpleSolidPy'],
    classifiers=[
        "Programming Language :: Python",
        #"Programming Language :: Python :: 3",
        #"Development Status :: 4 - Beta",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    packages=find_packages(),
    #install_requires=[],
)
