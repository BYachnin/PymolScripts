#A* -------------------------------------------------------------------
#B* This file contains source code for the PyMOL computer program
#C* copyright 1998-2000 by Warren Lyford Delano of DeLano Scientific. 
#D* -------------------------------------------------------------------
#E* It is unlawful to modify or remove this copyright notice.
#F* -------------------------------------------------------------------
#G* Please see the accompanying LICENSE file for further information. 
#H* -------------------------------------------------------------------
#I* Additional authors of this source file include:
#-*     Kristian Rother
#-*     (www.rubor.de)
#-*     (kristian.rother@charite.de)
#Z* -------------------------------------------------------------------

#  This is a modified version created by Seth Harris (sharris@msg.ucsf.edu) and includes
#  code submitted by Laurency Pearl as well.

MOVIE_HELP_TEXT="""
--- rMovie: easy movie scripting in PyMOL ---
Script  : rMovie
Author  : Kristian Rother 
Date    : 16.7.2003
Version : 0.6
Contact : kristian.r@gmx.de

Copyright (C) 2002 K. Rother

Movie is an extension for the PyMOL Molecular Graphics System.

Movie for PyMOL facilitates creation of high-quality animations. Translation, rotation and other commands can be assigned to frame ranges, resulting in a much shorter scripting of animations. Additionaly, smooth movements are enabled.

It is assumed that you have already gathered experience with the standard PyMOL animation commands, or are at least familiar with the 'frame' and 'state' concepts.

Most movie commands will require a frame/state range assigned to a specific action. Thus, you dont have to worry about how to use the mset command correctly. Just say what you want to see.

Frames can be specified to cover individual frames, states or ranges of both. The frame ranges of several commands may very well overlap (with states, this is more difficult - not tested).

Examples of frame/state ranges:
    1-10       # frame 1 to 10
    10         # frame 10 only
    1-100:1-10 # multiple states are looped through
    1-100:5    # one state only
    1:8        # state no.8 in frame no.1
    1:1-10     # this is crap, don't know what happens
    200-1      # same
    1-50:10-5  # same


The following new commands are provided:

    *

mvMove(frames,axis,totalDistance) 

   Moves the environment over the given frame range, 
   the moved distance summing up to the totalDistance given.
   Example     : mvMove 20-40,x,80
   Description : in frames 20 to 40, the molecule will be shifted to the right,
                 by a total of 80 Angstroms or 2 Angstrom per frame.

    *

mvTurn frames,axis,totalAngle

   Turns the world over the given frame range, 
   the rotation angle summing up to the totalAngle given.
   Example     : mvTurn 10-200,x,90
   Description : in frames 10 to 200, the world will be turned 90 degrees
                 around its X axis.

    *

mvRot(frames,object,axis,totalAngle) 

   Rotates the object over the given frame range, 
   the rotation angle summing up to the totalAngle given.
   Example     : mvRot 1-100,heavych,z,180
   Description : rotates the heavych object about the z axis by 180 degrees in the
                first 100 frames.

    *

mvSet(frames,variable,startValue,endValue) 

   Applies a gradient to a PyMOL variable in the specified frame range. 
   Example     : mvSet 1-20,transparency,1.0,0.0
   Description : lets the surface gracefully fade in!

    *

mvCmd(frames,command) 

   Executes a command in all frames specified.
   Example     : mvCmd 10,orient
   Description : Moves the view to its original position in frame 10.

    *

mvSinrot(), mvSinmove(), mvSinturn(), mvSinset() 

   They work exactly like mvRot, mvMove, mvTurn and mvSet but
   a trigonometric function is used to calculate the incremental steps 
   applied to each frame. This produces very smooth movements, which is
   especially useful when several movements are overlapping.

    *

mvGradCol(frames,object,R1,G1,B1,R2,G2,B2)

   Over the given frame range, the color of the selection object is
   faded gradually from the RGB value set '1' to '2'.

    *
    
movie()

   Assembles and plays a movie that has been specified by the other
   commands. This is always the last command used.

    *

mvClear()

   Clears everything entered previously.

    *

pngseq(path [,ray])

   Sets a path for creating a PNG file for each frame while playing the movie. A value for ray > 0 lets each frame being raytraced. When pngseq has been issued, the movie will run only once (for the sake of your harddisk).
   Example     : pngseq movies/movie1/,1
   Description : will create raytraced png images for each frame when the movie starts.

And Seth (and Morri) have incorporated Laurence Pearl's camera_view_travel to make:

mvViewTravel(frames,startview,endview)
	
	interpolate between startview and endview over the given frames
	
mvSinViewTravel(frames,startview,endview)

	as above but done in a sin smoothed motion
	
storeview(name)

	writes a view to a file called "name" 
	
ribbon_ride (selection, framesperresidue, zbuffer, halfslab, frequency)
	
	"flies" through a structure visiting every "frequency"th alpha carbon using the
	mvViewTravel command to interpolate between the views at a speed of framesperresidue
	and at a viewpoint backed off by the zbuffer command.
	defaults are something like selection of "mol", zbuffer of 30, 20 framesperresidue, 
	and visiting each alpha carbon (frequency=1)

peak_tour (selection, zoom_buffer, frames_per_move, stall_frames)

	goes through a selection of peaks (or waters, or whatever), visiting each atom
	in turn and doing a little dance at each stop.  Handy for visiting waters or potential
	waters

"""
MOVIE_SHORT_HELP_TEXT="""
--- rMovie: easy movie scripting in PyMOL ---
Copyright (C) 2002 K. Rother

Examples for frames/states:
    10         # frame 10 only
    20-199     # frame 20 to 199
    1-100:5    # state 5 only
    1-100:1-10 # multiple states are looped through

mvTurn frames,totalAngle  - Turns the world over the given frame range.
mvRot  frames,object,axis,totalAngle    - Rotates the object over the given frame range.
mvMove frames,axis,totalDistance - Moves the environment over the given frame range.
mvSet  frames,variable,start,end - Applies a gradient to a PyMOL variable.
mvSinrot, mvSinmove, mvSinTurn mvSinset    - Like above but with trigonometric smoothing.
mvCmd  frames,command            - Executes a command in all frames specified.
mvGradCol frames,color,R1,G1,B1,R2,G2,B2 - fades a color gradually.
movie                            - Assembles and plays a movie.
mvClear                          - Clears everything entered previously.
pngseq path [,ray]               - Writes out png files for each frame.
"""

