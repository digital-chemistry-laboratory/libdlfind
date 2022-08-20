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

# Statement of need

One example of such as workflow engine is [QCEngine](https://github.com/MolSSI/QCEngine) from the [The Molecular Science Software Institute](https://molssi.org), which currently support the geometry optimization backends [geomeTRIC](https://github.com/leeping/geomeTRIC) and [PyBerny](https://github.com/jhrmnn/pyberny). Coincidentally, these are also the backends supported by the [PySCF](https://github.com/pyscf/pyscf/) program.

[ChemShell](https://www.chemshell.org) and its Python version Py-ChemShell[@lu_2019] support DL-FIND as the geometry optimization backend. We wanted a leaner interface that would allow the user to supply their own arbitrary backends for calculation of energies, gradients and Hessians.

 and [Sella](https://github.com/zadorlab/sella) which are focused on library use as well as  and [pysisyphus](https://github.com/eljost/pysisyphus) that are focused on command line use.

# Features and implementation

# Acknowledgements

# References