#!/bin/python3

import argparse
import pathlib
import ruamel.yaml

import internals.lint as l



yaml = ruamel.yaml.YAML(typ='rt') 
yaml.brace_single_entry_mapping_in_flow_sequence = True
yaml.preserve_quotes = True
yaml.indent(sequence=2, offset=0, mapping=4)
yaml.width = 3200


parser = argparse.ArgumentParser()


parser.add_argument("source_dir", type=str)
parser.add_argument("dest_file", type=str)
parser.add_argument("--overwrite", action="store_true")
parser.add_argument("--force_nme", action="store_true")

args = parser.parse_args()

source_path = pathlib.Path(args.source_dir).resolve()
dest_file = pathlib.Path(args.dest_file).resolve()

if not source_path.is_dir():
	print("Source path has to be a directory!")
	exit(1)

if dest_file.exists() and dest_file.is_dir():
	print("Destination has to be a file!")
	exit(1)
elif not args.overwrite:
	print("Destination exists, aborting. Pass --overwrite if you really want to overwrite the file.")
	exit(1)

source_files = [source_file for source_file in source_path.glob('*.yaml')]

# We want to process these in order; ideally, the order would be independent, but it's nice to be able to enforce an order
source_files.sort()

with open(dest_file, "w", encoding="utf-8") as dest:
	first = True
	for source_file in source_files:
		with open(source_file, encoding="utf-8") as s:
			y = yaml.load(s)

			l.lint(y, source_file)

			
			if (first):
				first = False
			else:
				dest.write("---\n")
			yaml.dump(y, dest)
			
			
			