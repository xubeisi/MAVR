#!/usr/bin/env python
__author__ = 'Sergei F. Kliver'

import argparse
import os

from Bio import SeqIO

from Routines.Sequence import record_by_expression_generator


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input_file", action="store", dest="input_file",
                    help="Input file with sequences")
parser.add_argument("-c", "--symbol_to_use", action="store", dest="char_to_use",
                    default="X",
                    help="Symbol to use to replace selenocystein")
parser.add_argument("-o", "--output", action="store", dest="output",
                    help="File to write output")
parser.add_argument("-f", "--format", action="store", dest="format", default="fasta",
                    help="Format of input and output files. Allowed formats genbank, fasta(default)")

args = parser.parse_args()

tmp_index_file = "temp.idx"

print("Parsing %s..." % args.input_file)
sequence_dict = SeqIO.index_db(tmp_index_file, args.input_file, format=args.format)
with open(args.out_prefix + ".ids", "w") as out_fd:
    for record_id in sequence_dict:
        sequence_dict[record_id].seq = sequence_dict[record_id].replace("U", args.char_to_use)
        sequence_dict[record_id].seq = sequence_dict[record_id].replace("u", args.char_to_use)

SeqIO.write(record_by_expression_generator(sequence_dict), args.output, args.format)
os.remove(tmp_index_file)


