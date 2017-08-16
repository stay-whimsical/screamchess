import unittest
import src.camera.process_img as pi
import time

class TestBoardState(unittest.TestCase):

    def test_start_state(self):
        state = pi.get_board_state('src/camera/qrcodes/start_state.png')
        print('state = ' + str(state))

class TestQrScan(unittest.TestCase):

    def test_scanner(self):
        start = time.time()
        img = pi.open_image('src/camera/qrcodes/WR1.png')
        self.assertEquals(pi.scan_qr_code(img), ['WR1'])
        img = pi.open_image('src/camera/qrcodes/WR2.png')
        self.assertEquals(pi.scan_qr_code(img), ['WR2'])
        img = pi.open_image('src/camera/qrcodes/WB1.png')
        self.assertEquals(pi.scan_qr_code(img), ['WB1'])
        img = pi.open_image('src/camera/qrcodes/WB2.png')
        self.assertEquals(pi.scan_qr_code(img), ['WB2'])
        img = pi.open_image('src/camera/qrcodes/WK1.png')
        self.assertEquals(pi.scan_qr_code(img), ['WK1'])
        img = pi.open_image('src/camera/qrcodes/WK2.png')
        self.assertEquals(pi.scan_qr_code(img), ['WK2'])
        img = pi.open_image('src/camera/qrcodes/WK.png')
        self.assertEquals(pi.scan_qr_code(img), ['WK'])
        img = pi.open_image('src/camera/qrcodes/WQ.png')
        self.assertEquals(pi.scan_qr_code(img), ['WQ'])
        img = pi.open_image('src/camera/qrcodes/WP1.png')
        self.assertEquals(pi.scan_qr_code(img), ['WP1'])
        img = pi.open_image('src/camera/qrcodes/WP2.png')
        self.assertEquals(pi.scan_qr_code(img), ['WP2'])
        img = pi.open_image('src/camera/qrcodes/WP3.png')
        self.assertEquals(pi.scan_qr_code(img), ['WP3'])
        img = pi.open_image('src/camera/qrcodes/WP4.png')
        self.assertEquals(pi.scan_qr_code(img), ['WP4'])
        img = pi.open_image('src/camera/qrcodes/WP5.png')
        self.assertEquals(pi.scan_qr_code(img), ['WP5'])
        img = pi.open_image('src/camera/qrcodes/WP6.png')
        self.assertEquals(pi.scan_qr_code(img), ['WP6'])
        img = pi.open_image('src/camera/qrcodes/WP7.png')
        self.assertEquals(pi.scan_qr_code(img), ['WP7'])
        img = pi.open_image('src/camera/qrcodes/WP8.png')
        self.assertEquals(pi.scan_qr_code(img), ['WP8'])
        end = time.time()
        print('Scanned and asserted vals for 32 images in ' + str(end - start)
              + ' about ' + str((end-start)/32) + ' per image on average')

class TestWhiteCheck(unittest.TestCase):
    def setUp(self):
        self.pixels = [(255, 255, 255, 255), (255, 255, 255, 255),
                       (255, 255, 255, 255),
                       (255, 255, 255, 255), (255, 255, 255, 255),
                       (255, 255, 255, 255),
                       (255, 255, 255, 255), (255, 255, 255, 255),
                       (255, 255, 255, 255),
                       (255, 255, 255, 255), (255, 255, 255, 255),
                       (255, 255, 255, 255),
                       (255, 255, 255, 255), (255, 255, 255, 255),
                       (255, 255, 255, 255),
                       (255, 255, 255, 255), (255, 255, 255, 255),
                       (255, 255, 255, 255),
                       (255, 255, 255, 255), (255, 255, 255, 255),
                       (255, 255, 255, 255),
                       (255, 255, 255, 255), (255, 255, 255, 255),
                       (255, 255, 255, 255),
                       (255, 255, 255, 255), (255, 255, 255, 255),
                       (255, 255, 255, 255),
                       (255, 255, 255, 255), (255, 255, 255, 255),
                       (255, 255, 255, 255),
                       (255, 255, 255, 255), (255, 255, 255, 255),
                       (255, 255, 255, 255),
                       (255, 255, 255, 255), (255, 255, 255, 255),
                       (255, 255, 255, 255),
                       (255, 255, 255, 255), (255, 255, 255, 255),
                       (255, 255, 255, 255),
                       (255, 255, 255, 255), (255, 255, 255, 255),
                       (255, 255, 255, 255)]  # len 42, e.g. 6x7

    def test_row_white_success(self):
        self.assertTrue(pi.row_white(self.pixels, 0, 6, 10))
        self.assertTrue(pi.row_white(self.pixels, 1, 6, 10))
        self.assertTrue(pi.row_white(self.pixels, 2, 6, 10))
        self.assertTrue(pi.row_white(self.pixels, 3, 6, 10))
        self.assertTrue(pi.row_white(self.pixels, 4, 6, 10))
        self.assertTrue(pi.row_white(self.pixels, 5, 6, 10))
        self.assertTrue(pi.row_white(self.pixels, 6, 6, 10))

    def test_col_white_success(self):
        self.assertTrue(pi.col_white(self.pixels, 1, 10))
        self.assertTrue(pi.col_white(self.pixels, 2, 10))
        self.assertTrue(pi.col_white(self.pixels, 3, 10))
        self.assertTrue(pi.col_white(self.pixels, 4, 10))
        self.assertTrue(pi.col_white(self.pixels, 5, 10))
        self.assertTrue(pi.col_white(self.pixels, 6, 10))

    def test_row_white_fail(self):
        pixels = self.pixels[:]
        # Add a solid black row to the bottom
        pixels.extend([(0,0,0,255) for x in xrange(6)])
        self.assertFalse(pi.row_white(pixels, 7, 6, 10))

    def test_col_white_fail(self):
        pixels = self.pixels[:]
        # Add a solid black row to the bottom
        pixels.extend([(0,0,0,255) for x in xrange(6)])
        self.assertFalse(pi.col_white(pixels, 1, 10))
        self.assertFalse(pi.col_white(pixels, 2, 10))
        self.assertFalse(pi.col_white(pixels, 3, 10))
        self.assertFalse(pi.col_white(pixels, 4, 10))
        self.assertFalse(pi.col_white(pixels, 5, 10))
        self.assertFalse(pi.col_white(pixels, 6, 10))



if __name__ == '__main__':
    unittest.main()