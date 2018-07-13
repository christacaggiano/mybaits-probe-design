from collections import defaultdict


def align_read(reference, read):
    seq = read.sequence

    dashes_beginning = max(0, read.start-reference.start)
    dashes_end = max(0, reference.end - read.end)
    seq_start = max(0, reference.start-read.start)
    seq_end = max(0, read.end-reference.end)

    seq = seq[seq_start:-(seq_end+1)]
    aligned_string = "-" * dashes_beginning + seq+ "-" * dashes_end
    read.sequence = aligned_string

    marked_alignment = mark_alignment(reference.sequence, aligned_string)

    return "\n".join([reference.sequence, marked_alignment, aligned_string])


def mark_alignment(reference_string, read_string):

    alignment_indicators = []

    for ref_nt, read_nt in zip(reference_string, read_string):
        if read_nt == "-":
            alignment_indicators.append(" ")
        elif read_nt == ref_nt:
            alignment_indicators.append("|")
        else:
            alignment_indicators.append(".")
    return "".join(alignment_indicators)


def find_cpg_pattern(read, reference):

    locations = reference.cpg_locations
    d = defaultdict(lambda: ".", {"-": "-", "C": "1", "T": "0"})
    return "".join([d[read.sequence[location]] for location in locations])


def quantify_patterns(pattern_list):
    counts = []
    for index_group in zip(*pattern_list):
        counts.append((index_group.count("0"), index_group.count("1")))
    return counts
