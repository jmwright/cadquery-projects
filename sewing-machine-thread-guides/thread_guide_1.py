import cadquery as cq

core_rad = 45.0 / 2.0

# Objects to make the basic shape of the guide
guide_core = (cq.Workplane("XY")
           .circle(core_rad)
           .extrude(3.0))

guide_fan = (cq.Workplane("XY")
                .moveTo(0.0, -10.0)
                .hLine(core_rad + 15)
                .threePointArc((0.0, core_rad + 15), (-core_rad - 15, -10.0))
                .close()
                .extrude(3.0))

# Fuse both objects so they act as one
guide = guide_core.union(guide_fan)
            
# Put guide holes in fan
guide = guide.faces(">Z").workplane(centerOption="ProjectedOrigin").polarArray(core_rad + 7.5, -10, 90, 6).circle(2.5).cutThruAll()

# Center shaft boss
#guide = guide.faces(">Z").workplane(centerOption="ProjectedOrigin").circle(10.0).extrude(7.0)

# Put the center hole in
guide = guide.faces(">Z").workplane(centerOption="ProjectedOrigin").circle(9.75 / 2.0).cutThruAll()

# Put the set screw holes in
guide = guide.faces("<Z").workplane(centerOption="ProjectedOrigin", invert=True).transformed(offset = (0, 0, 7)).transformed(rotate=(0, 90, 0)).circle(2.5 / 2.0).cutThruAll()

# Export to STL for printing
guide.val().exportStl("/home/jwright/Downloads/guide_1.stl", precision=0.0001)

show_object(guide)