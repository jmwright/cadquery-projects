from random import randint
import cadquery as cq
from Helpers import show


# Generates a random solid, and keeps trying till it finds one
def generate(width=10, height=10, startingPoints=6):
    points = []

    # Make sure that we get stop points for the random points that make sense
    xStop = w
    yStop = h / 2.0

    points.append((0.0, h / 2.0))

    for i in range(1, startingPoints - 1):
        # Genreate a random point for two edges to connect at
        x = randint(0, xStop)
        y = randint(1, yStop)  # The 0.1 start is to help get a solid

        points.append((x, y))

    points.append((w, h / 2.0))

    # Append a point that is back on the base to close the mirror
    points.append((w, 0.0))

    for point in points:
        print(point)

    try:
        # Profile of our beam that we will later test
        crossSection = cq.Workplane('XZ').polyline(points).mirrorX()
    except:
        print("Points for outline not valid.")
        return None

    try:
        beam = crossSection.extrude(100)
    except:
        print("Not a valid cross-section, could not extrude")
        return None

    # Check to make sure our resulting shape is a valid solid
    if not beam.val().wrapped.isValid():
        return None

    # Check to see that we have the correct number of faces
    # if beam.faces().size() != startingPoints * 2 + 2:
    #     return None

    return beam

# Overall allowed dimensions of the beam
w = 10.0  # Width
h = 10.0  # Height

# The number of points that we can manipulate (same as number of edges
startingPoints = 6  # Half of the number of starting edges

# Keep looping until we get a valid solid
beam = None
while beam is None:
    beam = generate(w, h, startingPoints)

show(beam)
