#!/usr/bin/env bash
#SBATCH --array=1-914%914
#SBATCH --time=100:00:00         # Run time in hh:mm:ss
#SBATCH --mem-per-cpu=4192       # Minimum memory required per CPU (in megabytes)
#SBATCH --job-name=Duni_anolis
#SBATCH --error=/work/pavlov/okochenova/genomes_workdir/Duni/logs/exonerate_anolis.ncbi.%A_%a.err
#SBATCH --output=/work/pavlov/okochenova/genomes_workdir/Duni/logs/exonerate_anolis.ncbi.%A_%a.out

module load exonerate/2.2
source /work/pavlov/okochenova/profile

SPLITED_PEP_DIR="/work/pavlov/okochenova/genomes/anolis/pep/anolis_carolinensis/"
PEP_FILE="${SPLITED_PEP_DIR}anolis_carolinensis.ensembl_${SLURM_ARRAY_TASK_ID}.fasta"

GENOME="/work/pavlov/okochenova/genomes/Darevskia/D_uni_v2.fa"

EXONERATE_OUTPUT_DIR="/work/pavlov/okochenova/genomes_workdir/Duni/exonerate_anolis_pep/"
mkdir -p ${EXONERATE_OUTPUT_DIR}
EXONERATE_OUTPUT_FILE="${EXONERATE_OUTPUT_DIR}/exonerate_anolis_pep_${SLURM_ARRAY_TASK_ID}.out"


exonerate  --model protein2genome --showalignment --showquerygff --showtargetgff \
           -n 10 -q ${PEP_FILE} -t ${GENOME} > ${EXONERATE_OUTPUT_FILE}
