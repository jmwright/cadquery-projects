import cadquery as cq
from Helpers import show
import glob

# This should really generate the wires for the letters and extrude them
# You must specify the full path to the letters directory holding STEP files
lettersPath = '/home/jwright/Documents/CadQuery/Projects/cadquery-projects/english-to-aurebesh-3d/letters/'

# Word to translate (all lower case)
toTranslate = "abcdefghijklmnopqrstuvwxyz."


def loadLetter(letter):
    # Collect all the STEP files related to this letter
    files = glob.glob(lettersPath + letter + '.step')

    letter = cq.importers.importStep(files[0])

    return letter.combine()

# Add a 3D aurebesh letter for each english letter in the string
totalWidth = 0.0
widthDiff = 0.0
for c in toTranslate:
    if c == '.':
        curLetter = loadLetter("period")
    else:
        curLetter = loadLetter(c)

    # Helps keep the letter spacing consistent, even when letter sizes vary
    widthDiff = 22 - curLetter.val().BoundingBox().DiagonalLength

    # Move the letters so they're consistently spaced
    totalWidth += curLetter.val().BoundingBox().DiagonalLength\
        + widthDiff / 2.0
    curLetter = curLetter.translate((totalWidth + widthDiff, 0.0, 0.0))

    show(curLetter)