from pymol import cmd
import string,os,re
from math import *

def __init__(self):
    # define a set of new PyMOL commands for creation of movies
    cmd.extend('movie',movie)
    cmd.extend('mvClear',mvClear) # clear cached instructions
    cmd.extend('mvRot',mvRot)     # rotate over frame range
    cmd.extend('mvMove',mvMove)   # move over frame range
    cmd.extend('mvTurn',mvTurn)   # turn over frame range
    cmd.extend('mvCmd',mvCmd)     # do anything during a frame range
    cmd.extend('mvSet',mvSet)     # adjust parameter over frame range
    cmd.extend('mvSinrot',mvSinrot)   # rotate smoothly
    cmd.extend('mvSinmove',mvSinmove) # move smoothly
    cmd.extend('mvSinturn',mvSinturn) # turn smoothly 
    cmd.extend('mvSinset',mvSinset)   # set smoothly
    cmd.extend('pngseq',pngseq)
    cmd.extend('mvGradCol',mvGradCol)
    cmd.extend('mvSinViewTravel',mvSinViewTravel)
    cmd.extend('mvViewTravel',mvViewTravel)
    
def help():
    print MOVIE_SHORT_HELP_TEXT

class mvMovie:    
    def __init__(self):
        """Stores data of what should appear in the movie."""
        self.movie=[]
        self.maxframe = 1
        self.framestates = {}
        self.pngPath=""
        self.ray=0

    def addFrameStates(self, framestates):
        """Stores list of (frame,state) tuples in a dictionary."""
        for fs in framestates:
            self.framestates[str(fs[0])] = fs[1]

    def getState(self,frame):
        key = str(frame)
        if self.framestates.has_key(key):
            return self.framestates[key]
        else:
            return 1 # state one, if none specified            

mv = mvMovie()

# ---------------------------------------------------------
# internal stuff

def getFrameStates(fstring):
    """Returns a list of (frame,state) tuples parsed from a string like
    1-10       # frame 1 to 10, state 1
    10         # frame 10 only
    1-100:1-10 # multiple states are looped through
    1-100:5    # one state only
    1-50:10-5  # reverse order is ok, too
    1:8        # state no.8 in frame no.1
    1:1-10     # this is crap, don't know what happens
    """

    t=string.split(fstring,":")
    frames=t[0] # the first token is frame range
    if len(t)==2: states = t[1] # the second token is state range
    else: states='1' # only state number 1 is used

    # parse frame substring
    t=string.split(frames,"-")
    firstFrame=int(t[0]) # first token is starting frame
    if len(t)==2: lastFrame=int(t[1]) # second token is end frame
    else: lastFrame = firstFrame # only one frame is used
    
    # parse state substring
    t=string.split(states,"-")
    firstState=int(t[0]) # first token is starting state
    if len(t)==2: lastState=int(t[1]) # second token is end state
    else: lastState = firstState # only one state is used

    # compile list of frames/states
    framestates = []
    if lastFrame == firstFrame or lastFrame < firstFrame:
        framestates.append((firstFrame,firstState))
        lastFrame = firstFrame
    else:
        stateinc = (lastState - firstState) * 1.0 / (lastFrame-firstFrame)
        for i in range(lastFrame - firstFrame): 
            frame = firstFrame + i            
            state = firstState + int(stateinc * i)
            framestates.append((frame,state))

    # put values into mv for compiling the movie later
    if mv.maxframe < lastFrame: mv.maxframe = lastFrame
    mv.addFrameStates(framestates)
    
    # print framestates
    return framestates

# -------------------------------------
# here come the commands

def mvClear():
    """Deletes the movie."""
    mv.movie=[]
    cmd.mclear()
    cmd.frame(1)
    mv.ray=0
    mv.pngPath=""
    mv.maxframe = 1


def pngseq(path="."+os.sep,ray=0):
    """Sets a path for creating a PNG sequence while playing the movie.
    Ray lets raytrace each frame.
    """    
    mv.pngPath=path
    if mv.pngPath[-1]!=os.sep:
        mv.pngPath=mv.pngPath+os.sep
    mv.ray=ray


def mvGradCol(frames="1",selection="",startR="1.0",startG="1.0",startB="1.0",endR="0.0",endG="0.0",endB="0.0"):
    """
    mvGradCol(frames,selection,R1,G1,B1,R2,G2,B2) - changes colour gradually from (R1,G1,B1) to (R1,G1,B1) through the specified frame range and on the specified selection.
    """
    # provided by Tserk Wassenaar 2003
    tmpc="_temp_color"
    # fix by Gabe Lander to make mvGradCol allow coloring different selections differently
    """
Don't know if anyone's caught this already, but I noticed that if you use the "mvGradCol" function to color 2 different sections of a pdb 2 different colors at once, both will be colored the same.
Making the "tmp_color" variable dynamic fixes this by just changing one line:
    """
    tmpc="_%s_color"%(selection)
    framestates = getFrameStates(frames)
    nFrames = len(framestates)
    
    stRV=float(startR)
    endRV=float(endR)
    incR = (endRV-stRV)/(1.0*nFrames)
    stGV=float(startG)
    endGV=float(endG)
    incG = (endGV-stGV)/(1.0*nFrames)
    stBV=float(startB)
    endBV=float(endB)
    incB = (endBV-stBV)/(1.0*nFrames)

    j=0
    for fs in framestates:
        mv.movie.append((fs[0],fs[1],"set_color %s,[ %f,%f,%f ]"%(tmpc,stRV+j*incR,stGV+j*incG,stBV+j*incB)))
        mv.movie.append((fs[0],fs[1],"color %s, %s"%(tmpc,selection)))
        j=j+1


