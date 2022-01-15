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

"""Callback function types."""

from ctypes import c_double, c_int, CFUNCTYPE, POINTER

type_dlf_error = CFUNCTYPE(None)

type_dlf_get_gradient = CFUNCTYPE(
    None,
    c_int,  # integer(c_int), intent(in), value :: nvar
    POINTER(c_double),  # real(c_double), intent(in) :: coords(nvar)
    POINTER(c_double),  # real(c_double), intent(out) :: energy
    POINTER(c_double),  # real(c_double), intent(out) :: gradient(nvar)
    c_int,  # integer(c_int), intent(in), value :: iimage
    c_int,  # integer(c_int), intent(in), value :: kiter
    POINTER(c_int),  # integer(c_int), intent(out) :: status
)

type_dlf_get_hessian = CFUNCTYPE(
    None,
    c_int,  # integer(c_int), intent(in) :: nvar
    POINTER(c_double),  # real(c_double), intent(in) :: coords(nvar)
    POINTER(c_double),  # real(c_double), intent(out) :: hessian(nvar, nvar)
    POINTER(c_int),  # integer, intent(out) :: status
)

type_dlf_get_multistate_gradients = CFUNCTYPE(
    None,
    c_int,  # integer(c_int), intent(in), value :: nvar
    POINTER(c_double),  # real(c_double), intent(in) :: coords(nvar)
    POINTER(c_double),  # real(c_double), intent(out) :: energy(2)
    POINTER(c_double),  # real(c_double), intent(out) :: gradient(nvar, 2)
    POINTER(c_double),  # real(c_double), intent(out) :: coupling(nvar)
    c_int,  # integer(c_int), intent(in), value :: needcoupling
    c_int,  # integer(c_int), intent(in), value :: iimage
    POINTER(c_int),  # integer(c_int), intent(out) :: status
)

