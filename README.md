# cell-free DNA methylation biomarker discovery in ALS
## Mybaits probe capture design
## Summer 2018

________________________________________________________________

## Project Goal

* Given three tissues of interest- brain, muscle, leukocytes- and CpG sites found using sparse PCA, design probes to capture cell free DNA that can illustrate tissue of origin between ALS and control cell-free DNA.

* List of CpG of interest contain ~100-1,000 CpGs determined to be differentially methylated given reference tissue profiling from ENCODE, Roadmap, and other annotation projects.  

## Code Design

* Code designed to find all reads covering a CpG of interest in WGBS data (4 ALS and 4 CTRL merged)

```
├── README.md
├── data
│   ├── muscle_cpgs_125.hg38.txt
├── output
│   ├── muscle_probes_125.txt
│   └── muscle_probes_125_patterns_all.txt
└── src
    ├── __init__.py
    ├── design
    │   ├── MethylRead.py
    │   ├── __init__.py
    │   └── cfDNA.py
    ├── run.py
    ├── run.sh
    └── utils
        ├── __init__.py
        └── io.py
```




## File 1
probes.txt




* File contains three fasta headers per CpG of interest, one for reference sequence, and one for
>chr1:1093248-1093499|number_of_cpgs=5|tissue=muscle|reference
