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
cmd.do("run https://raw.githubusercontent.com/BYachnin/PymolScripts/master/ray_tracer.py")
cmd.do("run https://raw.githubusercontent.com/BYachnin/PymolScripts/master/antibody_tools.py")

#Try to set up a pyrosetta link
import sys,os
main_to_pyrsrv = '/source/src/python/PyRosetta/src/' # How to get from main to the location of the PyMOL-RosettaServer files

#Figure out if we should use the python2 or python3 version
if sys.version_info[0] == 2:
    pyr_scpt = "PyMOL-RosettaServer.py"
elif sys.version_info[0] == 3:
    pyr_scpt = "PyMOL-RosettaServer.python3.py"

#Check the environment variables for Rosetta
pyr_scpt_path = None
if 'ROSETTA' in os.environ:
    pyr_scpt_path = os.environ['ROSETTA'] + '/main' + main_to_pyrsrv
elif 'ROSDB' in os.environ:
    pyr_scpt_path = os.environ['ROSDB'] + '/..' + main_to_pyrsrv
elif 'ROSETTA3_DB' in os.environ:
    pyr_scpt_path = os.environ['ROSETTA3_DB'] + '/..' + main_to_pyrsrv

#If we have a route to the PyMOL-RosettaServer files and we can find a file at that location
if pyr_scpt_path and os.path.exists(pyr_scpt_path + pyr_scpt):
    #Run the script in PyMOL
    cmd.do("run " + pyr_scpt_path + pyr_scpt)

#End of pyrosetta link stuff
