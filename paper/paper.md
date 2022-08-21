---
title: "libdlfind: A C API and Python interface to the DL-FIND geometry optimization library"
tags:
  - Fortran
  - Python
  - geometry optimization
  - quantum chemistry
authors:
  - name: Kjell Jorner 
    orcid: 0000-0002-4191-6790
    affiliation: "1, 2, 3"
  - name: Alán Aspuru-Guzik^[Corresponding author]
    orcid: 0000-0002-8277-4434
    affiliation: "1, 2, 4, 5, 6, 7"
affiliations:
  - name: Department of Computer Science, University of Toronto, 40 St. George St, Toronto, Ontario M5S 2E4, Canada
    index: 1
  - name: Department of Chemistry, Chemical Physics Theory Group, 80 St. George St., University of Toronto, Ontario M5S 3H6, Canada
    index: 2
  - name: Department of Chemistry and Chemical Engineering, Chalmers University of Technology, Kemigården 4, SE-41258, Gothenburg, Sweden
    index: 3
  - name: Department of Chemical Engineering & Applied Chemistry, 200 College St., University of Toronto, Ontario M5S 3E5, Canada
    index: 4
  - name: Department of Materials Science & Engineering, 184 College St., University of Toronto, Ontario M5S 3E4, Canada
    index: 5
  - name: Vector Institute for Artificial Intelligence, 661 University Ave. Suite 710, Toronto, Ontario M5G 1M1, Canada
    index: 6
  - name: Lebovic Fellow, Canadian Institute for Advanced Research (CIFAR), 661 University Ave., Toronto, Ontario M5G 1M1, Canada
    index: 7
date: 20 August 2022
bibliography: paper.bib
---

# Summary

`libdlfind` is a C API and Python interface to the DL-FIND[@dlfind_2009]
geometry optimization package. It is intended for use by other programs as an
optimization backend. DL-FIND features robust geometry optimization routines for
a variety of optimization tasks such as minima, transition states and conical
intersections. It is fast, scales well, and is optimized for use in QM/MM
calculations. We envision that `libdlfind` will find use in workflows 
for high-throughput calculations and as geometry optimization backend for 
quantum-chemistry programs.

# Statement of need

Modern computational workflows for high-throughput quantum-chemical
optimizations of molecules and materials are often written in Python. They serve
as the ["glue"](https://numpy.org/doc/stable/user/c-info.python-as-glue.html)
between many different executables and libraries. However, most molecular
geometry optimization algorithms are embedded within executable programs and
tightly connected to the specific quantum-chemical methods. For better
flexibility, geometry optimization should be carried out with a library that
can accept energies, gradients and Hessians from arbitrary sources. 

An example of a workflow engine that utilizes such libraries is
[QCEngine](https://github.com/MolSSI/QCEngine) [@qcengine_2021] from the [The
Molecular Science Software Institute](https://molssi.org). QCEngine currently
supports the geometry optimization backends
[geomeTRIC](https://github.com/leeping/geomeTRIC) [@geometric_2016],
[PyBerny](https://github.com/jhrmnn/pyberny) and
[OptKing](https://github.com/psi-rking/optking). geomeTRIC and PyBerny are also
supported by the
[PySCF](https://github.com/pyscf/pyscf/) [@pyscf_2018; pyscf_2020] quantum
chemistry program. In addition to those libraries, the recent
[Sella](https://github.com/zadorlab/sella) package is an optimization library for
the [Atomic Simulation Environment](https://gitlab.com/ase/ase) [@ase_2017]
focused on library use and
[pysisyphus](https://github.com/eljost/pysisyphus) [@pysisyphus_2021] is focused
on command line use.

DL-FIND is written in Fortran and designed to be interfaced from
Fortran with limited support from C. It can be used together with a series of
quantum chemistry codes via [ChemShell](https://www.chemshell.org) and its
Python version Py-ChemShell [@chemshell_2019]. In comparison, `libdlfind` provides a
leaner interface that allows the user to supply their own arbitrary functions
for calculation of energies, gradients and Hessians. `libdlfind` therefore
fulfills the need of ease of integration into modern Python-based workflows. The
general C API of `libdlfind` takes advantage of Modern Fortran [@fortran_2022] C
interoperability and allows access from any language with a C Foreign Function
Interface (CFFI). A Python API is packaged for installation via `pip` and
`conda`, and it would be straightforward to package also for other languages
such as with [BinaryBuilder](https://binarybuilder.org) for Julia. The
LGPL-3.0-or-later license further allows wide adoptation.

# Features and implementation

The source code from DL-FIND is used in unmodified form from Py-ChemShell
v21.0.1. On top of this, `libdlfind` adds a number of Fortran module files to
create a C API. The end user interacts with the C-interoperable function
`api_dl_find` which takes a number of user-supplied callback functions to
calculate energies, gradients and Hessians. The library is well documented in
the `README.md` with a number of usage examples from Python, with emphasis on
robustness and thread-safe parallelization. The MPI parallelization of DL-FIND
is currently not supported. 

DL-FIND itself provides the following optimization types:

- Minima
- Transition states
- Reaction paths
- Conical intersections

The following coordinate systems are available:

- (Mass-weighted) Cartesian coordinates
- Delocalized internal coordinates
- Hybrid delocalized coordinates

In addition, constraints and freezing of atoms is also supported. DL-FIND is
further optimized for use in QM/MM calculations.

# Acknowledgements

Cyrille Lavigne, Ivan Pribec and Sebastian Ehlert are acknowledged for
helpful feedback during the development of the library. K.J. acknowledges funding
through an International Postdoc grant from the Swedish Research Council (No.
2020-00314). A. A.-G. thanks Dr. Anders G. Frøseth for his generous support. A.
A.-G. also acknowledges the generous support of Natural Resources Canada and the
Canada 150 Research Chairs program.

> ⚠️ Add Alán additional acknowledgments

# References