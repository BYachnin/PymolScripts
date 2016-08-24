from pymol import cmd

def goto(pathname):
    path_select = {
        "drive": "D:\Users\Brahm Yachnin\Documents\Google Drive",
        "design": "D:\Users\Brahm Yachnin\Documents\Google Drive\design",
        "pdbs": "D:\Users\Brahm Yachnin\Documents\Google Drive\PDB Files",
        "dropbox": "D:\Users\Brahm Yachnin\Documents\Dropbox"
    }
    
    os.chdir(path_select.get(pathname, "."))
    print "Changing to the following directory:"
    print path_select.get(pathname, ".")

cmd.extend("goto",goto)
