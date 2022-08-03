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

"""Factory functions."""

from __future__ import annotations

from ctypes import c_double, c_int, pointer
import functools
from typing import Callable, Optional

import numpy as np
from numpy.ctypeslib import as_array
from numpy.typing import ArrayLike


def dlf_get_gradient_wrapper(func: Callable) -> Callable:
    """Factory function for dlf_get_gradient."""

    @functools.wraps(func)
    def wrapper(
        nvar: int,
        coords: pointer[c_double],
        energy: pointer[c_double],
        gradient: pointer[c_double],
        iimage: int,
        kiter: int,
        status: pointer[c_int],
        *args,
        **kwargs,
    ) -> None:
        coords_ = as_array(coords, (nvar,)).reshape(-1, 3)
        e, g = func(coords_, iimage, kiter, *args, **kwargs)
        energy[0] = c_double(e)
        gradient_ = as_array(gradient, (nvar,))
        gradient_[:] = g.reshape(-1)
        status[0] = c_int(0)
        return

    return wrapper


def dlf_get_hessian_wrapper(func: Callable) -> Callable:
    """Factory function for dlf_get_hessian."""

    @functools.wraps(func)
    def wrapper(
        nvar: int,
        coords: pointer[c_double],
        hessian: pointer[c_double],
        status: pointer[c_int],
    ) -> None:
        coords_ = as_array(coords, shape=(nvar,)).reshape((-1, 3))
        hessian_ = as_array(hessian, shape=(nvar,))
        hessian = func(coords_)
        hessian_[:, :] = hessian
        status[0] = c_int(0)
        return

    return wrapper


def dlf_get_multistate_gradients_wrapper(func: Callable) -> Callable:
    """Factory function for dlf_get_multistate_gradients."""

    @functools.wraps(func)
    def wrapper(
        nvar: int,
        coords: pointer[c_double],
        energy: pointer[c_double],
        gradient: pointer[c_double],
        coupling: pointer[c_double],
        needcoupling: int,
        iimage: int,
        status: pointer[c_int],
    ) -> None:
        coordinates_ = as_array(coords, (nvar,)).reshape(-1, 3)
        e_1, e_2, g_1, g_2, _ = func(coordinates_, needcoupling, iimage)
        energy_ = as_array(energy, (2,))
        energy_[0] = e_1
        energy_[1] = e_2
        gradient_ = as_array(gradient, (2, int(nvar / 3), 3))
        gradient_[0, :, :] = g_1
        gradient_[1, :, :] = g_2
        if needcoupling == 1:
            coupling_ = as_array(coupling, (int(nvar / 3), 3))
            coupling_[:, :] = 0.0
        status[0] = c_int(0)
        return

    return wrapper


