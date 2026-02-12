#!/bin/bash
#SBATCH -J ase_ex1_group_0
#SBATCH -o ase_ex1_group_0_%j.out
#SBATCH -e ase_ex1_group_0_%j.err
#SBATCH --partition=workshopp
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --ntasks=1
#SBATCH --exclusive

# Load Environment (now includes OMPI flags)
source /nlsasfs/home/gpucbh/gpucbh-pr/DFT-FE-Workshop/sacrosanct/dftfe_socket_interface/ase-dftfe-socket/setup_remote.sh

# Run Python Script
echo "Starting O2 Ground State Calculation with DFT-FE-ASE calculator on $(hostname)"
python3 /nlsasfs/home/gpucbh/vyakti50/dftfe_ase/ex1.py
echo "Run completed"
