# These are quick visualization tools for antibody and antibody-antigen structures.
from enum import Enum
from pymol import cmd

#Helper functions


#CDR Definitions
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

#Pymol commands
def select_cdrs(object = "all", heavy="H", light="L", cdr_def = 'North-Aho'):
    """
DESCRIPTION

	***
	
USAGE

	select_cdrs object
	
ARGUMENTS

	object = string: name of the object

NOTES


    """
    #Get the appropriate CDR definitions
    cdrs = {
        'NORTH-AHO': NorthAHo
    }

    #Figure out which objects to work on.
    #If the argument object is 'all', work on all objects.
    #If the argument object is a specific object that is already present, work on that.
    #Otherwise, assume it is a slash-delimited list and go from there.
    if object == "all":
        objects = cmd.get_object_list()
    elif object in cmd.get_object_list():
        objects = [object]
    else:
        objects = object.split('/')

    #Verify that all items in objects are current pymol objects
    if not all( obj in cmd.get_object_list() for obj in objects ):
        raise Exception('One or more objects do not exist in your current PyMOL session.')

    #Verify that cdr_def is a supported CDR definition
    if not cdr_def.upper() in cdrs.keys():
        raise Exception('You specified an unsupported CDR definition.  Currently supported definitions include ' + str(list(cdrs.keys()))  )

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

