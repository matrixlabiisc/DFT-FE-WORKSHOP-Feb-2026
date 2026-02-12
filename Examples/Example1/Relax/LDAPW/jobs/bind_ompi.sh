#!/bin/bash
set -euo pipefail

local_rank=${OMPI_COMM_WORLD_LOCAL_RANK:-0}

gpus=( 0 1 2 3 4 5 6 7 )
nics=(
  mlx5_0:1,mlx5_1:1
  mlx5_0:1,mlx5_1:1
  mlx5_2:1,mlx5_3:1
  mlx5_2:1,mlx5_3:1
  mlx5_6:1,mlx5_7:1
  mlx5_6:1,mlx5_7:1
  mlx5_8:1,mlx5_9:1
  mlx5_8:1,mlx5_9:1
)

if (( local_rank >= 8 )); then
  echo "ERROR: local_rank ${local_rank} exceeds GPU count"
  exit 1
fi

export CUDA_VISIBLE_DEVICES=${gpus[$local_rank]}
export UCX_NET_DEVICES=${nics[$local_rank]}


exec "$@"

