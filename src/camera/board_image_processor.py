"""
This module contains the main image processing class for the current
setup with the camera beneath the chess board. It uses colors
to distinguish among the pieces. It also has a setup mode to
initialize the location of the center of each square on the board.
"""
import cv2
import numpy as np
import bisect
import math
import operator
from PIL import Image
from camera.setup_board import get_square_centers_from_board

# TODO: refactor to put all code and magic numbers in here, but for now
#       just importing the other working modules

# TODO put this in the class
def open_image(image_path):
    """Simple wrapper to load an image obj from an image file."""
    with open(image_path, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
    return image

class BoardProcessor:
    """
    You can poll the BoardProcessor at any time to get the current
    state from the last image it successfully processed.
    """

    def __init__(self, debug_image_mode=False):
        self._num_squares = 8  # Width of board, standard chess board
        self._contour_len_threshold = 10  # Perimeter of shape in pixels
        self._centers = []
        self._cur_state = [ [None for x in xrange(self._num_squares)] for x in xrange(self._num_squares) ]
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

    def set_color_map(self, color_map):
        self._color_map = color_map

    def _cache_pil_im(self, image_path):
        self._pil_im = open_image(image_path)

    def _open_image(self, image_path):
        self._cache_pil_im(image_path)
        return cv2.imread(image_path)

    def _show_image(self, im_array, title='image', show_this_image=False):
        if self._debug_images or show_this_image:
            cv2.imshow(title, im_array)
            cv2.waitKey(0)

    def update_state(self, image):
        state = self.get_board_state(image)
        if state != self._cur_state:
            self._cur_state = state

    def get_cur_state(self):
        return self._cur_state

    def setup_board(self, image_path):
        """Get the center of each square from a given board image,
        corresponding to it's i-j position in a 2d array (representing
        the board state).
        """
        self._centers = self._sort_centers(
            get_square_centers_from_board(image_path, self._num_squares))

    def _setup_default_board(self):
        """For the case when we don't have time to put all the little
        squares.
        
        I apologize for the formatting but I am a monster."""
        self._centers={(387, 440): (7, 6), (190, 192): (3, 3), (82, 384): (6, 1), (210, 445): (7, 3), (21, 383): (6, 0), (327, 444): (7, 5), (20, 135): (2, 0), (71, 256): (4, 1), (477, 130): (2, 7), (452, 437): (7, 7), (196, 258): (4, 3), (460, 316): (5, 7), (20, 78): (1, 0), (74, 319): (5, 1), (397, 65): (1, 6), (69, 138): (2, 1), (73, 79): (1, 1), (331, 8): (0, 5),(455, 379): (6, 7), (25, 19): (0, 0), (326, 126): (2, 5),(198, 67): (1, 3), (129, 133): (2, 2), (139, 321): (5, 2),(194, 128): (2, 3), (269, 320): (5, 4), (265, 7): (0, 4),(132, 10): (0, 2), (454, 9): (0, 7), (340, 184): (3, 5),(203, 386): (6, 3), (395, 9): (0, 6), (273, 445): (7, 4),(200, 9): (0, 3), (263, 62): (1, 4), (332, 320): (5, 5),(458, 65): (1, 7), (140, 388): (6, 2), (145, 442): (7, 2),(131, 71): (1, 2), (394, 253): (4, 6), (338, 389): (6, 5),(17, 260): (4, 0), (330, 255): (4, 5), (269, 385): (6, 4),(136, 259): (4, 2), (32, 437): (7, 0), (16, 202): (3, 0),(398, 190): (3, 6), (76, 13): (0, 1), (21, 321): (5, 0),(262, 129): (2, 4), (69, 199): (3, 1), (395, 387): (6, 6),(390, 126): (2, 6), (399, 317): (5, 6), (264, 190): (3, 4),(262, 258): (4, 4), (130, 194): (3, 2), (460, 253): (4, 7),(458, 188): (3, 7), (89, 439): (7, 1), (198, 321): (5, 3),(330, 66): (1, 5)}


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
            if self._debug_images:
                print('dists [0] = ', dists[0], '< ', half_square_threshold)
            return self._centers[dists[0][1]]

    def _shape_in_square(self, image):
        centers = self._get_centers(image)
        if len(centers) > 0:
            return True
        return False


    def get_board_state(self, image):
        """Breaks the image into an image per square, and looks at a radius around the center
        of each square to see if it has a piece in it. 

        Returns the board state
        """
        if not self._centers:
            self._setup_default_board()
        height, width, channels = image.shape
        radius = height/(self._num_squares*2)
        board = [ [None for x in xrange(self._num_squares)] for x in xrange(self._num_squares)]
        for pixels, indices in self._centers.items():
            
            cropped = self._pil_im.crop((pixels[0] - radius, pixels[1] - radius, pixels[0] + radius, pixels[1] + radius))

            im = np.array(cropped)
            
            if self._get_circle_in_square(im):
                board[indices[0]][indices[1]] = True

#            for piece, color_range in self._color_map.items():
#                #filtered_square = self._get_convolved_image(im, color_range)
#                if self._debug_images:
#                    self._show_image(filtered_square, 'filtered square')
#                if self._shape_in_square(filtered_square):
#                    # just early out - don't check the other color options...
#                    # may want to change this later...we'll see how noisy it is
#                    board[indices[0]][indices[1]] = piece
        return board


    def get_board_state_retired(self, image):
        """Return the state of the board (in terms of pieces in each
        square) from the given board image.

        Centers are np.arrays, which have point-like behavior for subtraction.
        """
        if not self._centers:
            self._setup_default_board()
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
                if self._debug_images:
                    print('Now for shape center', shape_center)
                coords = self._point_within_square(shape_center,
                                                   half_square_threshold)
                if self._debug_images:
                    print('coordinate = ', coords)
                if coords is not None:
                    board[coords[0]][coords[1]] = piece
        return board

    def _get_circle_in_square(self, im):

        imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        #circle = self._get_circle(imgray)
        self._show_image(imgray)
#        Nighttime 
#        ret,thresh = cv2.threshold(imgray,182,222,0)
        ret,thresh = cv2.threshold(imgray,100,160,0)
        thresh = cv2.bitwise_not(thresh)
        # print 'thresh = ', thresh
        self._show_image(thresh)
        mask = cv2.inRange(thresh, 100, 255)
        self._show_image(mask)

        # RETR_LIST=1, CHAIN_APPROX_SIMPLE=2
        contours, heirarchy = cv2.findContours(
             mask, cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(im, contours, -1, (0,255,0), 3)
        circles = []
        for cnt in contours:
            (x,y),radius = cv2.minEnclosingCircle(cnt)
            center = (int(x),int(y))
            radius = int(radius)
            area = cv2.contourArea(cnt)
            circle_area = math.pi * radius**2
            if circle_area < 250.0 or abs(area - circle_area) > 100.0:  # Arbitrary magic threshold
                continue
            if self._debug_images:
                print("center",center)
                print("radius",radius)
            if radius < 5 or radius > 15:
                continue
            if self._debug_images:
                print 'contour area =', area, 'circle_area = ', circle_area
            
            cv2.circle(im, center, radius, (0, 255, 0), 2)
            self._show_image(im, show_this_image=False)
            circles.append(center)
        if len(circles) == 1:
            return True
        elif len(circles) > 1:
            print '\033[31;1m SOMETHING WEIRD HERE...\033[0m', circles
        else:
            return False
    def _get_circle(self, im):
        contours, heirarchy = cv2.findContours(
             im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for cnt in contours:
            if cv2.isContourConvex(cnt):
                self._show_image(im)
                return True
        return False




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
        contours, heirarchy = cv2.findContours(
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

