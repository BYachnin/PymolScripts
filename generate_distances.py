from pymol import cmd

def generate_distances(obj1, startres, endres, atname, filename="", resi_offset=0):
    if (filename != ""):
        file = open(filename, 'w')
    for first_res_iterate in range(int(startres), int(endres)):
        for second_res_iterate in range(int(first_res_iterate)+1, int(endres)+1):
            mydist=cmd.get_distance(atom1=obj1 + " and resi " + str(first_res_iterate) + " and name " + atname, atom2=obj1 + " and resi " + str(second_res_iterate) + " and name " + atname)
            print str(first_res_iterate) + " " + str(second_res_iterate) + " " + str(mydist)
            if (filename != ""):
                file.write("AtomPair " + atname + " " + str(int(first_res_iterate)+int(resi_offset)) + " " + atname + " " + str(int(second_res_iterate)+int(resi_offset)) + " HARMONIC " + str(mydist) + " " + str(2) + "\n")
            
    if (filename != ""):
        file.close()
        
cmd.extend("generate_distances", generate_distances)