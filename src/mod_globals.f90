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

module mod_globals
  use mod_api

  implicit none
  procedure(dlf_error_interface), pointer :: dlf_error_callback => null()
  procedure(dlf_get_gradient_interface), pointer :: dlf_get_gradient_callback => null()
  procedure(dlf_get_hessian_interface), pointer :: dlf_get_hessian_callback => null()
  procedure(dlf_get_multistate_gradients_interface), pointer :: dlf_get_multistate_gradients_callback=> null()
  procedure(dlf_get_params_interface), pointer :: dlf_get_params_callback => null()
  procedure(dlf_put_coords_interface), pointer :: dlf_put_coords_callback => null()
  procedure(dlf_update_interface), pointer :: dlf_update_callback => null()

end module
