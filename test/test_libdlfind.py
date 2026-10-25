"""Tests for libdlfind."""
from __future__ import annotations

import ctypes
import functools

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
from libdlfind.lib import lib


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


def diagonalise(matrix: NDArray[np.float_], canonical: bool) -> NDArray[np.float_]:
    """Eigenvectors of a symmetric 3x3 matrix, as dlf_cartesian_align gets them.

    Calls DL-FIND's own dlf_matrix_diagonalise and, if `canonical`,
    dlf_align_canon_eigvec on the result, through the package's library.
    """
    n = ctypes.c_int(3)
    a = np.asfortranarray(matrix, dtype=np.float64)
    evals = np.zeros(3)
    evecs = np.zeros((3, 3), order="F")
    ptr = ctypes.POINTER(ctypes.c_double)
    lib.dlf_matrix_diagonalise_(
        ctypes.byref(n),
        a.ctypes.data_as(ptr),
        evals.ctypes.data_as(ptr),
        evecs.ctypes.data_as(ptr),
    )
    if canonical:
        lib.dlf_align_canon_eigvec_(
            ctypes.byref(n), evals.ctypes.data_as(ptr), evecs.ctypes.data_as(ptr)
        )
    return evecs


def hcn_hnc_rsmat() -> NDArray[np.float_]:
    """rsmat = rmat^T rmat as dlf_cartesian_align builds it for HCN and HNC."""
    hcn = np.array(
        [
            [1.161096161538, -0.001204758176, -0.190337130816],
            [0.347870282512, -0.000030399671, 0.504910840255],
            [-0.528511960915, 0.001235157849, 1.254153462882],
        ]
    )
    hnc = np.array(
        [
            [1.131321434060, 0.005761457067, 1.162840010393],
            [-0.559417268123, -0.006048726577, -0.215517847999],
            [0.347641351124, 0.000287269515, 0.523950664661],
        ]
    )
    coords1, coords2 = hcn / 0.529177210903, hnc / 0.529177210903
    coords2 = coords2 + (coords1 - coords2).mean(axis=0)
    rmat = (coords1 - coords1.mean(axis=0)).T @ (coords2 - coords1.mean(axis=0)) / 3
    return rmat.T @ rmat


@pytest.mark.parametrize(
    "matrix",
    [
        # rsmat from a stalled HCN/HNC NEB run; eigenvalues 3.18, 2.9e-14, 2.2e-16
        np.array(
            [
                [1.77713427, -0.00828267, -1.58034390],
                [-0.00828267, 0.00003860, 0.00736549],
                [-1.58034390, 0.00736549, 1.40534504],
            ]
        ),
        hcn_hnc_rsmat(),
    ],
    ids=["stalled-neb", "hcn-hnc"],
)
def test_align_eigenvectors_degenerate(matrix: NDArray[np.float_]) -> None:
    """For a linear molecule the alignment eigenvectors must not depend on noise."""
    rng = np.random.default_rng(0)
    raw0, canon0 = diagonalise(matrix, False), diagonalise(matrix, True)
    raw_change = canon_change = 0.0
    for _ in range(300):
        noise = rng.uniform(-1, 1, (3, 3)) * 10 ** rng.uniform(-15, -13)
        perturbed = matrix + (noise + noise.T) / 2
        raw = diagonalise(perturbed, False)
        canon = diagonalise(perturbed, True)
        raw_change = max(raw_change, np.abs(raw - raw0).max())
        canon_change = max(canon_change, np.abs(canon - canon0).max())
    assert raw_change > 1e-6  # the raw eigenvectors do jump, or this tests nothing
    assert canon_change < 1e-10


def test_align_eigenvectors_nondegenerate() -> None:
    """Well-separated eigenvalues: the eigenvectors are unchanged up to sign."""
    matrix = np.array([[3.0, 0.4, 0.1], [0.4, 2.0, 0.3], [0.1, 0.3, 1.0]])
    canonical, raw = diagonalise(matrix, True), diagonalise(matrix, False)
    assert_allclose(np.abs(canonical), np.abs(raw))
