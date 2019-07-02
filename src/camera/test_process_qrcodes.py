import unittest
import src.camera.process_board_img as pi
import time



class TestBoardState(unittest.TestCase):

    def test_start_state(self):
        state = pi.get_board_state('src/camera/qrcodes/large_setup.png')
        self.assertEquals(state, [['BR1', 'BP1', 0, 0, 0, 0, 'WP1', 'WR1'],
                                  ['BK1', 'BP2', 0, 0, 0, 0, 'WP2', 'WK1'],
                                  ['BB1', 'BP3', 0, 0, 0, 0, 'WP3', 'WB1'],
                                  ['BQ', 'BP4', 0, 0, 0, 0, 'WP4', 'WQ'],
                                  ['BK', 'BP5', 0, 0, 0, 0, 'WP5', 'WK'],
                                  ['BB2', 'BP6', 0, 0, 0, 0, 'WP6', 'WB2'],
                                  ['BK2', 'BP7', 0, 0, 0, 0, 'WP7', 'WK2'],
                                  ['BR2', 'BP8', 0, 0, 0, 0, 'WP8', 'WR2']])

    def test_start_state_rotated(self):
        state = pi.get_board_state(
            'src/camera/qrcodes/large_setup_rotated.png')
        self.assertEquals(state, [['BR1', 'BP1', 0, 0, 0, 0, 'WP1', 'WR1'],
                                  ['BK1', 'BP2', 0, 0, 0, 0, 'WP2', 'WK1'],
                                  ['BB1', 'BP3', 0, 0, 0, 0, 'WP3', 'WB1'],
                                  ['BQ', 'BP4', 0, 0, 0, 0, 'WP4', 'WQ'],
                                  ['BK', 'BP5', 0, 0, 0, 0, 'WP5', 'WK'],
                                  ['BB2', 'BP6', 0, 0, 0, 0, 'WP6', 'WB2'],
                                  ['BK2', 'BP7', 0, 0, 0, 0, 'WP7', 'WK2'],
                                  ['BR2', 'BP8', 0, 0, 0, 0, 'WP8', 'WR2']])

    def test_downscaled_state_rotated(self):
        state = pi.get_board_state(
            'src/camera/qrcodes/downscaled_setup_rotated.png', resize=True)
        self.assertEquals(state, [['BR1', 'BP1', 0, 0, 0, 0, 'WP1', 'WR1'],
                                  ['BK1', 'BP2', 0, 0, 0, 0, 'WP2', 'WK1'],
                                  ['BB1', 'BP3', 0, 0, 0, 0, 'WP3', 'WB1'],
                                  ['BQ', 'BP4', 0, 0, 0, 0, 'WP4', 'WQ'],
                                  ['BK', 'BP5', 0, 0, 0, 0, 'WP5', 'WK'],
                                  ['BB2', 'BP6', 0, 0, 0, 0, 'WP6', 'WB2'],
                                  ['BK2', 'BP7', 0, 0, 0, 0, 'WP7', 'WK2'],
                                  ['BR2', 'BP8', 0, 0, 0, 0, 'WP8', 'WR2']])

    def test_fail_on_low_res(self):
        state = pi.get_board_state(
            'src/camera/qrcodes/start_state.png')
        self.assertEquals(state, [['BR1', 'BP5', 0, 0, 0, 0, 'WP3', 'WR1'],
                                  ['BK1', 'BP2', 0, 0, 0, 0, 'WP2', 'WK2'],
                                  ['BB1', 'BP3', 0, 0, 0, 0, 'WP6', 'WB2'],
                                  ['BK', 'BP8', 0, 0, 0, 0, 'WP4', 'WK'],
                                  # missing WP7
                                  ['BQ', 'BP7', 0, 0, 0, 0, 0, 'WQ'],
                                  ['BB2', 'BP6', 0, 0, 0, 0, 'WP5', 'WB1'],
                                  # missing WK1
                                  ['BK2', 'BP1', 0, 0, 0, 0, 'WP1', 0],
                                  ['BR2', 'BP4', 0, 0, 0, 0, 'WP8', 'WR2']])


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
        pixels.extend([(0,0,0,255) for x in range(6)])
        self.assertFalse(pi.row_white(pixels, 7, 6, 10))

    def test_col_white_fail(self):
        pixels = self.pixels[:]
        # Add a solid black row to the bottom
        pixels.extend([(0,0,0,255) for x in range(6)])
        self.assertFalse(pi.col_white(pixels, 1, 10))
        self.assertFalse(pi.col_white(pixels, 2, 10))
        self.assertFalse(pi.col_white(pixels, 3, 10))
        self.assertFalse(pi.col_white(pixels, 4, 10))
        self.assertFalse(pi.col_white(pixels, 5, 10))
        self.assertFalse(pi.col_white(pixels, 6, 10))



if __name__ == '__main__':
    unittest.main()