def make_dlf_get_params(  # noqa: C901
    *,
    coords: ArrayLike,
    coords2: Optional[ArrayLike] = None,
    spec: Optional[ArrayLike] = None,
    tolerance: Optional[float] = None,
    printl: int = 0,
    maxcycle: Optional[int] = None,
    maxene: Optional[int] = None,
    tatoms: Optional[int] = None,
    icoord: Optional[int] = None,
    iopt: Optional[int] = None,
    iline: Optional[int] = None,
    maxstep: Optional[float] = None,
    scalestep: Optional[float] = None,
    lbfgs_mem: Optional[int] = None,
    nimage: Optional[int] = None,
    nebk: Optional[int] = None,
    dump: Optional[int] = None,
    restart: Optional[int] = None,
    nz: int = 0,
    ncons: int = 0,
    nconn: int = 0,
    update: Optional[int] = None,
    maxupd: Optional[int] = None,
    delta: Optional[float] = None,
    soft: Optional[float] = None,
    inithessian: Optional[int] = None,
    carthessian: Optional[int] = None,
    tsrel: Optional[int] = None,
    maxrot: Optional[int] = None,
    tolrot: Optional[float] = None,
    nframe: int = 0,
    nmass: int = 0,
    nweight: int = 0,
    timestep: Optional[float] = None,
    fric0: Optional[float] = None,
    fricfac: Optional[float] = None,
    fricp: Optional[float] = None,
    imultistate: Optional[int] = None,
    state_i: Optional[int] = None,
    state_j: Optional[int] = None,
    pf_c1: Optional[float] = None,
    pf_c2: Optional[float] = None,
    gp_c3: Optional[float] = None,
    gp_c4: Optional[float] = None,
    ln_t1: Optional[float] = None,
    ln_t2: Optional[float] = None,
    printf: Optional[int] = None,
    tolerance_e: Optional[float] = None,
    distort: Optional[float] = None,
    massweight: Optional[int] = None,
    minstep: Optional[float] = None,
    maxdump: Optional[int] = None,
    task: Optional[int] = None,
    temperature: Optional[float] = None,
    po_pop_size: Optional[int] = None,
    po_radius: Optional[float] = None,
    po_contraction: Optional[float] = None,
    po_tolerance_r: Optional[float] = None,
    po_tolerance_g: Optional[float] = None,
    po_distribution: Optional[int] = None,
    po_maxcycle: Optional[int] = None,
    po_init_pop_size: Optional[int] = None,
    po_reset: Optional[int] = None,
    po_mutation_rate: Optional[float] = None,
    po_death_rate: Optional[float] = None,
    po_scalefac: Optional[float] = None,
    po_nsave: Optional[int] = None,
    ntasks: int = 1,
    tdlf_farm: Optional[int] = None,
    n_po_scaling: Optional[int] = None,
    neb_climb_test: Optional[int] = None,
    neb_freeze_test: Optional[int] = None,
    nzero: Optional[int] = None,
    coupled_states: Optional[int] = None,
    qtsflag: Optional[int] = None,
    imicroiter: Optional[int] = None,
    maxmicrocycle: Optional[int] = None,
    micro_esp_fit: Optional[int] = None,
) -> Callable:
    """Factory function for dlf_get_params."""

    def dlf_get_params(
        nvar_: int,
        nvar2_: int,
        nspec_: int,
        coords_: pointer[c_double],
        coords2_: pointer[c_double],
        spec_: pointer[c_double],
        ierr_: pointer[c_int],
        tolerance_: pointer[c_double],
        printl_: pointer[c_int],
        maxcycle_: pointer[c_int],
        maxene_: pointer[c_int],
        tatoms_: pointer[c_int],
        icoord_: pointer[c_int],
        iopt_: pointer[c_int],
        iline_: pointer[c_int],
        maxstep_: pointer[c_double],
        scalestep_: pointer[c_double],
        lbfgs_mem_: pointer[c_int],
        nimage_: pointer[c_int],
        nebk_: pointer[c_int],
        dump_: pointer[c_int],
        restart_: pointer[c_int],
        nz_: pointer[c_int],
        ncons_: pointer[c_int],
        nconn_: pointer[c_int],
        update_: pointer[c_int],
        maxupd_: pointer[c_int],
        delta_: pointer[c_double],
        soft_: pointer[c_double],
        inithessian_: pointer[c_int],
        carthessian_: pointer[c_int],
        tsrel_: pointer[c_int],
        maxrot_: pointer[c_int],
        tolrot_: pointer[c_double],
        nframe_: pointer[c_int],
        nmass_: pointer[c_int],
        nweight_: pointer[c_int],
        timestep_: pointer[c_double],
        fric0_: pointer[c_double],
        fricfac_: pointer[c_double],
        fricp_: pointer[c_double],
        imultistate_: pointer[c_int],
        state_i_: pointer[c_int],
        state_j_: pointer[c_int],
        pf_c1_: pointer[c_double],
        pf_c2_: pointer[c_double],
        gp_c3_: pointer[c_double],
        gp_c4_: pointer[c_double],
        ln_t1_: pointer[c_double],
        ln_t2_: pointer[c_double],
        printf_: pointer[c_int],
        tolerance_e_: pointer[c_double],
        distort_: pointer[c_double],
        massweight_: pointer[c_int],
        minstep_: pointer[c_double],
        maxdump_: pointer[c_int],
        task_: pointer[c_int],
        temperature_: pointer[c_double],
        po_pop_size_: pointer[c_int],
        po_radius_: pointer[c_double],
        po_contraction_: pointer[c_double],
        po_tolerance_r_: pointer[c_double],
        po_tolerance_g_: pointer[c_double],
        po_distribution_: pointer[c_int],
        po_maxcycle_: pointer[c_int],
        po_init_pop_size_: pointer[c_int],
        po_reset_: pointer[c_int],
        po_mutation_rate_: pointer[c_double],
        po_death_rate_: pointer[c_double],
        po_scalefac_: pointer[c_double],
        po_nsave_: pointer[c_int],
        ntasks_: pointer[c_int],
        tdlf_farm_: pointer[c_int],
        n_po_scaling_: pointer[c_int],
        neb_climb_test_: pointer[c_int],
        neb_freeze_test_: pointer[c_int],
        nzero_: pointer[c_int],
        coupled_states_: pointer[c_int],
        qtsflag_: pointer[c_int],
        imicroiter_: pointer[c_int],
        maxmicrocycle_: pointer[c_int],
        micro_esp_fit_: pointer[c_int],
    ) -> None:
        coords__ = as_array(coords_, (nvar_,))
        coords__[:] = np.ascontiguousarray(coords, dtype=np.float64).reshape(-1)
        if coords2 is not None:
            coords2__ = as_array(coords2_, (nvar2_,))
            coords2__[:] = np.ascontiguousarray(coords2, dtype=np.float64).reshape(-1)
        if spec is not None:
            spec__ = as_array(spec_, (nspec_,))
            spec__[:] = np.ascontiguousarray(spec, dtype=np.float64).reshape(-1)
        if tolerance is not None:
            tolerance_[0] = c_double(tolerance)
        if printl is not None:
            printl_[0] = c_int(printl)
        if maxcycle is not None:
            maxcycle_[0] = c_int(maxcycle)
        if maxene is not None:
            maxene_[0] = c_int(maxene)
        if tatoms is not None:
            tatoms_[0] = c_int(tatoms)
        if icoord is not None:
            icoord_[0] = c_int(icoord)
        if iopt is not None:
            iopt_[0] = c_int(iopt)
        if iline is not None:
            iline_[0] = c_int(iline)
        if maxstep is not None:
            maxstep_[0] = c_double(maxstep)
        if scalestep is not None:
            scalestep_[0] = c_double(scalestep)
        if lbfgs_mem is not None:
            lbfgs_mem_[0] = c_int(lbfgs_mem)
        if nimage is not None:
            nimage_[0] = c_int(nimage)
        if nebk is not None:
            nebk_[0] = c_int(nebk)
        if dump is not None:
            dump_[0] = c_int(dump)
        if restart is not None:
            restart_[0] = c_int(restart)
        if nz is not None:
            nz_[0] = c_int(nz)
        if ncons is not None:
            ncons_[0] = c_int(ncons)
        if nconn is not None:
            nconn_[0] = c_int(nconn)
        if update is not None:
            update_[0] = c_int(update)
        if maxupd is not None:
            maxupd_[0] = c_int(maxupd)
        if delta is not None:
            delta_[0] = c_double(delta)
        if soft is not None:
            soft_[0] = c_double(soft)
        if inithessian is not None:
            inithessian_[0] = c_int(inithessian)
        if carthessian is not None:
            carthessian_[0] = c_int(carthessian)
        if tsrel is not None:
            tsrel_[0] = c_int(tsrel)
        if maxrot is not None:
            maxrot_[0] = c_int(maxrot)
        if tolrot is not None:
            tolrot_[0] = c_double(tolrot)
        if nframe is not None:
            nframe_[0] = c_int(nframe)
        if nmass is not None:
            nmass_[0] = c_int(nmass)
        if nweight is not None:
            nweight_[0] = c_int(nweight)
        if timestep is not None:
            timestep_[0] = c_double(timestep)
        if fric0 is not None:
            fric0_[0] = c_double(fric0)
        if fricfac is not None:
            fricfac_[0] = c_double(fricfac)
        if fricp is not None:
            fricp_[0] = c_double(fricp)
        if imultistate is not None:
            imultistate_[0] = c_int(imultistate)
        if state_i is not None:
            state_i_[0] = c_int(state_i)
        if state_j is not None:
            state_j_[0] = c_int(state_j)
        if pf_c1 is not None:
            pf_c1_[0] = c_double(pf_c1)
        if pf_c2 is not None:
            pf_c2_[0] = c_double(pf_c2)
        if gp_c3 is not None:
            gp_c3_[0] = c_double(gp_c3)
        if gp_c4 is not None:
            gp_c4_[0] = c_double(gp_c4)
        if ln_t1 is not None:
            ln_t1_[0] = c_double(ln_t1)
        if ln_t2 is not None:
            ln_t2_[0] = c_double(ln_t2)
        if printf is not None:
            printf_[0] = c_int(printf)
        if tolerance_e is not None:
            tolerance_e_[0] = c_double(tolerance_e)
        if distort is not None:
            distort_[0] = c_double(distort)
        if massweight is not None:
            massweight_[0] = c_int(massweight)
        if minstep is not None:
            minstep_[0] = c_double(minstep)
        if maxdump is not None:
            maxdump_[0] = c_int(maxdump)
        if task is not None:
            task_[0] = c_int(task)
        if temperature is not None:
            temperature_[0] = c_double(temperature)
        if po_pop_size is not None:
            po_pop_size_[0] = c_int(po_pop_size)
        if po_radius is not None:
            po_radius_[0] = c_double(po_radius)
        if po_contraction is not None:
            po_contraction_[0] = c_double(po_contraction)
        if po_tolerance_r is not None:
            po_tolerance_r_[0] = c_double(po_tolerance_r)
        if po_tolerance_g is not None:
            po_tolerance_g_[0] = c_double(po_tolerance_g)
        if po_distribution is not None:
            po_distribution_[0] = c_int(po_distribution)
        if po_maxcycle is not None:
            po_maxcycle_[0] = c_int(po_maxcycle)
        if po_init_pop_size is not None:
            po_init_pop_size_[0] = c_int(po_init_pop_size)
        if po_reset is not None:
            po_reset_[0] = c_int(po_reset)
        if po_mutation_rate is not None:
            po_mutation_rate_[0] = c_double(po_mutation_rate)
        if po_death_rate is not None:
            po_death_rate_[0] = c_double(po_death_rate)
        if po_scalefac is not None:
            po_scalefac_[0] = c_double(po_scalefac)
        if po_nsave is not None:
            po_nsave_[0] = c_int(po_nsave)
        if ntasks is not None:
            ntasks_[0] = c_int(ntasks)
        if tdlf_farm is not None:
            tdlf_farm_[0] = c_int(tdlf_farm)
        if n_po_scaling is not None:
            n_po_scaling_[0] = c_int(n_po_scaling)
        if neb_climb_test is not None:
            neb_climb_test_[0] = c_int(neb_climb_test)
        if neb_freeze_test is not None:
            neb_freeze_test_[0] = c_int(neb_freeze_test)
        if nzero is not None:
            nzero_[0] = c_int(nzero)
        if coupled_states is not None:
            coupled_states_[0] = c_int(coupled_states)
        if qtsflag is not None:
            qtsflag_[0] = c_int(qtsflag)
        if imicroiter is not None:
            imicroiter_[0] = c_int(imicroiter)
        if maxmicrocycle is not None:
            maxmicrocycle_[0] = c_int(maxmicrocycle)
        if micro_esp_fit is not None:
            micro_esp_fit_[0] = c_int(micro_esp_fit)
        ierr_[0] = c_int(0)

        return

    return dlf_get_params


def dlf_put_coords_wrapper(func: Callable) -> Callable:
    """Factory function for dlf_put_coords."""

    @functools.wraps(func)
    def wrapper(
        nvar: int,
        switch: int,
        energy: float,
        coords: pointer[c_double],
        iam: int,
        *args,
        **kwargs,
    ) -> None:
        coords_ = as_array(coords, (nvar,)).reshape(-1, 3)
        func(switch, energy, coords_, iam, *args, **kwargs)

        return

    return wrapper
