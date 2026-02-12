#!/bin/bash
#SBATCH -J ase_ex3_group_z
#SBATCH -o ase_ex3_group_z_%j.out
#SBATCH -e ase_ex3_group_z_%j.err
#SBATCH --partition=workshopp
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --ntasks-per-node=1
#SBATCH --exclusive

# Load Environment (now includes OMPI flags)
source /nlsasfs/home/gpucbh/gpucbh-pr/DFT-FE-Workshop/sacrosanct/dftfe_socket_interface/ase-dftfe-socket/setup_remote.sh

# Run Python Script
# Ensure the python script commands use 'mpirun -n 2' or match ntasks
echo "Starting O2 relaxation MACE-ASE calculator on $(hostname)"
python3 /nlsasfs/home/gpucbh/vyakti50/dftfe_ase/ex3.py
echo "Run completed"
