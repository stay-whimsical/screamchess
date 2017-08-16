import zbarlight
from PIL import Image
from collections import Counter


def get_board_state(image_path, resize=False, qr=True, color=False,
                    captured_image=False):
    """Gets the board state from a given static image file.

    :param image_path: path to an image of a chess board covered in pieces
                       with qrcodes on the bottom of them
    :return: The board state as an 8-length array of 8-length arrays, with
             0 in very position except where there are pieces.
    """
    image = open_image(image_path)
    if captured_image:
        image = crop_to_board(image)
    if resize:
        width = 1200
        height = 1200
        image = increase_resolution(image, width, height)
    num_squares = 8
    board_state = process_squares(image, num_squares, qr, color)
    return board_state

def crop_to_board(image):
    """Our image is not square, it is also warped. For now, we are just
    cropping down to the region that has the chess board in it. There
    are some un-warping filters we can apply as well, based on the
    specific camera specs - TODO

    NOTE These are super magic numbers that we will dial in as we get the
    camera set up.
    """
    board_width = 530
    height_diff = board_width - image.height
    crop = image.crop((0, 0, board_width, image.height))
    # NOTE we are dropping the A in RGBA to be more efficient - just need to
    #      conform with the rest of the tests TODO
    square_im = Image.new('RGB', (board_width, board_width))
    square_im.paste(crop, (0, height_diff))
    # Fill in the extra space with the last row of pixels repeated
    for i in range(board_width - image.height):
        square_im.paste(crop.crop((0, 0, board_width, height_diff)), (0, i))
    return square_im

def increase_resolution(image, width, height):
    # Resampling schemas: Image.BLINEAR, Image.BICUBIC, Image.LANCZOS,
    #                     default is Image.NEAREST
    image = image.resize((width, height), resample=Image.LANCZOS)
    return image

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

def process_squares(image, num_squares, qr, color, shrink=0):
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

    # Note, below is nicer python, but it changed the order in which the
    # columns were processed....TODO: need to investigate
    #state = [[0]*num_squares]*num_squares
    state = [[0 for x in xrange(num_squares)] for x in xrange(num_squares)]

    for i in xrange(num_squares):
        for j in xrange(num_squares):
            crop_box = (w_offset*i + shrink, h_offset*j + shrink,
                        w_offset*(i+1) - shrink, h_offset*(j+1) - shrink)
            crop = image.crop(crop_box)
            if qr:
                set_state_from_qr_code(crop, state, i, j)
            if color:
                set_state_from_color(crop, state, i, j)

    return state

def set_state_from_qr_code(image, state, i, j):
    codes = scan_qr_code(image)
    if codes is None and j in {0, 1, 6, 7}:
        codes = iterative_shrink(image, 1, 20)  # catches corner
    # if codes is None and j in {0, 1, 6, 7}:
    #     codes = iterative_expand(crop) # doesn't catch anything
    if codes is not None:
        assert len(codes) == 1, 'got many codes' + str(codes)
        state[i][j] = codes[0]
    else:
        if j in {0, 1, 6, 7}:
            print('should have gotten something for ' + str((i, j)))
            # crop.show()

def get_color_map():
    return {(42, 90, 9): 'WR1',      # green
            (104, 118, 138): 'WB2',  # blue
            (68, 30, 56): 'WP6',     # purple
    }

def set_state_from_color(image, state, i, j):
    fuzz = 2
    num_pixel_threshold = 15
    color_map = get_color_map()
    colors = Counter(image.getdata())
    for color in color_map:
        num_pixels_hit = 0
        # make the color fuzzy

        fuzzy_color = [(r, g, b) for r in range(color[0] - fuzz, color[0] + fuzz)
                       for g in range(color[1] - fuzz, color[1] + fuzz)
                       for b in range(color[2] - fuzz, color[2] + fuzz)]
        for fcol in fuzzy_color:
            if color_in_square(colors, fcol):
                num_pixels_hit += colors[fcol]
        if num_pixels_hit > num_pixel_threshold:
            state[i][j] = color_map[color]

def scan_qr_code(image):
    """Get codes from image object

    :param image: an image object (from PIL.Image)
    :return: result of zbarlight scan_code (list of text scanned from qrcode)
    """
    return zbarlight.scan_codes('qrcode', image)

def color_in_square(colors, color):
    """Get colors from the given pixel color count"""
    # There will be some noise - but it doesn't matter, we're looking for our
    # specific colors
    return color in colors