type_dlf_get_params = CFUNCTYPE(
    None,
    c_int,  # integer(c_int), intent(in) :: nvar
    c_int,  # integer(c_int), intent(in) :: nvar2
    c_int,  # integer(c_int), intent(in) :: nspec
    POINTER(c_double),  # real(c_double), intent(inout) :: coords(nvar)
    POINTER(c_double),  # real(c_double), intent(inout) :: coords2(nvar2)
    POINTER(c_int),  # integer(c_int), intent(inout) :: spec(nspec)
    POINTER(c_int),  # integer(c_int), intent(out) :: ierr
    POINTER(c_double),  # real(c_double), intent(inout) :: tolerance
    POINTER(c_int),  # integer(c_int), intent(inout) :: printl
    POINTER(c_int),  # integer(c_int), intent(inout) :: maxcycle
    POINTER(c_int),  # integer(c_int), intent(inout) :: maxene
    POINTER(c_int),  # integer(c_int), intent(inout) :: tatoms
    POINTER(c_int),  # integer(c_int), intent(inout) :: icoord
    POINTER(c_int),  # integer(c_int), intent(inout) :: iopt
    POINTER(c_int),  # integer(c_int), intent(inout) :: iline
    POINTER(c_double),  # real(c_double), intent(inout) :: maxstep
    POINTER(c_double),  # real(c_double), intent(inout) :: scalestep
    POINTER(c_int),  # integer(c_int), intent(inout) :: lbfgs_mem
    POINTER(c_int),  # integer(c_int), intent(inout) :: nimage
    POINTER(c_double),  # real(c_double), intent(inout) :: nebk
    POINTER(c_int),  # integer(c_int), intent(inout) :: dump
    POINTER(c_int),  # integer(c_int), intent(inout) :: restart
    POINTER(c_int),  # integer(c_int), intent(inout) :: nz
    POINTER(c_int),  # integer(c_int), intent(inout) :: ncons
    POINTER(c_int),  # integer(c_int), intent(inout) :: nconn
    POINTER(c_int),  # integer(c_int), intent(inout) :: update
    POINTER(c_int),  # integer(c_int), intent(inout) :: maxupd
    POINTER(c_double),  # real(c_double), intent(inout) :: delta
    POINTER(c_double),  # real(c_double), intent(inout) :: soft
    POINTER(c_int),  # integer(c_int), intent(inout) :: inithessian
    POINTER(c_int),  # integer(c_int), intent(inout) :: carthessian
    POINTER(c_int),  # integer(c_int), intent(inout) :: tsrel
    POINTER(c_int),  # integer(c_int), intent(inout) :: maxrot
    POINTER(c_double),  # real(c_double), intent(inout) :: tolrot
    POINTER(c_int),  # integer(c_int), intent(inout) :: nframe
    POINTER(c_int),  # integer(c_int), intent(inout) :: nmass
    POINTER(c_int),  # integer(c_int), intent(inout) :: nweight
    POINTER(c_double),  # real(c_double), intent(inout) :: timestep
    POINTER(c_double),  # real(c_double), intent(inout) :: fric0
    POINTER(c_double),  # real(c_double), intent(inout) :: fricfac
    POINTER(c_double),  # real(c_double), intent(inout) :: fricp
    POINTER(c_int),  # integer(c_int), intent(inout) :: imultistate
    POINTER(c_int),  # integer(c_int), intent(inout) :: state_i
    POINTER(c_int),  # integer(c_int), intent(inout) :: state_j
    POINTER(c_double),  # real(c_double), intent(inout) :: pf_c1
    POINTER(c_double),  # real(c_double), intent(inout) :: pf_c2
    POINTER(c_double),  # real(c_double), intent(inout) :: gp_c3
    POINTER(c_double),  # real(c_double), intent(inout) :: gp_c4
    POINTER(c_double),  # real(c_double), intent(inout) :: ln_t1
    POINTER(c_double),  # real(c_double), intent(inout) :: ln_t2
    POINTER(c_int),  # integer(c_int), intent(inout) :: printf
    POINTER(c_double),  # real(c_double), intent(inout) :: tolerance_e
    POINTER(c_double),  # real(c_double), intent(inout) :: distort
    POINTER(c_int),  # integer(c_int), intent(inout) :: massweight
    POINTER(c_double),  # real(c_double), intent(inout) :: minstep
    POINTER(c_int),  # integer(c_int), intent(inout) :: maxdump
    POINTER(c_int),  # integer(c_int), intent(inout) :: task
    POINTER(c_double),  # real(c_double), intent(inout) :: temperature
    POINTER(c_int),  # integer(c_int), intent(inout) :: po_pop_size
    POINTER(c_double),  # real(c_double), intent(inout) :: po_radius
    POINTER(c_double),  # real(c_double), intent(inout) :: po_contraction
    POINTER(c_double),  # real(c_double), intent(inout) :: po_tolerance_r
    POINTER(c_double),  # real(c_double), intent(inout) :: po_tolerance_g
    POINTER(c_int),  # integer(c_int), intent(inout) :: po_distribution
    POINTER(c_int),  # integer(c_int), intent(inout) :: po_maxcycle
    POINTER(c_int),  # integer(c_int), intent(inout) :: po_init_pop_size
    POINTER(c_int),  # integer(c_int), intent(inout) :: po_reset
    POINTER(c_double),  # real(c_double), intent(inout) :: po_mutation_rate
    POINTER(c_double),  # real(c_double), intent(inout) :: po_death_rate
    POINTER(c_double),  # real(c_double), intent(inout) :: po_scalefac
    POINTER(c_int),  # integer(c_int), intent(inout) :: po_nsave
    POINTER(c_int),  # integer(c_int), intent(inout) :: ntasks
    POINTER(c_int),  # integer(c_int), intent(inout) :: tdlf_farm
    POINTER(c_int),  # integer(c_int), intent(inout) :: n_po_scaling
    POINTER(c_double),  # real(c_double), intent(inout) :: neb_climb_test
    POINTER(c_double),  # real(c_double), intent(inout) :: neb_freeze_test
    POINTER(c_int),  # integer(c_int), intent(inout) :: nzero
    POINTER(c_int),  # integer(c_int), intent(inout) :: coupled_states
    POINTER(c_int),  # integer(c_int), intent(inout) :: qtsflag
    POINTER(c_int),  # integer(c_int), intent(inout) :: imicroiter
    POINTER(c_int),  # integer(c_int), intent(inout) :: maxmicrocycle
    POINTER(c_int),  # integer(c_int), intent(inout) :: micro_esp_fit
)

type_dlf_put_coords = CFUNCTYPE(
    None,
    c_int,  # integer(c_int), intent(in), value :: nvar
    c_int,  # integer(c_int), intent(in), value :: switch
    c_double,  # real(c_double), intent(in), value :: energy
    POINTER(c_double),  # real(c_double), intent(in) :: coords(nvar)
    c_int,  # integer(c_int), intent(in), value :: iam
)

type_dlf_update = CFUNCTYPE(None)
