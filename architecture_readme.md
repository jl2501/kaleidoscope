The relationships between the Group,Object and Attribute models and Views:
X_Models render into X_Views which render to the screen

common steps to using kaleidoscope with an object type:
    1) create the object to be displayed via kaleidoscope
    2) create an ObjectModelSpec that says which attribtues to display with what colors
    3) create an ObjectModel from the actual object and the ObjectModelSpec
    4) the ObjectModel creates the AttributeModels (AttributeModel creates AttributeView)
    5) create a GroupModel to contain multiple objects of the same type in a sequence
    6) render the GroupModel into a GroupView (renders each ObjectModel into an
        ObjectView. Each ObjectModel renders its AttributeModels into AttributeViews)
    7) render the GroupView to display it on a screen

Collections are a TODO ATM
