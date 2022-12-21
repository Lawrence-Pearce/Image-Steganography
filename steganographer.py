from PIL import Image


def generateNewImage(message, imgFilePath, outputFilePath, characterIndexFilePath):
    """takes in a message, an image file path, an output file path, and a character index file path as arguments,
    and generates a new image with the message encoded into it."""

    def generateRGBFromMessage(message, characterIndexFilePath):
        with open(characterIndexFilePath) as f:  # get the characters
            characterLookup = f.readline()

        rgbMessage = []  # list containing all the rgb

        for i in range(round((len(message) / 3) + 0.5)):
            messageBlock = message[:3]
            currentRValue = 255  # note that value 255 is used as a "Nothing here" value
            currentGValue = 255
            currentBValue = 255

            currentRGBValueUpdate = "r"
            for character in messageBlock:
                numValue = characterLookup.find(character)
                if numValue == -1:
                    numValue = 254  # value for an unknown character

                if currentRGBValueUpdate == "r":
                    currentRValue = numValue
                    currentRGBValueUpdate = "g"

                elif currentRGBValueUpdate == "g":

                    currentGValue = numValue
                    currentRGBValueUpdate = "b"

                elif currentRGBValueUpdate == "b":
                    currentBValue = numValue

            rgbMessage.append((currentRValue, currentGValue, currentBValue))
            message = message[3:]

        return rgbMessage

    # open image and get the pixels
    originalImg = Image.open(imgFilePath)
    pixels = originalImg.load()
    lengthOfRow = originalImg.size[0] - 1

    messageRGB = generateRGBFromMessage(message, characterIndexFilePath)

    row = 0
    column = 0

    for rGBValue in messageRGB:  # iterate over all the new pixels
        if column > lengthOfRow:  # hit the end of the row, move to the next one
            column = 0
            row += 1

        pixels[column, row] = rGBValue
        column += 1

    originalImg.save(fp=outputFilePath)


def retrieveTextFromImage(imgFilePath, characterIndexFilePath):
    """Retrieves the rgb value from the specified image and converts to plain text using specified character index"""

    def retrieveRGBFromImage(imgFilePath):
        # open image and get the pixels
        image = Image.open(imgFilePath)
        pixels = image.load()
        size = image.size
        lengthOfRow = size[0] - 1
        messageRGB = []

        column = 0
        row = 0
        for i in range(size[0] * size[1]):
            if column > lengthOfRow:  # hit the end of the row, move to the next one
                column = 0
                row += 1

            pixel = pixels[column, row]
            messageRGB.append(pixel)
            column += 1
            if "255" in str(pixel):
                break

        return messageRGB

    rgbMessage = retrieveRGBFromImage(imgFilePath)  # get the list of pixels
    with open(characterIndexFilePath) as f:  # get the characters
        characterLookup = f.readline()

    textMessage = ""

    for entry in rgbMessage:  # iterate over all the pixels
        for value in entry:
            if value == 255:
                pass
            elif value == 254:
                textMessage += "□"  # unrecognised character
            else:
                textMessage += characterLookup[value]  # get the character substitute

    return textMessage
