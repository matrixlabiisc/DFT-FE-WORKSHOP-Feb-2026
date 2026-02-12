from ase import Atoms, units
from ase.units import Bohr
import numpy as np
from ase.calculators.dftfe import DFTFESocketCalculator
from ase.md.langevin import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.io import write
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

atoms.calc = DFTFESocketCalculator(
    command=run_cmd,
    host="127.0.0.1",
    port=0,
    mesh_size=1.0,
    polynomial_order=7,
    tolerance=5e-5,
    xc='GGA-PBE',
    scf_mixing=0.5,
    spin_polarized=False,
    compute_forces=True,
    verbosity=1,
    use_device=True,
    keep_scratch=True,
    log_file="ex4_group_x.log"
)

# --- MD Setup ---
temperature = 300
timestep = 1.0 * units.fs
friction = 0.02

MaxwellBoltzmannDistribution(atoms, temperature_K=temperature)

dyn = Langevin(
    atoms,
    timestep,
    temperature_K=temperature,
    friction=friction
)

# --- Trajectory Saving (Only ~3 snapshots) ---
traj_file = "ex4_group_x.xyz"

# Initial frame
write(traj_file, atoms)

def write_frame():
    write(traj_file, atoms, append=True)
    print(f"Step={dyn.nsteps}  PE={atoms.get_potential_energy():.6f} eV")

# Save at steps 5 and 10
dyn.attach(write_frame, interval=5)

# --- Run MD ---
print("Starting MD run with DFT-FE socket calculator...")
dyn.run(steps=10)
print("MD finished.")

atoms.write("ex4_final_group_x.cif")
