from PIL import Image
import zbarlight


def get_board_state(image_path):
    """Gets the board state from a given static image file.

    :param image_path: path to an image of a chess board covered in pieces
                       with qrcodes on the bottom of them
    :return: The board state as an 8-length array of 8-length arrays, with
             0 in very position except where there are pieces.
    """
    image = open_image(image_path)
    num_squares = 8
    board_state = process_squares(image, num_squares)
    return board_state

def open_image(image_path):
    """Simple wrapper to load an image obj from an image file."""
    with open(image_path, 'rb') as image_file:
        image = Image.open(image_file)
        image.load()
    return image

def iterative_shrink(crop, shrink, shrink_lim):
    width, height = crop.size
    while shrink < shrink_lim:
        crop_box = (shrink, shrink, width-shrink, height-shrink)
        cropped = crop.crop(crop_box)
        codes = scan_qr_code(cropped)
        if codes is not None:
            return codes
        shrink += 1

def iterative_expand(crop, expand=10, threshold=10):
    crop_box = expand_crop_box(crop, expand, threshold)
    cropped = crop.crop(crop_box)
    codes = scan_qr_code(cropped)
    if codes is not None:
        return codes

def expand_crop_box(crop, expand, threshold):
    """Expand until we start getting all white columns on either side"""
    width, height = crop.size
    print('width height = ' + str((width, height)))
    l = width/2 - expand/2
    r = width/2 + expand/2
    b = height/2 - expand/2
    t = height/2 + expand/2
    print('starting with crop box ' + str((l, b, r, t)))
    some_black = True
    while some_black and (l > 0 and r < width and b > 0 and t < height):
        some_black = False
        cropped = crop.crop((l, b, r, t))
        data = cropped.getdata()
        cropped.show()
        if not row_white(data, t - b - 1, r - l, threshold):
            t += expand
            some_black = True
        if not row_white(data, 0, r - l, threshold):
            b -= expand
            some_black = True
        if not col_white(data, 1, threshold):
            l -= expand
            some_black = True
        if not col_white(data, r, threshold):
            r += expand
            some_black = True

    return (l, b, r, t)

def show_image_from_pixel_array(pixels, width, height):
    mode = 'RGBA'
    im2 = Image.new(mode, (width, height))
    im2.putdata(pixels)
    im2.show()

def row_white(pixels, row, width, threshold):
    pixel_data = list(pixels)
    perfect_white = 255*4
    row_pixels = pixel_data[(row)*width:(row+1)*width]
#    show_image_from_pixel_array(row_pixels, len(row_pixels), 1)
    for i, val in enumerate(row_pixels):
        if sum(val) < perfect_white - threshold:
            return False
    return True

def col_white(pixels, col, threshold):
    assert col != 0, 'Cannot mod by 0 - column should be 1 indexed'
    pixel_data = list(pixels)
    perfect_white = 255*4
    for i, val in enumerate(pixel_data):
        if i % col == 0:
            if sum(val) < perfect_white - threshold:
                return False
    return True


def process_squares(image, num_squares, shrink=0):
    """Iterate over the squares in the image to process each for qrcodes.

    :param image: PIL.Image object
    :param num_squares: The square root of the number of expected squares
                        to divide the image into. (E.g. num_squares = 8 means
                        an 8x8 chess board)
    :param shrink_offset: Amount to shrink in per square
    :return: A num_squares x num_squares list of lists containing the qrcode
             scan result per square
    """
    w_offset = image.width/num_squares
    h_offset = image.height/num_squares

    state = [[0 for x in xrange(num_squares)] for x in xrange(num_squares)]

    for i in xrange(num_squares):
        for j in xrange(num_squares):
            crop_box = (w_offset*i + shrink, h_offset*j + shrink,
                        w_offset*(i+1) - shrink, h_offset*(j+1) - shrink)
            crop = image.crop(crop_box)
            codes = scan_qr_code(crop)
            if codes is None and j in {0, 1, 6, 7}:
                codes = iterative_shrink(crop, 1, 20) # catches corner
            # if codes is None and j in {0, 1, 6, 7}:
            #     codes = iterative_expand(crop) # doesn't catch anything
            if codes is not None:
                assert len(codes) == 1, 'got many codes' + str(codes)
                state[i][j] = codes[0]
            else:
                if j in {0, 1, 6, 7}:
                    print('should have gotten something for ' + str((i, j)))
                    #crop.show()
    return state

def scan_qr_code(image):
    """Get codes from image object

    :param image: an image object (from PIL.Image)
    :return: result of zbarlight scan_code (list of text scanned from qrcode)
    """
    return zbarlight.scan_codes('qrcode', image)