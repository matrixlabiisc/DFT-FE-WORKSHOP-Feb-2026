from ase import Atoms
from ase.units import Bohr, Hartree
import numpy as np
import os
# Strict requirement from previous steps
from ase.calculators.dftfe import DFTFE

# --- System Setup ---
# 1. Define Cell (Bohr) and convert to Angstrom
box_dims_bohr = np.array([40.0, 42.0, 38.0])
cell_ang = np.diag(box_dims_bohr) * Bohr 

# 2. Define Positions (Bohr) - Centered in the box
center = box_dims_bohr / 2.0
rel_pos_bohr = np.array([
    [-1.2, 0.0, 0.0],
    [ 1.2, 0.0, 0.0]
])
abs_pos_bohr = center + rel_pos_bohr
pos_ang = abs_pos_bohr * Bohr

# Create Atoms object
atoms = Atoms(symbols=['O', 'O'],
              positions=pos_ang,
              cell=cell_ang,
              pbc=[False, False, False])

# --- Calculator Setup ---
# PATHS FIXED FOR WORKSHOP ENVIRONMENT
base_dir = "/nlsasfs/home/gpucbh/gpucbh-pr/DFT-FE-Workshop/sacrosanct/dftfe_socket_interface"
psp_path = os.path.join(base_dir, "ase-dftfe-socket/psp_library")
dftfe_bin = os.path.join(base_dir, "DFTFE/install/real/bin/dftfe")

# Run Command construction
# We assume env.sh is sourced before running python, so just export PSP path and run
# Using N=1 or N=2 for diagnostic if not scheduled
run_cmd = f"export DFTFE_PSP_PATH={psp_path} && srun -n 1 {dftfe_bin}"

print(f"Running O2 Ground State with Socket Interface...")
print(f"Binary: {dftfe_bin}")
print(f"PSP Path: {psp_path}")

calc = DFTFE(
    command=run_cmd,
    host="127.0.0.1",
    port=0,
    mesh_size=1.0,
    polynomial_order=7,
    tolerance=5e-5,
    xc='GGA-PBE',
    scf_mixing=0.5,
    spin_polarized=False,
    cheby_wfc_block_size=5,   
    compute_stress=True,
    wfc_block_size=5,
    fermi_temp=500.0,
    num_kohn_sham=15,
    atom_ball_radius=6.0,
    verbosity=1,
    use_device=True,
    keep_scratch=True,
    log_file=os.path.join(os.path.dirname(os.path.abspath(__file__)), "ex1_group_0.log")
)

atoms.calc = calc

try:
    energy = atoms.get_potential_energy()
    print(f"Total Free Energy: {energy / Hartree} Hartree")
except Exception as e:
    print(f"Calculation Failed: {e}")
