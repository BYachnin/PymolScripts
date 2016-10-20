import platform

def rcinit():

	cmd.reinitialize()
	#start_dir = os.getcwd()
	
	
	cmd.do("run https://raw.githubusercontent.com/BYachnin/PymolScripts/master/pymolrc.py")
	
	#os.chdir(start_dir)
	return
	
cmd.extend("rcinit",rcinit)
