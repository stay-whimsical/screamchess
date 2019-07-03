import cv2
import numpy as np
import bisect
import math
import operator
import zbarlight
from PIL import Image
from camera.setup_board import get_square_centers_from_board

class BoardImg:
    """
    Represents the image when rendered per-cell
    """
    image_pixel_width = 1280 # FIXME one global, also on each img - warn if off?
    image_pixel_height = 960
    num_squares = 8

    def __init__(self, img):
        self.raw_img = img
        height, width, channels = img.shape
        self.height = height
        self.width = width
        self.cell_radius = self.height / (self.num_squares*2)

        self.cell_width = self.width/self.num_squares
        self.cell_height = self.height/self.num_squares

        self.centers = []
        for j in range(self.num_squares):
            xs = [ i*self.cell_width for i in range(self.num_squares) ]
            ys = [ j*self.cell_height for i in range(self.num_squares) ]
            self.centers.extend(list(zip(xs, ys)))
        print("centers = ", self.centers)

        self.square_index = 0

    def next_square(self):
        """Iterate through chessboard squares"""
        print("centers = ", self.centers)
        for index, (x, y) in enumerate(self.centers):
            ll = int(x)
            lr = int(x+self.cell_radius)
            ul = int(y)
            ur = int(y + self.cell_radius)
            print("indices = ", ll, lr, ul, ur)
            cropped = self.raw_img[ll:lr, ul:ur]
            i = index % (self.num_squares)
            j = math.floor(index / self.num_squares)
            self.square_index += 1
            yield (i, j, cropped)

    def get_pil():
        raise UnimplementedError

class QRBoardProcessor:
    """
    The QR Board Processor Maintains an Internal State of the Board, and
    can update it, given an image
    """
    board_width = 8

    def __init__(self):
        self._cur_state = self.empty_state()

    def update(self, captured_img):
        # FIXME: cache img if that is something you want to do
        img = BoardImg(captured_img)

        state = self.get_board_state(img)
        if state != self._cur_state:
            self._cur_state = state
        return self._cur_state

    @staticmethod
    def empty_state():
        return [ [None for x in range(QRBoardProcessor.board_width)]
                 for x in range(QRBoardProcessor.board_width) ]

    @staticmethod
    def scan_qr_code(image):
        """Get codes from image object

        :param image: an image object (from PIL.Image)
        :return: result of zbarlight scan_code (list of text scanned from qrcode)
        """
        return zbarlight.scan_codes('qrcode', image)


    def get_board_state(self, img):
        """Looks at each square, using the "center" hints, and reads QR codes.

        NOTE: This is embarrassingly parallelizable, if we needed to optimize
        Returns the board state
        """
        board = self.empty_state()
        for (i, j, square) in img.next_square():
            cv2.imshow("square", square)
            cv2.waitKey(0)
            im = np.array(square)
            tmp_img_pil = img.get_tmp_img_pil()
            qr = self.scan_qr_code(tmp_img_pil)
            print("Got QR code: ", qr, " for [", i, ", ", j, "]")
            if qr is not None:
                board[i][j] = True

        return board
