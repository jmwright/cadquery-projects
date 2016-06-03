import math
import FreeCAD
import pint
import cadquery as cq
from Helpers import show

# Units handling
ureg = pint.UnitRegistry()

# ################################################### #
# THIS IS THE ONLY VARIALBE YOU SHOULD HAVE TO CHANGE #
# BE SURE NOT TO REMOVE THE UNITS                     #
# ################################################### #
# freq = 145.8 * ureg.MHz  # Receive frequency
freq = 915.0 * ureg.MHz  # Receive frequency


def createSMConnector():
    length = 20.66
    width = 9.5
    thickness = 2.19

    # Create the basic shape of the terminal
    term = cq.Workplane('XY').box(length, width, thickness)\
        .edges('|Z').fillet(width / 2.001)\
        .edges('|X').fillet(0.5)\
        .faces('>Z').workplane().center(length / 2.0 - width / 2.0, 0.0)\
        .circle(width / 2.0).circle(4.6 / 2.0).extrude(7.0)\
        .edges('>Z').fillet(0.2)

    # Put the top holes in the terminal
    term = term.faces('<Z').workplane()\
        .center(-length / 2.0 + width / 2.0, 0.0)\
        .circle(5.25 / 2.0).cutThruAll()

    # Put the side hole in that accepts the wire
    hole = cq.Workplane('YZ').center(0.0, 5.7 - thickness).circle(4.25 / 2.0)\
             .extrude(length / 2.0)
    term = term.cut(hole)

    return term


def createMDConnector():
    # Implement this properly
    return cq.Workplane('XY').box(2, 2, 2)


def createLGConnector():
    # Implement this properly
    return cq.Workplane('XY').box(3, 3, 3)


def createConnector(frequency):
    if freq >= 600.0 * ureg.MHz and freq <= 1000.0 * ureg.MHz:
        return createSMConnector()
    elif freq >= 300.0 * ureg.MHz and freq < 600.0 * ureg.MHz:
        return createMDConnector()
    elif freq >= 30.0 * ureg.MHz and freq < 300.0 * ureg.MHz:
        return createLGConnector()
    else:
        FreeCAD.Console.PrintError(frequency + " is not valid for this design.")
        return None


def pvcEndCap():
    od = 76.2
    id = 63.5
    len = od / 2.0
    holeDp = len - 10.0

    cap = cq.Workplane('XY').circle(od / 2.0).extrude(len)\
        .edges('>Z').fillet(3.0).edges('<Z').chamfer(3.0)
    hole = cq.Workplane('XY').circle(id / 2.0).extrude(holeDp)

    cap = cap.cut(hole)

    return cap


# TODO: Change this so that only the frequency is needed
def groundPlane(frequency, gp_dia):
    thickness = 5.0

    plane = cq.Workplane('XY').circle(gp_dia / 2.0).extrude(thickness)\
        .edges().fillet(thickness / 2.1)

    return plane


# Shortcut for outputting messages
def println(msg):
    FreeCAD.Console.PrintMessage(msg + "\r\n")

# CONSTANTS #
C = 299.792 * ureg['megameter/sec']  # speed of light
PI = math.pi                         # The 3.14 pi
ROM14DIA = 0.00162814 * ureg.meter   # Diameter of 14 ga Romex
termColor = (184, 115, 51, 0.0)      # The color of the aerial terminals

# Wavelength in a vacuum based on the given frequency
vac_wl = C / freq

# Our material affects the wave velocity and thus the dimensions of the
# aerials and ground plane
wavelength = None
if freq >= 600.0 * ureg.MHz and freq <= 1000.0 * ureg.MHz:
    wavelength = vac_wl * 0.93  # wavelength in copper
elif freq >= 300.0 * ureg.MHz and freq < 600.0 * ureg.MHz:
    wavelength = vac_wl * 0.83  # wavelength in RG-62
elif freq >= 30.0 * ureg.MHz and freq < 300.0 * ureg.MHz:
    wavelength = vac_wl * 0.66  # wavelength in RG-213
