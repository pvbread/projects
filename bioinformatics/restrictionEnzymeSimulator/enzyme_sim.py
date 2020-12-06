#!/usr/bin/env python3

# enzyme_sim.py -- Restriction Enzyme Simulation
# Written by Pedro Vizzarro Vallejos
# December 5th, 2020
# Usage: enzyme_sim.py enzyme_file mydna_file
#-----------------------------------------------------------------------------
# Main program
''' 
A program that takes an enzyme file in simplified Staden file format 
and applies it to a dna file, producing a report of the
number of matches in the dna, also producing output files with cleaved dna.
The output files are stored in a new directory enzyme_simulation_output.
This has been tested for Mac compatibility, but not for Windows, although
it should work as well.

A word of caution:
Using 2 files with the same name but different file extensions will cause the
output files to override.

E.g.: dna.fasta and dna.txt will produce output files named dna_enzyme
This is to avoid overly long text files such as XM_002638640.fasta_AatII
If however, you need to have this overlapping functionality, you can simply
comment out lines 137-140 of the code and it should now output as
dna.suffix_enzyme etc.
'''
#-----------------------------------------------------------------------------

import sys
import os.path
import re

def file_processing():

	def usage():
		print("Usage: enzyme_sim.py enzyme_file mydna_file\n")
		exit()

	if len(sys.argv) != 3:
		print("Missing or too many arguments.")
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
			#for fasta formatting
			if ".fasta" in sys.argv[2]:
				temp_string = ""
				split_data = dna_data.split("\n")
				for i in range(len(split_data)):
					if i != 0:
						temp_string += split_data[i]
				dna_data = temp_string

			dna_data = dna_data.replace(' ', '').replace('\n', '')
			valid_chars = ['a', 'c', 'g', 't']
			for char in dna_data:
				if char.lower() not in valid_chars:
					print("Error, non A-C-G-T char in file")
					valid_read = False
				
	except:
		print("Something went wrong with reading your dna file")
		usage()
	
	if not valid_read:
		print("Error, non A-C-G-T char in file")
		usage()

	try:
		with open(sys.argv[1]) as enzyme_file:
			enzyme_data = enzyme_file.read()
	except:
		print("Something went wrong with reading your enzyme file")
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
				dna_fragments.append(dna[(occurences[i-1]+cut_index):occurences[i]+cut_index])
				dna_fragments.append(dna[occurences[i]+cut_index:-1])
			else:
				dna_fragments.append(dna[occurences[i]+cut_index:occurences[i+1]+cut_index])

		if dna_fragments:
			return dna_fragments
		
		
	enzyme_list = enzymes.split('\n')
	enzyme_name_list = []
	output_file_count = 0
	output_file_fragments = {}
	total_fragments = 0

	for enzyme in enzyme_list:
		if enzyme: #this accounts for any empty splits (from line 103)
			cut_pattern = re.search('/.*/', enzyme)
			enzyme_name = enzyme.replace(cut_pattern.group(0), '')
			enzyme_name_list.append(enzyme_name)
			cut_pattern = cut_pattern.group(0).replace('/', '')
			dna_fragments = apply_cut(cut_pattern, dna)

			if dna_fragments:

				output_dir = os.path.join(os.getcwd(),"enzyme_simulation_output")
				if not os.path.exists(output_dir):
					os.mkdir(output_dir)
				dna_file_name = sys.argv[2]

				#take out these 4 lines if you wish to preserve the file extension in output file
				if ".txt" in sys.argv[2]:
					dna_file_name = sys.argv[2].split(".txt")[0]
				elif ".fasta" in sys.argv[2]:
					dna_file_name = sys.argv[2].split(".fasta")[0]

				#this filters any directory prefixes for both windows/mac
				if "/" in dna_file_name:
					dna_file_name = dna_file_name[dna_file_name.rfind("/")+1:]
				elif "\\" in dna_file_name:
					dna_file_name = dna_file_name[dna_file_name.rfind("\\")+1:]
				if "/" in enzyme_name:
					enzyme_name = enzyme_name[enzyme_name.rfind("/")+1:]
				elif "\\" in enzyme_name:
					enzyme_name = enzyme_name[enzyme_name.rfind("\\")+1:]
		
				output_name = "{}_{}".format(dna_file_name, enzyme_name)
				output_path = os.path.join(output_dir, output_name)
				output_content = open(output_path, "w+")
				for fragment in dna_fragments:
					output_content.write("{}\n".format(fragment))
				output_content.close()

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

