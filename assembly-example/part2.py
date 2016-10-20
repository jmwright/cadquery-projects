import cadquery as cq
from Helpers import show

result = cq.Workplane('XY').circle(30.0).extrude(10)\
    .faces('>Z').workplane().hole(20.1)

result.val().exportStep('/home/jwright/Downloads/assembly_example/part2.step')

# show(result)
