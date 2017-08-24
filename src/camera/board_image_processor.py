"""
This module contains the main image processing class for the current
setup with the camera beneath the chess board. It uses colors
to distinguish among the pieces. It also has a setup mode to
initialize the location of the center of each square on the board.
"""
import cv2
import numpy as np
import bisect
import operator
from src.camera.setup_board import get_square_centers_from_board

# TODO: refactor to put all code and magic numbers in here, but for now
#       just importing the other working modules


class BoardProcessor:
    """
    You can poll the BoardProcessor at any time to get the current
    state from the last image it successfully processed.
    """

    def __init__(self, debug_image_mode=False):
        self._num_squares = 8  # Width of board, standard chess board
        self._contour_len_threshold = 10  # Perimeter of shape in pixels
        self._centers = []
        self._cur_state = None
        self._debug_images = debug_image_mode
        self._color_map = {'WB': (np.array([110, 50, 50]),  # light blue
                                  np.array([130, 255, 255])),
                           # Also BK with dot
                           'BB': (np.array([222, 50, 50]),  # dark blue
                                  np.array([243, 255, 255])),
                           # Also BR with dot
                           'WP': (np.array([57, 50, 50]),  # green
                                  np.array([96, 255, 255])),
                           # also BQ with dot
                           'WR': (np.array([110, 50, 50]),  # purple
                                  np.array([130, 255, 255])),
                           # also WK with dot - this seems to be off
                           'BP': (np.array([351, 50, 50]),  # red
                                  np.array([360, 255, 255])),
                           # also WQ with dot
                           'WP': (np.array([25, 50, 50]),  # yellow
                                  np.array([55, 255, 255])),
                           # also WK with dot
                           }

    @staticmethod
    def _open_image(image_path):
        return cv2.imread(image_path)

    def _show_image(self, im_array, title='image'):
        if self._debug_images:
            cv2.imshow(title, im_array)
            cv2.waitKey(0)

    def setup_board(self, image_path):
        """Get the center of each square from a given board image,
        corresponding to it's i-j position in a 2d array (representing
        the board state).
        """
        self._centers = self._sort_centers(
            get_square_centers_from_board(image_path, self._num_squares))

    def _sort_centers(self, centers):
        """Sort the centers into a 2D array.

        Take the (min, min), and then for each point get the vector from the
        min to that point. Sort the vectors by length, and multiply by the
        jacobian. Just kidding. I'm not clever.

        If everything were not warped, we would be making a transformation
        from (i*w, j*h) = i, j     -> However, things are warped. So. Nope.

        Alright, what if we just sort by y, break it into rows of 8, then
        sort by x, and then store point -> (i, j) pair

        Return:
            The 2D array of the center points, in their proper i,j position.
        """
        center_dict = {}
        center_array = []  # purely for quick visualization and debugging
        sorted_by_y = centers[:]
        sorted_by_y.sort(key=operator.itemgetter(1))
        for i in range(self._num_squares):
            row = sorted_by_y[i*self._num_squares:(i+1)*self._num_squares]
            row.sort()
            for j, point in enumerate(row):
                center_dict[point] = (i, j)
            center_array.append(row)
        if self._debug_images:
            print 'Got centers of board:'
            for row in center_array:
                print row
        return center_dict

    def _point_within_square(self, shape_center, half_square_threshold):
        """Get the i,j coordinate of the square center closest to this point
        and test whether it is within the half-square threshold"""
        dists = []
        for square_center in self._centers:
            bisect.insort(dists, (np.linalg.norm(np.array(square_center) -
                                                 np.array(shape_center)),
                                  square_center))
        assert len(dists) > 0, ('Got no dists from ', str(shape_center),
                                str(self._centers))
        if dists[0][0] < half_square_threshold:
            print('dists [0] = ', dists[0], '< ', half_square_threshold)
            return self._centers[dists[0][1]]

    def get_board_state(self, image_path):
        """Return the state of the board (in terms of pieces in each
        square) from the given board image.

        Centers are np.arrays, which have point-like behavior for subtraction.
        """
        image = self._open_image(image_path)
        height, width, channels = image.shape
        half_square_threshold = height / (self._num_squares * 2)
        # Fun python fact - the code commented below makes copies of each list
        # board = [ [0]*self._num_squares ]*self._num_squares
        board = [ [None for x in xrange(self._num_squares)]
                  for x in xrange(self._num_squares)]
        # Get a convolved image for each color in our color map
        for piece, color_range in self._color_map.items():
            filtered_image = self._get_convolved_image(image, color_range)
            if self._debug_images:
                print('Now for piece', piece, 'color range', color_range)
                self._show_image(filtered_image, 'convolved')
            # I love O(n**2). As sweet as microwaved bananas.
            for shape_center in self._get_centers(filtered_image):
                print('Now for shape center', shape_center)
                coords = self._point_within_square(shape_center,
                                                   half_square_threshold)
                print('coordinate = ', coords)
                if coords is not None:
                    board[coords[0]][coords[1]] = piece
        return board

    def _get_convolved_image(self, image, color_range):
        """Get an image mask filtered to just the locations of a certain
        color within the provided color range.
        """
        lower, upper = color_range
        # put into HSV color space because hue is more reliable - RGB varies
        # based on brightness - so we would have lots of possible values
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        self._show_image(hsv, 'HSV')

        # Threshold the HSV image to get only colors within the range
        mask = cv2.inRange(hsv, lower, upper)  # TODO is it actually more
                                               #      optimal to overwrite?
        self._show_image(mask, 'Masked by ' + str(lower) + str(upper))

        # Blur the mask - this helps bring out more of the colored pixels
        blurred = cv2.GaussianBlur(mask, (5, 5), 0)
        self._show_image(blurred, 'Blurred')

        # Dilate the image to make the blue spots bigger
        # TODO: figure out which dilate configuration makes the best shapes
        kernel = cv2.getStructuringElement((cv2.MORPH_DILATE), (4, 4))
        dilated = cv2.dilate(blurred, kernel, iterations=5)
        self._show_image(dilated, 'Dilated')

        # TODO: threshold one more time
        thresh = 127
        im_bw = cv2.threshold(dilated, thresh, 255, cv2.THRESH_BINARY)[1]
        self._show_image(im_bw, 'Threshold')

        return im_bw

    def _get_centers(self, image):
        """Image needs to be a masked image, easily contourizable."""
        centers = []
        cnt_im_array, contours, heirarchy = cv2.findContours(
            image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Filter out small contours around noise
        cnts = [c for c in contours if len(c) > self._contour_len_threshold]
        for c in cnts:
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
            cv2.drawContours(image, [c], -1, (0, 255, 0), 2)
            cv2.circle(image, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(image, "center", (cX - 20, cY - 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        self._show_image(image, 'Centers')
        return centers

