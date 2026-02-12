from ase import Atoms
from ase.units import Bohr
import numpy as np
from ase.optimize import FIRE, LBFGS
from ase.io import read
import os

# MACE Calculator
from mace.calculators import MACECalculator

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
model_path = "/nlsasfs/home/gpucbh/gpucbh-pr/DFT-FE-Workshop/sacrosanct/2023-12-03-mace-128-L1_epoch-199.model"
device = "cuda"

print(f"Loading MACE model from: {model_path}")
print(f"Device: {device}")

atoms.calc = MACECalculator(
    model_path=model_path,
    device=device,
    default_dtype="float64"
)

print("Stage 1: FIRE relaxation starting...")

opt1 = FIRE(
    atoms,
    trajectory="ex3_stage1.traj",
    logfile="ex3_group_z.log"
)

opt1.run(fmax=0.05)

# Write relaxed structure in XYZ
atoms.write("ex3_group_z.xyz")

print("Stage 1 complete. Structure written to ex3_group_z.xyz")

# # ------------------------------------------------------------------
# # Stage 2: Read structure and continue relaxation with LBFGS
# # ------------------------------------------------------------------
from ase import Atoms
from ase.units import Bohr
import numpy as np
from ase.optimize import FIRE, LBFGS
from ase.io import read
import os

# # MACE Calculator
# from mace.calculators import MACECalculator
# # --- Calculator Setup ---
# model_path = "/nlsasfs/home/gpucbh/gpucbh-pr/DFT-FE-Workshop/sacrosanct/2023-12-03-mace-128-L1_epoch-199.model"
# device = "cuda"

# print(f"Loading MACE model from: {model_path}")
# print(f"Device: {device}")

# print("Stage 2: Reading relaxed structure and continuing with LBFGS...")

# atoms2 = read("ex3_stage1_relaxed.xyz")

# atoms2.calc = MACECalculator(
#     model_path=model_path,
#     device=device,
#     default_dtype="float64"
# )

# opt2 = LBFGS(
#     atoms2,
#     trajectory="ex3_stage2.traj",
#     logfile="ex3_stage2_relax.log"
# )

# opt2.run(fmax=0.01)

# atoms2.write("ex3_final_relaxed.cif")

# energy = atoms2.get_potential_energy()

# print("Two-stage relaxation finished.")
# print("Final energy (eV):", energy)
