from pymol import cmd
import os

def load_pdblist(pdblist, addext = 0):
	"""
DESCRIPTION

	Load a list of PDBs from a text file.  All the PDBs should be in the current working directory.  The text file should contain a PDB filename per line.  If addext is 1, .pdb will be added to names in the file.
	
USAGE

	load_pdblist mypdbs.txt
	load_pdblist mypdbswithoutextension.txt, addext = 1
	
ARGUMENTS

	pdblist = string: Name of the file containing the pdb list.
	addext = boolean: Should .pdb be added to the end of each name in the file.  Set to true if only the prefix is written in the file.
	
NOTES
	"""

	#Load the pdblist, and convert to a list.
	listfile = open(pdblist, 'r')
	pdbs = listfile.readlines()
	
	for pdb in pdbs:
		pdbname = pdb.strip()
		if (addext):
			pdbname = pdb.strip() + '.pdb'
		
		cmd.load(pdbname)
						
cmd.extend('load_pdblist', load_pdblist)
#Configure the selector argument to be a selection when tab completing.
#cmd.auto_arg[0]['rand_sequence'] = [ cmd.selection_sc, 'selection', ' ' ]