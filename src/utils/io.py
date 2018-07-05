import pysam 
from design.MethylRead import MethylRead, mark_cpgs
from design.cfDNA import * 
from collections import defaultdict

def open_sam(sam_file):

    return pysam.AlignmentFile(sam_file, "r")


def load_cpgs(bed_file, cpgs_per_region, tissue):

    cpgs = {}

    # for each cpg in the bed file of interest
    with open(bed_file) as bed:

        for line in bed:
            splitline = (line.strip("\n")).split("\t")
            chrom, start, end, strand = splitline[:4]
            strand = format_strand(strand) 

            if (chrom, start, end) not in cpgs: 
                cpgs[(chrom, start, end)] = MethylRead(chrom, start, end, strand, tissue)

    return filter_cpgs(cpgs, cpgs_per_region)


def format_strand(strand): 
    return strand == "R"


def filter_cpgs(cpg_dictionary, cpgs_per_region): 

    fail_filter = []

    for cpg in cpg_dictionary: 
        read = cpg_dictionary[cpg]

        if read.cpg_number < cpgs_per_region: 
            fail_filter.append(cpg)

    for cpg in fail_filter: 
        del cpg_dictionary[cpg]

    return list(cpg_dictionary.values())


def write_output(reference, output_file, read_type, read=None):
    
    if read_type == "read":
        header, sequence = format_print(reference, read_type, read)
    else: 
        header, sequence = format_print(reference, read_type)

    print(header, file=output_file)
    print(sequence, file=output_file)


def format_print(reference, read_type, read=None):  
 
    if read_type == "reference": 
        return ">" + reference.name  + "|number_of_cpgs=" + str(reference.cpg_number) + "|tissue=" + str(reference.tissue) + "|" + "reference", reference.reference

    elif read_type == "methylated": 
        return ">" + reference.name  + "|number_of_cpgs=" + str(reference.cpg_number) + "|tissue=" + str(reference.tissue) + "|" + "fully_converted_methylated", reference.methylated
    
    elif read_type == "read":
        return ">" + read.name  + "|read_number=" + str(read.read_number), align_read(reference, read)


def fetch_reads(reference, sam_file): 

    cpg_start = int(reference.start + (reference.size-1)/2) 
    cpg_end = cpg_start + 1
    
    print(reference.sequence[cpg_start-1:cpg_end+1])

    mapped_reads = sam_file.fetch(region=reference.chrom + ":" + str(cpg_start) + "-" + str(cpg_end))

    cpg_reads = []

    read_number = 1
    fails = 0  
    for cfdna_read in mapped_reads: 
        
        pos = cfdna_read.get_reference_positions()

      
        if pos[-1]-pos[0]+1 == len(cfdna_read.query_sequence):
            cpg_reads.append(MethylRead(reference.chrom, pos[0], pos[-1], cfdna_read.is_reverse,  reference.tissue, cfdna_read.query_sequence, read_number, cpg_start))
            read_number += 1
        else: 
            fails +=1 

    return cpg_reads, fails
         

def write_patterns(cpg, patterns_list, out):
    quantified_patterns = quantify_patterns(patterns_list) 
    

    pattern_header = "> " + str(cpg.name) + "("
    cpg_number = 1 
    for cpg in quantified_patterns:
        if cpg[0]+cpg[1] == 0: 
            pattern_header += "cpg" + str(cpg_number) + ": " + "NA, "
        else: 
            prop_methylated = round(cpg[1]/(cpg[0]+cpg[1]), 3) 
            pattern_header += "cpg" + str(cpg_number) + ": " + str(prop_methylated) + ", "
        cpg_number += 1 

    print(pattern_header[:-1] + ")", file=out)

    for pattern in patterns_list: 

        print(pattern, file=out)































