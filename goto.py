from pymol import cmd

def goto(pathname):
    path_select = {
        "drive": "E:\Users\Brahm\Documents\Google Drive",
        "design": "E:\Users\Brahm\Documents\Google Drive\design",
        "pdbs": "E:\Users\Brahm\Documents\Google Drive\PDB Files",
        "dropbox": "E:\Users\Brahm\Documents\Dropbox"
    }
    
    os.chdir(path_select.get(pathname, "."))
    print "Changing to the following directory:"
    print path_select.get(pathname, ".")

cmd.extend("goto",goto)
