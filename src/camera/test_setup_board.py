import unittest
import time
import src.camera.setup_board as sb


class TestCenterInference(unittest.TestCase):

    def test_setup_board(self):
        output = [(16, 202), (17, 260), (20, 78), (20, 135), (21, 321),
                  (21, 383), (25, 19), (32, 437), (69, 138), (69, 199),
                  (71, 256), (73, 79), (74, 319), (76, 13), (82, 384),
                  (89, 439), (129, 133), (130, 194), (131, 71), (132, 10),
                  (136, 259), (139, 321), (140, 388), (145, 442), (190, 192),
                  (194, 128), (196, 258), (198, 67), (198, 321), (200, 9),
                  (203, 386), (210, 445), (262, 129), (262, 258), (263, 62),
                  (264, 190), (265, 7), (269, 320), (269, 385), (273, 445),
                  (326, 126), (327, 444), (330, 66), (330, 255), (331, 8),
                  (332, 320), (338, 389), (340, 184), (387, 440), (390, 126),
                  (394, 253), (395, 9), (395, 387), (397, 65), (398, 190),
                  (399, 317), (452, 437), (454, 9), (455, 379), (458, 65),
                  (458, 188), (460, 253), (460, 316), (477, 130)]
        start = time.time()
        centers = sb.get_square_centers_from_board(
            'src/camera/captured_images/blue_squares.png',
            8, show_images=False)
        end = time.time()
        print('Got centers in ', end - start, ' seconds')
        self.assertEqual(centers, output)

if __name__ == '__main__':
    unittest.main()