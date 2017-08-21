"""
TODO: Instead, use image convolutions to really isolate the shapes
of the blue squares, and then use the contours and get the centers of
the shapes.


    dilate(src, kernel[, dst[, anchor[, iterations[, borderType[, borderValue]]]]]) -> dst
    .   @brief Dilates an image by using a specific structuring element.
    .
    .   The function dilates the source image using the specified structuring element that determines the
    .   shape of a pixel neighborhood over which the maximum is taken:
    .   \f[\texttt{dst} (x,y) =  \max _{(x',y'):  \, \texttt{element} (x',y') \ne0 } \texttt{src} (x+x',y+y')\f]
    .
    .   The function supports the in-place mode. Dilation can be applied several ( iterations ) times. In
    .   case of multi-channel images, each channel is processed independently.
    .
    .   @param src input image; the number of channels can be arbitrary, but the depth should be one of
    .   CV_8U, CV_16U, CV_16S, CV_32F or CV_64F.
    .   @param dst output image of the same size and type as src\`.

    .   @param kernel structuring element used for dilation; if elemenat=Mat(), a 3 x 3 rectangular
    .   structuring element is used. Kernel can be created using getStructuringElement
    .   @param anchor position of the anchor within the element; default value (-1, -1) means that the
    .   anchor is at the element center.
    .   @param iterations number of times dilation is applied.
    .   @param borderType pixel extrapolation method, see cv::BorderTypes
    .   @param borderValue border value in case of a constant border
    .   @sa  erode, morphologyEx, getStructuringElement
(END)

"""
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
    print('img height and widht = ', height, width)

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
    print('Got openCV image')
    if show_images:
        show_image(hsv)

    # Blur the image to reduce some of the noise
    # Blurring before the mask actually super increased the noise
    # blurred = cv2.GaussianBlur(hsv, (5, 5), 0)
    # if show_images:
    #     show_image(blurred)

    # Threshold the HSV image to get only colors within the range
    mask = cv2.inRange(hsv, lower, upper)
    print('Got mask')
    if show_images:
        show_image(mask)

    mask = cv2.GaussianBlur(mask, (5, 5), 0)
    if show_images:
        show_image(mask)


    # Dilate the image to make the blue spots bigger
    kernel = cv2.getStructuringElement((cv2.MORPH_DILATE), (4, 4))
    mask = cv2.dilate(mask, kernel, iterations=5)
    if show_images:
        show_image(mask)

    cnt_im_array, cnts, heirarchy = cv2.findContours(
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



    # print('got centers = ', centers)
    # center_dict = dedupe_centers(centers, height, num_squares)
    # print('got center dict = ', center_dict)
    # center_dict = insert_centers(center_dict, height, num_squares)
    # print('now center dict = ', center_dict)


    # for x, col in center_dict.items():
    #     for y in col:
    #         cv2.circle(mask, (x, y), 7, (255, 255, 255), -1)
    #         cv2.putText(mask, "center", (x - 20, y - 20),
    #                     cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    #     print('got center at ', cX, cY)
    #     if show_images:
    #         show_image(mask)

    print('Centers =', centers)
    return centers


# def dedupe_centers(centers, height, num_squares):
#     distance_threshold = 10.0  # euclidian pixel distance to dedupe
#
#     to_dedupe = defaultdict(list)
#     # Note - this is quadratic right now - there's certainly a way to
#     # optimize this, but I am just brute forcing it for POC
#     #
#     for center in centers:
#         for neighbor in centers:
#             if ((neighbor[0] - center[0]) ** 2 + (
#                 neighbor[1] - center[1]) ** 2) ** 0.5 < distance_threshold:
#                 to_dedupe[center].append(neighbor)
#     for dupe in to_dedupe:
#




def dedupe_centers_retired(centers, height, num_squares):
    """
    This is actually the wrong way to do it - it tries to combine everything
    into an axis aligned grid - but that's exactly why we're NOT doing it this
    way - we want to have exact placements for the centers.

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
    deduped_x = defaultdict(list)
    prev_val = sorted_keys[0]
    print 'now combining by x', sorted_keys
    for i, val in enumerate(sorted_keys[1:]):
        print '\t for i, val', i, val
        if val - prev_val > square_size - x_threshold:
            print '\t\t \033[36;1m far enough away. adding', prev_val, '\033[0m'
            deduped_x[prev_val].extend(c_dict[prev_val])
            prev_val = val
        else:
            print '\t\t \033[31;1m NOT far enough away. combining val', val, 'with prev_val', prev_val, '\033[0m'
            prev_val_col = c_dict[prev_val]  # store column to combine
            prev_val = prev_val + (val - prev_val) / 2
            # Store the combined lists of the previous y columns
            c_dict[prev_val] = c_dict[val] + prev_val_col
    # TODO figure out how to dedupe the last one...
    print('adding last prev_val', prev_val)
    deduped_x[prev_val] = c_dict[prev_val]
    res_x = deduped_x.keys()
    res_x.sort()
    print('res_x = ', res_x)

    res = {}
    # Do the same for each y column
    for x, col in deduped_x.items():
        sorted_col = col[:]
        sorted_col.sort()
        deduped_y = []
        prev_val = sorted_col[0]
        for i, val in enumerate(sorted_col[1:]):
            if val - prev_val > square_size - y_threshold:
                deduped_y.append(prev_val)
                prev_val = val
            else:
                prev_val = prev_val + (val - prev_val) / 2
        # TODO figure out how to dedupe the last one
        deduped_y.append(prev_val)
        res[x] = deduped_y
    return res

def insert_centers(found_centers, height, num_squares):
    # TODO use height in check?
    assert len(found_centers) == num_squares, 'Missing whole columns'
    threshold = 10
    full_rows = {x: col for x, col in found_centers.items()
                 if len(col) == num_squares}
    for x, col in found_centers.items():
        if len(col) == num_squares:
            continue
        if len(col) < num_squares:
            for i, val in enumerate(col):
                if len(col) == num_squares:  # TODO: better loop construction
                    break
                row_vals = [full[i] for full in full_rows.values()]
                avg_value = sum(row_vals) / float(len(col))
                if abs(avg_value - val) < threshold:
                    continue
                else:
                    bisect.insort(col, int(avg_value))
        assert len(col) == num_squares, 'incorrect number values for column'
        full_rows[x] = col
    return full_rows


def show_image(im_array):
    cv2.imshow('image', im_array)
    cv2.waitKey(0)
