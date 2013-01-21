from shaape.style import Style
import nose
import unittest
from nose.tools import *

class TestStyle(unittest.TestCase):

    def test_init(self):
        style = Style()
        assert style != None
        style = Style(option_list = ['red', 'flat', 'no-shadow', 3])
        assert style.color() == Style.COLORS['red']
        assert style.fill_type() == 'flat'
        assert style.shadow() == 'off'
        assert style.width() == 3
        style = Style(option_list = ['gradient', 'shadow', 3.2])
        assert style.fill_type() == 'gradient'
        assert style.shadow() == 'on'
        assert style.width() == 3.2
        style = Style(option_list = ['solid'])
        assert style.fill_type() == 'solid'
        style = Style(option_list = ['dashed'])
        assert style.fill_type() == 'dashed'
        style = Style(option_list = ['dash-dotted'])
        assert style.fill_type() == 'dash-dotted'
        style = Style(option_list = ['dotted'])
        assert style.fill_type() == 'dotted'

    def test_merge(self):
        style1 = Style(option_list = ['red', 'flat', 'no-shadow', 3])
        style2 = Style(option_list = ['blue', 'dotted'])
        style1.merge(style2)
        assert style1.color() == Style.COLORS['blue']
        assert style1.fill_type() == 'dotted'
        assert style1.shadow() == 'off'
        assert style1.width() == 3

    def test_target_type(self):
        style = Style()
        assert style.target_type() == ''
        style.set_target_type('line')
        assert style.target_type() == 'line'
        style.set_target_type('fill')
        assert style.target_type() == 'fill'

    def test_name_pattern(self):
        style = Style(name_pattern = "(abc)|(def)")
        assert style.name_pattern() == "(abc)|(def)"

    def test_shadow(self):
        style = Style()
        assert style.shadow() == Style.DEFAULT_STYLE['shadow']
        style.set_shadow('off')
        assert style.shadow() == 'off'
        style.set_shadow('on')
        assert style.shadow() == 'on'

    def test_color(self):
        style = Style()
        assert style.color() == Style.DEFAULT_STYLE['color']
        style.set_color((0.1, 0.2, 0.3))
        assert style.color() == (0.1, 0.2, 0.3)
        style.set_color((0.1, 0.2, 0.3, 0.4))
        assert style.color() == (0.1, 0.2, 0.3, 0.4)
        assert_raises(ValueError, style.set_color, (0.1, 0.2))
        
    def test_width(self):
        style = Style()
        assert style.width() == Style.DEFAULT_STYLE['width']
        style.set_width(10.1)
        assert style.width() == 10.1
        assert_raises(ValueError, style.set_width, -1)
        assert_raises(ValueError, style.set_width, 0)

    def test_cmp(self):
        style1 = Style('abc', 'line', ['red', 'flat', 'no-shadow', 3])
        style2 = Style('', '', [])
        assert style1 != style2
        style2.set_name_pattern('abc')
        assert style1 != style2
        style2.set_target_type('line')
        assert style1 != style2
        style2.set_options(['red', 'flat', 'no-shadow', 3])
        assert style1 == style2
        assert style1 != 1

    def test_repr(self):
        assert str(Style('abc', 'line', ['red', 'flat', 'no-shadow', 3])) == "(name_pattern: abc, target_type:line, options:{'color': [1, 0, 0], 'width': 3, 'shadow': 'off', 'type': 'flat'}, prio:-1)", Style('abc', 'line', ['red', 'flat', 'no-shadow', 3])

