!  Copyright 2021 Kjell Jorner
!
!  This file is part of libdlfind.
!
!  libdlfind is free software: you can redistribute it and/or modify
!  it under the terms of the GNU Lesser General Public License as
!  published by the Free Software Foundation, either version 3 of the
!  License, or (at your option) any later version.
!
!  libdlfind is distributed in the hope that it will be useful,
!  but WITHOUT ANY WARRANTY; without even the implied warranty of
!  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
!  GNU Lesser General Public License for more details.
!
!  You should have received a copy of the GNU Lesser General Public
!  License along with libdlfind.  If not, see
!  <http://www.gnu.org/licenses/>.

module mod_api
  use, intrinsic :: iso_c_binding, only: c_double, c_int

  implicit none

  abstract interface
    subroutine dlf_error_interface() bind(c)
    end subroutine
  end interface

  abstract interface
    subroutine dlf_get_gradient_interface(nvar, coords, energy, gradient, iimage, kiter, status) bind(c)
      import c_double, c_int

      implicit none
      integer(c_int), intent(in), value :: nvar
      real(c_double), intent(in) :: coords(nvar)
      real(c_double), intent(out) :: energy
      real(c_double), intent(out) :: gradient(nvar)
      integer(c_int), intent(in), value :: iimage
      integer(c_int), intent(in), value :: kiter
      integer(c_int), intent(out) :: status
    end subroutine
  end interface

  abstract interface
    subroutine dlf_get_hessian_interface(nvar, coords, hessian, status) bind(c)
      import c_double, c_int

      implicit none
      integer(c_int), intent(in) :: nvar
      real(c_double), intent(in) :: coords(nvar)
      real(c_double), intent(out) :: hessian(nvar, nvar)
      integer, intent(out) :: status
    end subroutine
  end interface

  abstract interface
    subroutine dlf_get_multistate_gradients_interface(nvar, coords, energy, gradient, coupling, needcoupling, iimage, status) &
        bind(c)
      import c_double, c_int

      implicit none
      integer(c_int), intent(in), value :: nvar
      real(c_double), intent(in) :: coords(nvar)
      real(c_double), intent(out) :: energy(2)
      real(c_double), intent(out) :: gradient(nvar, 2)
      real(c_double), intent(out) :: coupling(nvar)
      integer(c_int), intent(in), value :: needcoupling
      integer(c_int), intent(in), value :: iimage
      integer(c_int), intent(out) :: status
    end subroutine
  end interface

  abstract interface
    subroutine dlf_get_params_interface( &
      nvar, nvar2, nspec, coords, coords2, spec, ierr, tolerance, printl, maxcycle, maxene, tatoms, icoord, iopt, iline, &
      maxstep, scalestep, lbfgs_mem, nimage, nebk, dump, restart, nz, ncons, nconn, update, maxupd, delta, soft, inithessian, &
      carthessian, tsrel, maxrot, tolrot, nframe, nmass, nweight, timestep, fric0, fricfac, fricp, imultistate, state_i, &
      state_j, pf_c1, pf_c2, gp_c3, gp_c4, ln_t1, ln_t2, printf, tolerance_e, distort, massweight, minstep, maxdump, task, &
      temperature, po_pop_size, po_radius, po_contraction, po_tolerance_r, po_tolerance_g, po_distribution, po_maxcycle, &
      po_init_pop_size, po_reset, po_mutation_rate, po_death_rate, po_scalefac, po_nsave, ntasks, tdlf_farm, n_po_scaling, &
      neb_climb_test, neb_freeze_test, nzero, coupled_states, qtsflag, imicroiter, maxmicrocycle, micro_esp_fit) bind(c)
      import c_double, c_int

      implicit none
      integer(c_int), intent(in), value :: nvar
      integer(c_int), intent(in), value :: nvar2
      integer(c_int), intent(in), value :: nspec
      real(c_double), intent(inout) :: coords(nvar)
      real(c_double), intent(inout) :: coords2(nvar2)
      integer(c_int), intent(inout) :: spec(nspec)
      integer(c_int), intent(out) :: ierr
      real(c_double), intent(inout) :: tolerance
      integer(c_int), intent(inout) :: printl
      integer(c_int), intent(inout) :: maxcycle
      integer(c_int), intent(inout) :: maxene
      integer(c_int), intent(inout) :: tatoms
      integer(c_int), intent(inout) :: icoord
      integer(c_int), intent(inout) :: iopt
      integer(c_int), intent(inout) :: iline
      real(c_double), intent(inout) :: maxstep
      real(c_double), intent(inout) :: scalestep
      integer(c_int), intent(inout) :: lbfgs_mem
      integer(c_int), intent(inout) :: nimage
      real(c_double), intent(inout) :: nebk
      integer(c_int), intent(inout) :: dump
      integer(c_int), intent(inout) :: restart
      integer(c_int), intent(inout) :: nz
      integer(c_int), intent(inout) :: ncons
      integer(c_int), intent(inout) :: nconn
      integer(c_int), intent(inout) :: update
      integer(c_int), intent(inout) :: maxupd
      real(c_double), intent(inout) :: delta
      real(c_double), intent(inout) :: soft
      integer(c_int), intent(inout) :: inithessian
      integer(c_int), intent(inout) :: carthessian
      integer(c_int), intent(inout) :: tsrel
      integer(c_int), intent(inout) :: maxrot
      real(c_double), intent(inout) :: tolrot
      integer(c_int), intent(inout) :: nframe
      integer(c_int), intent(inout) :: nmass
      integer(c_int), intent(inout) :: nweight
      real(c_double), intent(inout) :: timestep
      real(c_double), intent(inout) :: fric0
      real(c_double), intent(inout) :: fricfac
      real(c_double), intent(inout) :: fricp
      integer(c_int), intent(inout) :: imultistate
      integer(c_int), intent(inout) :: state_i
      integer(c_int), intent(inout) :: state_j
      real(c_double), intent(inout) :: pf_c1
      real(c_double), intent(inout) :: pf_c2
      real(c_double), intent(inout) :: gp_c3
      real(c_double), intent(inout) :: gp_c4
      real(c_double), intent(inout) :: ln_t1
      real(c_double), intent(inout) :: ln_t2
      integer(c_int), intent(inout) :: printf
      real(c_double), intent(inout) :: tolerance_e
      real(c_double), intent(inout) :: distort
      integer(c_int), intent(inout) :: massweight
      real(c_double), intent(inout) :: minstep
      integer(c_int), intent(inout) :: maxdump
      integer(c_int), intent(inout) :: task
      real(c_double), intent(inout) :: temperature
      integer(c_int), intent(inout) :: po_pop_size
      real(c_double), intent(inout) :: po_radius
      real(c_double), intent(inout) :: po_contraction
      real(c_double), intent(inout) :: po_tolerance_r
      real(c_double), intent(inout) :: po_tolerance_g
      integer(c_int), intent(inout) :: po_distribution
      integer(c_int), intent(inout) :: po_maxcycle
      integer(c_int), intent(inout) :: po_init_pop_size
      integer(c_int), intent(inout) :: po_reset
      real(c_double), intent(inout) :: po_mutation_rate
      real(c_double), intent(inout) :: po_death_rate
      real(c_double), intent(inout) :: po_scalefac
      integer(c_int), intent(inout) :: po_nsave
      integer(c_int), intent(inout) :: ntasks
      integer(c_int), intent(inout) :: tdlf_farm
      integer(c_int), intent(inout) :: n_po_scaling
      real(c_double), intent(inout) :: neb_climb_test
      real(c_double), intent(inout) :: neb_freeze_test
      integer(c_int), intent(inout) :: nzero
      integer(c_int), intent(inout) :: coupled_states
      integer(c_int), intent(inout) :: qtsflag
      integer(c_int), intent(inout) :: imicroiter
      integer(c_int), intent(inout) :: maxmicrocycle
      integer(c_int), intent(inout) :: micro_esp_fit
    end subroutine
  end interface

  abstract interface
    subroutine dlf_put_coords_interface(nvar, switch, energy, coords, iam) bind(c)
      import c_double, c_int

      implicit none
      integer(c_int), intent(in), value :: nvar
      integer(c_int), intent(in), value :: switch
      real(c_double), intent(in), value :: energy
      real(c_double), intent(in) :: coords(nvar)
      integer(c_int), intent(in), value :: iam
    end subroutine
  end interface

  abstract interface
    subroutine dlf_update_interface() bind(c)
    end subroutine
  end interface

end module
