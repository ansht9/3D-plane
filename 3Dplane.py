import numpy as np
from solid import *
from solid.utils import *

# Parameters for the wing
span = 200  # Span of the wing in mm
root_chord = 60  # Chord length at the root in mm
tip_chord = 20  # Chord length at the tip in mm
thickness = 10  # Maximum thickness of the wing

# Define the airfoil shape at root and tip
def airfoil(chord, thickness):
    x = np.linspace(0, chord, 30)
    y_upper = 5 * thickness/100 * (0.2969*np.sqrt(x/chord) - 0.1260*(x/chord) - 0.3516*np.power(x/chord,2) + 0.2843*np.power(x/chord,3) - 0.1015*np.power(x/chord,4))
    y_lower = -y_upper
    return list(zip(x, y_upper)) + list(reversed(list(zip(x, y_lower))))

# Create 3D model
def wing_model(span, root_chord, tip_chord, thickness):
    root_airfoil = airfoil(root_chord, thickness)
    tip_airfoil = airfoil(tip_chord, thickness)
    
    # Use polygon points to create 3D shape
    points = []
    for i, (rx, ry) in enumerate(root_airfoil):
        points.append([rx, 0, ry])
    for i, (tx, ty) in enumerate(tip_airfoil):
        points.append([tx, span, ty])
    
    # Generate faces
    faces = []
    num_points = len(root_airfoil)
    for i in range(num_points-1):
        faces.append([i, i+1, num_points+i+1, num_points+i])
    
    # Create the wing using polyhedron
    return polyhedron(points=points, faces=faces)

# Generate the model
wing = wing_model(span, root_chord, tip_chord, thickness)

# Save to SCAD file
scad_render_to_file(wing, 'airplane_wing.scad')
