from camera import board_image_processor as bip
from chess.models import *
import cv2
import numpy as np
from media.sound import *

def show_webcam(mirror=False):
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        #chess_state = process_image(img)
        cv2.imshow('webcam', img)
        if cv2.waitKey(1) == 27:
            break



def one_frame(id=0):
    # FIXME: Store the cam
   cam = cv2.VideoCapture(id)
   cam.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
   cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
   ret_val, img = cam.read()
   #print("width: " + str(cam.get(3)))
   #print("height: " + str(cam.get(4)))
   # cv2.imwrite("testimage3.png", img)
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
    print('Now initializing board processor')
    board_processor = bip.BoardProcessor(debug_image_mode=False)
    #board_processor = test_color_ranges()
    #board_processor = bip.BoardProcessor()
    state = board_processor.get_cur_state()
    board = Board()
    while True:
        #img = one_frame()
        print('reading a frame')
        try:
            img = one_frame()
            tmp_im_path = '/tmp/img.jpg'
            cv2.imwrite(tmp_im_path, img)
            board_processor._cache_pil_im(tmp_im_path)
            board_processor._show_image(img, show_this_image=False)
            board_processor.update_state(img)
            ret_state = board_processor.get_cur_state()
            if ret_state != state:
                pieces = []
                for i in range(0,8):
                    for j in range(0,8):
                        if board.state[i][j].piece:
                            pieces.append(board.state[i][j].piece)
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
                            m.append('P')
                    print(m)
                state = ret_state
            else:
                print('No new state',)
        except Exception as e:
            print('\033[31;1m GOT EXCEPTION', e, '\033[0m')
    # show_webcam()

if __name__ == '__main__':
    main()
    #main_get_color_ranges()
