#!/usr/bin/env python3

# pdbHistogram.py -- PDB Histogram
# Written by Pedro Vizzarro Vallejos
# December 5th, 2020
# Usage: ./pdbhistogram.py <my_pdb_file>
#-----------------------------------------------------------------------------
# Main program
''' 
Creates a histogram of atoms and residue from a pdb file. Can output a report
of multiple atoms or residue at once if necessary.

It has the following commands (please access the help command for more detailed
information on each function)

-- help
-- total
-- atomhistogram
-- reshistogram
-- atominfo
-- residueinfo

'''
#-----------------------------------------------------------------------------

import sys
import os.path
import re

def file_processing():
	def usage():
		print("Usage: ./pdbhistogram.py <my_pdb_file>")
		exit()

	if len(sys.argv) != 2: # #file doesn't exist or #file can't be opened:
		print("You must provide at least one pdb file for processing.")
		usage()

	if not os.path.isfile(sys.argv[1]):
		print("The provided arguments are not files")
		usage()

	try:
		with open(sys.argv[1]) as pdb_file:
			pdb_data = pdb_file.read()
			filtered_data = pdb_data.split('\n')
			new_filtered_data = []
			for line in filtered_data:
				if line[0:4]=='ATOM':
					new_filtered_data.append(line)

			atoms = {}
			for item in new_filtered_data:
				atoms[item[6:11]] = [item[12:16], item[16], item[17:20], item[17:20], item[19],\
										item[22:26], item[26], item[30:38], item[38:46], item[46:54],\
										item[54:60], item[60:66], item[76:78], item[78:80]]
		
			return atoms
	except:
		print("Something went wrong with reading your dna file")
		usage()

def run_program(atoms):
	# command list:
	def show_commands():
		print("-- help\n-- total\n-- atomhistogram\n-- reshistogram\n-- atominfo\n-- residueinfo\n-- quit\n")

	def help_information(query=0):
		
		#base case
		if not query:
			print("\n1. total\n2. atomhistogram\n3. reshistogram\n4. atominfo\n5. residueinfo\n")
			while(type(query) != "int" and (query > 5 or query < 1)):
				try:
					query = int(input("Please enter a number 1-5 for info on a specific command: "))
				except:
					pass

		if query == 1:
			print("\nUsage: total\nThis command outputs how many distinct files are in the provided file.\n")
		if query == 2:
			print("\nUsage: atomhistogram\nThis command outputs a list of atom frequencies in the file, from most frequent to least.\n")
		if query == 3:
			print("\nUsage: reshistogram\nThis command outputs a list of residue frequencies in the file, from most frequent to least.\n")
		if query == 4:
			print("\nUsage (case-sensitive): atominfo <atom_name(s)>\nExample: atominfo C4 OR atominfo P Na\nThis command outputs information on given atom(s).\n")
		if query == 5:
			print("\nUsage (case-sensitive): residueinfo <residue_name(s)>\nExample: residueinfo LYS or residue GLY PRO\nThis command outputs information on given residue(s).\n")


	def get_atom_residue_freq(item):
		frequencies = {}
		for value in atoms.values():
			try:
				frequencies[value[item]] += 1
			except:
				frequencies[value[item]] = 1
		sorted_frequencies = sorted(frequencies.items(), key=lambda x: (-x[1],x[0])) # the - takes care of reverse ordering
		for key, value in sorted_frequencies:
			print("{}: {}".format(key.strip(' '), value))
		print("\n")


	def atomresidueinfo(item, idx):
		instances = 0
		serial = []
		serial_string = ''
		for key, value in atoms.items():
			if value[idx].strip(' ') == item:
				instances += 1
				serial.append(key.strip(' '))
		if not instances:
			print("No instances of {} found in the file, check spelling or case-sensitivity.".format(item))

		else:
			item_type = 'element'
			if idx:
				item_type = 'residue'
			print("{} atom(s) of {} {}".format(instances, item_type, item))
			for number in range(len(serial)):
				if number == (len(serial)-1):
					serial_string += serial[number]
				else:
					serial_string += "{}, ".format(serial[number])
			print("Serial numbers are: {}\n".format(serial_string))

	valid_choice = ['help', 'total', 'atomhistogram', 'reshistogram', 'atominfo', 'residueinfo', 'quit']

	def input_validator(input1, input2=None):
		if input1 == 'atominfo' or input1 == 'residueinfo' and input2 == None:
			print("Info commands require second argument. Usage:  atominfo <atom_name> or residueinfo <residue_name>")
			return False
		if input1 in valid_choice:
			return True

	user_choice = ['', '']
	print("Welcome to the pdb histogram program.")
	
	while (not input_validator(user_choice[0], user_choice[1])):
		show_commands()
		user_choice = input('Please write out the option you want to pick: ').split(' ')
		if len(user_choice) == 1:
			user_choice.append('') # this keeps the input for the while-loop valid
		if user_choice[0] not in valid_choice:
			print('Option not found, please check spelling. Type "help" for usage instructions.')

		if user_choice[0] == 'total':
			print("{} atoms in file {}\n".format(len(atoms), sys.argv[1]))
			user_choice[0] = ''

		if user_choice[0] == 'atomhistogram':
			get_atom_residue_freq(0)
			user_choice[0] = ''

		if user_choice[0] == 'reshistogram':
			get_atom_residue_freq(2)
			user_choice[0] = ''

		if user_choice[0] == 'atominfo' and (not user_choice[1]):
			print("Missing argument.")
			help_information(4)
			user_choice[0] = ''
		elif user_choice[0] == 'atominfo':
			for i in range(1,len(user_choice)):
				atomresidueinfo(user_choice[i], 0)
			for i in range(len(user_choice)):
				user_choice[i] = ''

		if user_choice[0] == 'residueinfo' and (not user_choice[1]):
			print("Missing argument.")
			help_information(5)
			user_choice[0] = ''
		elif user_choice[0] == 'residueinfo':
			for i in range(1,len(user_choice)):
				atomresidueinfo(user_choice[i], 2)
			for i in range(len(user_choice)):
				user_choice[i] = ''

		if user_choice[0] == 'help':
			help_information()
			user_choice[0] = ''

	if user_choice[0] == 'quit':
		print("Thank you for using the pdb histogram program.")
		exit()

def main():
	atoms = file_processing()
	run_program(atoms)

main()
