#!/usr/bin/env python3

import sys
import os.path
import re

#error and file checking function

## need to add fasta format compatibility

def file_processing():

	def usage():
		print("Usage: ./enzyme_sim.py restriction_enzyme_file dna_file")
		exit()

	if len(sys.argv) != 3:
		usage()

	if not os.path.isfile(sys.argv[1]) or not os.path.isfile(sys.argv[2]):
		print("The provided arguments are not files")
		usage()

	dna_data = ""
	enzyme_data = ""
	valid_read = True

	#dna_file check
	try:
		with open(sys.argv[2]) as dna_file:
			dna_data = dna_file.read()
			dna_data = dna_data.replace(' ', '').replace('\n', '')
			valid_chars = ['a', 'c', 'g', 't']
			for char in dna_data:
				if char.lower() not in valid_chars:
					print("Error, non A-C-G-T char in file")
					valid_read = False
	except:
		print("Something went wrong with reading your dna file")
		usage()

	try:
		with open(sys.argv[1]) as enzyme_file:
			enzyme_data = enzyme_file.read()
	except:
		print("Something went wrong with reading your enzyme file")
		usage()

	if not valid_read:
		usage()

	return enzyme_data, dna_data

#program function

def program(enzymes, dna):

	output = {}

	def apply_cut(pattern, dna):

		cut_index = pattern.find("'")
		pattern = pattern.replace("'", '')
		occurences = [index.start() for index in re.finditer(pattern, dna)]
		dna_fragments = []
		for i in range(len(occurences)):
			if i == 0:
				dna_fragments.append(dna[0:occurences[i]+cut_index])
				if len(occurences) == 1:
					dna_fragments.append(dna[occurences[i]+cut_index:-1])

			elif i == (len(occurences)-1):
				dna_fragments.append(dna[(occurences[i-1]+cut_index):occurences[i]+cut_index])#deal with negative index
				dna_fragments.append(dna[occurences[i]+cut_index:-1])
			else:
				dna_fragments.append(dna[occurences[i]+cut_index:occurences[i+1]+cut_index])

		if dna_fragments:
			return dna_fragments
		
		
	enzyme_list = enzymes.split('\n')
	enzyme_list.pop(-1) #removes the last empty split
	enzyme_name_list = []
	output_file_count = 0
	output_file_fragments = {}
	total_fragments = 0

	for enzyme in enzyme_list:
		cut_pattern = re.search('/.*/', enzyme)
		enzyme_name = enzyme.replace(cut_pattern.group(0), '')
		enzyme_name_list.append(enzyme_name)
		cut_pattern = cut_pattern.group(0).replace('/', '')
		dna_fragments = apply_cut(cut_pattern, dna)

		if dna_fragments:
			output_name = "{}_{}".format(sys.argv[2], enzyme_name)
			output = open(output_name, "w+")	
			for fragment in dna_fragments:
				output.write("{}\n".format(fragment))
			output.close()
			output_file_count += 1
			output_file_fragments[enzyme_name] = len(dna_fragments)
			total_fragments += len(dna_fragments)

	enzyme_string = ""
	for i in range(len(enzyme_name_list)):
		if i == (len(enzyme_name_list)-1):
			enzyme_string += enzyme_name_list[i]
		else:
			enzyme_string += enzyme_name_list[i] + ", "

	print("{} restriction enzymes in {} file".format(len(enzyme_name_list),sys.argv[1]))
	print("Names of the restriction enzymes in {} file: {}".format(sys.argv[1], enzyme_string))
	print("{} output file(s) created".format(output_file_count))
	print("Specific rectriction enzyme fragment count:")
	for key, value in output_file_fragments.items():
		print("{}: {}".format(key, value))
	print("Total fragments: {}".format(total_fragments))

def main():
	enzyme_data, dna_data = file_processing()
	program(enzyme_data, dna_data)
	exit()

main()

