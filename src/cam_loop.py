# from camera import board_image_processor as bip
from camera import qr_board_processor as bip
from chess.models import *
import cv2
import numpy as np
import sys
from media.sound import *

def one_frame(id=0):
    # FIXME: Store the cam
   cam = cv2.VideoCapture(id)
   cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
   cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
   ret_val, img = cam.read()
   return img

def show_all_hsv_color_ranges(steps, board_processor):
    step_size = 180/steps
    hsv = one_frame()
    for i in range(steps):
        lower = np.array([i*step_size, 50, 50])
        upper = np.array([(i+1)*step_size, 255, 255])
        conv = board_processor._get_convolved_image(hsv, (lower, upper))
        board_processor._show_image(conv)

def test_color_ranges():
    board_processor = bip.BoardProcessor()
    red = (np.array([0, 50, 50]), np.array([18, 255, 255]))
    green = (np.array([19, 50, 50]), np.array([36, 255, 255]))
    blue = (np.array([90, 50, 50]), np.array([108, 255, 255]))
    color_map = {'W': green, 'B': blue}
    board_processor.set_color_map(color_map)
    return board_processor

def blend_images(num):
    alpha = 0.5
    beta = 1.0 - alpha
    gamma = 0.0
    img = one_frame()
    for i in range(num):
        img2 = one_frame()
        img = cv2.addWeighted(img, alpha, img2, beta, gamma)
    return img

def main_get_color_ranges():
    board_processor = bip.BoardProcessor(debug_image_mode=False)
    show_all_hsv_color_ranges(10, board_processor)

def main():
    # FIXME add real arg handling if we need it, e.g. num visible squares...
    cell_radius = None
    if len(sys.argv) > 1:
       cell_radius = float(sys.argv[1])
    debug = len(sys.argv) > 2
    print('Now initializing board processor', 'with debug ' if debug else '')
    board_processor = bip.QRBoardProcessor(cell_radius=cell_radius, debug=debug)
    board = Board()
    state = board_processor.empty_state()
    while True:
        try:
            img = one_frame()
            ret_state = board_processor.update(img)
            if ret_state != state:

                pieces = []
                for i in range(0,8):
                    for j in range(0,8):
                        if board.state[i][j].piece:
                            pieces.append(board.state[i][j].piece)

                # FIXME: Currently does not track specific pieces
                piece_index = random.randint(0, len(pieces) - 1)
                if pieces:
                    play_sound(pieces[piece_index], random_action())

                print('\033[34;1m Got state change, new state = \033[0m')
                for row in ret_state:
                    m = []
                    for x in row:
                        if x is None:
                            m.append('-')
                        else:
                            m.append(x)
                    print(m)
                state = ret_state
            else:
                print('No new state',)
        except Exception as e:
            print('\033[31;1m Could not process frame due to', e, '\033[0m')
            raise e

if __name__ == '__main__':
    main()
