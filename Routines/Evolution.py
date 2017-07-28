__author__ = 'mahajrod'

from Routines.Phylogenetics import PhylogeneticsRoutines


class EvolutionRoutines(PhylogeneticsRoutines):
    def __init__(self):
        PhylogeneticsRoutines.__init__(self)

    @staticmethod
    def split_paml_bootstrap_samples(bootstrap_file, output_directory, output_prefix,
                                     output_extension="phy"):
        counter = 1
        with open(bootstrap_file, "r") as bootstrap_fd:
            for line in bootstrap_fd:

                seq_number, pos_number = map(int, line.strip().split())

                output_file = "%s/%s_%i.%s" % (output_directory,
                                               output_prefix,
                                               counter,
                                               output_extension)
                with open(output_file, "w") as out_fd:
                    out_fd.write(line)
                for i in range(0, seq_number):
                    out_fd.write(bootstrap_fd.next())
                counter += 1
