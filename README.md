# libdlfind

`libdlfind` is a Python interface to the DL-FIND geometry optimization library.

## Example

## Installation

### Installation with pip

```shell
$ pip install libdlfind
```

### Installation with conda

Coming.

### Shared library

The shared library can also be used to interface with other languages than Python, such as C. It can be built with cmake and then found in the ``build`` folder (given that compilers and BLAS can be found by cmake).

```shell
$ git clone <ADRESS>
$ cd libdlfind
$ cmake -B build -DCMAKE_BUILD_TYPE=Release 
$ make -C build
```

## Usage

`libdlfind` tries to stay as close as possible to the behavior of the original DL-FIND code. Optimization is called via the main function `dl_find` with the following signature

```python
def dl_find(
    nvarin: int,
    nvarin2: int,
    nspec: int,
    master: int = 1,
    *,
    dlf_error: Callable = dummy_dlf_error,
    dlf_get_gradient: Callable = dummy_dlf_get_gradient,
    dlf_get_hessian: Callable = dummy_dlf_get_hessian,
    dlf_get_multistate_gradients: Callable = dummy_dlf_get_multistate_gradients,
    dlf_get_params: Callable,
    dlf_put_coords: Callable = dummy_dlf_put_coords,
    dlf_update: Callable = dummy_dlf_update,
) -> None
```

For typical optimizations, `nvarin`, `nvarin2` and `nspec` can be set from the number of atoms of the system: 

```python
from libdlfind import dl_find
n_atoms = 3
nvarin = 3 * n_atoms
nvarin2 = 0
n_spec = 2 * n_atoms
```

As there is currently no MPI support for `libdlfind`, the `master` argument can safely be left at the default value. The following seven functions are described in the [documentation](docs/documentation.pdf). The most imporant are:

- `dlf_get_params` is always needed
- `dlf_get_gradient` is needed for ground state optimizations
- `dlf_get_multistate_gradients` is needed for conical intersection optimizations
- `dlf_put_coords` is needed for capturing the output of the optimization

The less important are:

- `dlf_get_hessian` is needed when Hessian information is used for the optimizations
- `dlf_error` allows error handling if DL-FIND crashes
- `dlf_update` allows the calling code to update any neighbour list (for QM/MM)

The functions should be C interoperable and need to be either (a) dummies for the functions that are not needed for a particular calculation type, or (b) created by `libdlfind` function factories. The dummy functions simply do nothing, and this is the default value for all expect `dlf_put_coords`, which is needed for all calculation types. The user therefore only needs to give `dl_find` the functions needed for a specific calculation type.

#### Factory functions

The easiest way to create the functions is by the factory functions in `libdlfind.factories`.

##### dld_error

To construct the `dlf_error` function, we need a function that does something in response to DL-FIND crashing.

```python
def error_func():
    raise Exception("Error in DL-FIND.")
    
dlf_error = make_dlf_error(error_func)
```

We could potentially catch this exception and handle it:

```python
try:
    dl_find(
        nvarin,
        nvarin2,
        nspec,
        dlf_get_params=dlf_get_params,
        dlf_get_gradient=dlf_get_gradient,
        dlf_error=dlf_error
    )
except:
    energy = 0
    coordinates = None
```

##### dlf_get_gradient

To construct `dlf_get_gradient`, we need a function that calculates the energy and gradients. It takes take three arguments, `coordinates`, `iimage` and `kiter`, of which the latter two can be ignored most of the time.  It should return the energy as a float and the gradient as a NumPy array with shape (n_atoms, 3). In the example below, we use a calculator object of some type to calculate the energy and gradient based on the coordinates. `functools.partial` is used to create a function which only has the three arguments expected by DL-FIND and the factory function `make_dlf_get_gradient` constructs the C-interoperable function that we can pass to `dl_find`.

```python
def e_g_func(coordinates: np.ndaray, iimage: int, kiter: int, calculator: object):
    calculator.coordinates = coordinates # coordinates is a np.ndarray with shape (n_atoms, 3)
    energy, gradient = calculator.sp(return_gradient=True)
    return energy, gradient

dlf_get_gradient = make_dlf_get_gradient(functools.partial(e_g_func, calculator=calculator))
```

##### dlf_get_hessian

The `dlf_get_hessian` function takes one argument, `coordinates` as a NumPy array of shape (n_atoms, 3) and should return the Hessian as a NumPy array with shape (n_atoms * 3, n_atoms * 3). Here is an example of how it can be created:

```python	
def hess_func(coordinates: np.ndarray, calculator):
    calculator.coordinates = coordinates * BOHR_TO_ANGSTROM
    hessian = calculator.hessian()
    return hessian

dlf_get_hessian = make_dlf_get_hessian(functools.partial(hess_func, calculator=calculator))
```

##### dlf_put_coords



###### dlf_update



### Keywords

DL-FIND is a powerful optimization package with many options. They are partially described in the DL-FIND [documentation](docs/documentation.pdf)
and more in detail in [api.f90](src/api.f90) and [dlf global module.f90](src/dlf global module.f90).

The most important parameters for regular optimizations are:

- `printl`: Print level

- `icoord`: Type of coordinate system

- `iopt`: Type of optimisation algorithm

- `iline`: Type of line search or trust radius

For optimizations using Hessian information:

- `inithessian`: Type of initial Hessian

- `update`: Hessian update mechanism

For conical intersection optimizations:

- `imultistate`: Multistate calculations

- `imicroiter`: Microiterative optimization
- `spec`: Fragment and frozen atom information

## Background

libdlfind adds a C compatible API to the original DL-FIND Fortran code. It uses the original code from DL-FIND (downloaded November 2021) in unmodified form and adds three files. 

- api.f90: 
- mod_api.f90: Abstract interfaces callback functions from C 
- mod_globals.f90: Module that stores pointers to callback functions.

Currently, the MPI parallelization of DL-FIND is not supported.

The original code can be obtained at the [ChemShell website](https://www.chemshell.org/dl-find). 

## Acknowledgements

- Cyrille Lavigne (@clavigne) for many helpful discussions and suggestions.