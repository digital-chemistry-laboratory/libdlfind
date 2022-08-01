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

subroutine api_dl_find(nvarin, nvarin2, nspec, master, dlf_error_c, dlf_get_gradient_c, dlf_get_hessian_c, &
                       dlf_get_multistate_gradients_c, dlf_get_params_c, dlf_put_coords_c, dlf_update_c) bind(c)
  use mod_globals
  use mod_api
  use iso_c_binding, only: c_int, c_double, c_funptr, c_f_procpointer

  implicit none
  integer(c_int), intent(in), value :: nvarin ! number of variables to read in 3*nat
  integer(c_int), intent(in), value :: nvarin2 ! number of variables to read in in the second array (coords2)
  integer(c_int), intent(in), value :: nspec ! number of values in the integer array spec
  integer(c_int), intent(in), value :: master ! 1 if this task is the master of a parallel run, 0 otherwise
  type(c_funptr), intent(in), value :: dlf_error_c, dlf_get_gradient_c, dlf_get_hessian_c, dlf_get_multistate_gradients_c, &
                                       dlf_get_params_c, dlf_put_coords_c, dlf_update_c ! Functions received from C side

  ! Assign procedure pointers
  call c_f_procpointer(dlf_error_c, dlf_error_callback)
  call c_f_procpointer(dlf_get_gradient_c, dlf_get_gradient_callback)
  call c_f_procpointer(dlf_get_hessian_c, dlf_get_hessian_callback)
  call c_f_procpointer(dlf_get_multistate_gradients_c, dlf_get_multistate_gradients_callback)
  call c_f_procpointer(dlf_get_params_c, dlf_get_params_callback)
  call c_f_procpointer(dlf_put_coords_c, dlf_put_coords_callback)
  call c_f_procpointer(dlf_update_c, dlf_update_callback)

  ! Call main DL-FIND subroutine
  call dl_find(nvarin, nvarin2, nspec, master)
end subroutine

subroutine dlf_error()
  use mod_globals, only: dlf_error_callback

  implicit none

  call dlf_error_callback()
  error stop "DL-FIND crashed after calling dlf_error."
end subroutine

subroutine dlf_get_gradient(nvar, coords, energy, gradient, iimage, kiter, status)
  use mod_globals, only: dlf_get_gradient_callback
  use dlf_parameter_module, only: rk

  implicit none
  integer, intent(in) :: nvar ! number of xyz variables (3*nat)
  real(rk), intent(in) :: coords(nvar) ! coordinates
  real(rk), intent(out) :: energy ! energy
  real(rk), intent(out) :: gradient(nvar) ! gradient
  integer, intent(in) :: iimage ! current image (for NEB)
  integer, intent(in) :: kiter ! flag related to microiterations
  integer, intent(out) :: status ! return code

  call dlf_get_gradient_callback(nvar, coords, energy, gradient, iimage, kiter, status)
end subroutine

subroutine dlf_get_hessian(nvar, coords, hessian, status)
  use mod_globals, only: dlf_get_hessian_callback
  use dlf_parameter_module, only: rk

  implicit none
  integer, intent(in) :: nvar ! number of xyz variables (3*nat)
  real(rk), intent(in) :: coords(nvar) ! coordinates
  real(rk), intent(out) :: hessian(nvar, nvar) ! hessian
  integer, intent(out) :: status ! return code

  call dlf_get_hessian_callback(nvar, coords, hessian, status)
end subroutine

subroutine dlf_get_multistate_gradients(nvar, coords, energy, gradient, coupling, needcoupling, iimage, status)
  use mod_globals, only: dlf_get_multistate_gradients_callback
  use dlf_parameter_module, only: rk

  implicit none
  integer, intent(in) :: nvar ! number of xyz variables (3*nat)
  real(rk), intent(in) :: coords(nvar) ! coordinates
  real(rk), intent(out) :: energy(2) ! multistate energy
  real(rk), intent(out) :: gradient(3, nvar/3, 2) ! xyz multistate gradients
  real(rk), intent(out) :: coupling(3, nvar/3) ! xyz interstate coupling gradient
  integer, intent(in) :: needcoupling ! true if interstate coupling gradients should be calculated
  integer, intent(in) :: iimage ! current image (for NEB)
  integer, intent(out) :: status ! return code
  call dlf_get_multistate_gradients_callback(nvar, coords, energy, gradient, coupling, needcoupling, iimage, status)
end subroutine

