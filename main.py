import steganographer

# hide text
steganographer.generateNewImage(message="This is an example message",
                                imgFilePath="input\\canvas.png",
                                outputFilePath="output\\messageCanvas.png",
                                characterIndexFilePath='characterLookup.txt')

# retrieve text from the image just made
print(steganographer.retrieveTextFromImage(imgFilePath="output\\messageCanvas.png",
                                           characterIndexFilePath='charactersLookup.txt'))