def mvTurn(frames="1",axis="z",totalAngle=360):
    """
    mvTurn(frames,axis,totalAngle) - rotates the environment over the given
       frame range, the rotation angle summing up to the totalAngle given.
       """    
    framestates = getFrameStates(frames)
    nFrames = len(framestates)
    angleIncrement = float(totalAngle)/(1.0*nFrames)

    for fs in framestates:
        mv.movie.append((fs[0],fs[1],"turn %s,%f"%(axis,angleIncrement)))


def mvRot(frames="1",object="all",axis="z",totalAngle=360):
    """
    mvRot(frames,object,axis,totalAngle) - rotates the object over the given
       frame range, the rotation angle summing up to the totalAngle given.
       """    
    framestates = getFrameStates(frames)
    nFrames = len(framestates)
    angleIncrement = float(totalAngle)/(1.0*nFrames)

    for fs in framestates:
        mv.movie.append((fs[0],fs[1],"rotate %s,%f,%s"%(axis,angleIncrement,object)))


def mvMove(frames="1",axis="x",totalDistance="0"):
    """
    mvMove(frames,axis,totalDistance) - moves the environment over the given
       frame range, the moved distance summing up to the totalDistance given.
       """    
    framestates = getFrameStates(frames)
    nFrames = len(framestates)
    distanceIncrement = float(totalDistance)/(1.0*nFrames)

    for fs in framestates:
        mv.movie.append((fs[0],fs[1],"move %s,%f"%(axis,distanceIncrement)))

           
def mvCmd(frames="1",command=""):
    """
    mvCmd(frames,command) - executes a command in all frames specified.
       """    
    framestates = getFrameStates(frames)
    nFrames = len(framestates)

    for fs in framestates:
        mv.movie.append((fs[0],fs[1],command))


def mvSet(frames="1",variable="",object="all",startValue="0.0",endValue="1.0"):
    """
    mvSet(frames,variable,selection,startValue,endValue) - lets a variable go through a gradient in the specified frame range. Great for fading effects!
       """    
    framestates = getFrameStates(frames)
    nFrames = len(framestates)

    stV=float(startValue)
    endV=float(endValue)
    increment = (endV-stV)/(1.0*nFrames)

    j=0
    for fs in framestates:
        mv.movie.append((fs[0],fs[1],"set %s,%f,%s"%(variable,stV+j*increment,object)))
        j=j+1


def mvSinturn(frames="1",axis="z",totalAngle=360):
    """
    mvSinturn(frames,axis,totalAngle) - rotates the environment over the
       given frame range, the angles summing up to the totalAngle given.
       The incremental steps will be calculated with the sinus function to
       make the rotation smoother.
       """    
    framestates = getFrameStates(frames)
    nFrames = len(framestates)
    angle = float(totalAngle)
    arcIncrement=pi/(1.0*nFrames)
    
    j=1
    prev=1.0
    for fs in framestates:
        arc=cos(j*arcIncrement)
        # print arc,"  *   ",abs(arc-prev)*0.5
        angleIncrement=angle*abs(arc-prev)*0.5
        mv.movie.append((fs[0],fs[1],"turn %s,%f"%(axis,angleIncrement)))
        prev=arc
        j=j+1

def mvSinrot(frames="1",object='all',axis="z",totalAngle=360):
    """
    mvSinrot(frames,axis,totalAngle) - rotates the object over the
       given frame range, the angles summing up to the totalAngle given.
       The incremental steps will be calculated with the sinus function to
       make the rotation smoother.
       """    
    framestates = getFrameStates(frames)
    nFrames = len(framestates)
    angle = float(totalAngle)
    arcIncrement=pi/(1.0*nFrames)
    
    j=1
    prev=1.0
    for fs in framestates:
        arc=cos(j*arcIncrement)
        # print arc,"  *   ",abs(arc-prev)*0.5
        angleIncrement=angle*abs(arc-prev)*0.5
        mv.movie.append((fs[0],fs[1],"rotate %s,%f,%s"%(axis,angleIncrement,object)))
        prev=arc
        j=j+1

def mvSinmove(frames="1",axis="x",totalDistance="0"):
    """
    mvSinmove(frames,axis,totalDistance) - moves the environment over the given
       frame range, the moved distance summing up to the totalDistance given.
       The incremental steps will be calculated with the sinus function to
       make the movement smoother.
       """    
    framestates = getFrameStates(frames)
    nFrames = len(framestates)
    dist = float(totalDistance)
    arcIncrement=pi/(1.0*nFrames)
    
    j=1
    prev=1.0
    for fs in framestates:
        arc=cos(j*arcIncrement)
        # print arc,"  *   ",abs(arc-prev)*0.5
        distanceIncrement=dist*abs(arc-prev)*0.5
        mv.movie.append((fs[0],fs[1],"move %s,%f"%(axis,distanceIncrement)))
        prev=arc
        j=j+1
    
