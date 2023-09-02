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
        scale = float(
            input("Enter the scale to which the image is to be resampled: "))
        print("Resampling image...")
        resampledImg = resampleImage(img=grayImg, scale=scale)
        print("Resampling complete, saving resampled image as resampled_" + fileName + ".")
        saveImageRaw(img=resampledImg, fileName="resampled_" + fileName)
        print("Resampling back to original size...")
        resampledBackImg = resampleImage(
            img=resampledImg.tolist(), scale=1/scale)
        print(
            "Resampling complete, saving resampled image as resampledBack_" + fileName + ".")
        saveImageRaw(img=resampledBackImg,
                     fileName="resampledBack_" + fileName)
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


def saveImageRaw(img: np.ndarray, fileName: str):
    """
    Saves the provided image as a file with the provided file name

    Parameters:
    img (ndarray): A numpy array
    fileName (str): The name of the file to be saved
    """
    imageio.v2.imwrite(fileName, img)


def resampleImage(img: list, scale: float):
    """
    Resamples the image using linear interpolation to rescale to the 
    given scale. 

    Parameters: 
    img (list): A list of lists
    scale (float): The scale to which the result is created

    Returns:
    outputImage (nparray): A numpy array of the resampled image
    """
    imgArray = imageio.core.util.asarray(img)
    imgArray = imgArray.astype(np.uint8)
    height, width = imgArray.shape
    newHeight = int(height*scale)
    newWidth = int(width*scale)
    outputImage = np.zeros((newHeight, newWidth), dtype=np.uint8)
    for i in range(newHeight):
        for j in range(newWidth):
            x = j/scale
            y = i/scale
            x1 = int(np.floor(x))
            x2 = int(np.ceil(x))
            y1 = int(np.floor(y))
            y2 = int(np.ceil(y))
            if x1 == x2:
                x2 += 1
            if y1 == y2:
                y2 += 1
            if x2 >= width:
                x2 = width - 1
            if y2 >= height:
                y2 = height - 1
            Q11 = imgArray[y1, x1]
            Q12 = imgArray[y2, x1]
            Q21 = imgArray[y1, x2]
            Q22 = imgArray[y2, x2]
            dx1 = x - x1
            dx2 = x2 - x
            dy1 = y - y1
            dy2 = y2 - y
            denom = ((x2-x1)*(y2-y1))
            if denom == 0:
                denom = 1
            Q = (Q11*dx2*dy2 + Q21*dx1*dy2 + Q12*dx2 *
                 dy1 + Q22*dx1*dy1) / denom
            outputImage[i, j] = Q
    return outputImage


if __name__ == "__main__":
    main()
    # img = importImage('gateway.jpg')
    # print(img[0][0])
