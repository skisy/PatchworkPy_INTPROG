#-------------------------------------------------------------------------------
# Autumn Assignment - Patchwork Sampler
#
# 660273
# Autumn Teaching Block 2012
#-------------------------------------------------------------------------------
from graphics import *

def main():
    width, height, colourSequence = getInputs()
    patchworkWin = GraphWin("Patchwork Magic", width * 100, height * 100)
    patchColourList, patchList = drawPatchworkPattern(patchworkWin, height,
                                                        width, colourSequence)
    # Allow user to click a patch to change colour as many times as desired
    while True:
        try:
            click = patchworkWin.getMouse()
            changePatchColour(click, patchList, width, height,
                                                colourSequence, patchColourList)
        # Exception handler for GraphicsError raisesd by graphics.py if getMouse
        # is attempted within a closed window, (i.e. if user clicks OS exit button)
        except GraphicsError:
            break

def getInputs():
    colourSequence = []
    # Get and validate dimensions
    width = getValidDimension("across")
    print("You entered the width as {0} patches".format(width))
    height = getValidDimension("down")
    print("You entered the height as {0} patches".format(height))
    # Get and validate 4 colours, append each to colourSequence list
    print("Valid colours are: red, blue, yellow, green, magenta, orange, cyan")
    print("You may choose each colour only once")
    for colourIndex in range(1, 5):
        colourSequence.append(getValidColour(colourIndex, colourSequence))
    return width, height, colourSequence

def drawPatchworkPattern(win, height, width, colourSequence):
    patchList = []
    patchColourList = []            # colourIndex for each patch is appended
                                    # to list to be used by changePatchColour
    colourIndex = 0
    for patchY in range(height):
        patchPositionY = patchY * 100       # Coord for top of each row (y)
                                            # acts as y offset value for patches
        for patchX in range(width):
            patchPositionX = patchX * 100   # Coord for left of each column (x)
                                            # acts as x offset value for patches
            colour = colourSequence[colourIndex]
            # Draw inner patches
            if patchY >= 1 and patchY <= height - 2 and patchX >= 1 and \
                                                    patchX <= width - 2:
                patch = drawInnerPatch(win, patchPositionX,
                                patchPositionY, colour)
                patchList.append(patch)     # Each patch is appened to patchList
            # Draw outer patches
            else:
                patch = drawOuterPatch(win, patchPositionX, patchPositionY,
                                 colour)
                patchList.append(patch)
            # List is 4 items long, if index at end of list then reset index
            if colourIndex == 3:
                colourIndex = 0
            else:
                colourIndex = colourIndex + 1       # Cycles through colours
            patchColourList.append(colour)
    return patchColourList, patchList

def changePatchColour(click, patchList, width, height, colourSequence, patchColourList):
    clickX = click.getX() // 100
    clickY = click.getY() // 100
    patchNumber = 0             # Will give position in patchList of patch
    for y in range(height):
        for x in range(width):
            # Locates clicked patch, compares click coords & patch top left coords
            if clickY == y and clickX == x:
                # Loops for each object in patch
                for patch in range(len(patchList[patchNumber])):
                        # Get patch colour
                        oldColour = patchColourList[patchNumber]
                        # Find colour in colourSequence list
                        colourIndex = colourSequence.index(oldColour)
                        # Reset index if at boundary
                        if colourIndex == 3:
                            colourIndex = 0
                        else:
                            colourIndex = colourIndex + 1
                        # Set new colour for patch
                        newColour = colourSequence[colourIndex]
                        # Define patch in list as variable
                        obj = patchList[patchNumber][patch]
                        # Set object to new colour
                        obj.setFill(newColour)
                # Update list to reflect colour change
                patchColourList[patchNumber] = newColour
            patchNumber = patchNumber + 1

def getValidDimension(direction):
    valid = False
    while valid == False:
        dimension = input(
            "Enter number of patches {0} between 4 and 9 inclusive: ".format(direction))
        # isInt function checks input is integer - returns boolean to isInteger
        isInteger = isInt(dimension)
        if isInteger == True:
            dimension = int(dimension)

            # dimension inputs must be between 4 and 9
            if dimension >= 4 and dimension <= 9:
                valid = True
            else:
                print("'{0}' is not between 4 and 9 inclusive!".format(dimension))
    return dimension

