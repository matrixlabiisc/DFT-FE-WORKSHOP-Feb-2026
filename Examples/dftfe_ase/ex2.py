from ase import Atoms
from ase.units import Bohr, Hartree
import numpy as np
from ase.calculators.dftfe import DFTFE
from ase.optimize import FIRE, LBFGS
from ase.io import read
import os

# --- System Setup ---
box_dims_bohr = np.array([40.0, 42.0, 38.0])
cell_ang = np.diag(box_dims_bohr) * Bohr

center = box_dims_bohr / 2.0
rel_pos_bohr = np.array([
    [-1.2, 0.0, 0.0],
    [ 1.2, 0.0, 0.0]
])
abs_pos_bohr = center + rel_pos_bohr
pos_ang = abs_pos_bohr * Bohr

atoms = Atoms(
    symbols=['O', 'O'],
    positions=pos_ang,
    cell=cell_ang,
    pbc=[False, False, False]
)

# --- Calculator Setup ---
base_dir = "/nlsasfs/home/gpucbh/gpucbh-pr/DFT-FE-Workshop/sacrosanct/dftfe_socket_interface"
psp_path = os.path.join(base_dir, "ase-dftfe-socket/psp_library")
dftfe_bin = os.path.join(base_dir, "DFTFE/install/real/bin/dftfe")

run_cmd = f"export DFTFE_PSP_PATH={psp_path} && srun -n 1 {dftfe_bin}"

def make_calc():
    return DFTFE(
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
        compute_forces=True,
        use_device=True,
        keep_scratch=True,
        log_file="ex2_group_y.log"
    )

atoms.calc = make_calc()

print("Stage 1: FIRE relaxation starting...")

opt1 = FIRE(
    atoms,
    trajectory="ex2_stage1.traj",
    logfile="ex2_stage1_relax.log"
)

opt1.run(fmax=0.05)

# Write relaxed structure in XYZ (format change demonstration)
atoms.write("ex2_group_y.xyz")

print("Stage 1 complete. Structure written to ex2_group_y.xyz")

# ------------------------------------------------------------------
# Stage 2: Read structure and continue relaxation with LBFGS
# PUT THIS IN A DIFFERENT FILE AND GET THE FINAL RELAXED STRUCTURE
# ------------------------------------------------------------------
# from ase import Atoms
# from ase.units import Bohr, Hartree
# import numpy as np
# from ase.calculators.dftfe import DFTFE
# from ase.optimize import FIRE, LBFGS
# from ase.io import read
# import os

# #--- Calculator Setup ---
# base_dir = "/nlsasfs/home/gpucbh/gpucbh-pr/DFT-FE-Workshop/sacrosanct/dftfe_socket_interface"
# psp_path = os.path.join(base_dir, "ase-dftfe-socket/psp_library")
# dftfe_bin = os.path.join(base_dir, "DFTFE/install/real/bin/dftfe")

# run_cmd = f"export DFTFE_PSP_PATH={psp_path} && srun -n 1 {dftfe_bin}"

# def make_calc():
#     return DFTFE(
#         command=run_cmd,
#         host="127.0.0.1",
#         port=0,
#         mesh_size=1.0,
#         polynomial_order=7,
#         tolerance=5e-5,
#         xc='GGA-PBE',
#         scf_mixing=0.5,
#         spin_polarized=False,
#         cheby_wfc_block_size=5,
#         compute_stress=True,
#         wfc_block_size=5,
#         fermi_temp=500.0,
#         num_kohn_sham=15,
#         atom_ball_radius=6.0,
#         verbosity=1,
#         compute_forces=True,
#         use_device=True,
#         keep_scratch=True,
#         log_file="ex2_stage2_dftfe.log"
#     )


# print("Stage 2: Reading relaxed structure and continuing with LBFGS...")

# atoms2 = read("ex2_stage1_relaxed.xyz")
# atoms2.calc = make_calc()

# opt2 = LBFGS(
#     atoms2,
#     trajectory="ex2_stage2.traj",
#     logfile="ex2_stage2_relax.log"
# )

# opt2.run(fmax=0.01)

# atoms2.write("ex2_final_relaxed.cif")

# energy = atoms2.get_potential_energy()

# print("Two-stage relaxation finished.")
# print("Final energy (Hartree):", energy / Hartree)
