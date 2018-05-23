import cadquery as cq

# All dimensions are in millimeters

# Sets the pitch of the header pin spacing
pin_spacing = 3.0

# Individual header pin dimensions
pin_width = 0.63
pin_height = 0.63
pin_length = 12.0
body_height = 2.5
body_length = 2.5

# Array of pin dimensions (rows by columns)
rows = 2
columns = 3

# The conductor
def generatePin():
    pin = cq.Workplane('XY').rect(pin_width, pin_height).extrude(pin_length) \
                            .faces('>Z or <Z').edges().chamfer(0.15)

    return pin

# Plastic body that helps hold sets of pins together
def generateBody():
    body = cq.Workplane('XY').workplane(offset=3.0).rect(body_height, pin_spacing) \
                             .extrude(body_length).faces('<Z').vertices() \
                             .rect(0.5, 0.5).cutBlind(body_length) \
                             .faces('<Z').workplane().rect(pin_width, pin_height) \
                             .cutThruAll()

    return body

# Generate the array of header pins by calling the generators and placing
# the returned pins in rows and columns
for row in xrange(rows):
    for col in xrange(columns):
        # Current header position
        pin_x = row * body_height
        pin_y = col * pin_spacing

        show_object(generatePin().translate((pin_x, pin_y, 0)), options={"rgba": (233, 214, 107, 0.0)})
        show_object(generateBody().translate((pin_x, pin_y, 0)), options={"rgba": (90, 90, 90, 0.0)})
