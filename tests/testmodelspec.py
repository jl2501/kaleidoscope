"""Test the model specifications"""
import unittest
from kaleidoscope.modelspec import ObjectModelSpec

class Simple(object):
    def __init__(self):
        self.simple_attribute = '_simple_value_'
        self.list_attribute = list([0,1,2,3,4,5])
        self.dict_attribute = dict({'key1' : 'value1', 'key2' : 'value2'})

class TestObjectModelSpec(unittest.TestCase):
    def setUp(self):
        self.simple = Simple()


    def test_init(self):
        oms = ObjectModelSpec(colors=['bright green on black', 'bright white on black'], attributes=['simple_attribute', 'list_attribute', 'dict_attribute'])
        self.assertEqual(oms.colors[0], 'bright green on black')
        self.assertEqual(oms.attributes[0],'simple_attribute')

if __name__ == '__main__':
    unittest.main()
