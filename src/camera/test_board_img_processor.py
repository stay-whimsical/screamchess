import unittest
import time
import src.camera.board_image_processor as bip



class TestGetColors(unittest.TestCase):
    """
    Hue range [0,179], Saturation range is [0,255] and Value range is [0,255]
    """

    def setUp(self):
        self._processor = bip.BoardProcessor(debug_image_mode=True)
        self._processor.setup_board('src/camera/captured_images/'
                                    'blue_squares.png')


    def test_initial_state(self):
        image_path = 'src/camera/captured_images/finalll.png'
        self._processor._show_image(self._processor._open_image(image_path),'Start image')
        img = self._processor._open_image(image_path)
        start = time.time()
        state = self._processor.get_board_state(img)
        end = time.time()
        print("got state")
        for row in state:
            print row
        print('Got board state from colors in ', end - start)

    @unittest.skip('This image is no longer up to snuff')
    def test_better_light(self):
        start = time.time()
        img = self._processor._open_image('src/camera/captured_images/okay_light_good_colors.png')
        state = pi.get_board_state(img,
                                   qr=False, color=True,
                                   color_map=color_map)
        print("got state", state)
        end = time.time()
        print('Got board state from colors in ', end - start)

#    @unittest.skip("need to make the color_map")
    def test_three_colors(self):
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


class TestSetupBoard(unittest.TestCase):

    def setUp(self):
        self._processor = bip.BoardProcessor()

    def test_setup_board(self):
        # As array, deprecated but still useful to see
        # output = [(16, 202), (17, 260), (20, 78), (20, 135), (21, 321),
        #           (21, 383), (25, 19), (32, 437), (69, 138), (69, 199),
        #           (71, 256), (73, 79), (74, 319), (76, 13), (82, 384),
        #           (89, 439), (129, 133), (130, 194), (131, 71), (132, 10),
        #           (136, 259), (139, 321), (140, 388), (145, 442), (190, 192),
        #           (194, 128), (196, 258), (198, 67), (198, 321), (200, 9),
        #           (203, 386), (210, 445), (262, 129), (262, 258), (263, 62),
        #           (264, 190), (265, 7), (269, 320), (269, 385), (273, 445),
        #           (326, 126), (327, 444), (330, 66), (330, 255), (331, 8),
        #           (332, 320), (338, 389), (340, 184), (387, 440), (390, 126),
        #           (394, 253), (395, 9), (395, 387), (397, 65), (398, 190),
        #           (399, 317), (452, 437), (454, 9), (455, 379), (458, 65),
        #           (458, 188), (460, 253), (460, 316), (477, 130)]
        output = {(387, 440): (7, 6), (190, 192): (3, 3), (82, 384): (6, 1),
                  (210, 445): (7, 3), (21, 383): (6, 0), (327, 444): (7, 5),
                  (20, 135): (2, 0), (71, 256): (4, 1), (477, 130): (2, 7),
                  (452, 437): (7, 7), (196, 258): (4, 3), (460, 316): (5, 7),
                  (20, 78): (1, 0), (74, 319): (5, 1), (397, 65): (1, 6),
                  (69, 138): (2, 1), (73, 79): (1, 1), (331, 8): (0, 5),
                  (455, 379): (6, 7), (25, 19): (0, 0), (326, 126): (2, 5),
                  (198, 67): (1, 3), (129, 133): (2, 2), (139, 321): (5, 2),
                  (194, 128): (2, 3), (269, 320): (5, 4), (265, 7): (0, 4),
                  (132, 10): (0, 2), (454, 9): (0, 7), (340, 184): (3, 5),
                  (203, 386): (6, 3), (395, 9): (0, 6), (273, 445): (7, 4),
                  (200, 9): (0, 3), (263, 62): (1, 4), (332, 320): (5, 5),
                  (458, 65): (1, 7), (140, 388): (6, 2), (145, 442): (7, 2),
                  (131, 71): (1, 2), (394, 253): (4, 6), (338, 389): (6, 5),
                  (17, 260): (4, 0), (330, 255): (4, 5), (269, 385): (6, 4),
                  (136, 259): (4, 2), (32, 437): (7, 0), (16, 202): (3, 0),
                  (398, 190): (3, 6), (76, 13): (0, 1), (21, 321): (5, 0),
                  (262, 129): (2, 4), (69, 199): (3, 1), (395, 387): (6, 6),
                  (390, 126): (2, 6), (399, 317): (5, 6), (264, 190): (3, 4),
                  (262, 258): (4, 4), (130, 194): (3, 2), (460, 253): (4, 7),
                  (458, 188): (3, 7), (89, 439): (7, 1), (198, 321): (5, 3),
                  (330, 66): (1, 5)}
        start = time.time()
        self._processor.setup_board('src/camera/captured_images/'
                                    'blue_squares.png')
        end = time.time()
        print('Got centers in ', end - start, ' seconds')
        self.assertEqual(self._processor._centers, output)

if __name__ == '__main__':
    unittest.main()
