#!/usr/bin/env python
import os

from Bio import SeqIO


from CustomCollections.GeneralCollections import IdList, SynDict


class EggNOGRoutines:
    def __init__(self):

        pass

    @staticmethod
    def edit_profile_names_in_fam_file(input_fam_file, output_fam_file, comments_prefix="#"):
        if comments_prefix:
            comments_prefix_len = len(comments_prefix)

        with open(input_fam_file) as in_fd:
            with open(output_fam_file) as out_fd:
                for line in in_fd:
                    if comments_prefix:
                        if line[:comments_prefix_len] == comments_prefix:
                            out_fd.write(line)
                    line_list = line.split("\t")
                    fam_name = line_list[0].split(".")[1]
                    out_fd.write("%s\t%s" % (fam_name, line_list[1]))


