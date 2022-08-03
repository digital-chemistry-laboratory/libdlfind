# libdlfind

`libdlfind` is a C-API and Python interface to the [DL-FIND](https://www.chemshell.org/dl-find) geometry optimization library. It is mainly intended for use in high-level libraries as an optimization backend. 

## Installation

### Installation with pip

```shell
$ pip install libdlfind
```

### Installation with conda

```shell
$ conda install -c conda-forge libdlfind
```

### Shared library

The shared library can also be used to interface with other languages than Python. It can be built with CMake and installed.

```shell
$ git clone https://github.com/kjelljorner/libdlfind.git
$ cd libdlfind
$ cmake -B build -DCMAKE_BUILD_TYPE=Release 
$ cmake --build build
$ cmake --install build # Optionally use --prefix
```

## Example

Here we illustrate the use of libdlfind to optimize a molecule with [xtb](https://github.com/grimme-lab/xtb) using [xtb-python](https://github.com/grimme-lab/xtb-python).

```python
import functools

import numpy as np
from libdlfind import dl_find
from libdlfind.callback import (dlf_get_gradient_wrapper,
                                dlf_put_coords_wrapper, make_dlf_get_params)
from xtb.interface import Calculator
from xtb.utils import get_method

# Create function to calculate energies and gradients
@dlf_get_gradient_wrapper
def e_g_func(coordinates, iimage, kiter, calculator):
    calculator.update(coordinates)
    results = calculator.singlepoint()
    energy = results.get_energy()
    gradient = results.get_gradient()
    return energy, gradient

# Create function to store results from DL-FIND
@dlf_put_coords_wrapper
def store_results(switch, energy, coordinates, iam, traj_coords, traj_energies):
    traj_coords.append(np.array(coordinates))
    traj_energies.append(energy)
    return

def main():
    # Create hydrogen molecule
    numbers = np.array([1, 1])
    positions = np.array([[0.0, 0.0, 0.0], [0.0, 0.0, 1.5]])  # Coordinates in Bohr

    # Create XTB calculator
    calculator = Calculator(get_method("GFN2-xTB"), numbers, positions)

    # Two lists for storing results
    traj_energies = []
    traj_coordinates = []

    dlf_get_params = make_dlf_get_params(coords=positions)
    dlf_get_gradient = functools.partial(e_g_func, calculator=calculator)
    dlf_put_coords = functools.partial(
        store_results, traj_coords=traj_coordinates, traj_energies=traj_energies
    )
	
    # Run DL-FIND
    dl_find(
        nvarin=len(numbers) * 3,
        dlf_get_gradient=dlf_get_gradient,
        dlf_get_params=dlf_get_params,
        dlf_put_coords=dlf_put_coords,
    )
	
    # Print results
    print(f"Number of iterations: {len(traj_energies)}")
    print(f"Finaly energy (a.u.): {traj_energies[-1]}")

if __name__ == "__main__":
    main()
```

With the output

```
Number of iterations: 4
Finaly energy (a.u.): -0.9826861748759066
```

## Usage

`libdlfind` tries to stay as close as possible to the behavior of the original DL-FIND code. Optimization is called via the main function `dl_find` with the following signature

```python
def dl_find(
    nvarin: int,
    nvarin2: int = 0,
    nspec: int | None = None,
    master: int = 1,
    *,
    dlf_error: Callable = lambda *args: None,
    dlf_get_gradient: Callable = lambda *args: None,
    dlf_get_hessian: Callable = lambda *args: None,
    dlf_get_multistate_gradients: Callable = lambda *args: None,
    dlf_get_params: Callable,
    dlf_put_coords: Callable = lambda *args: None,
    dlf_update: Callable = lambda *args: None,
) -> None:
```

For typical optimizations, `nvarin` can be set from the number of atoms of the system: 

```python
n_atoms = 3
nvarin = 3 * n_atoms
```

As there is currently no MPI support for `libdlfind`, the `master` argument can safely be left at the default value. The following seven user-supplied functions are described in the [documentation](docs/documentation.pdf). The most important are:

- `dlf_get_params` is always needed
- `dlf_get_gradient` is needed for ground state optimizations
- `dlf_get_multistate_gradients` is needed for minimum energy crossing point optimizations
- `dlf_put_coords` is needed for capturing the output of the optimization

The less important are:

- `dlf_get_hessian` is needed when Hessian information is used for optimization
- `dlf_error` allows error handling if DL-FIND crashes
- `dlf_update` allows the calling code to update any neighbour list (for QM/MM)

The functions should be C-interoperable and need to be either (a) dummies for the functions that are not needed for a particular calculation type or (b) created by `libdlfind` decorators or function factories. The dummy functions simply do nothing, and this is the default value for all expect `dlf_put_coords`, which is needed for all calculation types. The user therefore only needs to give `dl_find` the functions needed for a specific calculation type.

#### Decorators and factory functions

The easiest way to create the functions is with the decorators and factory functions in `libdlfind.callback`.

##### dlf_error

The `dlf_error` function does something in response to DL-FIND crashing, and should ideally not return control to DL-FIND. In Python, this is not easy to achieve. Unfortunately, we also cannot catch exceptions as `dlf_error` is a callback function that is called from the Fortran side. There  is therefore little use for `dlf_error` from Python, but it could conceivably be used for cleanup of files generated by DL-FIND.

```python
from pathlib import Path

def dlf_error():
    p = Path("qts_reactant.txt")
    p.unlink()
    return
```

##### dlf_get_gradient

To construct `dlf_get_gradient`, we need a function that calculates the energy and gradients. It takes take three arguments, `coordinates`, `iimage` and `kiter`, of which the latter two can be ignored most of the time.  It should return the energy as a float and the gradient as a NumPy array with shape (n_atoms, 3). In the example below, we use a calculator object of some type to calculate the energy and gradient based on the coordinates. `functools.partial` is used to create a function which only has the three arguments expected by DL-FIND.

```python
import functools
from libdlfind.callback import dlf_get_gradient_wrapper

@dlf_get_gradient_wrapper
def e_g_func(coordinates: NDArray, iimage: int, kiter: int, calculator: object):
    calculator.coordinates = (
        coordinates  # coordinates is an array with shape (n_atoms, 3) in Bohr
    )
    energy, gradient = calculator.sp(return_gradient=True)
    return energy, gradient

dlf_get_gradient = functools.partial(e_g_func, calculator=calculator)
```

##### dlf_get_hessian

The `dlf_get_hessian` function takes one argument, `coordinates` and should return the Hessian as a NumPy array with shape (n_atoms * 3, n_atoms * 3). Here is an example of how it can be created.

```python
import functools
from libdlfind.callback import dlf_get_hessian_wrapper

@dlf_get_hessian_wrapper
def hess_func(coordinates: NDArray, calculator: object):
    calculator.coordinates = (
        coordinates  # coordinates is an array with shape (n_atoms, 3) in Bohr
    )
    hessian = calculator.hessian()
    return hessian

dlf_get_hessian = functools.partial(hess_func, calculator=calculator)
```

##### dlf_get_multistate_gradients

The `dlf_get_multistate_gradients` is used for multi-state optimizations such as for minimum energy crossing points (MECPs). It is similar to `dlf_get_gradient` but requires the calculation of two energies and gradients, one for each state, as well as their coupling (for certain algorithms). Here's an example of how it can be created.

```python
import functools
from libdlfind.callback import dlf_get_multistate_gradients_wrapper

@dlf_get_multistate_gradients_wrapper
def ms_e_g_func(
    coordinates: NDArray,
    needcoupling: int,
    iimage: int,
    calculator_1: object,
    calculator_2: object,
):
    coordinates = (
        coordinates * BOHR_TO_ANGSTROM
    )  # coordinates is an array with shape (n_atoms, 3) in Bohr
    calculator_1.coordinates = coordinates
    calculator_2.coordinates = coordinates
    e_1, g_1 = calculator_1.sp(
        return_gradient=True
    )  # g_1 and g_2 are arrays with shape (n_atoms, 3) in Hartree/Bohr
    e_2, g_2 = calculator_2.sp(return_gradient=True)
    return e_1, e_2, g_1, g_2, None  # Returns no coupling

dlf_get_multistate_gradients = functools.partial(
    ms_e_g_func,
    calculator_1=calculator_1,
    calculator_2=calculator_2,
)
```

The argument `needcoupling` will be 1 if multistate couplings should be calculated, and 0 otherwise. `iimage` is used for MPI runs.

##### dlf_get_params

The `dlf_get_params` function supplies all parameters for the DL-FIND calculation. There's a very large number of parameters, which are covered in some detail in the [Keywords section](#Keywords). All calculations require the coordinates, while other parameters can be given optionally.

```py3
from libdlfind.callback import make_dlf_get_params

dlf_get_params = make_dlf_get_params(
    coords=coordinates,  # coordinates is an array with shape (n_atoms, 3) in Bohr
    printl=1  # Increases print level
)
```

##### dlf_put_coords

The `dlf_put_coords` function allows storage of the results of the optimization. The following example stores the coordinates and energies of all points in the `traj_coordinates` and `traj_energies` lists.

```python
import functools
from libdlfind.callback import dlf_put_coords_wrapper

@dlf_put_coords_wrapper
def store_results(
    switch: int,
    energy: float,
    coordinates: NDArray,
    iam: int,
    traj_energies: Sequence,
    traj_coords: Sequence,
):
    traj_energies.append(energy)
    traj_coords.append(
        np.array(coordinates)
    )  # np.array creates a copy of the coordinate array at this point in time
    return

dlf_put_coords = functools.partial(
    store_results, traj_energies=traj_energies, traj_coords=traj_coordinates
)
```

If the argument `switch` is 1, `coordinates` contains the actual geometry. If `switch` is 2, `coordinates` contains the transition mode. `iam` is a flag applied for MPI runs.

##### dlf_update

The `dlf_update` function allows updating of neighbor lists for algorithms that require that. It doesn't seem to be used in DL-FIND so far and therefore we have no good use cases.

### Keywords

DL-FIND is a powerful optimization package with many options. They are partially described in the DL-FIND [documentation](docs/documentation.pdf)
and more in detail in [api.f90](src/api.f90) and [dlf global module.f90](src/dlf global module.f90).

The most important parameters for regular optimizations are:

- `printl`: Print level

- `icoord`: Type of coordinate system

- `iopt`: Type of optimization algorithm

- `iline`: Type of line search or trust radius

For optimizations using Hessian information:

- `inithessian`: Type of initial Hessian

- `update`: Hessian update mechanism

For conical intersection optimizations:

- `imultistate`: Multistate calculations

- `imicroiter`: Micro-iterative optimization
- `spec`: Fragment and frozen atom information

### Robust usage

#### Silence DL-FIND printout with wurlitzer

DL-FIND prints output to the standard output and standard error steams, which can clutter the output from a Python workflow. To silence these, we can use the [Wurlitzer](https://github.com/minrk/wurlitzer) package and the `pipes` context manager.

```python
from wurlitzer import pipes
    
with pipes() as (stdout, stderr):
    dl_find(
        nvarin=nvarin,
        dlf_get_gradient=dlf_get_gradient,
        dlf_get_params=dlf_get_params,
        dlf_put_coords=dlf_put_coords,
    )
```

#### Avoid crashes with pebble

DL-FIND sometimes handles errors by calling `STOP` on the Fortran side. Unfortunately, this will also terminate the parent process that launched DL-FIND. When running libdlfind as part of a larger workflow with many optimizations, this could be disastrous. A workaround is to use a separate Python process to isolate DL-FIND. If that process crashes, we can catch that as an exception. For this we will use the [Pebble](https://github.com/noxdafox/pebble) library. We create a wrapper function where DL-FIND is called, and decorate this function with `concurrent.process` from Pebble.

```py3
from pebble import concurrent, ProcessExpired

@concurrent.process
def opt_mol(mol):
    ...
    dl_find(
        nvarin=nvarin,
        dlf_get_gradient=dlf_get_gradient,
        dlf_get_params=dlf_get_params,
        dlf_put_coords=dlf_put_coords,
    )
    return traj_energies, traj_coordinates

def main():
    ...
    future = opt_mol(mol)
    try:
        traj_energies, traj_coordinates = future.result()
    except ProcessExpired:
        traj_energies, traj_coordinates = None, None
    ...

if __name__ == "__main__":
    main()
```

#### Parallel execution

DL-FIND makes extensive use of global variables stored in modules. For this reason, parallel execution with shared memory will lead to crashes and/or unreliable results. The MPI capabilities of DL-FIND are not supported in libdlfind. Running multiple single-threaded jobs in parallel can be done with for example [`pebble.ProcessPool`](https://pythonhosted.org/Pebble/#pools) or [`concurrent.futures.ProcessPoolExecutor`](https://docs.python.org/3/library/concurrent.futures.html#processpoolexecutor). In that case, each process will have its own copy of the shared library and global variables.


## Background

libdlfind adds a lightweight and general C-compatible API to the DL-FIND Fortran code. It uses the original DL-FIND code from Py-ChemShell (v21.0.1) in unmodified form and adds three files:

- api.f90: C-interoperable interface functions
- mod_api.f90: Abstract interfaces callback functions from C 
- mod_globals.f90: Module that stores pointers to callback functions.

Currently, the MPI parallelization of DL-FIND is not supported.

The original code can be obtained at the [ChemShell website](https://www.chemshell.org/dl-find) after registration.

## Citation

DL-FIND should be cited as:

Johannes Kästner, Joanne M. Carr, Thomas W. Keal, Walter Thiel, Adrian Wander, and Paul Sherwood, *J. Phys. Chem. A*, 2009, 113 (43), 11856-11865.

## Acknowledgements

Cyrille Lavigne ([@clavigne](https://github.com/clavigne)), Ivan Pribec ([@ivan-pi](https://github.com/ivan-pi)) and Sebastian Ehlert ([@awvwgk](https://github.com/awvwgk)) for many helpful suggestions.