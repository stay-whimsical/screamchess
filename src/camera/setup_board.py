import cv2
import numpy as np
import bisect
from collections import Counter, defaultdict


def open_image(image_path):  # TODO delete
    return cv2.imread(image_path)

def get_square_centers_from_board(image_path, num_squares, show_images=False):
    """

    TODO: less copy pasta from process_board

    :param state:
    :param i:
    :param j:
    :param color_map:
    :return:
    """
    image = open_image(image_path)
    height, width, channels = image.shape

    contour_len_threshold = 10
    num_pixel_threshold = 15


    centers = []

    # Hue range [0,179], Saturation range is [0,255] and Value range is [0,255]
    lower = np.array([100, 10, 50])  # light blue
    upper = np.array([150, 150, 255]) # dark blue

    print('\033[33;1m SETUP MODE: Now processing image to get square '
          'centers\033[0m')

    # put into HSV color space because hue is more reliable - RGB varies
    # based on brightness - so we would have lots of possible values
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    print('Got openCV image')
    if show_images:
        show_image(hsv)

    # Threshold the HSV image to get only colors within the range
    mask = cv2.inRange(hsv, lower, upper)
    print('Got mask')
    if show_images:
        show_image(mask)

    cnt_im_array, cnts, heirarchy = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    print "I found %d %s shapes" % (len(cnts), 'blue')
    # loop over the contours and filter out ones that are too small
    for c in cnts:
        print 'len contour = ', len(c)
        # Filter out small contours around noise
        if len(c) < 4:
            continue
        # draw the contour and show it
        cv2.drawContours(mask, [c], -1, (230, 255, 0), 2)

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
    print('got center at ', cX, cY)
    show_image(mask)

    print('Centers =', centers)


def dedupe_centers(centers, height, num_squares):
    """

    :param centers:
    :return: Dictionary of x vals to column of y values
    """
    square_size = float(height/num_squares)
    x_threshold = 5  # pixels to filter for noise
    y_threshold = 5
    c_dict = defaultdict(list)
    for x, y in centers:
        c_dict[x].append(y)
    sorted_keys = c_dict.keys()[:]
    sorted_keys.sort()
    # combine by x
    print('Starting with x_vals', sorted_keys)
    deduped_x = defaultdict(list)
    prev_val = sorted_keys[0]
    for i, val in enumerate(sorted_keys[1:]):
        print('now examining ', val, 'vs', prev_val)
        if val - prev_val > square_size - x_threshold:
            print('they are distant enough, adding prev_val')
            deduped_x[prev_val].extend(c_dict[prev_val])
            prev_val = val
        else:
            prev_val_col = c_dict[prev_val]  # store column to combine
            prev_val = prev_val + (val - prev_val) / 2
            print('they are too close, combining to', prev_val)
            # Store the combined lists of the previous y columns
            c_dict[prev_val] = c_dict[val] + prev_val_col
    # TODO figure out how to dedupe the last one...
    deduped_x[prev_val] = c_dict[prev_val]
    res_x = deduped_x.keys()
    res_x.sort()
    print('Got deduped x_vals', [(r, c_dict[r]) for r in res_x])

    res = {}
    # Do the same for each y column
    for x, col in deduped_x.items():
        sorted_col = col[:]
        sorted_col.sort()
        print('now deduping', sorted_col)
        deduped_y = []
        prev_val = sorted_col[0]
        for i, val in enumerate(sorted_col[1:]):
            if val - prev_val > square_size - x_threshold:
                deduped_y.append(prev_val)
                prev_val = val
            else:
                prev_val = prev_val + (val - prev_val) / 2
        # TODO figure out how to dedupe the last one
        deduped_y.append(prev_val)
        print('got deduped column', deduped_y)
        res[x] = deduped_y
    print('got res', res)
    return res

    #
    # sorted_distances = distances.keys()[:]
    # sorted_distances.sort()
    # for index, distance in enumerate(sorted_distances):
    #     if distance < square_size - x_threshold:
    #         # Get indices to delete them
    #         lower = sorted_keys[distances[distance]]
    #         upper = sorted_keys[distances[distance] + 1]
    #         x_mid = (upper + lower) / 2.0  # Should also be distance/2
    #         # Concatenate the two lists
    #         c_dict[x_mid] = c_dict[lower][:] + c_dict[upper][:]
    #         del c_dict[lower]
    #         del c_dict[upper]
    # x_vals = c_dict.keys()
    # x_vals.sort()
    # print('Got x combined to ', x_vals)
    #
    # for x_val, column in c_dict.items():
    #     print('Starting with ', column)
    #     # combine by y
    #     sorted_col = column[:]
    #     sorted_col.sort()
    #     deduped_col = []
    #     for i, val in enumerate(sorted_col[1:]):
    #         distance = val - sorted_col[i-1]
    #         if distance < square_size - y_threshold:
    #             y_mid = distance/2.0
    #             deduped_col.append(y_mid)
    #     c_dict[x_val] = deduped_col
    #     print('Got y combined to', deduped_col)
    #
    # print('Length = ', sum([len(col) for col in c_dict.values()]))
    # return c_dict
    #







def get_square_centers_from_board_retired(image_path, num_squares,
                                          show_images=False):
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
    # TODO: remove the below images
    #image = 'src/camera/captured_images/testimage.png'
    #image = 'src/camera/captured_images/black_squares.png'

    image = 'src/camera/captured_images/blue_squares.png'
    get_square_centers_from_board(image, 8)



if __name__ == '__main__':
    test()