def mvSinset(frames="1",variable="",startValue="0.0",endValue="1.0",option=""):
    """
    mvSet(frames,variable,startValue,endValue) - lets a variable go through
    a gradient in the specified frame range. Great for fading effects!
    The incremental steps will be calculated with the sinus function to
    make the movement smoother.
    """        
    framestates = getFrameStates(frames)
    nFrames = len(framestates)
    arcIncrement=pi/(1.0*nFrames)
    stV=float(startValue)
    endV=float(endValue)
    
    j=1
    prev=1.0
    sum=0.0
    for fs in framestates:
        arc=cos(j*arcIncrement)
        increment=(endV-stV)*abs(arc-prev)*0.5
        sum=sum+increment
        mv.movie.append((fs[0],fs[1],"set %s,%f,%s"%(variable,stV+sum,option)))
        prev=arc
        j=j+1


def movie():
    """Creates the movie and plays it."""
    cmd.frame(1) # reset frame counter
    
    nFrames=mv.maxframe

    # compile list of molecule states
    states=[]
    for n in range(nFrames):
        states.append(mv.getState(n+1))

    # compile mset command string "1 2 3 4 x3 5" from state list [1,2,3,4,4,4,5]
    statelist=""
    n=0
    count=0     
    while n<nFrames:
        actual=states[n]
        next=0
        if n<nFrames-1:
            next=states[n+1]
        if next==actual:
            count=count+1
        else:
            if count>0:
                statelist=statelist+"%s x%i "%(actual,count+1)
            else:
                statelist=statelist+"%s "%(actual)
            count=0
        n=n+1
            
    # Specify movie length
    print "creating movie with %i frames."%(nFrames)
    # cmd.mset("1 x%i"%(nFrames)) # earlier, without state support
    cmd.mset(statelist)

    # create empty frame-2do-lists
    do=["zero frame is unused"]
    for i in range(nFrames):
        do.append("")

    # push all movie commands to the 2do-list
    for m in mv.movie:
        do[m[0]]=do[m[0]]+m[2]+";"
    
    # check for png output and raytracing:
    if mv.pngPath!="":
        i=1
        while i<=nFrames:
            num=str(i)
            null="0000"
            num=null[0:4-len(num)]+num # create numbered file names
            if mv.ray:
                do[i]=do[i]+"ray;"
            do[i]=do[i]+"png %spymol%s.png;"%(mv.pngPath,num)
            i=1+1
        nFrames=nFrames+1
        do.append("mstop")        

    # now let action happen in the frames
    i=1
    while i<=nFrames:
        cmd.mdo(i,do[i])
        i=i+1                

    # start the movie
    #cmd.mplay()

def storeview(viewname):
        """
        Store the current view as a set view command under the given filename
        """
        view=cmd.get_view()
        of=open(viewname,"w")
        oof=open(viewname+"a","w")
        oof.write(`view`+"\n")
        oof.close()
        #also echo to screen
        print ("set_view (\\")
        of.write("set_view (\\\n")
        for x in range(0,6):
                for y in range(0,3):
                        index=x*3+y
                        print ("%15.9f" %view[index]),
                        of.write("%15.9f" %view[index])
                        if x==5 and y==2:
                                print (" "),
                                of.write(" ")
                        else:
                                print (","),
                                of.write(",")
                if x<5:
                        print("\\")
                        of.write("\\\n")
                else:
                        print(")")
                        of.write(")\n")
        of.close()

# ----------------------------------------------
# camera_travel - Laurence Pearl, November 2003
#     Pythonized by Lieven Buts, November 2003
#     Adapted to the movie.py framework by Morri Feldman and Seth Harris, December, 2003

def quaternion(view):
	""" 
	Returns a quaternion representation of a view matrix.
	"""

	nxt = [1,2,0]
	q = [0.0,0.0,0.0,1.0]

	tr = view[0]+view[4]+view[8]
	if tr > 0.0 :
		s = sqrt(tr + 1.0)
		qw1 = s / 2.0
		s = 0.5 / s
		return ( (view[5] - view[7]) * s,
			 	(view[6] - view[2]) * s,
				(view[1] - view[3]) * s,
				qw1                      )
	else :
		i = 0
		if (view[4] > view[0]):     i = 1
		if (view[8] > view[i+3*i]): i = 2
		j = nxt[i]
		k = nxt[j]
		s = sqrt ((view[i+i*3] - (view[j+j*3] + view[k+k*3])) + 1.0)
		q[i] = s * 0.5
		if (s != 0.0): s = 0.5 / s
		q[3] = (view[k+3*j] - view[j+3*k]) * s
		q[j] = (view[j+3*i] + view[i+3*j]) * s
		q[k] = (view[k+3*i] + view[i+3*k]) * s
		return q

def mvViewTravel(frames=1,old_view=(1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0),new_view=(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)):
	"""
	Generate progressive view matrices to move the camera smoothly
	from the current view to a new view provided as an argument.

         first   - start frame
         nframes - duration
         new_view  - PyMol view matrix that defines the view at the end 
	of the sequence
	"""
	framestates= getFrameStates(frames)
	nframes=len(framestates)
	ff=float(1.0/nframes)

#       print ( "view : (" + "%8.3f, "*17 + "%8.3f)" ) % (old_view)
#       print "oldtran : %8.3f %8.3f %8.3f" % (old_view[12], old_view[13], old_view[14])

#       capture new zoom/clip parameters
	ozc1 = new_view[11]
	ozc2 = new_view[15]
	ozc3 = new_view[16]

#       calculate shift in zoom/clip parameters
	dzc1 = (ozc1 - old_view[11]) * ff
	dzc2 = (ozc2 - old_view[15]) * ff
	dzc3 = (ozc3 - old_view[16]) * ff

	ozc1 = old_view[11]
	ozc2 = old_view[15]
	ozc3 = old_view[16]

#       capture new translation vector component
	ox = new_view[12]
	oy = new_view[13]
	oz = new_view[14]

