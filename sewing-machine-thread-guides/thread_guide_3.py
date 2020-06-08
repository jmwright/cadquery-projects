import cadquery as cq

# A few adjustable positions
b_len = 22
ang_x = 25
ang_y = 42

# Small hole positions
sm_holes = [(6, 4), (6, 9)]

# Large hole positions
lg_holes = [(0, 41), (-7, 41), (7, 41), (-12, 45), (-3.5, 47), (3.5, 47), (12, 45)]

# Slot positions
slot1_pos = [(0, 28)]
slot2_pos = [(-10, 32)]
slot3_pos = [(10, 32)]

# Main body
guide = (cq.Workplane("XY").moveTo(10, 0)
                           .vLine(b_len)
                           .lineTo(ang_x, ang_y)
                           .threePointArc((0, 53), (-ang_x, ang_y))
                           .lineTo(-10, b_len)
                           .vLine(-b_len)
                           .close()
                           .extrude(2.0))

# Add large holes
guide = guide.faces(">Z").workplane(centerOption="ProjectedOrigin").pushPoints(lg_holes).circle(2.0).cutThruAll()

# Add small holes
guide = guide.faces(">Z").workplane(centerOption="ProjectedOrigin").pushPoints(sm_holes).circle(1.5).cutThruAll()

# Add slots
guide = guide.faces(">Z").workplane(centerOption="ProjectedOrigin").pushPoints(slot1_pos).slot2D(10, 2.5, 90).cutThruAll()
guide = guide.faces(">Z").workplane(centerOption="ProjectedOrigin").pushPoints(slot2_pos).slot2D(10, 2.5, 125).cutThruAll()
guide = guide.faces(">Z").workplane(centerOption="ProjectedOrigin").pushPoints(slot3_pos).slot2D(10, 2.5, 55).cutThruAll()

# Break some of the edges
guide = guide.edges("|Z and >X").fillet(3)
guide = guide.edges("|Z and <X").fillet(3)
guide = guide.edges("|Z and <Y").fillet(3)

# Export to STL for printing
guide.val().exportStl("/home/jwright/Downloads/guide_3.stl", precision=0.0001)

show_object(guide)