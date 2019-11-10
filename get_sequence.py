#This function will print out the one-letter code sequence of a selection.
#If there are multiple chains, it will output each separately.
#If there are residues other than the 20 canonical AAs, they will be output as X.
#A residue with only hydrogens will be ignored, as will HOH or WAT.

from pymol import cmd

def get_sequence(seq_object):
	"""
DESCRIPTION

	The "get_sequence" command returns the one-letter code sequence of a selection to the terminal.
	
USAGE

	get_sequence seq_object
	
ARGUMENTS

	seq_object = string: name of the selection to be processed
	
NOTES

	If the selection contains multiple chains, each chain will be printed out separately with a title.
	Multi-object and multi-state selections may yield unexpected results, depending on the chain identifiers.
	If the selection has different chain IDs and segids, this may also result in unexpected chain ordering.
	Residues containing only hydrogen atoms and water molecules will be ignored.
	Other residues other than the 20 canonical amino acids will be output as residue X.
	"""

	#Create a dictionary containing the three-to-one letter code conversion.
	oneletter = {
		'ALA' : 'A',
		'CYS' : 'C',
		'ASP' : 'D',
		'GLU' : 'E',
		'PHE' : 'F',
		'GLY' : 'G',
		'HIS' : 'H',
		'ILE' : 'I',
		'LYS' : 'K',
		'LEU' : 'L',
		'MET' : 'M',
		'ASN' : 'N',
		'PRO' : 'P',
		'GLN' : 'Q',
		'ARG' : 'R',
		'SER' : 'S',
		'THR' : 'T',
		'VAL' : 'V',
		'TRP' : 'W',
		'TYR' : 'Y'
		}
	#Store by atom information in atomlist_chain, atomlist_resi, and atomlist_resn
	stored.atomlist_chain = []
	stored.atomlist_resi = []
	stored.atomlist_resn = []
	cmd.iterate(seq_object + ' and not elem H and not resn HOH and not resn WAT', 'stored.atomlist_chain.append(chain); stored.atomlist_resi.append(resi); stored.atomlist_resn.append(resn)')
	
	#Set up a tracking variable for chain and resn.
	curchain = ''
	curresi = ''
	
	#Set up an empty string to hold the sequences.
	out_seq = ''
	
	#Iterate over all indecies in the atomlist series.  Using atomlist_chain because they are all the same.
	for atomidx in range(len(stored.atomlist_chain)):
		#If this is a new chain...
		if (stored.atomlist_chain[atomidx] != curchain):
			#Reset the current chain.
			curchain = stored.atomlist_chain[atomidx]
			#Add a new chain identifier in the output sequence.
			if (out_seq != ''): out_seq = out_seq + '\n'
			out_seq = out_seq + "Chain " + curchain + ":\n"
			
			#Reset the curresi to an empty string to force a new residue.
			curresi = ''
			
		#If this is a new resi...
		if (stored.atomlist_resi[atomidx] != curresi):
			#Reset the current resi.
			curresi = stored.atomlist_resi[atomidx]
			#Generate the one-letter code of the residue.
			#If the residue is an unknown residue, make it 'X'
			if (stored.atomlist_resn[atomidx] not in oneletter):
				curletter = 'X'
			#Otherwise, get the value from the dictionary
			else:
				curletter = oneletter[stored.atomlist_resn[atomidx]]
				
			#Add the residue to the output sequence.
			out_seq = out_seq + curletter
	
	out_seq = out_seq + '\n'
	
	print(out_seq)
			

cmd.extend('get_sequence', get_sequence)
#Configure the seq_object argument to be a selection when tab completing.
cmd.auto_arg[0]['get_sequence'] = [ cmd.selection_sc, 'selection', ' ' ]