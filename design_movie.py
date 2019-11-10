from pymol import cmd
import random

def rand_sequence(selector, restypes = ['ALA','CYS','ASP','GLU','PHE','GLY','HIS','ILE','LYS','LEU','MET','ASN','PRO','GLN','ARG','SER','THR','VAL','TRP','TYR']):
	"""
DESCRIPTION

	The "rand_sequence" takes a selection and randomizes the amino acid identities in it.  Random rotamers are selected.
	
USAGE

	rand_sequence selector, restypes
	
ARGUMENTS

	selector = string: name of the selection to "design"
	restypes = list: Using three-letter codes, list the amino acid alphabet to use in "designing."  For example, to only allow Ser, Thr, or Tyr, use restypes = ['SER', 'THR', 'TYR'] .  Defaults to all 20 amino acids.
	
NOTES

	Any residues that do not contain a CA atom will be ignored.
	"""

	#Create lists to contain object, chain and resi info for each residue in selection.
	stored.atomlist_object = []
	stored.atomlist_chain = []
	stored.atomlist_resi = []
	#Populate the lists with all CA atoms in the selector.
	cmd.iterate('(' + selector + ') and name ca', 'stored.atomlist_object.append(model); stored.atomlist_chain.append(chain); stored.atomlist_resi.append(resi)')
	
	#Make a list of residue types
	#res_types = ['ALA','CYS','ASP','GLU','PHE','GLY','HIS','ILE','LYS','LEU','MET','ASN','PRO','GLN','ARG','SER','THR','VAL','TRP','TYR']
	
	#For each residue:
	#1. Select a random residue to mutate to.
	#2. Start the mutagenesis wizard interface.
	#3. Figure out how many backbone-dependent rotamers exist for that residue.
	#4. Select a random rotamer to mutate to.
	#5. Mutate to the desired residue.
	#6. Clean-up the wizard and make the mutation.
	for atomidx in range(len(stored.atomlist_resi)):
		curres = stored.atomlist_object[atomidx] + ' and chain ' + stored.atomlist_chain[atomidx] + ' and resi ' + stored.atomlist_resi[atomidx]
				
		#Pick a random residue type.
		newres = random.choice(restypes)
	
		#Set up the mutagenesis wizard.
		cmd.wizard('mutagenesis')
		cmd.refresh_wizard
		
		#Select the desired residue to mutate as (sele)
		cmd.select('sele','none')
		cmd.select('sele',curres)
	
		#Generate the library of backbone-independent rotamers.
		lib = cmd.get_wizard().ind_library.get(newres)
		
		print newres
		
		#Change the residue to the selected residue type
		cmd.get_wizard().do_select('''sele''')
		cmd.get_wizard().set_mode(newres)
		#If the residue is not GLY, pick a random rotamer and change to it.
		if (newres not in ('GLY', 'ALA')):
			newrot = random.randint(1,len(lib))
			cmd.get_wizard().do_state(newrot)
		#Apply the changes
		cmd.get_wizard().apply()
		#Clear the wizard
		cmd.get_wizard().clear()
		cmd.set_wizard()
						
cmd.extend('rand_sequence', rand_sequence)
#Configure the selector argument to be a selection when tab completing.
cmd.auto_arg[0]['rand_sequence'] = [ cmd.selection_sc, 'selection', ' ' ]

def design_movie(object, selector, frames, restypes = ['ALA','CYS','ASP','GLU','PHE','GLY','HIS','ILE','LYS','LEU','MET','ASN','PRO','GLN','ARG','SER','THR','VAL','TRP','TYR']):
	"""
DESCRIPTION

	The "design_movie" command makes a video of a simulated design protocol within a selection.
	
USAGE

	design_movie object, selector, frames, restypes
	
ARGUMENTS

	object = string: name of the object containing the "designed" selection
	selector = string: name of the selection to design.  Do not include the object name.
	frames = integer: the number of "designs" to make.
	restypes = list: Using three-letter codes, list the amino acid alphabet to use in "designing."  For example, to only allow Ser, Thr, or Tyr, use restypes = ['SER', 'THR', 'TYR'] .  Defaults to all 20 amino acids.
	
NOTES

	Here's my notes.
	"""
	
	#Loop over the number of frames we want.
	for frm in range(1,int(frames)+1):
		#Create a new object from selection.
		cmd.create('Design', object)
		#Make mutations in that new object.
		rand_sequence('Design and ' + selector, restypes)
		#Add the new object to the rosettify object as the next available state.
		cmd.create('rosettify', 'Design', target_state=-1)
		#Delete the Design object.
		cmd.delete('Design')
							
cmd.extend('design_movie', design_movie)
#Configure the selection argument to be a selection when tab completing.
cmd.auto_arg[0]['design_movie'] = [ cmd.selection_sc, 'selection', ' ' ]