else:
    wavelength = vac_wl * 0.93  # wavelength in copper

# Aerial length - Pint does not understand the MHz to meters conversion
aerial_len = (1005 / (C.magnitude / wavelength.magnitude)) * ureg.feet
aerial_len = aerial_len.to(ureg.meter)
aerial_dia = aerial_len / PI  # Loop diameter based on aerial length

# TODO: Figure out what the proper ground plane diameter is for the frequency
gp_dia = wavelength / 2.0
# Distance between center of aerials and ground plane
gp_aerial_centers = wavelength / 8.0

# Figure out the mast size
mast_dia = None  # Body tube diameter (m)
if freq < 120.0 * ureg.MHz:
    mast_dia = 0.0508 * ureg.meter                          # 2" dia
elif freq > 120.0 * ureg.MHz and freq < 500 * ureg.MHz:
    mast_dia = 0.0381 * ureg.meter                          # 1-1/2" dia
else:
    mast_dia = 0.01905 * ureg.meter                         # 3/4" dia

# Figure out the points for our loop to go through, this defines the sweep path
p1 = (0.0, 0.0)                          # Loop connection point #1 with mast
p2 = (0.0, aerial_dia.to(ureg.mm).magnitude)  # The top of the aerial loop
p2o = (0.0, p2[1] + 5.0)  # Cheat a little of offset the loops at the top
p3 = (mast_dia.to(ureg.mm).magnitude, 0.0)  # Loop connection point #2 w/ mast
aerial_path1 = cq.Workplane('XZ').center(p1[0], p1[1]).threePointArc(p2, p3)
aerial_path2 = cq.Workplane('YZ').center(p1[0], p1[1]).threePointArc(p2o, p3)

# TODO: Base the shape and dimensions of the cross sections off the frequency
# Set up the sections for our sweep
aerial_sec1 = cq.Workplane('YZ').circle(ROM14DIA.to(ureg.mm).magnitude)
aerial_sec2 = cq.Workplane('XZ').circle(ROM14DIA.to(ureg.mm).magnitude)

# Do the sweeps and translate because freecad does not handle offset arc paths
aerial_sweep1 = aerial_sec1.sweep(aerial_path1)\
    .translate((-mast_dia.to(ureg.mm).magnitude / 2.0, 0.0, 0.0))
aerial_sweep2 = aerial_sec2.sweep(aerial_path2)\
    .translate((0.0, -mast_dia.to(ureg.mm).magnitude / 2.0, 0.0))

# Output some of the dimensions that we have calculated
println("Aerial length: {0}".format(aerial_len.to(ureg.mm)))
println("Aerial diameter: {0}".format(aerial_dia.to(ureg.mm)))

# Generate the aerial connectors for the frequency we are at
term1 = createConnector(freq).rotate((0, 0, 0), (0, 0, 1), 180)\
            .translate((15.0, 0.0, -2.5))
term2 = createConnector(freq).translate((-15.0, 0.0, -2.5))
term3 = createConnector(freq).rotate((0, 0, 0), (0, 0, 1), 90)\
            .translate((0.0, -15.0, -2.5))
term4 = createConnector(freq).rotate((0, 0, 0), (0, 0, 1), 270)\
            .translate((0.0, 15.0, -2.5))

base = pvcEndCap().translate((0.0, 0.0, -76.2 / 2.0 - 3.0))

# TODO: Do the units right
plane = groundPlane(freq, gp_dia.to(ureg.mm).magnitude)\
            .translate((0.0, 0.0, -gp_aerial_centers.to(ureg.mm).magnitude))

# Render everything
# show(aerial_path1)
# show(aerial_path2)
# show(aerial_sec1)
# show(aerial_sec2)
show(aerial_sweep1)
show(aerial_sweep2)
show(term1, termColor)
show(term2, termColor)
show(term3, termColor)
show(term4, termColor)
#show(base, (255, 255, 255, 0.0))
show(plane)
