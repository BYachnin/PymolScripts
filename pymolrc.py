#start_dir = os.getcwd()
cmd.set("cartoon_fancy_helices", 1)
cmd.set("ignore_case", 1)
cmd.set("ignore_case_chain", 1)

#Dropbox scripts
#cd E:
#run \Users\Brahm\Documents\Dropbox\pymol\seq_diff.py
#run \Users\Brahm\Documents\Dropbox\pymol\goto.py
#run \Users\Brahm\Documents\Dropbox\pymol\modevectors.py
#run \Users\Brahm\Documents\Dropbox\pymol\figure_quality.py
#run \Users\Brahm\Documents\Dropbox\pymol\rcinit.py

#os.chdir(start_dir)

cmd.do("run https://raw.githubusercontent.com/BYachnin/PymolScripts/master/seq_diff.py")
cmd.do("run https://raw.githubusercontent.com/BYachnin/PymolScripts/master/goto.py")
cmd.do("run https://raw.githubusercontent.com/BYachnin/PymolScripts/master/modevectors.py")
cmd.do("run https://raw.githubusercontent.com/BYachnin/PymolScripts/master/figure_quality.py")
cmd.do("run https://raw.githubusercontent.com/BYachnin/PymolScripts/master/rcinit.py")
cmd.do("run https://raw.githubusercontent.com/BYachnin/PymolScripts/master/get_sequence.py")
cmd.do("run https://raw.githubusercontent.com/BYachnin/PymolScripts/master/pdb2pose.py")
cmd.do("run https://raw.githubusercontent.com/BYachnin/PymolScripts/master/color_by_restype.py")
cmd.do("run https://raw.githubusercontent.com/BYachnin/PymolScripts/master/design_movie.py")
cmd.do("run https://raw.githubusercontent.com/BYachnin/PymolScripts/master/loadBfacts.py")