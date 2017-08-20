import cv2
import numpy as np


def open_image(image_path):  # TODO delete
    return cv2.imread(image_path)

def get_square_centers_from_board(image_path, num_squares, show_images=False):
    """Setup method to be used before processing board state in order
    to determine the center of each square in the image.

    :param image_path:
    :return:
    """
    im_array = open_image(image_path)
    height, width, channels = im_array.shape
    square_size_guess = height/num_squares
    square_centers = [[(-1, -1)]*num_squares]*num_squares

    # Get a grayscale version of the image
    # Would probably be useful to do this for R, G, and B, then use all TODO
    imgray = cv2.cvtColor(im_array, cv2.COLOR_BGR2GRAY)
    if show_images:
        show_image(imgray)

    # Blur the image - makes more sense if we had higher contrast btwn shapes
    # blurred = cv2.GaussianBlur(imgray, (5, 5), 0)
    # show_image(blurred)

    # Threshold the image (turn it white and black around a threshold value)
    threshold_value = 200  # could iteratively reduce TODO
    max_clamp = 255  # set value above threshold to this
    min_clamp = 0  # set value below threshold to this
    ret, thresh = cv2.threshold(imgray, threshold_value, max_clamp, min_clamp)

    # Get contours from the image
    cnt_im_array, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE,
                                                  cv2.CHAIN_APPROX_SIMPLE)
    if show_images:
        show_image(cnt_im_array)

    cv2.imwrite('/tmp/contours.png', cnt_im_array)

    for i, col in enumerate(cnt_im_array):
        white_pixels = [(i, h) for h in np.where(col > 0)]


    # # Get edges from the image
    # edges = cv2.Canny(cnt_im_array, 100, 200)
    # show_image(edges)

    # contours is a list of all the contours in the image, each an np array
    # of x coordinates of boundary points
    # print('got len contours = ', len(contours))  # 213 contours


    # for cnt in contours:
    #     img = cv2.drawContours(im_array, [cnt], 0, (0, 255, 0), 3)
    #     show_image(img)

    # cv2.destroyAllWindows()

def is_white(im_array, x, y):
    """

    :param im_array: array of arrays: length of outer array = width of image,
                     length of inner array = height of image
                     value = 0 or 255 (thresholded)
    :param x:
    :param y:
    :return:
    """
    print('checking im_array', x, y, im_array[x][y])
    return im_array[x][y] == 255

def show_image(im_array):
    cv2.imshow('image', im_array)
    cv2.waitKey(0)







def test():
    image = 'src/camera/captured_images/testimage.png'
    get_square_centers_from_board(image, 8)



if __name__ == '__main__':
    test()


