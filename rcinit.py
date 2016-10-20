import platform

def rcinit():

	cmd.reinitialize()
	#start_dir = os.getcwd()
	
	
	cmd.do("@https://raw.githubusercontent.com/BYachnin/PymolScripts/master/pymolrc.pml")
	
	#os.chdir(start_dir)
	return
	
cmd.extend("rcinit",rcinit)
