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
        self.cell_radius = self.height / (self.num_squares)

        self.cell_width = self.width/self.num_squares
        self.cell_height = self.height/self.num_squares

        self.centers = []
        for j in range(self.num_squares):
            # FIXME: I might have width and height backwards
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
            cropped = self.raw_img[ul:ur, ll:lr]
            i = index % (self.num_squares)
            j = math.floor(index / self.num_squares)
            self.square_index += 1
            yield (i, j, cropped)

    def show(self):
        cv2.imshow("Processing Image", self.raw_img)

class QRBoardProcessor:
    """
    The QR Board Processor Maintains an Internal State of the Board, and
    can update it, given an image
    """
    board_width = 8

    def __init__(self):
        self._cur_state = self.empty_state()

    def update(self, captured_img):
        img = BoardImg(captured_img)

        img.show()

        self._cur_state = self.get_board_state(img)
        return self._cur_state

    @staticmethod
    def empty_state():
        return [ [None for x in range(QRBoardProcessor.board_width)]
                 for x in range(QRBoardProcessor.board_width) ]

    @staticmethod
    def scan_qr_code(img):
        """Get codes from image object

        :param img: a numpy array, that must be converted to PIL.Image for
                    zbarlight
        :return: result of zbarlight scan_code (list of text scanned from
                 qrcode)
        """
        return zbarlight.scan_codes('qrcode', Image.fromarray(img))

    def get_board_state(self, img):
        """Looks at each square, using the "center" hints, and reads QR codes.

        NOTE: This is embarrassingly parallelizable, if we needed to optimize
        Returns the board state
        """
        board = self.empty_state()
        for (i, j, square) in img.next_square():
            cv2.imshow("square", square)
            cv2.waitKey(0)
            qr = self.scan_qr_code(square)
            print("Got QR code: ", qr, " for [", i, ", ", j, "]")
            if qr is not None:
                board[i][j] = qr

        return board
