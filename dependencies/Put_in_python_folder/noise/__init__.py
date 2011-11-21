# NOISE - last updated for NodeBox 1.9.2
# Author: Tom De Smedt <tomdesmedt@organisms.be>
# Copyright (c) 2007 by Tom De Smedt.
# See LICENSE.txt for details.

# Python version adapted from Malcolm Kesson's code: 
# http://www.fundza.com/c4serious/noise/perlin/perlin.html

######################################################################################################

import random
from sys import maxint
from math import floor
from warnings import warn

######################################################################################################

try:
    
    """ Attempt to load the C library which is faster.
    """
    
    import _noise

    def seed(i=None):
    	if i == None: 
    		i = int(random.random()*maxint)
    	_noise.seed(int(i))
    	
    def shape(a):
    	a = [max(0, min(int(x), 512-1)) for x in a[:512]]
    	_noise.shape(a)
    
    def perlin(x, y, z):
        return _noise.perlin(x, y, z)
        
except:
    
    """ Pure Python implementation of the C library.
    """

    warn("Couldn't import fast C library, using native Python version.", Warning)
    
    p = []
    def seed(i=None):
    	# Populate the permutation array p (defines the pattern of the noise).
    	global p
    	if i == None: 
    		i = int(random.random()*maxint)
    	s = random.getstate()
    	random.seed(i)
    	p = [int(random.random()*256) for i in range(256)] * 2
    	random.setstate(s)

    def shape(a):
    	# Populates permutation array from a custom list.
    	global p
    	p = [max(0, min(int(x), 512-1)) for x in a[:512]]

    def fade(t): return t * t * t * (t * (t * 6 - 15) + 10)
    def lerp(t, a, b): return a + t * (b - a)
    def grad(hash, x, y, z):
        # Convert lo 4 bits of hash code into 12 gradient directions.
        h = hash & 15 
        u = x
        v = y
        if h >= 8: u = y
        if h >= 4:
            v = x
            if h != 12 and h != 14: v = z
        if (h&1) != 0: u = -u
        if (h&2) != 0: v = -v
        return u + v
    
    def perlin(x, y, z):
        
        global p
        
        # Find unit cuve that contains point.
        X = int(floor(x)) & 255
        Y = int(floor(y)) & 255
        Z = int(floor(z)) & 255
        
        # Find relative x, y, z of point in cube.
        x -= floor(x)
        y -= floor(y)
        z -= floor(z)
        
        # Compute fade curves for each of x, y, z.
        u = fade(x)
        v = fade(y)
        w = fade(z)
        
        # Hash coordinates of the 8 cube corners.
        A  = p[X  ] + Y
        AA = p[A  ] + Z
        AB = p[A+1] + Z
        B  = p[X+1] + Y
        BA = p[B  ] + Z
        BB = p[B+1] + Z

        # Add blended results from 8 corners of cube.
        return lerp(w, 
            lerp(v, 
                lerp(u, grad(p[AA  ], x  , y  , z  ), 
                        grad(p[BA  ], x-1, y  , z  )),
                lerp(u, grad(p[AB  ], x  , y-1, z  ), 
                        grad(p[BB  ], x-1, y-1, z  ))),
            lerp(v, 
                lerp(u, grad(p[AA+1], x  , y  , z-1), 
                        grad(p[BA+1], x-1, y  , z-1)),
                lerp(u, grad(p[AB+1], x  , y-1, z-1), 
                        grad(p[BB+1], x-1, y-1, z-1)))
            )

	# We may get lucky, there's a psyco patch for intel. 
    try:
        import psyco
    	psyco.bind(perlin)
    except:
        pass

######################################################################################################

def generate(x, y=0.0, z=0.0, width=1.0, height=1.0, depth=1.0, scale=1.0):
	
	""" Returns a random value between 0.0 and 1.0
	
	Returns random Perlin noise in one, two or three dimensions.
	The random sequence is more naturally ordered (like a gradient)
	than normal random sequences.
	
	Noise is generated on an infinite plane, so the actual value of 
	a coordinate is less important than the distance between 
	successive coordinates.The smaller the distance, the smoother the noise.
	
	Some additional parameters can make this easier to comprehend:
	
	If noise in two dimensions was a tile with width and height 1.0,
	x and y would range between 0.0 and 1.0. 
	Higher/lower values then expand the tile pattern.
	The scale parameter controls the zoom of the pattern
	(0.5 means "zoom out 200%").
	
	If you supply a different width and height 
	x and y are mapped between that.
	
	"""
	
	x = float(x)
	y = float(y)
	z = float(z)
	
	if width == 0 or height == 0 or depth == 0: return None
	if width  != 1: x /= width
	if height != 1: y /= height
	if depth  != 1: z /= depth
	
	if scale == 0: scale += 0.00000001
	if scale != 1:
		x /= scale
		y /= scale
		z /= scale
	
	return perlin(x, y, z) * 0.5 + 0.5

seed()
