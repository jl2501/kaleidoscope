import unittest
from kaleidoscope.view.attribute import AttributeView
from kaleidoscope.view.object import ObjectView

class TestAttributeView(unittest.TestCase):
    def test_init(self):
        attribute_value = '_symbolic_attribute_value_'
        av = AttributeView(attribute_value)
        self.assertEqual(av.get_render_output(), attribute_value)

class TestObjectView(unittest.TestCase):
    def setUp(self):
        av1 = AttributeView('1_test_attribute')
        av2 = AttributeView('2_test_attribute')
        self.avs = [av1, av2]

    def test_init(self):
        delimiter = ' | '
        ov = ObjectView(self.avs, delimiters=[delimiter])
        self.assertEqual(ov.get_render_output(),'1_test_attribute | 2_test_attribute') 


class TestGroupView(unittest.TestCase):
    def setup(self):
        pass
        


class TestCollectionView(unittest.TestCase):
    """writing unit tests for views is basically a tautology at this point. skipping."""
    def setup(self):
        pass


if __name__ == '__main__':
    unittest.main()
