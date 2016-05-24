import math
import FreeCAD
import cadquery as cq
from Helpers import show

# Driving parameter
freq = 145.8  # MHz
aerial_material = 'cu'  # Aerial material (cu, rg-62, rg-213)

# DO NOT CHANGE ANYTHING FROM HERE DOWN #


# Shortcut for outputting messages
def println(msg):
    FreeCAD.Console.PrintMessage(msg + "\r\n")

# Constants
C = 299.792  # speed of light (m/sec)

# Derived variables
vac_wl = C / freq        # wavelength in a vacuum (m)
cu_wl = vac_wl * 0.93          # wavelength in copper (m)
rg62_wl = vac_wl * 0.83        # wavelength in RG-62 (m)
rg213_wl = vac_wl * 0.66       # wavelength in RG-213 (m)

# Our material affects the wave velocity and thus the dimensions
wavelength = None
if aerial_material == "cu":
    wavelength = cu_wl
elif aerial_material == "rg-62":
    wavelength = rg62_wl
elif aerial_material == "rg-213":
    wavelength = rg213_wl
else:
    wavelength = cu_wl

# Relationships
aerial_len = (1005 / (C / wavelength)) * 0.3048  # Aerial length (m)
aerial_dia = aerial_len / math.pi  # The resulting diameter of the aerials
gp_dia = 2.0 * aerial_dia        # Ground plane dia = 2x aerial dia
gp_aerial_centers = 0.125 * wavelength     # Distance between center of aerials and ground plane (m)
base_dia = gp_dia / 2.0                    # The diameter of the antenna base

# Figure out the body tube size
mast_dia = None  # Body tube diameter (m)
if freq < 120.0:
    mast_dia = 0.0508  # 2" dia
elif freq > 120.0 and freq < 500:
    mast_dia = 0.0381  # 1-1/2" dia
else:
    mast_dia = 0.01905  # 3/4" dia

# TODO: Figure out why the aerials won't center around the origin
# Figure out the points for our loop to go through, this defines the sweep path
p1 = (mast_dia / 2.0, 0.0)   # Loop connection point #1 with mast
p2 = (0, aerial_dia)         # The top of the aerial loop
p3 = (-mast_dia / 2.0, 0.0)  # Loop connection point #2 with mast
aerial_path1 = cq.Workplane('XZ').center(p1[0], p1[1]).threePointArc(p2, p3)
aerial_path2 = cq.Workplane('YZ').center(p1[0], p1[1]).threePointArc(p2, p3)

# TODO: Base the shape and dimensions of the cross sections off the frequency
# Set up the sections for our sweep
# aerial_sec1 = cq.Workplane('YZ').circle(0.00162814).translate((p1[0], 0, -0.0007)).rotate((0, 0, 0), (0, 1, 0), -5)
aerial_sec1 = cq.Workplane('YZ').circle(0.00162814).translate((p1[0], 0, 0))
aerial_sec2 = cq.Workplane('XZ').circle(0.00162814).translate((0, p1[0], 0))

# Do the sweeps
aerial_sweep1 = aerial_sec1.sweep(aerial_path1)
aerial_sweep2 = aerial_sec2.sweep(aerial_path2)

# Output some of the dimensions that we have calculated
println("Aerial length: " + str(round(aerial_len, 5)) + " m")
println("Aerial diameter: " + str(round(aerial_dia, 5)) + " m")

# Render everything
show(aerial_path1)
show(aerial_path2)
show(aerial_sec1)
show(aerial_sec2)
show(aerial_sweep1)
show(aerial_sweep2)
