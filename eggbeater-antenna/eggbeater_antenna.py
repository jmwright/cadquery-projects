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
freq = 145.8 * ureg.MHz  # Receive frequency


# Shortcut for outputting messages
def println(msg):
    FreeCAD.Console.PrintMessage(msg + "\r\n")

# CONSTANTS #
C = 299.792 * ureg['meter/second']  # speed of light
PI = math.pi                        # The 3.14 pi
ROM14DIA = 0.00162814 * ureg.meter  # Diameter of 14 ga Romex

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
gp_dia = 2.0 * aerial_dia
# Distance between center of aerials and ground plane
gp_aerial_centers = 0.125 * wavelength

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

# Render everything
# show(aerial_path1)
# show(aerial_path2)
# show(aerial_sec1)
# show(aerial_sec2)
show(aerial_sweep1)
show(aerial_sweep2)
