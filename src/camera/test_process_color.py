import unittest
import src.camera.process_board_img as pi
import time
import numpy as np


class TestGetColors(unittest.TestCase):

    def test_initial_state(self):
        start = time.time()
        color_map = {'WP1': (np.array([110, 50, 50]),   # light blue
                             np.array([130, 255, 255])),
                     'BP1': (np.array([222, 50, 50]),   # dark blue
                             np.array([243, 255, 255])),
                     'WR1': (np.array([57, 50, 50]),    # green
                             np.array([96, 255, 255])),
                     'WB2': (np.array([110, 50, 50]),   # purple
                             np.array([130, 255, 255])),
                     'WP6': (np.array([351, 50, 50]),   # red
                             np.array([360, 255, 255])),
                     'BP6': (np.array([25, 50, 50]),    # yellow
                             np.array([55, 255, 255])),
                     }
        state = pi.get_board_state('src/camera/captured_images/'
                                   'okay_light_good_colors.png',
                                   qr=False, color=True,
                                   color_map=color_map)
        print("got state", state)
        end = time.time()
        print('Got board state from colors in ', end - start)

    @unittest.skip("need to make the color_map")
    def test_three_colors(self):
        color_map = {(42, 90, 9): 'WR1',  # green
                     (104, 118, 138): 'WB2',  # blue
                     (68, 30, 56): 'WP6',  # purple
                     }
        start = time.time()
        state = pi.get_board_state('src/camera/captured_images/testimage.png',
                                   qr=False, color=True,
                                   captured_image=True,
                                   color_map=color_map)
        end = time.time()
        print('Got board state from colors in ', end - start)


        # NOTE - the way the columns work, is sort of confusing - these are
        # columns, so the actual board state looks like
        #
        # 0   0   0   0   0   0   0   0
        # 0   0   0   0   0   0   0   0
        # 0   0   0   0   0   0   0   0
        # 0   0   0   0   0   0   0   0
        # 0   0   0   0   0  WB2 WR1  0
        # 0   0   0   0   0  WP6  0   0
        # 0   0   0   0   0   0   0   0
        # 0   0   0   0   0   0   0   0
        #
        self.assertEqual(state,
                         [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 'WB2', 'WP6', 0, 0],
                          [0, 0, 0, 0, 'WR1', 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0]])
        print('got state', state)


if __name__ == '__main__':
    unittest.main()