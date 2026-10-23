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


@dlf_get_gradient_wrapper
def lj_cluster(
    coordinates: NDArray[np.float_], iimage: int, kiter: int, energies: list[float]
) -> tuple[float, NDArray[np.float_]]:
    """Lennard-Jones energy and gradient (epsilon = sigma = 1)."""
    d = coordinates[:, None, :] - coordinates[None, :, :]
    r2 = (d**2).sum(-1) + np.eye(len(coordinates))
    inv6 = r2**-3
    energy = 2.0 * (inv6**2 - inv6)[np.triu_indices(len(coordinates), 1)].sum()
    forces = (24.0 * (2.0 * inv6**2 - inv6) / r2)[:, :, None] * d
    energies.append(energy)
    return energy, -forces.sum(axis=1)


def run_global_search(iopt: int) -> list[float]:
    """Run DL-FIND's stochastic (51) or genetic (52) search on an LJ7 cluster."""
    start = np.random.default_rng(0).uniform(-1.2, 1.2, size=(7, 3))
    energies: list[float] = []
    dl_find(
        nvarin=start.size,
        dlf_get_gradient=functools.partial(lj_cluster, energies=energies),
        dlf_get_params=make_dlf_get_params(
            coords=start, iopt=iopt, icoord=0, maxcycle=50, po_pop_size=4, po_maxcycle=5
        ),
    )
    return energies


def test_stochastic_search(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Stochastic search runs, and a fixed DLF_PO_SEED makes it reproducible."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DLF_PO_SEED", "1234")
    energies = run_global_search(51)
    assert len(energies) > 0
    assert np.all(np.isfinite(energies))
    assert_allclose(run_global_search(51), energies, rtol=0, atol=0)


def test_genetic_search(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Genetic search runs, and a fixed DLF_PO_SEED makes it reproducible."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("DLF_PO_SEED", "1234")
    energies = run_global_search(52)
    assert len(energies) > 0
    assert np.all(np.isfinite(energies))
    assert_allclose(run_global_search(52), energies, rtol=0, atol=0)