#       calculate shift vector
	dx = ox - old_view[12]
	dy = oy - old_view[13]
	dz = oz - old_view[14]

	dx = dx*ff
	dy = dy*ff
	dz = dz*ff

	ox = old_view[12]
	oy = old_view[13]
	oz = old_view[14]


#       capture old and new rotation matrix components in quaternion form

#       m[0][0] = v[0]  m[0][1] = v[1]  m[0][2] = v[2]
#       m[1][0] = v[3]  m[1][1] = v[4]  m[1][2] = v[5]
#       m[2][0] = v[6]  m[2][1] = v[7]  m[2][2] = v[8]

	qx1,qy1,qz1,qw1 = quaternion(old_view)
	qx2,qy2,qz2,qw2 = quaternion(new_view)

#       calc cosine
	cosom = qx1 * qx2 + qy1 * qy2 + qz1 * qz2 + qw1 * qw2

	limit = 0.001
	if cosom>1.0+limit:
		raise ValueError,"Cosine of omega way out of range (positive)"
	elif cosom>1.0:
		print "Warning: cosom corrected from ",cosom,"to",
		cosom = 1.0
		print cosom

	if cosom<-1.0-limit:
		raise ValueError,"Cosine of omega way out of range (negative)"
	elif cosom<-1.0:
		print "Warning: cosom corrected from ",cosom,"to",
		cosom = 1.0
		print cosom

#       adjust signs
	if (cosom < 0.0):
		cosom = -cosom
		to0 = -qx2
		to1 = -qy2
		to2 = -qz2
		to3 = -qw2
	else:
		to0 = qx2
		to1 = qy2
		to2 = qz2
		to3 = qw2

#       calc coefficients
	omega = acos(cosom)
	sinom = sin(omega)
	if sinom==0.0:
		sinom=limit
		print "Warning: sinom corrected!"

#       restore old view
	#cmd.set_view( ("%8.3f, " * 17 + "%8.3f") % tuple(old_view) )

#       loop interpolating over nframes generating interpolated quaternion
	a=0
	for fs in framestates:
	#for a in range(nframes+1):
		scale0 = sin((1.0 - float(a*ff)) * omega) / sinom
		scale1 = sin(float(a*ff) * omega) / sinom
	#	print a, omega
	#	print a,scale0,scale1
		rx = scale0 * qx1 + scale1 * to0;
		ry = scale0 * qy1 + scale1 * to1;
		rz = scale0 * qz1 + scale1 * to2;
		rw = scale0 * qw1 + scale1 * to3;

		# convert back to matrix
		x2 = rx + rx
		y2 = ry + ry
		z2 = rz + rz
		xx = rx * x2
		xy = rx * y2
		xz = rx * z2
		yy = ry * y2
		yz = ry * z2
		zz = rz * z2
		wx = rw * x2
		wy = rw * y2
		wz = rw * z2

		nv0 = 1.0 - (yy + zz)
		nv3 = xy - wz
		nv6 = xz + wy

		nv1 = xy + wz
		nv4 = 1.0 - (xx + zz)
		nv7 = yz - wx

		nv2 = xz - wy
		nv5 = yz + wx
		nv8 = 1.0 - (xx + yy)

		# update translation vector
		ox = ox + dx
		oy = oy + dy
		oz = oz + dz

		# update zoom/clip parameters

		ozc1 = ozc1 + dzc1
		ozc2 = ozc2 + dzc2
		ozc3 = ozc3 + dzc3

#		cmd.mdo("%d" % (first), ("set_view (" + "%8.3f, "*17 + "%8.3f)") %(nv0,nv1,nv2,nv3,nv4,nv5,nv6,nv7,nv8,old_view[9],old_view[10],ozc1,ox,oy,oz,ozc2,ozc3,old_view[17]))
#		first = first + 1

#		cmd.set_view( ("%8.3f, "*17 + "%8.3f") %(nv0,nv1,nv2,nv3,nv4,nv5,nv6,nv7,nv8,old_view[9],old_view[10],ozc1,ox,oy,oz,ozc2,ozc3,old_view[17]))
		mv.movie.append((fs[0],fs[1],"set_view (%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f)" %(nv0,nv1,nv2,nv3,nv4,nv5,nv6,nv7,nv8,old_view[9],old_view[10],ozc1,ox,oy,oz,ozc2,ozc3,old_view[17])))
		a=a+1
##########################
###  The following is similar to the above mvViewTravel
###  based on code provided by Laurence Pearl and more heavily modified
###  than the above by Seth Harris to create smoothed version of the 
###  view interpolation...less abrupt at the start and finish of motion

def mvSinViewTravel(frames=1,old_view=(1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0),new_view=(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)):
	"""
	Generate progressive view matrices to move the camera smoothly
	from the current view to a new view provided as an argument.

         frames - frames for the journey 
	 old_view - old view
         new_view - PyMol view matrix that defines the view at the end 
	of the sequence
	"""
	framestates= getFrameStates(frames)
	nframes=len(framestates)
	ff=float(1.0/nframes)

#	print ( "view : (" + "%8.3f, "*17 + "%8.3f)" ) % (old_view)
#       print "oldtran : %8.3f %8.3f %8.3f" % (old_view[12], old_view[13], old_view[14])

#       capture new zoom/clip parameters
	ozc1 = new_view[11]
	ozc2 = new_view[15]
	ozc3 = new_view[16]

#		save for later since in sin smoothing need to do zoom/clip parameters 
#		step by step also instead of a constant step size
	nv11 = new_view[11]
	nv15 = new_view[15]
	nv16 = new_view[16]
	
#       calculate shift in zoom/clip parameters
#	dzc1 = (ozc1 - old_view[11]) * ff
#	dzc2 = (ozc2 - old_view[15]) * ff
#	dzc3 = (ozc3 - old_view[16]) * ff

	ozc1 = old_view[11]
	ozc2 = old_view[15]
	ozc3 = old_view[16]

