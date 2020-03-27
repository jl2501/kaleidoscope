import unittest
import operator
import copy
from kaleidoscope.model import AttributeModel, ObjectModel, GroupModel, CollectionModel
from kaleidoscope.spec.object import ObjectModelSpec
from kaleidoscope.color import Color

class SimpleClass(object):
    """Simple Class for testing of attributes"""
    def __init__(self):
        self.simple_attribute = '_simple_value_'
        self.list_attribute = list([0,1,2,3,4,5])
        self.dict_attribute = dict({'key1' : 'value1', 'key2' : 'value2'})

class TestAttributeModel(unittest.TestCase):
    def setUp(self):
        self.simple = SimpleClass()

    def test_simple_color(self):
        am = AttributeModel(self.simple, 'simple_attribute', color=Color('green'))
        view = am.render_view()
        expected = ('\x1b[32m\x1b[40m\x1b[22m\x1b[0m\x1b[32m\x1b[40m\x1b[22m'
                '_simple_value_'
                '\x1b[0m\x1b[32m\x1b[40m\x1b[22m\x1b[0m')
        self.assertEqual(view.get_render_output(), expected)
        view.render()
        

    def test_modified_color_on_background(self):
        am = AttributeModel(self.simple, 'simple_attribute', color='bright white on green')
        view = am.render_view()
        expected = ('\x1b[32m\x1b[40m\x1b[22m\x1b[0m\x1b[37m\x1b[42m\x1b[1m'
                '_simple_value_'
                '\x1b[0m\x1b[32m\x1b[40m\x1b[22m\x1b[0m')
        self.assertEqual(view.get_render_output(), expected)
        view.render()

    def test_length(self):
        am = AttributeModel(self.simple, 'simple_attribute', color='green on black', length=5)
        view = am.render_view()
        expected = ('\x1b[32m\x1b[40m\x1b[22m\x1b[0m\x1b[32m\x1b[40m\x1b[22m'
                '_simp'
                '\x1b[0m\x1b[32m\x1b[40m\x1b[22m\x1b[0m')
        self.assertEqual(view.get_render_output(), expected)
        view.render()

    def test_list(self):
        am = AttributeModel(self.simple, 'list_attribute', color=Color('green'))
        view = am.render_view()
        expected =  ('\x1b[32m\x1b[40m\x1b[22m\x1b[0m\x1b[32m\x1b[40m\x1b[22m'
                '[0, 1, 2, 3, 4, 5]'
                '\x1b[0m\x1b[32m\x1b[40m\x1b[22m\x1b[0m')
        self.assertEqual(view.get_render_output(), expected)
        view.render()

    def test_get_source(self):
        am = AttributeModel(self.simple, 'list_attribute')
        self.assertEqual(self.simple, am.get_source())

    def test_get_spec(self):
        am = AttributeModel(self.simple, 'simple_attribute')
        self.assertEqual(None, am.get_spec())

    def test_set_color(self):
        am = AttributeModel(self.simple, 'simple_attribute')
        am.set_color('bright red on white')
        view = am.render_view()
        expected = ('\x1b[32m\x1b[40m\x1b[22m\x1b[0m\x1b[31m\x1b[47m\x1b[1m'
                '_simple_value_'
                '\x1b[0m\x1b[32m\x1b[40m\x1b[22m\x1b[0m')
        self.assertEqual(view.get_render_output(), expected)
        view.render()

    def test_get_name(self):
        am = AttributeModel(self.simple, 'dict_attribute')
        self.assertEqual(am.get_name(), 'dict_attribute')


class TestObjectModel(unittest.TestCase):
    """Test the ObjectModel Class"""
    def setUp(self):
        self.simple = SimpleClass()
        self.om_modeled_attributes = ['simple_attribute', 'list_attribute']
        self.oms = ObjectModelSpec(colors=['yellow', 'red'], attributes=self.om_modeled_attributes)

    def test_init(self):
        """Test the initialization of an ObjectModel"""
        om = ObjectModel(self.simple, spec=self.oms)
        self.assertIs(self.simple, om.source_object)
        for attribute_model_x in om.attribute_models:
            self.assertIn(attribute_model_x.name, self.om_modeled_attributes)

    def test_render(self):
        """Test the rendering of an ObjectModel"""
        om = ObjectModel(self.simple, spec=self.oms)
        expected = ('\x1b[33m\x1b[40m\x1b[22m'
                '_simple_value_'
                '\x1b[0m\x1b[33m\x1b[40m\x1b[22m'
                ' | '
                '\x1b[0m\x1b[31m\x1b[40m\x1b[22m'
                '[0, 1, 2, 3, 4, 5]'
                '\x1b[0m')
        actual = om.get_render_output()
        self.assertEqual(expected, actual)
        om.render()

        
        
