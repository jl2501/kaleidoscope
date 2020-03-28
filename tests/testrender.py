"""Test the render.color module"""
import unittest
from kaleidoscope.rendersys import Render

class SimpleClass(object):
    def __init__(self, *args,**kwargs):
        for k,v in kwargs.items():
            setattr(self,k,v)


class TestRenderingEngine(unittest.TestCase):
    def test_init(self):
        r = Render()
        

    def test_render_obj(self):
        r = Render()
        sc = SimpleClass(a='AAA', b='BBB', c='CCC', d='DDD', e='EEE')
        r.render_object(sc, attributes=['a','b','c','d','e'])


if __name__ == '__main__':
    unittest.main()