#       capture new translation vector component
	ox = new_view[12]
	oy = new_view[13]
	oz = new_view[14]

#       calculate shift vector
	dx = ox - old_view[12]
	dy = oy - old_view[13]
	dz = oz - old_view[14]

	dx = dx*ff
	dy = dy*ff
	dz = dz*ff

	ox = old_view[12]
	oy = old_view[13]
	oz = old_view[14]


#       capture old and new rotation matrix components in quaternion form

#       m[0][0] = v[0]  m[0][1] = v[1]  m[0][2] = v[2]
#       m[1][0] = v[3]  m[1][1] = v[4]  m[1][2] = v[5]
#       m[2][0] = v[6]  m[2][1] = v[7]  m[2][2] = v[8]

	qx1,qy1,qz1,qw1 = quaternion(old_view)
	qx2,qy2,qz2,qw2 = quaternion(new_view)

#       calc cosine
	cosom = qx1 * qx2 + qy1 * qy2 + qz1 * qz2 + qw1 * qw2

	limit = 0.001
	if cosom>1.0+limit:
		raise ValueError,"Cosine of omega way out of range (positive)"
	elif cosom>1.0:
		print "Warning: cosom corrected from ",cosom,"to",
		cosom = 1.0
		print cosom

	if cosom<-1.0-limit:
		raise ValueError,"Cosine of omega way out of range (negative)"
	elif cosom<-1.0:
		print "Warning: cosom corrected from ",cosom,"to",
		cosom = 1.0
		print cosom

#       adjust signs
	if (cosom < 0.0):
		cosom = -cosom
		to0 = -qx2
		to1 = -qy2
		to2 = -qz2
		to3 = -qw2
	else:
		to0 = qx2
		to1 = qy2
		to2 = qz2
		to3 = qw2

#       calc coefficients
	omega = acos(cosom)
	sinom = sin(omega)
	if sinom==0.0:
		sinom=limit
		print "Warning: sinom corrected!"

#       restore old view
	cmd.set_view( ("%8.3f, " * 17 + "%8.3f") % tuple(old_view) )

#       loop interpolating over nframes generating interpolated quaternion
	j=1
	prev=1.0
	sum=0.0
	a=0
	for fs in framestates:
	#for a in range(nframes+1):
		scale0 = sin((1.0 - float(sin((math.pi/2)*(2*a*ff-1))/2+0.5)) * omega) / sinom
		scale1 = sin((float(sin((math.pi/2)*(2*a*ff-1))/2+0.5) * omega)) / sinom
		#print a,scale0,scale1
		rx = scale0 * qx1 + scale1 * to0;
		ry = scale0 * qy1 + scale1 * to1;
		rz = scale0 * qz1 + scale1 * to2;
		rw = scale0 * qw1 + scale1 * to3;

		# convert back to matrix
		x2 = rx + rx
		y2 = ry + ry
		z2 = rz + rz
		xx = rx * x2
		xy = rx * y2
		xz = rx * z2
		yy = ry * y2
		yz = ry * z2
		zz = rz * z2
		wx = rw * x2
		wy = rw * y2
		wz = rw * z2

		nv0 = 1.0 - (yy + zz)
		nv3 = xy - wz
		nv6 = xz + wy

		nv1 = xy + wz
		nv4 = 1.0 - (xx + zz)
		nv7 = yz - wx

		nv2 = xz - wy
		nv5 = yz + wx
		nv8 = 1.0 - (xx + yy)

		# update translation vector
		ox = ox + dx
		oy = oy + dy
		oz = oz + dz

		# for sin smoothing need difference between this step and next step:
		diff = (sin(math.pi/2*((a+1)*2*ff-1))-sin(math.pi/2*(a*2*ff-1)))/2
		if diff < 0:
			print ("diff adjusted from negative")
			diff = 0
		#       calculate shift in zoom/clip parameters
		dzc1 = (nv11 - old_view[11]) * diff
		dzc2 = (nv15 - old_view[15]) * diff
		dzc3 = (nv16 - old_view[16]) * diff

		# update zoom/clip parameters

		ozc1 = ozc1 + dzc1
		ozc2 = ozc2 + dzc2
		ozc3 = ozc3 + dzc3
		#mv.movie.append((fs[0],fs[1],"color %s, %s"%(tmpc,selection)))

		mv.movie.append((fs[0],fs[1],"set_view (%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f,%f)" %(nv0,nv1,nv2,nv3,nv4,nv5,nv6,nv7,nv8,old_view[9],old_view[10],ozc1,ox,oy,oz,ozc2,ozc3,old_view[17])))
		
		a=a+1
		#cmd.mdo("%d" % (first), ("set_view (" + "%8.3f, "*17 + "%8.3f)") %(nv0,nv1,nv2,nv3,nv4,nv5,nv6,nv7,nv8,old_view[9],old_view[10],ozc1,ox,oy,oz,ozc2,ozc3,old_view[17]))
		#first = first + 1
##############################

######### What follows are several (probably redundant but I'm only just learning Python!)
######### subroutines used by the ribbon rider module
# this is just plodding through it.  There's probably a better way in NumPy
# as it is already packaged, but I don't know it.
def cross_product(a,b):
    """Cross product of two 3-d vectors.
    """
    cross = [0]*3
    cross[0] = a[1]*b[2]-a[2]*b[1]
    cross[1] = a[2]*b[0]-a[0]*b[2]
    cross[2] = a[0]*b[1]-a[1]*b[0]
    return cross

# normalize the vector    
def normvec(v,mag):
	vx=v[0]/mag
	vy=v[1]/mag
	vz=v[2]/mag
	return(vx,vy,vz)
    
