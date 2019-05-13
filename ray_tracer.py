from pymol import cmd
	
def ray_tracer (width, height, scenes = "all", ray = 1, directory = ""):
	"""
	ray_tracer will call png for scenes in a pymol session.  All these scenes will be
	produced with the same dimensions.  By default, all scenes are generated with ray
	tracing turned on in the current directory.  Files will be named the same as their
	scene names.
	
	width, height = The width and height in pixels of the resulting images.
	scenes = A scene or pythonic list of scenes to raytrace (e.g. "scene1" or ["scene1", "scene2"]).  By default, do all scenes.
	raytrace = Should we raytrace?  Passed on to ray in png command.
	directory = By default, images will be saved in the current directory.  A relative path can be given
		here for a different directory to be used.
	"""
	
	#Check if 'all' happens to be a scene name.  If so, print an error message and quit.
	assert !("all" in cmd.get_scene_list()), "You have 'all' as a scene name.  This causes a conflict with ray_tracer.  Change the scene name."
	
	#The directory name must end in a forward / (unless it is an empty string).  If it doesn't, add one for the user
	if (directory != "" and directory[-1:] != "/"): directory = directory + "/"
	
	#Figure out which scenes to png
	#if scenes == all, get all scenes and use that as our list.
	if (scenes == 'all'): scene_list = cmd.get_scene_list()
	#if scenes is a list object, use that as our list.
	elif (isinstance(scenes, list): scene_list = scenes
	#Otherwise, assume we have a string that corresponds to a scene name
	else: scene_list = ["scenes"]
	
	#scene_list should now have a list of all the scenes to render.
	#Loop over scene_list and cmd.png each one.
	for scene in scene_list:
		#Check that the scene actually exists, or spit out an error.
		if !(scene in cmd.get_scene_list()):
			print("The scene " + scene + " is not a scene in your pymol environment.  Skipping.")
			continue
			
		#Change to the appropriate scene.
		cmd.scene(scene)
		#Figure out the full name of the output file.
		imgname = directory + scene + ".png"
		
		#Actually make the image.
		cmd.png(filename = imgname, width = width, height = height, ray=ray)

cmd.extend("ray_tracer", ray_tracer);