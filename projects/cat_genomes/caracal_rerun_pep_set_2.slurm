#!/usr/bin/env bash
#SBATCH --array=1-34%34
#SBATCH --time=100:00:00          # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=8192       # Minimum memory required per CPU (in megabytes)
#SBATCH --job-name=cara
#SBATCH --error=/work/pavlov/okochenova/genomes_workdir/caracal/logs/exonerate_cat.%A_%a.err
#SBATCH --output=/work/pavlov/okochenova/genomes_workdir/caracal/logs/exonerate_cat.%A_%a.out

module load exonerate/2.2
source /work/pavlov/okochenova/profile

SPLITED_PEP_DIR="/work/pavlov/okochenova/genomes/cat/splited_pep_group_2/"

PEP_FILE="${SPLITED_PEP_DIR}cat_proteins_2_${SLURM_ARRAY_TASK_ID}.fasta"
CARACAL_GENOME="/work/pavlov/okochenova/genomes/caracal/final.assembly.fasta"
EXONERATE_OUTPUT_FILE="/work/pavlov/okochenova/genomes_workdir/caracal/exonerate_cat_pep_group_2/exonerate_cat_pep_group_2_${SLURM_ARRAY_TASK_ID}.out"

exonerate  --model protein2genome --showalignment --showquerygff --showtargetgff \
           -n 10 -q ${PEP_FILE} -t ${CARACAL_GENOME} > ${EXONERATE_OUTPUT_FILE}