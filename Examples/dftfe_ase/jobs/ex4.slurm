#!/bin/bash
#SBATCH -J ase_ex4_group_x
#SBATCH -o ase_ex4_group_x_%j.out
#SBATCH -e ase_ex4_group_x_%j.err
#SBATCH --partition=workshopp
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --ntasks-per-node=1
#SBATCH --exclusive

# Load Environment (now includes OMPI flags)
source /nlsasfs/home/gpucbh/gpucbh-pr/DFT-FE-Workshop/sacrosanct/dftfe_socket_interface/ase-dftfe-socket/setup_remote.sh

echo "Starting O2 MD with DFT-FE-ASE calculator on $(hostname)"
python3 /nlsasfs/home/gpucbh/vyakti50/dftfe_ase/ex4.py
echo "Run completed"
