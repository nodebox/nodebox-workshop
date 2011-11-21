# CLOUDSCAPE

# We're going to put perlin noise as a texture
# into Core Image.
coreimage = ximport("coreimage")

try:
    noise = ximport("noise")
except:
    noise = ximport("__init__")
    reload(noise)

size(400,400)

# Render some organic noise.
noise.seed()
w = 200
h = 200
for i in range(w):
	for j in range(h):
		d = noise.generate(i, j, width=w, height=h, scale=0.15)
		fill(0,0,0,d*1.2)
		s = 2
		rect(i*s, j*s, s, s)

# Save the output we've created up to now as an image.
# Then, clear the NodeBox canvas.
canvas.save("texture.jpg")
canvas.clear()

# Now get the rendered noise image into a layer,
# put it on a blue background.
canvas = coreimage.canvas(WIDTH, HEIGHT)
canvas.layer(color(0.25, 0.4, 0.75))
l = canvas.layer("texture.jpg")
l.blend_screen(75)
l.adjust_contrast(1.5)

# Add some realistic perspective distance.
l.distort(dx0=-400, dx1=400)

canvas.draw()