def isInt(value):
    try:    # attempt type cast of value to int
        int(value)
        isInteger = True
    except ValueError: # catch ValueError exception (inappropriate value for type)
        print("You must enter an integer, '{0}' is not an integer!".format(value))
        isInteger = False
    # If non-numerical string or float value entered ValueError occurs because not int
    return isInteger

def getValidColour(colourIndex, colourSequence):
    validColours = ["red", "blue", "yellow", "green", "magenta", "orange", "cyan"]
    colour = input("Enter colour {0} (type 'help' for list of colours):".format(
                                                                    colourIndex))
    colour = colour.lower()
    while colour == "help":
        print("Valid colours are: red, blue, yellow, green, magenta, orange, cyan")
        colour = input("Enter colour {0} (type 'help' for list of colours):".format(
                                                                    colourIndex))
    colourExists = colour in colourSequence # Looks for colour in colourSequence,
                                            # returns boolean
    valid = colour in validColours      # Looks to see if colour is valid
                                        # (exists in list)
    # Requests new input until input is valid colour and has not already been entered
    while colourExists == True or valid == False:
        colour = input(
        "Please enter a valid colour {0}, that you haven't already entered: ".format(
                                                                    colourIndex))
        colour = colour.lower()
        colourExists = colour in colourSequence
        valid = colour in validColours
    print("You chose the colour {0} as colour {1} in the sequence".format(colour,
                                                                     colourIndex))
    return colour

def drawOuterPatch(win, patchPositionX, patchPositionY, colour):
    patch = []
    squareSize = 10
    patchHeight = 100
    # Two opposite corners defined for each square
    # First square drawn top right corner
    # Each square drawn 10 down, 10 left from previous
    for square in range(1, 11):
        squareTopLeft = Point(patchHeight - squareSize * square + patchPositionX,
                                squareSize * (square - 1) + patchPositionY)
        squareBottomRight = Point(patchHeight - squareSize * (square - 1) +
                                patchPositionX, squareSize * square + patchPositionY)
        rectangle = drawRectangle(win, squareTopLeft, squareBottomRight, colour, "black")
        patch.append(rectangle)     # Each object appended to list patch
    return patch

def drawInnerPatch(win, patchPositionX, patchPositionY, colour):
    patch = []
    patchWidth = 100
    lineXYDistance = 10     # Start & end point difference of line is 10
    # Draws 9 lines across width of patch, 10 px spacing
    # First line 10 px down from top of patch
    for y in range(1, 10):
        horizontalLine = drawLine(win, Point(patchPositionX, 10 * y + patchPositionY),
                         Point(patchWidth + patchPositionX, 10 * y + patchPositionY),
                         colour)
        patch.append(horizontalLine)
    for y in range(5):
        for x in range(10):
            # rightSlopingLine start at top of patch
            rightSlopingLine = drawLine(win, Point(10 * x + patchPositionX,
                                        20 * y + patchPositionY),
                                        Point(10 * x + lineXYDistance  + patchPositionX,
                                        20 * y + lineXYDistance + patchPositionY),
                                        colour)
            # leftSlopingLine start 10 down from top of patch
            leftSlopingLine = drawLine(win, Point(10 * x + lineXYDistance +
                                        patchPositionX, 20 * y + 10 + patchPositionY),
                                        Point(10 * x + patchPositionX,
                                        20 * y + lineXYDistance + 10 + patchPositionY),
                                        colour)
            patch.append(rightSlopingLine)
            patch.append(leftSlopingLine)
    return patch

def drawLine(win, point1, point2, colour):
    line = Line(point1, point2)
    line.setOutline(colour)
    line.draw(win)
    return line

def drawRectangle(win, point1, point2, fillColour, outlineColour):
    rectangle = Rectangle(point1, point2)
    rectangle.setFill(fillColour)
    rectangle.setOutline(outlineColour)
    rectangle.draw(win)
    return rectangle

main()


