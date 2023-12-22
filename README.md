# PopulationStats
# **popoolationStats_na_KL.py**
#This script takes alignment files (BAMS) from pool-seq, subsamples to minimize effects of differential coverage and calculates a genome wide population statistic (Tajima's D) using Popoolation.
# **popoolationStats.sh**
#This shell script was used to unzip a zip file of the alignment files and run popoolationStats_na_KL.py on a condor pool.
# **popoolationStats.sub**
#This was the submit script created to submit the job and associated files (popoolationStats_na_KL.py, popoolationStats.sh, MtbNCBIH37Rv.fa, RNAseq_##.zip) to the condor pool.
# **popoolationStatsBoxplot.R**
#This is the Rscript used to create figures of the Tajima's D results