subroutine dlf_get_params( &
  nvar, nvar2, nspec, coords, coords2, spec, ierr, tolerance, printl, maxcycle, maxene, tatoms, icoord, iopt, iline, maxstep, &
  scalestep, lbfgs_mem, nimage, nebk, dump, restart, nz, ncons, nconn, update, maxupd, delta, soft, inithessian, carthessian, &
  tsrel, maxrot, tolrot, nframe, nmass, nweight, timestep, fric0, fricfac, fricp, imultistate, state_i, state_j, pf_c1, pf_c2, &
  gp_c3, gp_c4, ln_t1, ln_t2, printf, tolerance_e, distort, massweight, minstep, maxdump, task, temperature, po_pop_size, &
  po_radius, po_contraction, po_tolerance_r, po_tolerance_g, po_distribution, po_maxcycle, po_init_pop_size, po_reset, &
  po_mutation_rate, po_death_rate, po_scalefac, po_nsave, ntasks, tdlf_farm, n_po_scaling, neb_climb_test, neb_freeze_test, &
  nzero, coupled_states, qtsflag, imicroiter, maxmicrocycle, micro_esp_fit &
  )
  use dlf_parameter_module, only: rk
  use mod_globals, only: dlf_get_params_callback

  implicit none
  integer, intent(in) :: nvar ! number of xyz variables (3*nat)
  integer, intent(in) :: nvar2 ! number of variables to read in the second array (coords2)
  integer, intent(in) :: nspec ! number of values in the integer array spec
  real(rk), intent(inout) :: coords(nvar) ! start coordinates
  real(rk), intent(inout) :: coords2(nvar2) ! a real array that can be used depending on the calculation e.g. a second set of coordinates
  integer, intent(inout) :: spec(nspec) ! (nat) fragment number, or -1: frozen, -2: x frozen, see dlf_coords.f90
  integer, intent(out) :: ierr ! error code
  real(rk), intent(inout) :: tolerance ! main convergence criterion (Max grad comp.)
  integer, intent(inout) :: printl ! how verbosely to write info to stdout
  integer, intent(inout) :: maxcycle ! maximum number of cycles
  integer, intent(inout) :: maxene ! maximum number of E&G evaluations
  integer, intent(inout) :: tatoms ! atoms or arbitrary DOF
  integer, intent(inout) :: icoord ! type of internal coordinates
  integer, intent(inout) :: iopt ! type of optimisation algorithm
  integer, intent(inout) :: iline ! type of line search or trust radius
  real(rk), intent(inout) :: maxstep ! maximum length of the step in internals
  real(rk), intent(inout) :: scalestep ! constant factor with which to scale the step
  integer, intent(inout) :: lbfgs_mem ! number of steps in LBFGS memory
  integer, intent(inout) :: nimage ! Number of images (e.g. in NEB)
  real(rk), intent(inout) :: nebk ! force constant for NEB
  integer, intent(inout) :: dump ! after how many E&G calculations to dump a checkpoint file?
  integer, intent(inout) :: restart ! restart mode: 0 new, 1 read dump file ...
  integer, intent(inout) :: nz ! entries of nuclear charges (same order as coords)
  integer, intent(inout) :: ncons ! number of constraints
  integer, intent(inout) :: nconn ! number of user provided connections
  integer, intent(inout) :: update ! Hessian update scheme
  integer, intent(inout) :: maxupd ! Maximum number of Hessian updates
  real(rk), intent(inout) :: delta ! Delta-x in finite-difference Hessian
  real(rk), intent(inout) :: soft ! Abs(eigval(hess)) < soft -> ignored in P-RFO
  integer, intent(inout) :: inithessian ! Option for method of calculating the initial Hessian
  integer, intent(inout) :: carthessian ! Hessian update in cartesians?
  integer, intent(inout) :: tsrel ! Transition vector I/O absolute or relative?
  integer, intent(inout) :: maxrot ! maximum number of rotations in each DIMER step
  real(rk), intent(inout) :: tolrot ! angle tolerance for rotation (deg) in DIMER
  integer, intent(inout) :: nframe ! number of structures
  integer, intent(inout) :: nmass ! entries of atomic masses (nat or 0)
  integer, intent(inout) :: nweight ! entries of weights (nat or 0)
  real(rk), intent(inout) :: timestep ! time step
  real(rk), intent(inout) :: fric0 ! start friction
  real(rk), intent(inout) :: fricfac ! factor to reduce friction (<1) whenever the energy is decreasing
  real(rk), intent(inout) :: fricp ! friction to use whenever energy increasing
  integer, intent(inout) :: imultistate ! type of multistate calculation (0 = none)
  integer, intent(inout) :: state_i ! lower state
  integer, intent(inout) :: state_j ! upper state
  real(rk), intent(inout) :: pf_c1 ! penalty function parameter (aka alpha)
  real(rk), intent(inout) :: pf_c2 ! penalty function parameter (aka beta)
  real(rk), intent(inout) :: gp_c3 ! gradient projection parameter (aka alpha0)
  real(rk), intent(inout) :: gp_c4 ! gradient projection parameter (aka alpha1)
  real(rk), intent(inout) :: ln_t1 ! Lagrange-Newton orthogonalisation on threshold
  real(rk), intent(inout) :: ln_t2 ! Lagrange-Newton orthogonalisation off threshold
  integer, intent(inout) :: printf ! how verbosely files should be written
  real(rk), intent(inout) :: tolerance_e ! convergence criterion on energy change
  real(rk), intent(inout) :: distort ! shift start structure along coords2 (+ or -)
  integer, intent(inout) :: massweight ! use mass-weighted coordinates
  real(rk), intent(inout) :: minstep ! Hessian is not updated if step < minstep
  integer, intent(inout) :: maxdump ! do only dump restart file after the at most maxdump E&G evaluations
  integer, intent(inout) :: task ! number of taks for the task manager
  real(rk), intent(inout) :: temperature ! temperature for thermal analysis
  integer, intent(inout) :: po_pop_size ! sample population size
  real(rk), intent(inout) :: po_radius  ! per-atom search radii (the prevailing units)
  real(rk), intent(inout) :: po_contraction ! factor by which the search radius decreases between search cycles. Cycle = 1 energy eval for each member of the sample population.
  real(rk), intent(inout) :: po_tolerance_r ! tolerances on po_radius: stop if any component of po_radius shrinks to less than the corresponding component of po_tolerance_r
  real(rk), intent(inout) :: po_tolerance_g ! convergence criterion: max abs component of g
  integer, intent(inout) :: po_distribution ! type of distribn of sample points in space
  integer, intent(inout) :: po_maxcycle ! maximum number of cycles
  integer, intent(inout) :: po_init_pop_size ! size of initial population
  integer, intent(inout) :: po_reset ! number of cycles before population resetting
  real(rk), intent(inout) :: po_mutation_rate ! Fraction of the total number of coordinates in the population to be mutated (randomly shifted) per cycle
  real(rk), intent(inout) :: po_death_rate ! Fraction of the population to be replaced by offspring per cycle
  real(rk), intent(inout) :: po_scalefac ! Multiplying factor for the absolute gradient vector in the force_bias stoch. search scheme
  integer, intent(inout) :: po_nsave ! number of low-energy minima to store
  integer, intent(inout) :: ntasks ! number of taskfarms (workgroups)
  integer, intent(inout) :: tdlf_farm ! Some flag for the task farm
  integer, intent(inout) :: n_po_scaling ! entries of radii scaling factors in the parallel optimization (0 [meaning all radii set to the base value], or a pre-known nivar) i.e. nvarin2= nframe*nat*3 + nweight + nmass + n_po_scaling
  real(rk), intent(inout) :: neb_climb_test ! threshold scale factor for spawning climbing image
  real(rk), intent(inout) :: neb_freeze_test ! threshold scale factor for freezing NEB images
  integer, intent(inout) :: nzero ! number of zero vibrational modes in system
  integer, intent(inout) :: coupled_states   ! Do we need to calculate the interstate coupling gradient? If coupled_states is false, coupling = zero.
  integer, intent(inout) :: qtsflag ! additional info, like if tunnelig splittings are to be calculated (see dlf_qts.f90)
  integer, intent(inout) :: imicroiter ! flag for microiterative calculations =0 : standard, non-microiterative calculation >0 : microiterative calculation [=1 : inside macroiterative loop [=2 : inside microiterative loop]
  integer, intent(inout) :: maxmicrocycle ! max number of microiterative cycles before switching back to macro
  integer, intent(inout) :: micro_esp_fit ! fit ESP charges to inner region during microiterations

  call dlf_get_params_callback( &
    nvar, nvar2, nspec, coords, coords2, spec, ierr, tolerance, printl, maxcycle, maxene, tatoms, icoord, iopt, iline, maxstep, &
    scalestep, lbfgs_mem, nimage, nebk, dump, restart, nz, ncons, nconn, update, maxupd, delta, soft, inithessian, carthessian, &
    tsrel, maxrot, tolrot, nframe, nmass, nweight, timestep, fric0, fricfac, fricp, imultistate, state_i, state_j, pf_c1, pf_c2, &
    gp_c3, gp_c4, ln_t1, ln_t2, printf, tolerance_e, distort, massweight, minstep, maxdump, task, temperature, po_pop_size, &
    po_radius, po_contraction, po_tolerance_r, po_tolerance_g, po_distribution, po_maxcycle, po_init_pop_size, po_reset, &
    po_mutation_rate, po_death_rate, po_scalefac, po_nsave, ntasks, tdlf_farm, n_po_scaling, neb_climb_test, neb_freeze_test, &
    nzero, coupled_states, qtsflag, imicroiter, maxmicrocycle, micro_esp_fit &
    )
end subroutine

subroutine dlf_put_coords(nvar, switch, energy, coords, iam)
  use mod_globals, only: dlf_put_coords_callback
  use dlf_parameter_module, only: rk

  implicit none
  integer, intent(in) :: nvar ! number of xyz variables (3*nat)
  integer, intent(in) :: switch ! 1: coords contains actual geometry, 2: coords contains transition mode
  real(rk), intent(in) :: energy ! energy
  real(rk), intent(in) :: coords(nvar) ! coordinates
  integer, intent(in) :: iam ! flag for MPI runs

  call dlf_put_coords_callback(nvar, switch, energy, coords, iam)
end subroutine

subroutine dlf_update()
  use mod_globals, only: dlf_update_callback

  implicit none

  call dlf_update_callback()
end subroutine
