#!/bin/bash

#SBATCH -A crispr_carb
#SBATCH -p slurm
#SBATCH -t 4-00:00:00
#SBATCH -N 1
#SBATCH -n 64
#SBATCH -J carvme_gapfill
#SBATCH -e slurm-%j.err
#SBATCH -o slurm-%j.out

conda init
conda activate /people/lint730/carveme

MODEL="/rcfs/projects/crispr_carb/rhodobacter/model_gapfilled.xml"
MEDIADB="/rcfs/projects/crispr_carb/rhodobacter/data/media/CarveMeMinimalMediaFile.csv"
OUTPUT="/rcfs/rcfs/projects/crispr_carb/rhodobacter/model_gapfilled.xml"

gapfill $MODEL -m BL[dextrin],BL[pectin],BL[acgal],BL[abt__D],BL[arbt],BL[madg],BL[pala],BL[raffin],BL[salcn],BL[stys],BL[xylt],BL[gam],BL[Dara14lac],MM[cl],MM[na1] --mediadb $MEDIADB -o $OUTPUT --fbc2 -v
