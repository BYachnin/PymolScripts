# These are quick visualization tools for antibody and antibody-antigen structures.

from pymol import cmd

#Helper functions


#CDR Definitions
#class North-Aho(Enum):
#    L1_START =

#Pymol commands
def select_cdrs(object = "all"):
    """
DESCRIPTION

	***
	
USAGE

	select_cdrs object
	
ARGUMENTS

	object = string: name of the object

NOTES


    """
    #Figure out which objects to work on.
    #If the argument object is 'all', work on all objects.
    #If the argument object is a specific object that is already present, work on that.
    #Otherwise, assume it is a comma-delimited list and go from there.
    if object == "all":
        objects = cmd.get_object_list()
    elif object in cmd.get_object_list():
        objects = [object]
    else:
        objects = ",".split(object)

    print(object)
    print(objects)
    for obj in objects:
        cmd.select(obj + "_H1", "chain H and resi 24-42")
        cmd.select(obj + "_H2", "chain H and resi 57-69")
        cmd.select(obj + "_H3", "chain H and resi 107-138")
        cmd.select(obj + "_Hcdrs", "{0}_H1 or {0}_H2 or {0}_H3".format(obj))

        cmd.select(obj + "_L1", "chain L and resi 24-42")
        cmd.select(obj + "_L2", "chain L and resi 57-72")
        cmd.select(obj + "_L3", "chain L and resi 107-138")
        cmd.select(obj + "_Lcdrs", "{0}_L1 or {0}_L2 or {0}_L3".format(obj))

cmd.extend('select_cdrs', select_cdrs)
# Configure the seq_object argument to be a selection when tab completing.
# cmd.auto_arg[0]['get_sequence'] = [cmd.selection_sc, 'selection', ' ']
