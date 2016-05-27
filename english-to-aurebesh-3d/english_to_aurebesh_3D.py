import cadquery as cq
from Helpers import show
import glob

# This should really generate the wires for the letters and extrude them
# You must specify the full path to the letters directory holding STEP files
lettersPath = '/home/jwright/Documents/Mach_30/Projects/Apogee_III_Coin/letters/'

# Word to translate (all lower case)
toTranslate = "abcdefghijklmnopqrstuvwxyz."
# toTranslate = "jeremy"


def loadLetter(letter):
    # Collect all the STEP files related to this letter
    files = glob.glob(lettersPath + letter + '.step')

    letter = cq.importers.importStep(files[0])

    return letter.combine()

# Add a 3D aurebesh letter for each english letter in the string
i = 0
for c in toTranslate:
    if c == '.':
        curObject = loadLetter("period")
    else:
        curObject = loadLetter(c)

    curObject = curObject.translate((i * 20.0, 0.0, 0.0))
    i += 1

    show(curObject)