#Convert rotation vector and angle to quaternion
def vecang2quat (rotvec,ang):
	qx = rotvec[0] * math.sin(ang/2)
	qy = rotvec[1] * math.sin(ang/2)
	qz = rotvec[2] * math.sin(ang/2)
	qw = math.cos(ang/2)
	return (qx,qy,qz,qw)

# Convert quaternion form to matrix
# note that I'm setting up the matrix working across each row first:
# m[0]  m[1]  m[2]
# m[3]  m[4]  m[5]
# m[6]  m[7]  m[8]
def quat2mat (q):
	m = [0]*9
	m[0] = q[3]*q[3] + q[0]*q[0] - q[1]*q[1] - q[2]*q[2]
	m[1] = 2*q[0]*q[1] - 2*q[3]*q[2]
	m[2] = 2*q[0]*q[2] + 2*q[3]*q[1]
	m[3] = 2*q[0]*q[1] + 2*q[3]*q[2]
	m[4] = q[3]*q[3] - q[0]*q[0] + q[1]*q[1] - q[2]*q[2]
	m[5] = 2*q[1]*q[2] - 2*q[3]*q[0]
	m[6] = 2*q[0]*q[2] - 2*q[3]*q[1]
	m[7] = 2*q[1]*q[2] + 2*q[3]*q[0]
	m[8] = q[3]*q[3] - q[0]*q[0] - q[1]*q[1] + q[2]*q[2]
	return (m)
	
# normalize the quaternion to a unit value
def normquat (q):
	magquat = math.sqrt(q[0]*q[0] + q[1]*q[1] + q[2]*q[2] + q[3]*q[3])
	n=[0]*4
	n[0]=q[0]/magquat
	n[1]=q[1]/magquat
	n[2]=q[2]/magquat
	n[3]=q[3]/magquat
	return (n[0],n[1],n[2],n[3])

##### The Ribbon Rider module
### create by Seth Harris, January, 2004
### based on Seth's VRML pepcam fly through
def ribbon_ride(selection="mol",fperm="40",zbuff="30",halfslab="6",frequency="1"):
    # clear various movie memories, frames, caches
	cmd.do("mclear")
	cmd.do("mvClear")
	cmd.do("mset")
	cmd.do("frame 1")

	# get current view, just to inherit some flags like orthoscopic and ?
	# from how the user was looking at the world
	# that being said, most of the 18 view matrix arguments will be set de novo
	# by this routine
	old_view = cmd.get_view()

	fperm=int(fperm)
	frequency=int(frequency)
	zbuff=int(zbuff)
	halfslab=int(halfslab)
	
	#frame of reference vector...rotations are relative to this
	start=(0,0,-1)

	# parse mol selection to get array of Calpha coordinates
	cmd.create ("calpha","/" + selection + "////CA")
	calpha = cmd.get_model("calpha")
	# break calpha up so it only includes every xth atom, where x is frequency
	# passed in by user
	totalcount=len(calpha.atom)

	#define working list size
	listsizecorrect=0
	if (totalcount%frequency):
		listsizecorrect=1
	workinglist=[0]*(totalcount/frequency+listsizecorrect)
	lpcount=0
	indexcount=0
	for a in calpha.atom:
		# now only add this atom to the working array if our counter%frequency is 0
		# i.e. is evenly divisible by the frequency
		if (lpcount%frequency==0):
			workinglist[indexcount]=(a.coord[0],a.coord[1],a.coord[2])
			indexcount=indexcount+1
		lpcount=lpcount+1

	lpcount=0
	lastx=0
	target=(0,0,0)
	for b in workinglist:
		#cx=a.coord[0]
		#cy=a.coord[1]
		#cz=a.coord[2]
		cx=b[0]
		cy=b[1]
		cz=b[2]

		# calculate vector to next Calpha
		if (lastx):
			vx=cx-lastx
			vy=cy-lasty
			vz=cz-lastz
			target=(vx,vy,vz)
		#print "cx - lastx is: " + `cx` + " - " + `lastx`
		lastx=cx
		lasty=cy
		lastz=cz
		#print "target vector is: " + `target`
	#debugging control point
	#	if (lpcount==1000):
	#		print "breaking!"
	#		break
		if (lpcount>0):
			#print "We're in!"
			maga=math.sqrt(start[0]*start[0] + start[1]*start[1] + start[2]*start[2])
			magb=math.sqrt(target[0]*target[0] + target[1]*target[1] + target[2]*target[2])
			#print "mag a is " + `maga`
			#print "mag b is " + `magb`

	# normalize the target view vector b
			target=normvec(target,magb)
			#print "normalized target view vector is: " + `target`
	
			magb=math.sqrt(target[0]*target[0] + target[1]*target[1] + target[2]*target[2])
			#print "magnitude should now be one: " + `magb`
			magb=1

	#calculate cross product
			cprod=cross_product(start,target)
			#print "cross product is " + `cprod`
	
			magcross=math.sqrt(cprod[0]*cprod[0] + cprod[1]*cprod[1] + cprod[2]*cprod[2])
			#print "mag cross is " + `magcross`

	# calculate dot product
			dprod = (start[0]*target[0] + start[1]*target[1] + start[2]*target[2])
			#print "dot product is " + `dprod`
	
	# get angle between vectors
			sintheta = magcross/(maga*magb)
			theta1=asin(sintheta)
			theta2 = math.pi - theta1
	
			costheta = dprod/(maga*magb)
			theta3=acos(costheta)
			theta4=-theta3

	# have to check which solution of asin is correct by comparing with acos results
			diff1 = theta1 - theta3
			diff2 = theta2 - theta3
			diff3 = theta1 - theta4
			diff4 = theta2 - theta4
			diff1 = abs (diff1)
			diff2 = abs (diff2)
			diff3 = abs (diff3)
			diff4 = abs (diff4)
			if (diff1 < 0.01) :
				theta = theta1
	      
			elif (diff2 < 0.01) :
				theta = theta2
	
			elif (diff3 < 0.01) :
				theta = theta1;
	
			elif (diff4 < 0.01) :
				theta = theta2
		
			else :
				theta = 0

	# convert this rotation vector (cprod) and angle (theta) to quaternion form
			quat1 = vecang2quat(cprod,theta)

	#normalize the quat
			quat1 = normquat(quat1)

	# now convert the quaternion to a matrix
			mat = quat2mat(quat1)

			#print "new view matrix is " + `mat`
			cmd.set_view( ("%8.3f, "*17 + "%8.3f") %(mat[0],mat[1],mat[2],mat[3],mat[4],mat[5],mat[6],mat[7],mat[8],0,0,-zbuff,cx,cy,cz,zbuff-halfslab,zbuff+halfslab-2,old_view[17]))
			new=cmd.get_view()
			if (lpcount==0):
				original=new
			start_frame=(lpcount-1)*fperm
			end_frame=start_frame+fperm
			framerange="%s-%s"%(start_frame,end_frame)
			mvViewTravel(framerange,old_view,new)
			old_view=new
		lpcount=lpcount+1
	cmd.do("movie")

