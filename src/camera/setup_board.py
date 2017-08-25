"""
This module uses OpenCV to process a setup state image in order to find the
centers of each square. The expectation is that blue sticky notes will be
cut up into squares and placed at the center of each square.

"""
import cv2
import numpy as np
import bisect

def open_image(image_path):  # TODO delete
    return cv2.imread(image_path)

def get_square_centers_from_board(image_path, num_squares, show_images=False):
    """

    TODO: move this all over into board_image_processor

    :param state:
    :param i:
    :param j:
    :param color_map:
    :return:
    """
    image = open_image(image_path)
    height, width, channels = image.shape

    contour_len_threshold = 5

    centers = []

    # Hue range [0,179], Saturation range is [0,255] and Value range is [0,255]
    lower = np.array([100, 10, 50])  # light blue
    upper = np.array([160, 150, 255]) # dark blue

    print('\033[33;1m SETUP MODE: Now processing image to get square '
          'centers\033[0m')

    # put into HSV color space because hue is more reliable - RGB varies
    # based on brightness - so we would have lots of possible values
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    if show_images:
        show_image(hsv)

    # Threshold the HSV image to get only colors within the range
    mask = cv2.inRange(hsv, lower, upper)
    if show_images:
        show_image(mask)

    # Blur the mask - this helps bring out some of the darker stickies
    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    if show_images:
        show_image(mask)

    # Dilate the image to make the blue spots bigger
    # TODO: figure out which dilate configuration makes the best shape
    kernel = cv2.getStructuringElement((cv2.MORPH_DILATE), (4, 4))
    mask = cv2.dilate(mask, kernel, iterations=5)
    if show_images:
        show_image(mask)

    cnts, heirarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter out small contours around noise
    cnts = [c for c in cnts if len(c) > contour_len_threshold]

    print "I found %d %s shapes" % (len(cnts), 'blue')
    # loop over the contours and filter out ones that are too small
    for c in cnts:
        # # draw the contour and show it
        # cv2.drawContours(mask, [c], -1, (230, 255, 0), 2)

        # compute the center of the contour
        M = cv2.moments(c)
        denom = M["m00"]
        if denom == 0:
            continue
        cX = int(M["m10"] / denom)
        cY = int(M["m01"] / denom)

        # Insert center into our list of centers
        bisect.insort(centers, (cX, cY))

        # draw the contour and center of the shape on the image
        cv2.drawContours(mask, [c], -1, (0, 255, 0), 2)
        cv2.circle(mask, (cX, cY), 7, (255, 255, 255), -1)
        cv2.putText(mask, "center", (cX - 20, cY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    if show_images:
        show_image(mask)

    return centers


def show_image(im_array, title='image'):
    cv2.imshow(title, im_array)
    cv2.waitKey(0)
