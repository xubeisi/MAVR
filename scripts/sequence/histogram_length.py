#!/usr/bin/env python
__author__ = 'Sergei F. Kliver'

import os
import argparse

from numpy import arange, int32, append

from Bio import SeqIO

import matplotlib.pyplot as plt

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input_file", action="store", dest="input_file",
                    help="Input file with sequences")
parser.add_argument("-o", "--output_prefix", action="store", dest="output_prefix",
                    help="Prefix of output files")
parser.add_argument("-f", "--format", action="store", dest="format", default="fasta",
                    help="Format of input file. Default - fasta")
parser.add_argument("-b", "--number_of_bins", action="store", dest="number_of_bins", type=int,
                    help="Number of bins in histogram. Incompatible with -w/--width_of_bins option. Default - 30")
parser.add_argument("-w", "--width_of_bins", action="store", dest="width_of_bins", type=int,
                    help="Width of bins in histogram. Incompatible with -b/--number_of_bins option. Not set by default")
parser.add_argument("-n", "--min_length", action="store", dest="min_length", type=int, default=1,
                    help="Minimum length of sequence to count. Default - 1")
parser.add_argument("-x", "--max_length", action="store", dest="max_length", type=int,
                    help="Maximum length of sequence to count. Default - length of longest sequence")
args = parser.parse_args()

if (args.number_of_bins is not None) and (args.width_of_bins is not None):
    raise AttributeError("Options -w/--width_of_bins and -b/--number_of_bins mustn't be set simultaneously")
sequence_dict = SeqIO.index_db("temp.idx", args.input_file, args.format)

lengths = [len(sequence_dict[record].seq) for record in sequence_dict]
max_len = max(lengths)

if args.max_length is None:
    args.max_length = max_len

if (args.max_length != max_len) and (args.min_length != 1):
    filtered = []
    for entry in lengths:
        if args.min_length <= entry <= args.max_length:
            filtered.append(entry)
    else:
        filtered = lengths

plt.figure(1, figsize=(6, 6))
plt.subplot(1, 1, 1)

if args.number_of_bins:
    bins = args.number_of_bins
elif args.width_of_bins:
    bins = arange(args.min_length, args.max_length, args.width_of_bins, dtype=int32)
    bins = append(bins, [args.max_length])
else:
    bins = 30

plt.hist(lengths, bins=bins)
plt.xlim(xmin=args.min_length, xmax=args.max_length)
plt.xlabel("Length")
plt.ylabel("N")
plt.title("Distribution of sequence lengths")

for ext in ".png", ".svg", ".eps":
    plt.savefig(args.output_prefix + ext)

os.remove("temp.idx")