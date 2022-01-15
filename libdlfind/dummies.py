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

"""Dummy callback functions."""

from libdlfind.function_types import (
    type_dlf_error,
    type_dlf_get_gradient,
    type_dlf_get_hessian,
    type_dlf_get_multistate_gradients,
    type_dlf_get_params,
    type_dlf_put_coords,
    type_dlf_update,
)


@type_dlf_error
def dummy_dlf_error(*args) -> None:
    """Dummy function for dlf_error."""
    return


@type_dlf_get_gradient
def dummy_dlf_get_gradient(*args) -> None:
    """Dummy function for dlf_get_gradient."""
    return


@type_dlf_get_hessian
def dummy_dlf_get_hessian(*args) -> None:
    """Dummy function for dlf_get_hessian."""
    return


@type_dlf_get_multistate_gradients
def dummy_dlf_get_multistate_gradients(*args) -> None:
    """Dummy function for dlf_get_multistate_gradients."""
    return


@type_dlf_get_params
def dummy_dlf_get_params(*args) -> None:
    """Dummy function for dlf_get_params."""
    return


@type_dlf_put_coords
def dummy_dlf_put_coords(*args) -> None:
    """Dummy function for dlf_put_coords."""
    return


@type_dlf_update
def dummy_dlf_update(*args) -> None:
    """Dummy function for dlf_update."""
    return
