from pymol import cmd
import platform

if (platform.node() == "BrahmL"):
	def goto(pathname):
		path_select = {
			"drive": r"E:\Users\Brahm\Documents\Google Drive",
			"design": r"E:\Users\Brahm\Documents\Google Drive\design",
			"pdbs": r"E:\Users\Brahm\Documents\Google Drive\PDB Files",
			"dropbox": r"E:\Users\Brahm\Documents\Dropbox"
		}
    
		os.chdir(path_select.get(pathname, "."))
		print("Changing to the following directory:")
		print(path_select.get(pathname, "."))

	cmd.extend("goto",goto)

if (platform.node() == "Brahm"):
	def goto(pathname):
		path_select = {
			"drive": r"D:\Users\Brahm Yachnin\Documents\Google Drive",
			"design": r"D:\Users\Brahm Yachnin\Documents\Google Drive\design",
			"pdbs": r"D:\Users\Brahm Yachnin\Documents\Google Drive\PDB Files",
			"dropbox": r"D:\Users\Brahm Yachnin\Documents\Dropbox"
		}
    
		os.chdir(path_select.get(pathname, "."))
		print("Changing to the following directory:")
		print(path_select.get(pathname, "."))

	cmd.extend("goto",goto)