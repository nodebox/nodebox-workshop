# Import the library
try:
    # This is the statement you normally use.
    noise = ximport("noise")
except ImportError:
    # But since these examples are "inside" the library
    # we may need to try something different when
    # the library is not located in /Application Support
    noise = ximport("__init__")
    reload(noise)

size(500,500)

noise.seed()
w = 250
h = 100
stroke(0)
for i in range(w):
	d = noise.generate(i, i, width=w, height=h, scale=0.2 )
	ddd = noise.generate(i, i, width=w, height=h, scale=0.52 )
	print d
	fill(0,0,0,d*1.2)
	line(i*2, HEIGHT/2,i*2,HEIGHT/2-100*d)
	rect(i*2, HEIGHT/2, 1, 150.0*ddd)
