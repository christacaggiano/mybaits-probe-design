import csv
from utils.io import *
from design.cfDNA import find_cpg_pattern


def define_patterns(sequence, cpg_list):
    for item in cpg_list:
        print(item)

if __name__ == "__main__":

    # TODO: command line arguments
    bed_file = "../data/muscle_cpgs_125.hg38.txt"  # file that primers are being gotten for
    tissue = "muscle"
    output_file = "../output/muscle_probes_125.txt"  # output file name
    pattern_file = "../output/muscle_probes_125_patterns_all.txt"
    sam_file = "../../primary_methylation_data_ALS/merged_bam_files/all_merged.bam"
    cpgs_per_region = 3

    sam_file = open_sam(sam_file)
    cpgs = load_cpgs(bed_file, cpgs_per_region, tissue)

    all_fails = 0
    with open(output_file, "w") as out, open(pattern_file, "w") as pattern:
        for cpg in cpgs:
            write_output(cpg, out, "reference")
            write_output(cpg, out, "methylated")

            mapped_reads, fails = fetch_reads(cpg, sam_file)
            all_fails += fails
            cpg_patterns = []

            for read in mapped_reads:
                write_output(cpg, out, "read", read)

                cpg_patterns.append(find_cpg_pattern(read, cpg))

            if cpg_patterns:
                write_patterns(cpg, cpg_patterns, pattern)

        print("Failed probes:", all_fails)

    
