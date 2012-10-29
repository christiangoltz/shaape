import Image
import ImageChops
import math
import operator

class TestUtils(object):
    BLUR_INPUT = 'shaape/tests/input/blur.shaape'
    BLUR_GENERATED_IMAGE = 'shaape/tests/generated_images/blur.png'
    BLUR_EXPECTED_IMAGE = 'shaape/tests/expected_images/blur.png'
    ACCEPTABLE_RMS = 0
    
    @staticmethod
    def imagesEqual(image1, image2):
        try:
            img1 = Image.open(image1)
            img2 = Image.open(image2)
        except:
            return False
        diff = ImageChops.difference(img1, img2)
        h = ImageChops.difference(img1, img2).histogram()
        sq = (value*((idx%256)**2) for idx, value in enumerate(h))
        sum_of_squares = sum(sq)
        rms = math.sqrt(sum_of_squares/float(img1.size[0] * img1.size[1]))
        print(rms)
        return rms <= TestUtils.ACCEPTABLE_RMS
