#!/bin/bash
#SBATCH -J Si-PAW
#SBATCH -o dftfe_%j.out
#SBATCH -e dftfe_%j.err
#SBATCH --partition=workshopp
#SBATCH --time=02:00:00
#SBATCH --nodes=4
#SBATCH --gres=gpu:8
#SBATCH --ntasks-per-node=8
#SBATCH --cpus-per-task=16
#SBATCH --nodelist=scn31-10g,scn32-10g,scn33-10g,scn34-10g
#SBATCH --exclusive

export LD_LIBRARY_PATH=/nlsasfs/home/gpucbh/gpucbh-pr/dftfeDependencies/cudaCompat/compat:$LD_LIBRARY_PATH
export HPCX_HOME=/nlsasfs/home/gpucbh/gpucbh-pr/dftfeDependencies/hpcx
. /nlsasfs/home/gpucbh/gpucbh-pr/dftfeDependencies/spack/share/spack/setup-env.sh
spack load cuda gdrcopy cmake ninja nccl binutils numactl 
source $HPCX_HOME/hpcx-mt-init.sh
hpcx_load

export DFTFE_NUM_THREADS=8
export OMP_NUM_THREADS=1
export OMP_PLACES=cores

# MPI / UCX
export OMPI_MCA_pml=ucx
export PMIX_MCA_psec=native
export UCX_TLS=^cuda_ipc
export OMP_PLACES=cores
export OMP_PROC_BIND=spread

# MPI / UCX
export OMPI_MCA_pml=ucx
export OMPI_MCA_btl="^openib"
export OMPI_MCA_btl_vader_single_copy_mechanism=none
export PMIX_MCA_psec=native

export PATH=/nlsasfs/home/gpucbh/gpucbh-pr/dftfeDependencies/dftfe/dftfe_workshopBranch/install/real:$PATH


mpirun -n $SLURM_NTASKS ./bind_ompi.sh dftfe parameterFile-SC.prm > SC-OUT-4
