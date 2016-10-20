import cadquery as cq
from Helpers import show

result = cq.Workplane('XY').circle(10).extrude(100)

result.val().exportStep('/home/jwright/Downloads/assembly_example/part1.step')

# show(result)
