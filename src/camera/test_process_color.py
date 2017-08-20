import unittest
import src.camera.process_img as pi
import time


class TestGetColors(unittest.TestCase):
    def test_three_colors(self):
        state = pi.get_board_state('src/camera/captured_images/testimage.png',
                                   qr=False, color=True,
                                   captured_image=True)
        # color_map = {(42, 90, 9): 'WR1',  # green
        #              (104, 118, 138): 'WB2',  # blue
        #              (68, 30, 56): 'WP6',  # purple
        #             }

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