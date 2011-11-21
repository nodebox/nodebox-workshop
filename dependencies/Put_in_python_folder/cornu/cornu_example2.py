# Interactive Cornu editor.
# Click and drag points on the canvas.
# Your work will be saved as an SVG-file in this folder.

try:
    cornu = ximport("cornu")
except:
    cornu = ximport("__init__")
    reload(cornu)
    
points = []
drag = None

speed(40)
def draw():
    
    # Draw the Cornu path.
    if len(points) > 1:
        nofill()
        stroke(0)
        cornu.drawpath(points)
    
    # Draw the control points on the path.
    # The last point is indicated with a red oval.
    # Store the control points in a list,
    # so we can check if the mouse is clicked on one of them.
    handles = []
    for i, (x, y) in enumerate(points):
        nostroke()
        fill(0)
        if i == len(points)-1:
            fill(1,0,0)
        path = oval(x*WIDTH-4, y*HEIGHT-4, 8, 8)
        handles.append(path)

    global drag
    if not mousedown:
        if drag != None:
            export_svg()
        # If the mouse button is up, we are not dragging a control point.
        drag = None
    else:
        # If the mouse is down, 
        # check if it is clicked inside a control point.
        if drag == None:
            for i in range(len(handles)):
                if handles[i].contains(MOUSEX, MOUSEY):
                    drag = i
                    break
        # If so, drag the location of that point.
        # Otherwise, add a new point and drag that.
        x, y = MOUSEX/WIDTH, MOUSEY/HEIGHT
        if drag == None:
            points.append((x, y))
            drag = -1
        else:
            points[drag] = (x, y)
            
def export_svg():
    
    d = ""
    if len(points) > 1:
        for pt in cornu.path(points):
            if pt.cmd == MOVETO:
                d += "M "+str(pt.x)+" "+str(pt.y)+" "
            elif pt.cmd == LINETO:
                d += "L "+str(pt.x)+" "+str(pt.y)+" "
            elif pt.cmd == CURVETO:
                d += "C "
                d += str(pt.ctrl1.x)+" "+str(pt.ctrl1.y)+" "
                d += str(pt.ctrl2.x)+" "+str(pt.ctrl2.y)+" "
                d += str(pt.x)+" "+str(pt.y)+" "
    
    svg  = '<?xml version="1.0"?>\n'
    svg += '<svg width="'+str(WIDTH)+'pt" height="'+str(HEIGHT)+'pt">\n'
    svg += '<g>\n'
    svg += '<path d="'+d+'" fill="none" stroke="rgb(0,0,0)" />\n'
    svg += '</g>\n'
    svg += '</svg>\n'
    f = open("cornu_example2.svg", "w")
    f.write(svg)
    f.close()