class TestGroupModel(unittest.TestCase):
    """Test the GroupModel class"""
    def setUp(self):
        class SimpleClass2(object):
            def __init__(self, name='default_name', flavors=None, mood='happy'):
                self.name = name
                self.mood = mood
                if flavors is None:
                    self.flavors = ['vanilla', 'caramel', 'chocolate']
                else:
                    self.flavors = flavors

            
        def test_method_true(obj):
            return True

        self.simple1 = SimpleClass2()
        self.simple2 = SimpleClass2()
        self.simple3 = SimpleClass2(flavors=[
                'butter pecan',
                'mint chocolate chip',
                'cookies n cream'])
        self.simple4 = SimpleClass2(flavors=['caramel', 'dead rodent guts'])
        self.modeled_attributes1 = ['name', 'flavors']

        self.oms1 = ObjectModelSpec(colors=['green', 'yellow'], attributes=self.modeled_attributes1)
        self.oms2 = ObjectModelSpec(colors=['white', 'cyan'], attributes=['name', 'flavors'])
        self.oms3 = ObjectModelSpec(colors=['red', 'white', 'blue'], attributes=['name', 'flavors', 'mood'])

        self.om1 = ObjectModel(self.simple1, spec=self.oms1)
        self.om2 = ObjectModel(self.simple2, spec=self.oms1)

        self.om3 = ObjectModel(self.simple3, self.oms2)
        self.om4 = ObjectModel(self.simple4, self.oms2)

        self.om5 = ObjectModel(self.simple1, self.oms3)
        self.om6 = ObjectModel(self.simple2, self.oms3)
        self.om7 = ObjectModel(self.simple3, self.oms3)

        self.modeled_objects = [self.om1, self.om2]
        

    def test_init(self):
        """Test initialization of the GroupModel object"""
        gm = GroupModel('test_group', object_models=self.modeled_objects)
        for obj_x in self.modeled_objects:
            self.assertIn(obj_x, gm.object_models)

    def test_sort_attr(self):
        """Test initializing the GroupModel with the name of an attribute to sort the models by"""
        gm = GroupModel('test_group', object_models=self.modeled_objects, sort_attr='name')
        self.assertEqual(sorted([model_x.get_source().name for model_x in gm.object_models]), [model_x.get_source().name for model_x in gm.object_models])


    def test_test_method(self):
        """Test initializing the group with a test_method that tests the modeled objects for group membership"""
        modeled_objects = self.modeled_objects + [self.om3]
        gm = GroupModel('test_group', test_method=lambda x: 'caramel' in x.flavors, object_models=modeled_objects, sort_attr='name')
        for model_x in gm.object_models:
            self.assertIn('caramel', model_x.get_source().flavors)

    def test_insert(self):
        """Test inserting an object model at a specifc index in the object models list"""
        gm = GroupModel('test_group', test_method=lambda x: 'caramel' in x.flavors, object_models=self.modeled_objects, sort_attr='name')

        gm.insert_object_model(0, self.om2)
        self.assertEqual(self.om2, gm.object_models[0])

        gm.insert_object_model(1, self.om4)
        self.assertEqual(self.om4, gm.object_models[1])

    def test_pop(self):
        """Test popping an object model from the group"""
        gm = GroupModel('test_group', object_models=self.modeled_objects)
        self.assertEqual(self.om2, gm.pop_object_model())


    def test_remove(self):
        """Test removing an object model"""
        gm = GroupModel('test_group', object_models=self.modeled_objects)
        gm.remove_object_model(self.om2)
        self.assertNotIn(self.om2, gm.object_models)

    def test_get(self):
        """Test getting an object model"""
        gm = GroupModel('test_group', object_models=self.modeled_objects)
        self.assertEqual(gm.get_object_model(0), gm.object_models[0])


    def test_sort(self):
        """Test basic sorting of the object models"""
        gm = GroupModel('test_group', object_models=self.modeled_objects)
        gm.sort_object_models(key=lambda x: x.get_source().flavors[0])
        self.assertEqual(sorted(gm.object_models, key=lambda x: x.get_source().flavors[0]), gm.object_models)


    def test_reverse(self):
        """Test reverse_object_models method"""
        gm = GroupModel('test_group', object_models=self.modeled_objects)
        initial_list = copy.copy(gm.object_models)
        gm.reverse_object_models()
        initial_list.reverse()
        self.assertEqual(initial_list, gm.object_models)


    def test_render(self):
        """Test the rendering of a GroupView object"""
        gm = GroupModel(object_models=[self.om1, self.om2, self.om3, self.om4])
        gv = gm.render_view()
        actual = gv.get_render_output()
        expected = "\x1b[32m\x1b[40m\x1b[22m0: default_name\x1b[0m\x1b[32m\x1b[40m\x1b[22m | \x1b[0m\x1b[33m\x1b[40m\x1b[22m['vanilla', 'caramel', 'chocolate']   \x1b[0m\n\x1b[32m\x1b[40m\x1b[22m1: default_name\x1b[0m\x1b[33m\x1b[40m\x1b[22m | \x1b[0m\x1b[33m\x1b[40m\x1b[22m['vanilla', 'caramel', 'chocolate']   \x1b[0m\n\x1b[37m\x1b[40m\x1b[22m2: default_name\x1b[0m\x1b[37m\x1b[40m\x1b[22m | \x1b[0m\x1b[36m\x1b[40m\x1b[22m['butter pecan', 'mint chocolate chip', 'cookies n cream']   \x1b[0m\n\x1b[37m\x1b[40m\x1b[22m3: default_name\x1b[0m\x1b[36m\x1b[40m\x1b[22m | \x1b[0m\x1b[36m\x1b[40m\x1b[22m['caramel', 'dead rodent guts']   \x1b[0m"
        self.assertEqual(actual, expected)
        gv.render()

    def test_color_init(self):
        """Test the rendering of a GroupView object with initial color list"""
        gm = GroupModel(object_models=[self.om1, self.om2, self.om3, self.om4], colors=['dim green', 'green'])
        gv = gm.render_view()
        actual = gv.get_render_output()
        expected =  "\x1b[32m\x1b[40m\x1b[2m0: default_name\x1b[0m\x1b[32m\x1b[40m\x1b[2m | \x1b[0m\x1b[32m\x1b[40m\x1b[2m['vanilla', 'caramel', 'chocolate']   \x1b[0m\n\x1b[32m\x1b[40m\x1b[22m1: default_name\x1b[0m\x1b[32m\x1b[40m\x1b[22m | \x1b[0m\x1b[32m\x1b[40m\x1b[22m['vanilla', 'caramel', 'chocolate']   \x1b[0m\n\x1b[32m\x1b[40m\x1b[2m2: default_name\x1b[0m\x1b[32m\x1b[40m\x1b[2m | \x1b[0m\x1b[32m\x1b[40m\x1b[2m['butter pecan', 'mint chocolate chip', 'cookies n cream']   \x1b[0m\n\x1b[32m\x1b[40m\x1b[22m3: default_name\x1b[0m\x1b[32m\x1b[40m\x1b[22m | \x1b[0m\x1b[32m\x1b[40m\x1b[22m['caramel', 'dead rodent guts']   \x1b[0m"
        self.assertEqual(expected, actual)
        gv.render()


    def test_colors_with_two_delimiters(self):
        """Test display of a GroupModel when the ObjectModelSpecs have three attributes to display so we get 2 delimiters to inspect"""
        gm = GroupModel(object_models=[self.om5, self.om6, self.om7], colors=['dim green', 'green'])
        gv = gm.render_view()
        render_output = gv.get_render_output()
        expected_output = "\x1b[32m\x1b[40m\x1b[2m0: \x1b[0m\x1b[32m\x1b[40m\x1b[2mdefault_name\x1b[0m\x1b[32m\x1b[40m\x1b[2m | \x1b[0m\x1b[0m\x1b[32m\x1b[40m\x1b[2m['vanilla', 'caramel', 'chocolate']\x1b[0m\x1b[32m\x1b[40m\x1b[2m | \x1b[0m\x1b[0m\x1b[32m\x1b[40m\x1b[2mhappy\x1b[0m\n\x1b[32m\x1b[40m\x1b[22m1: \x1b[0m\x1b[32m\x1b[40m\x1b[22mdefault_name\x1b[0m\x1b[32m\x1b[40m\x1b[22m | \x1b[0m\x1b[0m\x1b[32m\x1b[40m\x1b[22m['vanilla', 'caramel', 'chocolate']\x1b[0m\x1b[32m\x1b[40m\x1b[22m | \x1b[0m\x1b[0m\x1b[32m\x1b[40m\x1b[22mhappy\x1b[0m\n\x1b[32m\x1b[40m\x1b[2m2: \x1b[0m\x1b[32m\x1b[40m\x1b[2mdefault_name\x1b[0m\x1b[32m\x1b[40m\x1b[2m | \x1b[0m\x1b[0m\x1b[32m\x1b[40m\x1b[2m['butter pecan', 'mint chocolate chip', 'cookies n cream']\x1b[0m\x1b[32m\x1b[40m\x1b[2m | \x1b[0m\x1b[0m\x1b[32m\x1b[40m\x1b[2mhappy\x1b[0m\n"
        self.assertEqual(expected_output, render_output)
        gv.render()




class TestCollectionModel(unittest.TestCase):
    """Test the CollectionModel class"""
    def setUp():
        pass







if __name__ == '__main__':
    unittest.main()
