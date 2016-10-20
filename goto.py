from pymol import cmd
import platform

if (platform.node() == "BrahmL"):
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

if (platform.node() == "Brahm"):
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