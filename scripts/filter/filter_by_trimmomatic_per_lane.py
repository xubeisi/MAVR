#!/usr/bin/env python
__author__ = 'Sergei F. Kliver'

# TODO: WORKS only for PE DATA
import os
import sys
import argparse

from Tools.Filter import Trimmomatic
#from Tools.Filter import FastQC

from Routines.File import check_path, save_mkdir

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--sample_directory", action="store", dest="samples_dir", required=True,
                    type=lambda s: check_path(os.path.abspath(s)),
                    help="Directory with samples")
parser.add_argument("-s", "--samples", action="store", dest="samples",
                    help="Comma-separated list of subdirectories(one per sample) to handle. "
                         "If not set all subdirectories will be considered as containing samples."
                         "In sample directory should one(in case SE reads) or two(in case PE reads) files."
                         "Filenames should should contain '_1.fq' or '_1.fastq' for forward(left) reads, "
                         " '_2.fq' or '_2.fastq' for reverse(right) reads and '.fq' or '.fastq' for SE reads")
parser.add_argument("-o", "--output_dir", action="store", dest="output_dir",
                    type=lambda s: check_path(os.path.abspath(s)),
                    default="./", help="Directory to write output. Default: current directory")
parser.add_argument("-t", "--threads", action="store", dest="threads", default=1, type=int,
                    help="Number of threads to use in Trimmomatic. Default - 1.")

parser.add_argument("-a", "--adapters", action="store", dest="adapters", type=os.path.abspath,
                    help="File with adapters to trim. If not set - skip this stage")
parser.add_argument("-m", "--mismatch_number", action="store", dest="mismatch_number", type=int, default=2,
                    help="Number of mismatches in adapter seed. Works only if -a/--adapters option is set. Default - 2.")
parser.add_argument("-p", "--pe_score", action="store", dest="pe_score", type=int, default=30,
                    help="PE reads adapter score. Works only if -a/--adapters option is set. Default - 30.")
parser.add_argument("-e", "--se_score", action="store", dest="se_score", type=int, default=10,
                    help="SE reads adapter score. Works only if -a/--adapters option is set. Default - 10.")
parser.add_argument("-n", "--min_adapter_len", action="store", dest="min_adapter_len", type=int, default=1,
                    help="Minimum length of adapter fragment. Works only if -a/--adapters option is set. Default - 1.")

parser.add_argument("-g", "--sliding_window_size", action="store", dest="sliding_window_size", type=int,
                    help="Size of sliding window when checking quality. If not set - skip this stage")
parser.add_argument("-q", "--average_quality_threshold", action="store", dest="average_quality_threshold", default=15,
                    type=int,
                    help="Quality threshold for sliding window. Works only if -q/--average_quality_threshold is set"
                         "Default - 15.")
parser.add_argument("-b", "--base_quality", action="store", dest="base_quality", default="phred33",
                    help="Type of base quality. Possible variants: phred33, phred64. Default - phred33 ")


parser.add_argument("-l", "--min_length", action="store", dest="min_len", type=int,
                    help="Minimum length of read to retain. If not set - skip this stage")
parser.add_argument("-j", "--path_to_trimmomatic_dir", action="store", dest="path_to_trimmomatic_dir", default="",
                    help="Path to Trimmomatic directory")

args = parser.parse_args()

Trimmomatic.jar_path = args.path_to_trimmomatic_dir
Trimmomatic.threads = args.threads
#print(Trimmomatic.path)
#print(Trimmomatic.jar_path)
samples = args.samples.split(",") if args.samples else sorted(os.listdir(args.samples_dir))

for sample in samples:
    print("Handling %s" % sample)

    sample_dir = "%s%s/" % (args.samples_dir, sample)

    sample_out_dir = "%s%s/" % (args.output_dir, sample)
    save_mkdir(sample_out_dir)
    trimmomatic_log = "%s/trimmomatic.log" % sample_out_dir
    trimmomatic_time_log = "%s/trimmomatic.time.log" % sample_out_dir

    files_from_sample_dir = sorted(os.listdir(sample_dir))

    filtered_files_from_sample_dir = []
    prefix_list = []
    for filename in files_from_sample_dir:
        if ".fq" == filename[-3:]:
            filtered_files_from_sample_dir.append("%s%s" % (sample_dir, filename))
            prefix_list.append("%s%s" % (sample_out_dir, filename[:-3]))
        elif ".fastq" == filename[-6:]:
            filtered_files_from_sample_dir.append("%s%s" % (sample_dir, filename))
            prefix_list.append("%s%s" % (sample_out_dir, filename[:-6]))
        elif ".fq.gz" == filename[-6:]:
            filtered_files_from_sample_dir.append("%s%s" % (sample_dir, filename))
            prefix_list.append("%s%s" % (sample_out_dir, filename[:-6]))
        elif ".fastq.gz" == filename[-9:]:
            filtered_files_from_sample_dir.append("%s%s" % (sample_dir, filename))
            prefix_list.append("%s%s" % (sample_out_dir, filename[:-9]))

    if len(filtered_files_from_sample_dir) % 2 != 0:
        print("Not all read files are paired for sample %s. Skipping..." % sample)
        continue

    number_of_lanes = len(filtered_files_from_sample_dir) / 2

    for lane_number in range(0, number_of_lanes):
        output_prefix = "%s%s.TMF" % (sample_out_dir, sample)
        left_reads_file = filtered_files_from_sample_dir[lane_number*2]
        right_reads_file = filtered_files_from_sample_dir[lane_number*2 + 1]

        Trimmomatic.timelog = trimmomatic_time_log
        Trimmomatic.filter(left_reads_file, output_prefix=prefix_list[lane_number*2],
                           output_prefix_left=prefix_list[lane_number*2+1],
                           output_extension="fq", right_reads=right_reads_file,
                           adapters_file=args.adapters,
                           mismatch_number=args.mismatch_number, pe_reads_score=args.pe_score, se_read_score=args.se_score,
                           min_adapter_len=args.min_adapter_len, sliding_window_size=args.sliding_window_size,
                           average_quality_threshold=args.average_quality_threshold,
                           leading_base_quality_threshold=None, trailing_base_quality_threshold=None,
                           crop_length=None, head_crop_length=None, min_length=args.min_len, logfile=trimmomatic_log,
                           base_quality=args.base_quality)

