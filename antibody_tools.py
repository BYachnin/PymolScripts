# These are quick visualization tools for antibody and antibody-antigen structures.
from enum import Enum
from pymol import cmd


# Helper functions
# Returns a list of objects from a string.  "all" gives all objects, or multiple objects can be /-delimited.
def parse_object_list(object_string):
    # If the argument object is 'all', work on all objects.
    # If the argument object is a specific object that is already present, work on that.
    # Otherwise, assume it is a slash-delimited list and go from there.
    if object_string == "all":
        objects = cmd.get_object_list()
    elif object_string in cmd.get_object_list():
        objects = [object_string]
    else:
        objects = object_string.split('/')

    # Verify that all items in objects are current pymol objects
    if not all(obj in cmd.get_object_list() for obj in objects):
        raise Exception('One or more objects do not exist in your current PyMOL session.')

    return(objects)

# CDR Definitions
class NorthAHo(Enum):
    L1_START = '24'
    L1_END = '42'
    L2_START = '57'
    L2_END = '72'
    L3_START = '107'
    L3_END = '138'
    H1_START = '24'
    H1_END = '42'
    H2_START = '57'
    H2_END = '69'
    H3_START = '107'
    H3_END = '138'


# Pymol commands
def select_cdrs(object="all", heavy="H", light="L", cdr_def='North-Aho'):
    """
DESCRIPTION

	***
	
USAGE

	select_cdrs object
	
ARGUMENTS

	object = string: name of the object

NOTES


    """
    # Get the appropriate CDR definitions
    cdrs = {
        'NORTH-AHO': NorthAHo
    }

    # Figure out which objects to work on.
    objects = parse_object_list(object)

    # Verify that cdr_def is a supported CDR definition
    if not cdr_def.upper() in cdrs.keys():
        raise Exception('You specified an unsupported CDR definition.  Currently supported definitions include ' + str(
            list(cdrs.keys())))

    cdr = cdrs[cdr_def.upper()]

    for obj in objects:
        cmd.select(obj + "_H1", "chain {0} and resi {1}-{2}".format(heavy, cdr.H1_START.value, cdr.H1_END.value))
        cmd.select(obj + "_H2", "chain {0} and resi {1}-{2}".format(heavy, cdr.H2_START.value, cdr.H2_END.value))
        cmd.select(obj + "_H3", "chain {0} and resi {1}-{2}".format(heavy, cdr.H3_START.value, cdr.H3_END.value))
        cmd.select(obj + "_Hcdrs", "{0}_H1 or {0}_H2 or {0}_H3".format(obj))

        cmd.select(obj + "_L1", "chain {0} and resi {1}-{2}".format(light, cdr.L1_START.value, cdr.L1_END.value))
        cmd.select(obj + "_L2", "chain {0} and resi {1}-{2}".format(light, cdr.L2_START.value, cdr.L2_END.value))
        cmd.select(obj + "_L3", "chain {0} and resi {1}-{2}".format(light, cdr.L3_START.value, cdr.L3_END.value))
        cmd.select(obj + "_Lcdrs", "{0}_L1 or {0}_L2 or {0}_L3".format(obj))

        cmd.select(obj + "_allcdrs", "{0}_Lcdrs or {0}_Hcdrs".format(obj))


cmd.extend('select_cdrs', select_cdrs)
# Configure the object argument to be an object when tab completing.
cmd.auto_arg[0]['select_cdrs'] = [cmd.object_sc, 'object', ' ']


# Function to colour antibodies
def colour_antibody(object="all", heavy_col="orange", light_col="yellow", h1="", h2="", h3="", l1="", l2="", l3="",
                    heavy="H", light="L", cdr_def="North-Aho"):
    """
DESCRIPTION

    ***

USAGE

    select_cdrs object

ARGUMENTS

    object = string: name of the object

NOTES


    """

    # First, figure out which objects to process
    objects = parse_object_list(object)

    # We will use select_cdrs to generate the appropriate selections.  This will also automatically error check in
    # the same way, so we don't have to do it again.  Pass through params.
    select_cdrs(object=object, heavy=heavy, light=light, cdr_def=cdr_def)

    # Loop over all objects to colour
    for obj in objects:
        # For all colouring, skip if we have an empty string.
        # First, colour the chains.
        if not heavy_col == "": cmd.color(heavy_col, "elem c and chain {0} and {1}".format(heavy, obj))
        if not light_col == "": cmd.color(light_col, "elem c and chain {0} and {1}".format(light, obj))

        # Now, colour the cdrs
        if not h1 == "": cmd.color(h1, "elem c and {}_H1".format(obj))
        if not h2 == "": cmd.color(h2, "elem c and {}_H2".format(obj))
        if not h3 == "": cmd.color(h3, "elem c and {}_H3".format(obj))
        if not l1 == "": cmd.color(l1, "elem c and {}_L1".format(obj))
        if not l2 == "": cmd.color(l2, "elem c and {}_L2".format(obj))
        if not l3 == "": cmd.color(l3, "elem c and {}_L3".format(obj))

cmd.extend('colour_antibody', colour_antibody)
# Configure the object argument to be an object when tab completing.
cmd.auto_arg[0]['colour_antibody'] = [cmd.object_sc, 'object', ' ']