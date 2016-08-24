def rcinit():

	cmd.reinitialize()
	#start_dir = os.getcwd()
	
	cmd.run("C:/Users/brahm/pymolrc.pml")
	
	#os.chdir(start_dir)
	return
	
cmd.extend("rcinit",rcinit)