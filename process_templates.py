#!/usr/bin/env python

import argparse
import glob
import json
import os
import shutil
import sys

def main(arglist=None):
	args = parse_args(arglist)
	rules = load_rules(args)
	check_rules(rules)
	query_for_missing_substitutions(rules['substitutions'])
	paths = process_inputs_into_pathlist(rules['inputs'])
	check_input_paths(paths)
	for path in paths:
		copy_and_replace(path, rules['substitutions'], rules['outputs'])

def parse_args(arglist):
	parser = argparse.ArgumentParser(
		description='A template-substitution engine that loads configuration '
		            'from a set of cascading json files. Note that substitutions '
		            'left null are queried.')
	parser.add_argument('rules_files',
		nargs='+',
		help='settings files to use')
	parser.add_argument('-i', dest='inputs',
		nargs='+',
		help='the file(s) to process as template inputs')
	parser.add_argument('-o', action='store', dest='outputs',
		help='the directory to store the output')
	return parser.parse_args(arglist)

def load_rules(args):
	rules = {}
	for path in args.rules_files:
		with open(path, 'r') as f:
			rules.update(json.load(f))
	if args.inputs:
		rules['inputs'] = args.inputs
	if args.outputs:
		rules['outputs'] = args.outputs
	return rules

def check_rules(rules):
	if 'inputs' not in rules:
		print >> sys.stderr, 'input files not specified!'
		sys.exit(1)
	if 'outputs' not in rules:
		print >> sys.stderr, 'output folder not specified!'
		sys.exit(2)
	if not os.path.exists(rules['outputs']):
		print >> sys.stderr, 'no such output directory: %s!' % rules['outputs']
		sys.exit(3)
	if not os.path.isdir(rules['outputs']):
		print >> sys.stderr, 'not an output directory: %s!' % rules['outputs']
		sys.exit(4)
	if 'substitutions' not in rules:
		sys.exit(0) # nothing to do

def check_input_paths(paths):
	if not paths:
		print >> sys.stderr, 'no files to process!'
		sys.exit(5)

def query_for_missing_substitutions(substitutions):
	for key in substitutions:
		if substitutions[key] is None:
			substitutions[key] = raw_input(
				'What value should be used for "' + key + '"? ')

def process_inputs_into_pathlist(inputs):
	'''Handle inputs as either a string or list,
	   and expand pattern-matching globs into path lists.
	'''
	paths = []
	if isinstance(inputs, basestring):
		paths.extend(glob.glob(inputs))
	else:
		for path in inputs:
			paths.extend(glob.glob(path))
	return paths

def copy_and_replace(input_path, substitutions, output_dir):
	text = read_file(input_path)
	text = make_substitutions(text, substitutions)
	output_path = os.path.join(output_dir, os.path.basename(input_path))
	write_file(output_path, text)
	shutil.copystat(input_path, output_path)

def read_file(path):
	with open(path, 'r') as i:
		return i.read()

def write_file(path, text):
		with open(path, 'w') as o:
			o.write(text)

def make_substitutions(text, substitutions):
	# todo: make this a single pass replacement step
	for key in substitutions:
		text = text.replace(template_pattern(key), substitutions[key])
	return text

def template_pattern(variable):
	return '[% ' + variable + ' %]';
	
if __name__ == '__main__':
	main()
