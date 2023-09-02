import imageio
import numpy as np


def main():
    while True:
        fileName = input("Enter the name of the file to be read: ")
        print("Reading file...")
        try:
            img = importImage(fileName=fileName)
        except:
            print("Error: File not found")
            break
        print("Converting to grayscale...")
        grayImg = convertToGrayscale(img=img)
        print("Conversion complete, saving grayscale image.")
        saveImage(img=grayImg, fileName="grayscale_" + fileName)
        print("Grayscale image saved as grayscale_" + fileName)
        choice = input("Would you like to convert another image? (y/n): ")
        if choice == "n":
            print("Thank you for using this tool.")
            break


def importImage(fileName: str):
    """
    Reads the image in the provided file name and returns the image as 
    a list of lists of lists, with each innermost list containing the 
    rgb values of a pixel

    Parameters: 
    fileName (str): The name of the file to be read

    Returns:
    imgList (list): A list of lists of lists
    """
    img = imageio.v2.imread(fileName)
    imgList = img.tolist()
    return imgList


def convertToGrayscale(img: list):
    """
    Process an image as a list of lists of lists and converts it to grayscale
    by taking the average value of the rgb values of each pixel

    Parameters:
    img (list): A list of lists of lists

    Returns:
    img (list): A list of lists. 
    """
    grayImage = []

    for row in img:
        grayRow = []
        for pixel in row:
            grayValue = int(sum(pixel)/3)
            grayRow.append(grayValue)
        grayImage.append(grayRow)
    return grayImage


def saveImage(img: list, fileName: str):
    """
    Saves the provided image as a file with the provided file name

    Parameters:
    img (list): A list of lists of lists
    fileName (str): The name of the file to be saved
    """
    grayArray = imageio.core.util.asarray(img)
    grayArray = grayArray.astype(np.uint8)
    print("conversion done !")
    imageio.v2.imwrite(fileName, grayArray)


if __name__ == "__main__":
    main()
    # img = importImage('gateway.jpg')
    # print(img[0][0])
