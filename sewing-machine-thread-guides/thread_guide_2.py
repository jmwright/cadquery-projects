import cadquery as cq

sm_holes = [(5, 14), (-5, 14), (5, -12), (-5, -12)]
lg_holes = [(25, 12),(14, 12), (25, 0), (14, 0), (-25, 12),(-14, 12), (-25, 0), (-14, 0)]

# Main body
guide = cq.Workplane("XY").rect(77, 42).extrude(3.0)

# Smaller holes
guide = guide.faces(">Z").workplane(centerOption="ProjectedOrigin").pushPoints(sm_holes).circle(1.0).cutThruAll()

# Bigger holes
guide = guide.faces(">Z").workplane(centerOption="ProjectedOrigin").pushPoints(lg_holes).circle(2.5).cutThruAll()

# Chamfers
guide = guide.edges("|Z and >Y").chamfer(10)

# Export to STL for printing
guide.val().exportStl("/home/jwright/Downloads/guide_2.stl", precision=0.0001)

show_object(guide)