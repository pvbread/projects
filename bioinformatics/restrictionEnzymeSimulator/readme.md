enzyme_sim.py -- Restriction Enzyme Simulation
<br />
<br />
December 5th, 2020<br />
Usage: enzyme_sim.py enzyme_file mydna_file<br />

<b>Main program</b>
<br /><br />
 
A program that takes an enzyme file in simplified Staden file format 
and applies it to a dna file, producing a report of the
number of matches in the dna, also producing output files with cleaved dna.
The output files are stored in a new directory enzyme_simulation_output.
This has been tested for Mac compatibility, but not for Windows, although
it should work as well.
<br /><br />
<b>A word of caution:</b>
Using 2 files with the same name but different file extensions will cause the
output files to override.
<br /><br />
E.g.: dna.fasta and dna.txt will produce output files named dna_enzyme
This is to avoid overly long text files such as XM_002638640.fasta_AatII
If however, you need to have this overlapping functionality, you can simply
comment out lines 137-140 of the code and it should now output as
dna.suffix_enzyme etc.
