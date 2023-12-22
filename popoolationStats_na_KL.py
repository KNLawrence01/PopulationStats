#!/usr/bin/env python

import sys
import subprocess
from collections import defaultdict
import pandas as pd
import numpy as np

#####
# This script takes in bams from pool-seq, subsamples to minimize effects of
# differential coverage and calculates genome wide population statistics (pi and Tajima's D) using Popoolation.
# Note: paths to Popoolation and Samtools scripts and path to reference genome  and target coverage for subsampling are hard coded.
#####
### Edited by Kadee L to get rid of pi and theta at end results
#Also changed to work for Mtb instead of GV

# check for command line arguments
if len(sys.argv) < 3:
    print("Usage: popoolationStats.py <output> <bam1> ... <bamN>")
    sys.exit(0)

bams =  sys.argv[2:]
outfile = sys.argv[1]

def popStats(bam,resultDict):
    # make pileup file using Samtools
    sample = bam.split(".")[0]
    pilefile = sample+".pileup"
    with open(pilefile,"w") as out:
        print("Converting bam to pileup ...")
        subprocess.call(["/opt/PepPrograms/samtools-1.11/samtools","mpileup","-B","-f",\
                "/opt/data/mtuberculosis/MtbNCBIH37Rv.fa",bam],stdout=out)
    
    # subsample pileup file 10X - repeat 9 times
    tajimasd = []
    for x in range(1,11):
        print("subsample #"+str(x)+" of "+pilefile+" ...")
        subfile = bam.split(".")[0]+"_subsampled_"+str(x)+".pileup"
        subprocess.call(["perl","/opt/PepPrograms/popoolation_1.2.2/basic-pipeline/subsample-pileup.pl",\
            "--input",pilefile,"--output",subfile,"--target-coverage","50","--max-coverage","1000",\
                "--min-qual","20","--fastq-type","sanger","--method","withoutreplace"])
        # calculate Tajima's D for each subsampled pileup file
        dfile = subfile.split(".")[0]+".d"
        print("Calculating stats ...")
        subprocess.call(["perl","/opt/PepPrograms/popoolation_1.2.2/Variance-sliding.pl","--measure","D","--pool-size",\
            "10000","--fastq-type","sanger","--min-count","2","--window-size","100000","--step-size",\
                "10000","--input",subfile,"--output",dfile])
    # average stats across windows and replicates
    tajimasd.append(list(pd.read_csv(dfile,sep="\t").iloc[:,4]))
    tajimasd2 = [float(td) for td in tajimasd[0] if td != 'na']
    tajimasdA = np.mean(tajimasd2)
    resultDict[sample] = [tajimasdA]
    return resultDict

# run popStats on all bams
statDict = {}
for bam in bams:
    popStats(bam,statDict)

# write genome-wide stats for all samples to output
with open(outfile,"w") as out:
    out.write("Sample\ttajimasD\n")
    for key,value in statDict.items():
        out.write(key+'\t'+'\t'.join([str(x) for x in value])+'\n')
