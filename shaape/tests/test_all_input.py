import nose
import unittest
from nose.tools import *
from shaape.shaape import Shaape
from shaape.tests.utils import TestUtils
import os

class TestAllInput(unittest.TestCase):

    INPUT_PATH = 'shaape/tests/input/'
    EXPECTED_IMAGES_PATH = 'shaape/tests/expected_images/'
    GENERATED_IMAGES_PATH = 'shaape/tests/generated_images/'

    def test_input(self):
        files = [ f for f in os.listdir(TestAllInput.INPUT_PATH) if os.path.isfile(os.path.join(TestAllInput.INPUT_PATH, f)) and os.path.splitext(f)[1] == '.shaape' ]
        for f in files:
            f_in = TestAllInput.INPUT_PATH + f
            f_out = TestAllInput.GENERATED_IMAGES_PATH + f + '.png'
            f_expected = TestAllInput.EXPECTED_IMAGES_PATH + f + '.png'
            shaape = Shaape(f_in, f_out)
            shaape.run()
            assert TestUtils.images_equal(f_out, f_expected), f_out + ' != ' + f_expected
