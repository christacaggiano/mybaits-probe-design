import subprocess

class MethylRead: 
    def __init__(self, chrom, start, end, strand, tissue, sequence=None, read_number=None):
        
        self.name = str(chrom) + ":" + str(start) + "-" + str(end)
        self.tissue = tissue

        self.chrom = chrom
        self.start = int(start)
        self.end = int(end) 
        self.size = int(end) - int(start)
        self.strand = strand

        self.reference = self.get_reference()
        self.methylated = self.get_methylated_reference()

        self.sequence = sequence if sequence is not None else self.reference
        self.read_number = read_number if read_number is not None else None 

        self.cpg_locations = self.identify_cpgs()
        self.cpg_number = len(self.cpg_locations)

    def __str__(self):
        return self.name
        

    def get_reference(self): 

        """
        using a compressed hg19 file, find the sequence for a region of interest
        :param chrom: chromosome of site of interest
        :param start: range start
        :param end: range end
        :return: sequence
        """
       
        # command to get the region from the two bit file from fasta
        cmd = ["/ye/zaitlenlabstore/christacaggiano/twoBit/twoBitToFa", "/ye/zaitlenlabstore/christacaggiano/twoBit/hg38.2bit",
            "stdout", "-seq=" + self.chrom, "-start=" + str(self.start), "-end=" + str(self.end)]

        # call command and get output
        result = subprocess.check_output(cmd)
        result = result.decode().upper()

        return self.format_sequence(result)

    def get_methylated_reference(self):

        methylated = self.reference

        for i in range(len(methylated)-1):
            if methylated[i] == "C" and methylated[i+1] != "G": 
                methylated = methylated[:i] + "T" + methylated[i+1:]
        return methylated
    
    def identify_cpgs(self): 

        cpg_positions = [] 

        for i in range(len(self.reference)-1):
            if self.reference[i] == "C" and self.reference[i+1] == "G": 
                cpg_positions.append(i) 

        return cpg_positions 

    def format_sequence(self, sequence_result): 
        
        for i in range(len(sequence_result)):
            if sequence_result[i] is "\n":
                break

        return sequence_result[i:].replace("\n", "")

def mark_cpgs(sequence): 

    for i in range(len(sequence)-1):
        if sequence[i] == "C" and sequence[i+1] == "G": 
            sequence = sequence[:i+1] + "*" + sequence[i+1:]

    return sequence

















