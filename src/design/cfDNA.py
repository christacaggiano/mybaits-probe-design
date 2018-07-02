
from Bio import pairwise2
from Bio.Seq import Seq
from Bio.pairwise2 import format_alignment
from collections import defaultdict


def align_read(reference, read):
    seq = read.sequence


    dashes_beginning = max(0, read.start-reference.start)
    dashes_end = max(0, reference.end - read.end)
    seq_start = max(0, reference.start-read.start)
    seq_end = max(0, read.end-reference.end)

    # print(read.start-reference.start)
    seq = seq[seq_start:-(seq_end+1)]

    aligned_string = "-"*dashes_beginning + seq+ "-"*dashes_end

    read.sequence = aligned_string

    return reference.methylated + "\n" + mark_alignment(reference.sequence, aligned_string) + "\n" + aligned_string

def mark_alignment(reference_string, read_string): 

    alignment_indicators = "" 

    for ref_nt, read_nt in zip(reference_string, read_string): 
        if read_nt is "-": 
            alignment_indicators += " "
        elif read_nt == ref_nt: 
            alignment_indicators += "|"
        else: 
            alignment_indicators += "."

    return alignment_indicators

def find_cpg_pattern(read, reference): 

    locations = reference.cpg_locations
    d  = defaultdict(lambda: ".", {"-":"-", "C":"1", "T":"0"})
    pattern = "".join([d[read.sequence[location]] for location in locations])
    return pattern


def quantify_patterns(pattern_list): 
    counts = []
    
    for i in range(len(pattern_list[0])):
        zero_count = len([str for str in pattern_list if str[i]=="0"])
        one_count = len([str for str in pattern_list if str[i]=="1"])
        counts.append((zero_count, one_count))
    
    return counts 











