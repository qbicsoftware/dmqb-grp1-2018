
from formats.abstract_format import AbsFormat


class Fasta(AbsFormat):
    """Fasta format validator following the NCBI definition.

    Validates whether the file at the given path is of the fasta format or not.
    Depending on the given code at the initialization it tests for DNA or aminoacid coding.

    The format definition can be found here:
    https://blast.ncbi.nlm.nih.gov/Blast.cgi?CMD=Web&PAGE_TYPE=BlastDocs&DOC_TYPE=BlastHelp (17.6.18)
    """

    def __init__(self, code):
        """Constructor for the fasta-Validator the given code decides whether it tests for DNA or aminoacid coding."""

        if code == "DNA":
            self.allowed = self.get_dna()
        if code == "AA":
            self.allowed = self.get_aa()

    def validate_file(self, file_path):
        """Validates whether the file at the given path is of the fastq format or not.

            :returns boolean whether the format is valid, string message why it is not or an empty string if valid.
        """

        file = open(file_path, "r")

        had_header = False
        count = 1
        for line in file:
            line = line.strip()
            if line == "":
                file.close()
                return False, "Error empty line at line: " + str(count)

            if had_header:
                if line.startswith(">"):
                    file.close()
                    return False, "Header without a sequence in line: " + str(count-1)

                result, message, char_pos = self.validate_line_coding(line)

                if result:
                    had_header = False
                    count += 1
                else:
                    file.close()
                    return False, message+" At line: " + str(count) + ":" + str(char_pos)

            else:
                if line.startswith(">"):
                    had_header = True
                    count += 1
                    continue
                else:
                    result, message, char_pos = self.validate_line_coding(line)

                    if result:
                        count += 1
                    else:
                        file.close()
                        return False, message + " at line: " + str(count) + ":" + str(char_pos)

        if had_header:
            file.close()
            return False, "Header at end of file with no sequence."

        file.close()
        return True, ""

    def validate_line_coding(self, line):
        """checks the given line for characters not allowed by the format either DNA or aminoacid coding"""
        c_count = 1
        for c in line:
            if c in self.allowed:
                c_count += 1
                continue
            else:
                return False, "Character not allowed [" + c + "] in sequence.", c_count

        return True, "", -1

    """
        A  adenosine          C  cytidine             G  guanine
        T  thymidine          N  A/G/C/T (any)        U  uridine 
        K  G/T (keto)         S  G/C (strong)         Y  T/C (pyrimidine) 
        M  A/C (amino)        W  A/T (weak)           R  G/A (purine)        
        B  G/T/C              D  G/A/T                H  A/C/T      
        V  G/C/A              -  gap of indeterminate length
    """

    @staticmethod
    def get_dna():
        """returns a list of all allowed characters coding for an base"""
        return ['A', 'C', 'G', 'T', 'N', 'U', 'K', 'S', 'Y', 'M', 'W', 'R', 'B', 'D', 'H', 'V', '-']

    """
        A  alanine               P  proline       
        B  aspartate/asparagine  Q  glutamine      
        C  cystine               R  arginine      
        D  aspartate             S  serine      
        E  glutamate             T  threonine      
        F  phenylalanine         U  selenocysteine
        G  glycine               V  valine        
        H  histidine             W  tryptophan        
        I  isoleucine            Y  tyrosine
        K  lysine                Z  glutamate/glutamine
        L  leucine               X  any
        M  methionine            *  translation stop
        N  asparagine            -  gap of indeterminate length
    """

    @staticmethod
    def get_aa():
        """returns a list of all allowed characters coding for an aminoacid"""
        return ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                'W', 'Y', 'Z', 'X', '*', '-']
