import nose
import unittest
from nose.tools import *
from shaape.shaape import Shaape
from shaape.tests.utils import TestUtils

class TestBugfixes(unittest.TestCase):

    BUG_1_INCORRECT_ARROW_JOINT_BEHAVIOR_INPUT = 'shaape/tests/input/bug_1_incorrect_arrow_joint_behavior.shaape'
    BUG_1_INCORRECT_ARROW_JOINT_BEHAVIOR_EXPECTED_IMAGE = 'shaape/tests/expected_images/bug_1_incorrect_arrow_joint_behavior.png'
    BUG_1_INCORRECT_ARROW_JOINT_BEHAVIOR_GENERATED_IMAGE = 'shaape/tests/generated_images/bug_1_incorrect_arrow_joint_behavior.png'

    def test_bug_1_incorrect_arrow_joint_behavior(self):
        shaape = Shaape(TestBugfixes.BUG_1_INCORRECT_ARROW_JOINT_BEHAVIOR_INPUT, TestBugfixes.BUG_1_INCORRECT_ARROW_JOINT_BEHAVIOR_GENERATED_IMAGE)
        shaape.run()
        assert TestUtils.images_equal(TestBugfixes.BUG_1_INCORRECT_ARROW_JOINT_BEHAVIOR_GENERATED_IMAGE, TestBugfixes.BUG_1_INCORRECT_ARROW_JOINT_BEHAVIOR_EXPECTED_IMAGE)
        
