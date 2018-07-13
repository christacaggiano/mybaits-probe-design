import subprocess
import re

class MethylRead:

    def __init__(self, chrom, start, end, strand, tissue, sequence=None, read_number=None):

        self.name = f"{chrom}:{start}-{end}"
        self.tissue = tissue
        self.chrom = chrom
        self.start = int(start)
        self.end = int(end)
        self.size = self.end - self.start
        self.strand = strand

        self.reference = self.get_reference()
        self.methylated = self.get_methylated_reference()

        self.sequence = sequence if sequence is not None else self.reference
        self.read_number = read_number

        self.cpg_locations = self.identify_cpgs()

    def __str__(self):
        return self.name

    @property
    def cpg_number(self):
        return len(self.cpg_locations)

    def get_reference(self):

        """
        using a compressed hg19 file, find the sequence for a region of interest
        :param chrom: chromosome of site of interest
        :param start: range start
        :param end: range end
        :return: sequence
        """

        # command to get the region from the two bit file from fasta
        cmd = [
            "/ye/zaitlenlabstore/christacaggiano/twoBit/twoBitToFa",
            "/ye/zaitlenlabstore/christacaggiano/twoBit/hg38.2bit",
            "stdout", "-seq=" + self.chrom, "-start=" + str(self.start),
            "-end=" + str(self.end)]

        # call command and get output
        result = subprocess.check_output(cmd)
        result = result.decode().upper()
        return MethylRead.format_sequence(result)


    def get_methylated_reference(self):
        pattern = r"C[ATC]"  # C followed not by G
        return re.sub(pattern, "TC", self.reference)


    def identify_cpgs(self):
        pattern = r"CG"
        return [m.start(0) for m in re.finditer(pattern, self.reference)]


    @staticmethod
    def format_sequence(sequence_result):
        header_idx = sequence_result.index("\n")
        return sequence_result[header_idx:].replace("\n", "")


def mark_cpg_of_interest(sequence, size):
    return sequence[:size] + "*" + sequence[size:]
