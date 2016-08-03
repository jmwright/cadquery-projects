from random import randint
import cadquery as cq
from Helpers import show


# Generates a random solid, and keeps trying till it finds one
def generate(width=10, height=10, points=6):
    points = []

    # Make sure that we get stop points for the random points that make sense
    xStop = w
    yStop = h / 2.0

    for i in range(1, startingPoints):
        # Genreate a random point for two edges to connect at
        x = randint(0, xStop)
        y = randint(1, yStop)  # The 0.1 start is to help get a solid

        points.append((x, y))

    # Add points that can be used to generate the cross section
    # for i in reversed(range(1, startingPoints)):
    #     # Make sure that we get stop points for the random points that make sense
    #     xStop = int(w / i)
    #     yStop = int((h / 2.0) / i)

    #     # The stops should not be less than the stops that have come before
    #     for point in points:
    #         if xStop < point[0]:
    #             xStop = point[0] + 1
    #         if yStop < point[1]:
    #             yStop = point[1] + 1

    #     # Genreate a random point for two edges to connect at
    #     x = randint(0, xStop)
    #     y = randint(1, yStop)  # The 0.1 start is to help get a solid

    #     points.append((x, y))

    # Append a point that is back on the base to close the mirror
    points.append((w, 0.0))

    # Points that we can manipulate and test
    # points = [(0.0, h / 2.0), (w, h / 2.0), (w, 0.0)]

    for point in points:
        print(point)

    try:
        # Profile of our beam that we will later test
        crossSection = cq.Workplane('XZ').polyline(points).mirrorX()
    except:
        print("Points for outline not valid.")

    try:
        beam = crossSection.extrude(100)
    except:
        print("Not a valid cross-section, could not extrude")

    try:
        show(crossSection)
        show(beam, (204, 204, 204, 0.0))
    except:
        print("Not a valid solid.")

# Overall allowed dimensions of the beam
w = 10.0  # Width
h = 10.0  # Height

# The number of points that we can manipulate (same as number of edges
startingPoints = 6  # Half of the number of starting edges

generate(w, h, startingPoints)
