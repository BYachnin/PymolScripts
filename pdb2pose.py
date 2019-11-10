#This function will return the Rosetta pose number for residues in a selection, if the object were saved to a PDB file.
#This will be determined based on the object that contains the selection.
#When determining pose numbering, residues with only hydrogens will be ignored, as will HOH or WAT.
#Strange multiple states, residue ordering, segis, and chains could result in unusual behaviour.

from pymol import cmd

def pdb2pose(poseres):
	"""
DESCRIPTION

	The "pdb2pose" command returns the Rosetta-style pose number of a selection of residues.
	
USAGE

	pdb2pose poseres
	
ARGUMENTS

	poseres = string: selection with the residues to process.
	
NOTES

	A selection that spans multiple objects is unsupported, and will produce an error.
	The pose numbering returned will be for the current version of the object.  Adding, removing, re-ordering, or sorting residues will alter the pose number.
	Multi-state selections may yield unexpected results.
	If the selection has different chain IDs and segids, this may also result in unexpected chain ordering.
	Residues containing only hydrogen atoms and water molecules will be ignored.
	"""
	
	#Determine what object contains the selection.
	poseobj = cmd.get_object_list(poseres)
	#Assert that the selection must be in a single object
	assert (len(poseobj) == 1), "Your selection spans multiple objects (or no objects).  Select one object only."
	
	#Count the number of residues in the selection.
	#First, set up a get_model object.
	selemodel = cmd.get_model(poseres)
	#Iterate over all atoms in selemodel, storing chain and resi in a list called atomlist.
	atomlist = []
	for curatom in selemodel.atom:
		atomlist.append(str(curatom.resi) + curatom.chain)
	#Remove duplicates by making converting atomlist to a set then a list.
	atomlist = list(set(atomlist))
	
	#atomlist should now have one instance of each residue in pdb numbering format (ie. 35A).
	
	#We now need to iterate over the poseobj.  Start counting at 1.  If we encounter a new residue, iterate counter.

	#First, store lists of chain and resi for the object in atomlist_chain, atomlist_resi, and atomlist_resn
	stored.atomlist_chain = []
	stored.atomlist_resi = []
	cmd.iterate(poseobj[0] + ' and not elem H and not resn HOH and not resn WAT', 'stored.atomlist_chain.append(chain); stored.atomlist_resi.append(resi)')
	
	#Set up a tracking variable for chain and resi.
	curchain = ''
	curresi = ''
	
	#Set up a pose number variable.
	posenum = 0
	
	#Iterate over all indecies in the atomlist series.  Using atomlist_chain because they are all the same.
	for atomidx in range(len(stored.atomlist_chain)):
		#If this is a new chain or new resi...
		if (stored.atomlist_chain[atomidx] != curchain or stored.atomlist_resi[atomidx] != curresi):
			#Reset the current chain and resi
			curchain = stored.atomlist_chain[atomidx]
			curresi = stored.atomlist_resi[atomidx]
			#Increment the posenum
			posenum = posenum + 1

			#Check if the current chain and resi are in atomlist.
			if (str(curresi) + curchain in atomlist):
				print("The pose number for residue " + str(curresi) + curchain + " is " + str(posenum) + ".\n")
			

cmd.extend('pdb2pose', pdb2pose)
#Configure the seq_object argument to be a selection when tab completing.
cmd.auto_arg[0]['pdb2pose'] = [ cmd.selection_sc, 'selection', ' ' ]