#################  PEAK TOUR #############################
## created by Seth Harris, sharris@msg.ucsf.edu         ##
## visit various entities sequentially such as peaks in ##
## your map file.                                       ##
## usage: peak_tour selection, zoom buffer, frames per move, stall frames             ##
## e.g.: peak_tour mypeaks, 6, 45, 10                   ##
## then type mplay to start the movie tour              ##

def peak_tour(selection="mol",zbuff="6",framespermove=45,stallframes=5):
        # zbuff is how far to stand back from the selection
        # framespermove is how many frames to spend at each peak of the selection
        # stallframes is how many frames to linger, unmoving before proceeding to next peak
        framespermove=int(framespermove)
        stallframes=int(stallframes)
        
        # clear various movie memories, frames, caches
        cmd.do("mclear")
        cmd.do("mvClear")
        cmd.do("mset")
        cmd.do("frame 1")
        
        # fetch model to find how many waypoints we will be visiting
        model = cmd.get_model(selection).atom
        stopovers=len(model)

        # set up some landmarks within our visit to each peak so can divvy up the rotation
        # or other movements easily
        for waypoints in range(stopovers):
                startframe=(waypoints)*framespermove+1+(waypoints)*stallframes
                mark1=int(startframe+framespermove/8)
                mark2=int(startframe+framespermove*3/8)
                mark3=int(startframe+framespermove/2)
                mark4=int(startframe+framespermove*5/8)
                mark5=int(startframe+framespermove*7/8)
                endframe=startframe+framespermove

        # This section describes whatever "dance" you want to do at each waypoint
        # you can use the mark1-5 defined above to divvy up the time at this waypoint
        # in this case it's 90 degree turn on y and x at each frame
                lit1="mvSinturn %s-%s,y,90" %(startframe,mark3)
                cmd.do(lit1)
                lit2="mvSinturn %s-%s,x,90" %(mark3,endframe)
                cmd.do(lit2)

        cmd.do("movie")

        # once you've defined the movie with "movie" (above) can then do the mdo
        # commands to set the views at various points to be sure we go from one atom
        # to the next.  These mdo commands would be wiped out if the "movie" or "mset"
        # commands were run after they are
        for waypoints in range(stopovers):
                startframe=(waypoints)*framespermove+1+(waypoints)*stallframes
                endframe=startframe+framespermove
                zoomview="zoom /%s///%s/, %s"%(selection, model[waypoints].resi, zbuff)
                cmd.mdo(startframe+1, zoomview)
                #print "waypoint: %s  command: %s" %(waypoints, zoomview)

############################### end of routines          ####################################
#############################################################################################
############################### now the export commands  ####################################
cmd.extend('movie',movie)
cmd.extend('mvClear',mvClear) # clear cached instructions
cmd.extend('mvRot',mvRot)     # rotate over frame range
cmd.extend('mvMove',mvMove)   # move over frame range
cmd.extend('mvTurn',mvTurn)   # turn over frame range
cmd.extend('mvCmd',mvCmd)     # do anything during a frame range
cmd.extend('mvSet',mvSet)     # adjust parameter over frame range
cmd.extend('mvSinrot',mvSinrot)   # rotate smoothly
cmd.extend('mvSinmove',mvSinmove) # move smoothly
cmd.extend('mvSinturn',mvSinturn) # turn smoothly 
cmd.extend('mvSinset',mvSinset)   # set smoothly
cmd.extend('pngseq',pngseq)
cmd.extend('mvGradCol',mvGradCol)
cmd.extend('storeview',storeview)
cmd.extend('mvSinViewTravel',mvSinViewTravel)
cmd.extend('mvViewTravel',mvViewTravel)
cmd.extend('ribbon_ride',ribbon_ride)
cmd.extend('peak_tour',peak_tour)

# make_pov.py                                                                                       
def make_pov(file):
  (header,data) = cmd.get_povray()
  povfile=open(file,'w')
  povfile.write(header)
  povfile.write(data)
  povfile.close()

cmd.extend('make_pov',make_pov)

from pymol import cmd
import glob

def load_models(files,obj):
  """
  load_models <files>, <object>

  loads multiple files (using filename globbing)
  into a single object (e.g. from modelling or NMR).

  e.g. load_models prot_*.pdb, prot
  """
  file_list = glob.glob(files)
  if file_list:
    file_list.sort()
    for name in file_list:
      cmd.load(name,obj,discrete=0)
  else:
    print "No files found for pattern %s" % files

cmd.extend('load_models',load_models)
