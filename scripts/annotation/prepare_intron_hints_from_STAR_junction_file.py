#!/usr/bin/env python
__author__ = 'Sergei F. Kliver'
import argparse

from Tools.Annotation import Exonerate, AUGUSTUS
from Routines.File import make_list_of_path_to_files

parser = argparse.ArgumentParser()

parser.add_argument("-i", "--input", action="store", dest="input", required=True,
                    help="File with junctions from STAR output")
parser.add_argument("-o", "--output", action="store", dest="output", required=True,
                    help="File to write gff with intron hints")
parser.add_argument("-m", "--min_supporting_readse", action="store", dest="min_supporting_reads", default=1,
                    type=int,
                    help="Minimum number of supporting reads to retain junction. Default: 1, i.e. "
                         "all junctions from file are retained")
parser.add_argument("-s", "--source", action="store", dest="source", default="RNASEQ",
                    help="Source of hints. Default: RNASEQ")
parser.add_argument("-p", "--priority", action="store", dest="priority", default=100, type=int,
                    help="Priority of hints. Default: 100")
args = parser.parse_args()

AUGUSTUS.convert_star_junctions_to_intron_hints(args.input, args.output,
                                                min_supporting_reads=args.min_supporting_reads,
                                                source=args.source, priority=100)