#!/bin/bash
#SBATCH --error=job.%J.err 
#SBATCH --output=job.%J.out

. "/home/vladimir/miniconda3/etc/profile.d/conda.sh"
conda activate yolo

# And finally run the job​
srun python train.py --img 640 --batch 16 --epochs 300 --data medicover.yaml --cfg yolov5s.yaml
