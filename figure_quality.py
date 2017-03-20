def figquality(colspace='rgb'):

	util.performance(0)
	cmd.set('ray_trace_fog', 0)
	cmd.set('antialias', 1.0)
	cmd.set('specular', 1)
	cmd.set('depth_cue', 0)
	cmd.set('cartoon_fancy_helices', 1)
	util.ray_shadows('none')
	cmd.set('mesh_radius', 0.02)
	cmd.set('bg_rgb', [1, 1, 1])
	cmd.set('ray_opaque_background', 0)
	cmd.set('transparency_mode',2)
	cmd.set('backface_cull',0)
	cmd.set('two_sided_lighting',1)
	cmd.set('''cache_frames''','''0''',quiet=0)
	cmd.space(colspace)

cmd.extend("figquality", figquality)

def moviemode():

	cmd.set("scene_buttons", 1)
	cmd.set("movie_panel", 1)
	cmd.set("matrix_mode", 1)
	cmd.set("cache_frames", 1)
	cmd.set("cache_display", 1)
	cmd.set('ray_opaque_background', 1)
	
cmd.extend("moviemode", moviemode)