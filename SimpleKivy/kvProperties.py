from kivy.properties import BooleanProperty,NumericProperty,StringProperty,ListProperty,ObjectProperty,BoundedNumericProperty,OptionProperty,AliasProperty,VariableListProperty, Property
from .utils import resolve_color



class ColorProperty(Property):
    """Custom property for handling colors as RGBA lists"""
    
    def __init__(self, defaultvalue=None, **kwargs):
        if defaultvalue == None:
            defaultvalue = [1, 1, 1, 1]  # default white
        defaultvalue=resolve_color(defaultvalue)
        super().__init__(defaultvalue=defaultvalue, **kwargs)
    
    def get(self, obj):
        """Getter always returns a 4-element list"""
        value = super().get(obj)
        if value is None:
            return [1, 1, 1, 1]
        if len(value) == 3:
            return list(value) + [1.0]
        return list(value)
    
    def set(self, obj, value):
        """Setter uses resolve_color to convert input to RGBA"""
        resolved = resolve_color(value)
        super().set(obj, resolved)