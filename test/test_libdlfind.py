"""Tests for libdlfind."""
from __future__ import annotations

import functools
from pathlib import Path

import numpy as np
from numpy.testing import assert_allclose
from numpy.typing import ArrayLike, NDArray
import pytest
import rdkit
from rdkit import Chem
from rdkit.Chem import AllChem

from libdlfind import dl_find
from libdlfind.callback import (
    dlf_get_gradient_wrapper,
    dlf_put_coords_wrapper,
    make_dlf_get_params,
)


def add_conformers_to_mol(mol: Chem.Mol, conformer_coordinates: ArrayLike) -> None:
    """Add conformers to RDKit Mol object."""
    conformer_coordinates: NDArray[np.float_] = np.array(conformer_coordinates)
    if len(conformer_coordinates.shape) == 2:
        conformer_coordinates.reshape(-1, conformer_coordinates.shape[0], 3)

    for coordinates in conformer_coordinates:
        conformer = Chem.Conformer()
        for i, coord in enumerate(coordinates):
            point = rdkit.Geometry.Point3D(*coord)
            conformer.SetAtomPosition(i, point)
        mol.AddConformer(conformer, assignId=True)


@dlf_get_gradient_wrapper
def e_g_func(
    coordinates: NDArray[np.float_], iimage: int, kiter: int, mol: Chem.Mol
) -> tuple[float, NDArray[np.float_]]:
    """Energy and gradient function."""
    mol.RemoveAllConformers()
    add_conformers_to_mol(mol, [coordinates])
    properties = AllChem.MMFFGetMoleculeProperties(mol)
    ff = AllChem.MMFFGetMoleculeForceField(mol, properties)
    energy = ff.CalcEnergy()
    gradient = np.ascontiguousarray(ff.CalcGrad()).reshape(-1, 3)
    return energy, gradient


@dlf_put_coords_wrapper
def store_results(
    switch: int,
    energy: float,
    coordinates: NDArray[np.float_],
    iam: int,
    traj_coords: list[NDArray[np.float_]],
    traj_energies: list[float],
) -> None:
    """Store results from optimization."""
    traj_coords.append(np.array(coordinates))
    traj_energies.append(energy)
    return


def test_methane_rdkit() -> None:
    """Test to optimize methane with RDKit and MMFF."""
    # Create Mol object
    smiles = "C"
    mol = Chem.MolFromSmiles(smiles)
    mol = Chem.AddHs(mol)
    AllChem.EmbedMolecule(mol)

    # Create callback functions
    traj_energies: list[NDArray[np.float_]] = []
    traj_coordinates: list[float] = []

    dlf_get_params = make_dlf_get_params(coords=mol.GetConformer().GetPositions())
    dlf_get_gradient = functools.partial(e_g_func, mol=mol)
    dlf_put_coords = functools.partial(
        store_results, traj_coords=traj_coordinates, traj_energies=traj_energies
    )

    # Run DL-FIND
    dl_find(
        nvarin=mol.GetNumAtoms() * 3,
        dlf_get_gradient=dlf_get_gradient,
        dlf_get_params=dlf_get_params,
        dlf_put_coords=dlf_put_coords,
    )

    assert_allclose(traj_energies[-1], 0.02638, atol=1e-5)


# Mueller-Brown (Theor. Chim. Acta 53, 75 (1979)) in x, y, plus a harmonic z so
# that DL-FIND sees one "atom". Energies scaled by 1e-3 to hartree-like values.
MB_A = np.array([-200.0, -100.0, -170.0, 15.0])
MB_a = np.array([-1.0, -1.0, -6.5, 0.7])
MB_b = np.array([0.0, 0.0, 11.0, 0.6])
MB_c = np.array([-10.0, -10.0, -6.5, 0.7])
MB_x0 = np.array([1.0, 0.0, -0.5, -1.0])
MB_y0 = np.array([0.0, 0.5, 1.5, 1.0])


@dlf_get_gradient_wrapper
def mueller_brown(
    coordinates: NDArray[np.float_], iimage: int, kiter: int
) -> tuple[float, NDArray[np.float_]]:
    """Mueller-Brown energy and gradient for a single point (x, y, z)."""
    x, y, z = coordinates[0]
    dx, dy = x - MB_x0, y - MB_y0
    t = MB_A * np.exp(MB_a * dx**2 + MB_b * dx * dy + MB_c * dy**2)
    energy = 1.0e-3 * t.sum() + 0.5 * z**2
    gx = 1.0e-3 * (t * (2 * MB_a * dx + MB_b * dy)).sum()
    gy = 1.0e-3 * (t * (MB_b * dx + 2 * MB_c * dy)).sum()
    return energy, np.array([[gx, gy, z]])


@dlf_put_coords_wrapper
def store_points(
    switch: int,
    energy: float,
    coordinates: NDArray[np.float_],
    iam: int,
    points: dict[int, tuple[float, NDArray[np.float_]]],
) -> None:
    """Keep the last point DL-FIND reports for each put_coords switch."""
    points[switch] = (energy, np.array(coordinates))


def test_prfo_connect_without_second_geometry(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """P-RFO + connect from a single geometry finds the saddle and both minima."""
    monkeypatch.chdir(tmp_path)
    points: dict[int, tuple[float, NDArray[np.float_]]] = {}
    start = np.array([[0.20, 0.30, 0.0]])  # near the saddle at (0.212, 0.293)
    dl_find(
        nvarin=3,
        dlf_get_gradient=mueller_brown,
        dlf_get_params=make_dlf_get_params(
            coords=start,
            iopt=10,
            icoord=0,
            inithessian=2,
            task=1011,
            printf=4,
            maxcycle=100,
        ),
        dlf_put_coords=functools.partial(store_points, points=points),
    )
    # task 1011 reports the saddle point (switch 3) and the two minima it
    # connects (switches 4 and 5), at the textbook Mueller-Brown values
    assert {3, 4, 5} <= set(points)
    energy_ts, xyz_ts = points[3]
    assert_allclose(xyz_ts[0, :2], [0.2125, 0.2930], atol=2e-3)
    assert_allclose(energy_ts, -72.249e-3, atol=1e-5)
    minima = sorted([points[4], points[5]], key=lambda p: p[0])
    assert_allclose(minima[0][1][0, :2], [0.6235, 0.0280], atol=2e-3)
    assert_allclose(minima[0][0], -108.167e-3, atol=1e-5)
    assert_allclose(minima[1][1][0, :2], [-0.0500, 0.4667], atol=2e-3)
    assert_allclose(minima[1][0], -80.768e-3, atol=1e-5)
