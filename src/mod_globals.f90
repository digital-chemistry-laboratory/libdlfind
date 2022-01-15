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
  procedure(c_dlf_error), pointer :: dlf_error_ => null()
  procedure(c_dlf_get_gradient), pointer :: dlf_get_gradient_ => null()
  procedure(c_dlf_get_hessian), pointer :: dlf_get_hessian_ => null()
  procedure(c_dlf_get_multistate_gradients), pointer :: dlf_get_multistate_gradients_ => null()
  procedure(c_dlf_get_params), pointer :: dlf_get_params_ => null()
  procedure(c_dlf_put_coords), pointer :: dlf_put_coords_ => null()
  procedure(c_dlf_update), pointer :: dlf_update_ => null()

end module
