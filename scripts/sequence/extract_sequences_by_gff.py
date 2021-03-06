#!/usr/bin/env python
__author__ = 'Sergei F. Kliver'

import argparse
import os

from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

from BCBio import GFF


from Routines.Sequence import record_generator


parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input_file", action="store", dest="input_file",
                    help="Input file with sequences")
parser.add_argument("-o", "--output_file", action="store", dest="output_file",
                    help="Output file with sequences")
parser.add_argument("-f", "--format", action="store", dest="format", default="fasta",
                    help="Format of input and output files. Allowed formats genbank, fasta(default)")
parser.add_argument("-t", "--type", action="store", dest="type", default="gene",
                    help="Types of sequences to extract")
parser.add_argument("-g", "--gff_file", action="store", dest="gff_file",
                    help="Gff file with annotations to extract")

args = parser.parse_args()

tmp_index_file = "temp.idx"
args.type = args.type.split(",")

print("Parsing %s..." % args.input_file)
sequence_dict = SeqIO.index_db(tmp_index_file, args.input_file, format=args.format)
annotations_dict = SeqIO.to_dict(GFF.parse(open(args.gff_file)))

SeqIO.write(record_generator(annotations_dict, sequence_dict, args.type), args.output_file, format=args.format)
os.remove(tmp_index_file)



