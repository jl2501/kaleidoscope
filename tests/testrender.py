"""Test the render.color module"""
import unittest
from kaleidoscope.rendersys import Render

class SimpleClass(object):
    def __init__(self, *args,**kwargs):
        for k,v in kwargs.items():
            setattr(self,k,v)


class TestRenderingEngine(unittest.TestCase):
    def setUp(self):
        self.r = Render()

    def test_render_obj(self):
        sc = SimpleClass(a='AAA', b='BBB', c='CCC', d='DDD', e='EEE')
        self.r.render_object(sc, attributes=['a','b','c','d','e'])

    def test_builtin_specname(self):
        l = [1,2,3,4]
        l_specname = self.r.make_default_specname_from_object(l)
        self.assertEqual('builtins.int', l_specname)

if __name__ == '__main__':
    unittest.main()
