#  Copyright 2021 Kjell Jorner
#
#  This file is part of libdlfind.
#
#  libdlfind is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as
#  published by the Free Software Foundation, either version 3 of the
#  License, or (at your option) any later version.
#
#  libdlfind is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with libdlfind.  If not, see
#  <http://www.gnu.org/licenses/>.

"""Python library for DL-FIND."""

from __future__ import annotations

from ctypes import c_int
from pathlib import Path
from typing import Callable

from numpy.ctypeslib import load_library

from libdlfind.function_types import (
    type_dlf_error,
    type_dlf_get_gradient,
    type_dlf_get_hessian,
    type_dlf_get_multistate_gradients,
    type_dlf_get_params,
    type_dlf_put_coords,
    type_dlf_update,
)

# Load shared library
path = Path(__file__).parent
lib = load_library("libdlfind", str(path))

# Define function from shared library and create Python wrapper
_dl_find = lib.api_dl_find
_dl_find.argtypes = [
    c_int,  # integer(c_int), intent(in) :: nvarin ! number of variables to read in 3*nat
    c_int,  # integer(c_int), intent(in) :: nvarin2 ! number of variables to read in in the second array (coords2) # noqa: B950
    c_int,  # integer(c_int), intent(in) :: nspec ! number of values in the integer array spec
    c_int,  # integer(c_int), intent(in) :: master ! 1 if this task is the master of a parallel run, 0 otherwise # noqa: B950
    type_dlf_error,  # type(c_funptr), intent(in), value :: c_dlf_error_
    type_dlf_get_gradient,  # type(c_funptr), intent(in), value :: c_dlf_get_gradient_
    type_dlf_get_hessian,  # type(c_funptr), intent(in), value :: c_dlf_get_hessian_
    type_dlf_get_multistate_gradients,  # type(c_funptr), intent(in), value :: c_dlf_get_multistate_gradients_ # noqa: B950
    type_dlf_get_params,  # type(c_funptr), intent(in), value :: c_dlf_get_params_
    type_dlf_put_coords,  # type(c_funptr), intent(in), value :: c_dlf_put_coords_
    type_dlf_update,  # type(c_funptr), intent(in), value :: c_dlf_update_
]


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
    """Run DL-FIND.

    For a description of the arguments, see the documentation in api.f90 and
    the DL-FIND manual. dlf_put_coords is always needed, and either one of
    dlf_get_gradient or dlf_get_multistate_gradients. The others can be
    replaced with dummy functions.

    Args:
        nvarin: Number of variables to read for the coords array (3 * number of
            atoms)
        nvarin2: Number of variables to read for the coords2 array
        nspec: Number of values in the integer array spec
        master: 1 if this task is the master of a parallel run, 0 otherwise
        dlf_error: dlf_error function for DL-FIND to call
        dlf_get_gradient: dlf_get_gradient function for DL-FIND to call
        dlf_get_hessian: dlf_get_hessian function for DL-FIND to call
        dlf_get_multistate_gradients: dlf_get_multistate_gradients function for
            DL-FIND to call
        dlf_get_params: dlf_get_params function for DL-FIND to call
        dlf_put_coords: dlf_put_coords function for DL-FIND to call
        dlf_update: dlf_update function for DL-FIND to call
    """
    n_atoms = int(nvarin / 3)

    # Set sensible default for nspec
    if nspec is None:
        nspec = 2 * n_atoms

    _dl_find(
        c_int(nvarin),
        c_int(nvarin2),
        c_int(nspec),
        c_int(master),
        type_dlf_error(dlf_error),
        type_dlf_get_gradient(dlf_get_gradient),
        type_dlf_get_hessian(dlf_get_hessian),
        type_dlf_get_multistate_gradients(dlf_get_multistate_gradients),
        type_dlf_get_params(dlf_get_params),
        type_dlf_put_coords(dlf_put_coords),
        type_dlf_update(dlf_update),
    )
