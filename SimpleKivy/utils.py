from kivy.clock import Clock
import types
import time
import re
import os
import re
import sys
from pathlib import Path
from kivy.resources import resource_paths, resource_add_path, resource_remove_path
from kivy.utils import platform
from typing import List, Optional
_did_auto_config=False
class DotDict:
    def __init__(self,**kwargs):
        self._orignal=kwargs
        for k,v in kwargs.items():
            setattr(self,k,v)
class PosHints(DotDict):
    def __getattr__(self,name):
        if name in self._orignal:
            return self._orignal[name]
        # print('-'*20)
        # print(f"{name=}")
        xp,yp=name.split('_')
        if xp in ('top','bottom') or yp in ('left','right'):
            yp,xp=xp,yp

        if xp in ('center','mid'):
            xp='center_x'
        if yp in ('center','mid'):
            yp='center_y'
        
        # print(f"{(xp,yp)=}")
        hint=self._orignal[xp].copy()
        # print('hint0=',hint)
        hint.update(self._orignal[yp])
        # print(f"{hint=}")
        return hint
pos_hints=PosHints(
    center={"center_x":.5,"center_y":.5},
    center_x={"center_x":.5},
    center_y={"center_y":.5},
    top={'top':1},
    bottom={'bottom':0},
    left={'left':0},
    right={'right':1},
    )
# print(pos_hints.top_center)

def schedule_multiple_once(*callbacks,timeout=0):
    for ci in callbacks:
        Clock.schedule_once(ci,timeout)

def callback_schedule(callback,timeout=0,*args,**kwargs):
    lc=lambda dt:callback(*args,**kwargs)
    Clock.schedule_once(lc,timeout=timeout)

def app_schedule_get_call(key,method,*args,**kwargs):
    Clock.schedule_once(lambda dt:getattr(get_kvApp()[key],method)(*args,**kwargs))

def create_derived_class(instance,**kwargs):
    class base(instance.__class__):
        pass
    # setattr(base,'lcolor',instance.lcolor)
    for k,v in kwargs.items():
        setattr(base,k,v)
    for k,v in instance.properties().items():
        setattr(base,k,v)
    return base

# def create_derived_class(instance, class_name="Derived"):
#     """
#     Creates a new class derived from instance's class, with all attributes
#     (including bound methods) from the instance transferred to the new class.
#     """
#     # Get the original class
#     original_class = instance.__class__
    
#     # Collect all instance attributes that differ from class defaults
#     modified_attrs = {}
    
#     for name, value in vars(instance).items():
#         # Skip special attributes
#         # if name.startswith('__') and name.endswith('__'):
#         #     continue
            
#         # Get class value if it exists
#         class_value = getattr(original_class, name, None)
        
#         # If attribute is different from class version or doesn't exist in class
#         if not (isinstance(value, types.MethodType) and value.__self__ is instance) and \
#            (not hasattr(original_class, name) or class_value != value):
#             modified_attrs[name] = value
    
#     # Handle bound methods - we need to create unbound methods for the new class
#     for name, method in vars(original_class).items():
#         if isinstance(method, (types.FunctionType, classmethod, staticmethod)):
#             # Get the potentially modified method from the instance
#             instance_method = getattr(instance, name, None)
#             if instance_method is not None and instance_method != method:
#                 if isinstance(instance_method, types.MethodType):
#                     # Convert bound method to unbound method for the new class
#                     modified_attrs[name] = instance_method.__func__
#                 else:
#                     modified_attrs[name] = instance_method
    
#     # Create the new class
#     new_class = type(class_name, (original_class,), modified_attrs)
    
#     return new_class


def wait_result(callback,interval=.2):
    while True:
        ans=callback()
        if ans:
            return ans
        time.sleep(.2)
def do_nothing(*a,**kw):
    pass
# def lambda_schedule_once()

# _kvWindow=[None]
# _kvApp=[None]
_kvApp = None
# _kvTextInput=[None]
def __getattr__(name):
    match name:
        case 'TextInput':
            from kivy.uix.textinput import TextInput
            return TextInput
        case 'Window':
            from kivy.core.window import Window
            return Window
        case 'SpinnerOption':
            from kivy.uix.spinner import SpinnerOption
            return SpinnerOption
        case 'Spinner':
            from kivy.uix.spinner import Spinner
            return Spinner
        case 'App':
            from kivy.app import App
            return App
        case 'DropDown':
            from kivy.uix.dropdown import DropDown
            return DropDown
        case 'Camera':
            from kivy.uix.image import Image
            from kivy.clock import Clock
            from kivy.graphics.texture import Texture
            from kivy.core.image import Image as CoreImage
            from kivy.properties import NumericProperty,OptionProperty,BooleanProperty
            import cv2
            class Camera(Image):
                state = OptionProperty("stop",options=("play","stop"))
                flipcode = OptionProperty(-1,options=(-1,0,1))
                _record_clock_event=None
                camera_index=NumericProperty(0)
                capture=None
                frame_texture=None
                playing=BooleanProperty(False)
                force_stop=False

                def __init__(self,**kwargs):
                #     # self.register_event_type('on_ref_press')
                    super(Camera, self).__init__(**kwargs)

                def on_camera_index(self,isinstance,value):
                    if self.capture:
                        self.capture.release()
                    self.start()

                def start(self):
                    self.capture = cv2.VideoCapture(self.camera_index)
                def close(self):
                    if self.capture:
                        self.stop()
                        self.capture.release()
                        self.capture=None

                def play(self):
                    if not self.capture:
                        self.start()

                    if not self._record_clock_event:
                        self._record_clock_event=Clock.schedule_interval(self.update, 1.0/30)
                    else:
                        self._record_clock_event.cancel()
                        self._record_clock_event()
                    self.playing=True
                def stop(self):
                    if self._record_clock_event:
                        self._record_clock_event.cancel()
                        self.playing=False

                def update(self, dt):
                    if self.force_stop:
                        self.close()
                        return
                    ret, frame = self.capture.read()
                    buf1 = cv2.flip(frame, self.flipcode)
                    buf = buf1.tobytes()
                    self.frame_texture=Texture.create(size=(frame.shape[1], frame.shape[0]), colorfmt='rgb')
                    self.frame_texture.blit_buffer(buf, colorfmt='bgr', bufferfmt='ubyte')
                    self.texture=self.frame_texture
                def on_state(self,ins,val):
                    print("Camera state = ",val)
                    if val=="play":
                        self.play()
                    elif val=="stop":
                        self.stop()
                        self.close()

            return Camera

        # case 'SplashScreen':
        #     if platform=='win':

        #         return SplashScreen
        #     else:
        #         raise AttributeError(f'This Feature has not been implemented for your platform "{platform}"')    

        case _:
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
def get_kvWindow():
    if _kvWindow[0]:
        pass
    else:
        from kivy.core.window import Window
        # class MyWindow(Window):  # Replace 'Window' with the actual base class name
        #     def __init__(self, *args, **kwargs):
        #         # Call the parent class constructor with the provided arguments
        #         super().__init__(*args, **kwargs)
                
        #         # Get the caller's frame information to extract line number and file name
        #         caller_frame = inspect.stack()[1]
        #         caller_file = caller_frame.filename
        #         caller_line = caller_frame.lineno
                
        #         # Print information about instantiation
        #         print(f"MyWindow instantiated at line {caller_line} in file {caller_file}")
        _kvWindow[0]=Window
    return _kvWindow[0]

def get_kvApp():
    global _kvApp
    # if _kvApp[0]:
    #     pass
    # else:
    #     from kivy.app import App
    #     _kvApp[0]=App.get_running_app()
    # return _kvApp[0]

    if _kvApp:
        pass
    else:
        from kivy.app import App
        _kvApp=App.get_running_app()
    return _kvApp

app_get=get_kvApp

def is_iterable(obj):
    try:
        iter(obj)
        return True
    except TypeError:
        return False

# def get_kvApp():
#     if _kvApp[0]:
#         pass
#     else:
#         from kivy.app import App
#         _kvApp[0]=App.get_running_app()
#     return _kvApp[0]


def auto_config(size=(800,600),exit_on_escape=False,multisamples=2,desktop=True,resizable=True,multitouch_emulation=False,**kwargs):
    global _did_auto_config
    from kivy.config import Config
    Config.set('kivy', 'exit_on_escape', int(exit_on_escape))
    Config.set('kivy', 'desktop', int(desktop))
    Config.set('graphics', 'resizable', int(resizable))
    Config.set('graphics', 'multisamples', multisamples)
    if not multitouch_emulation:
        Config.set('input', 'mouse', 'mouse,disable_multitouch')
    if size[0]:
        Config.set('graphics', 'width', size[0])
    if size[1]:
        Config.set('graphics', 'height', size[1])

    for k,v in kwargs.items():
        for kk,vv in v.items():
            Config.set(k, kk, vv)
    _did_auto_config=True


    # if title:
    #     from kivy.app import App
    #     _app=App.get_running_app()
    #     _app.title=title

SK_PATH_FILE = os.path.abspath(__file__)
SK_PATH = os.path.dirname(SK_PATH_FILE)
resource_add_path(SK_PATH)

abc='ABCDEFGHIJKLMNOPQRSTUVWXYZ'

def _event_manager(app,event):
    print('Event:',event)

def import_from(module, name):
    module = __import__(module, fromlist=[name])
    return getattr(module, name)

def get_transition(tname='slide'):
    t=import_from('kivy.uix.screenmanager',tname.title().replace('out','Out').replace('in','In')+'Transition')
    return t

def re_search(*args,default='',**kwargs):
    ans=re.search(*args,**kwargs)
    if not ans:
        return default
    else:
        return ans.group()
    # print(size)

class infinite:
    def __init__(self,*args,_name='',**kwargs):
        self._name=_name
        try:
            super(infinite, self).__init__(**kwargs)
        except:
            pass
    def __call__(self,*args,**kwargs):
        return infinite()
    def __getitem__(self, var, **args):
        if var in self.__dict__:
            v = self.__dict__[var]
            return v
        else:
            v=infinite()
            self.__dict__[var]=v
            return v
    def __getattr__(self, name):
        return infinite(_name=name)
    def __enter__(self,*args):
        return infinite()
    def __exit__(self,*args):
        return infinite()

class CaseInsensitiveDict(dict):

    @classmethod
    def _k(cls, key):
        return key.lower() if isinstance(key, str) else key

    def __init__(self, *args, **kwargs):
        super(CaseInsensitiveDict, self).__init__(*args, **kwargs)
        self._convert_keys()

    def __getitem__(self, key):
        return super(CaseInsensitiveDict, self).__getitem__(self.__class__._k(key))

    def __setitem__(self, key, value):
        super(CaseInsensitiveDict, self).__setitem__(
            self.__class__._k(key), value)

    def __delitem__(self, key):
        return super(CaseInsensitiveDict, self).__delitem__(self.__class__._k(key))

    def __contains__(self, key):
        return super(CaseInsensitiveDict, self).__contains__(self.__class__._k(key))

    def has_key(self, key):
        return super(CaseInsensitiveDict, self).has_key(self.__class__._k(key))

    def pop(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).pop(self.__class__._k(key), *args, **kwargs)

    def get(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).get(self.__class__._k(key), *args, **kwargs)

    def setdefault(self, key, *args, **kwargs):
        return super(CaseInsensitiveDict, self).setdefault(self.__class__._k(key), *args, **kwargs)

    def update(self, E={}, **F):
        super(CaseInsensitiveDict, self).update(self.__class__(E))
        super(CaseInsensitiveDict, self).update(self.__class__(**F))

    def _convert_keys(self):
        for k in list(self.keys()):
            v = super(CaseInsensitiveDict, self).pop(k)
            self.__setitem__(k, v)

class _Void:
    def __init__(self):
        pass
    
    def __add__(self, other):
        return other
    
    def __radd__(self, other):
        return other
    
    def __sub__(self, other):
        return other
    
    def __rsub__(self, other):
        return other
    
    def __mul__(self, other):
        return other
    
    def __rmul__(self, other):
        return other
    
    def __truediv__(self, other):
        return other
    
    def __rtruediv__(self, other):
        return other
    def __repr__(self):
        return ''
    def __str__(self):
        return ''
    def __float__(self):
        return 0.
    def __int__(self):
        return 0

def is_number(s):
    try:
        # Try converting the string to float
        float_num = float(s)
        return True
    except ValueError:
        # If ValueError is raised, it means the string is not a valid number
        return False



def find_letter_number_pairs(s):
    pattern = r'\b[a-zA-Z]\d+\b'
    matches = re.findall(pattern, s)
    return matches


class NamedColors:
    _colors={'': (0, 0, 0, 0), 'aliceblue': (0.9411764705882353, 0.9725490196078431, 1.0, 1.0), 'antiquewhite': (0.9803921568627451, 0.9215686274509803, 0.8431372549019608, 1.0), 'aqua': (0.0, 1.0, 1.0, 1.0), 'aquamarine': (0.4980392156862745, 1.0, 0.8313725490196079, 1.0), 'azure': (0.9411764705882353, 1.0, 1.0, 1.0), 'beige': (0.9607843137254902, 0.9607843137254902, 0.8627450980392157, 1.0), 'bisque': (1.0, 0.8941176470588236, 0.7686274509803922, 1.0), 'black': (0.0, 0.0, 0.0, 1.0), 'blanchedalmond': (1.0, 0.9215686274509803, 0.803921568627451, 1.0), 'blue': (0.0, 0.0, 1.0, 1.0), 'blueviolet': (0.5411764705882353, 0.16862745098039217, 0.8862745098039215, 1.0), 'brown': (0.6470588235294118, 0.16470588235294117, 0.16470588235294117, 1.0), 'burlywood': (0.8705882352941177, 0.7215686274509804, 0.5294117647058824, 1.0), 'cadetblue': (0.37254901960784315, 0.6196078431372549, 0.6274509803921569, 1.0), 'chartreuse': (0.4980392156862745, 1.0, 0.0, 1.0), 'chocolate': (0.8235294117647058, 0.4117647058823529, 0.11764705882352941, 1.0), 'coral': (1.0, 0.4980392156862745, 0.3137254901960784, 1.0), 'cornflowerblue': (0.39215686274509803, 0.5843137254901961, 0.9294117647058824, 1.0), 'cornsilk': (1.0, 0.9725490196078431, 0.8627450980392157, 1.0), 'crimson': (0.8627450980392157, 0.0784313725490196, 0.23529411764705882, 1.0), 'cyan': (0.0, 1.0, 1.0, 1.0), 'darkblue': (0.0, 0.0, 0.5450980392156862, 1.0), 'darkcyan': (0.0, 0.5450980392156862, 0.5450980392156862, 1.0), 'darkgoldenrod': (0.7215686274509804, 0.5254901960784314, 0.043137254901960784, 1.0), 'darkgray': (0.6627450980392157, 0.6627450980392157, 0.6627450980392157, 1.0), 'darkgreen': (0.0, 0.39215686274509803, 0.0, 1.0), 'darkgrey': (0.6627450980392157, 0.6627450980392157, 0.6627450980392157, 1.0), 'darkkhaki': (0.7411764705882353, 0.7176470588235294, 0.4196078431372549, 1.0), 'darkmagenta': (0.5450980392156862, 0.0, 0.5450980392156862, 1.0), 'darkolivegreen': (0.3333333333333333, 0.4196078431372549, 0.1843137254901961, 1.0), 'darkorange': (1.0, 0.5490196078431373, 0.0, 1.0), 'darkorchid': (0.6, 0.19607843137254902, 0.8, 1.0), 'darkred': (0.5450980392156862, 0.0, 0.0, 1.0), 'darksalmon': (0.9137254901960784, 0.5882352941176471, 0.47843137254901963, 1.0), 'darkseagreen': (0.5607843137254902, 0.7372549019607844, 0.5607843137254902, 1.0), 'darkslateblue': (0.2823529411764706, 0.23921568627450981, 0.5450980392156862, 1.0), 'darkslategray': (0.1843137254901961, 0.30980392156862746, 0.30980392156862746, 1.0), 'darkslategrey': (0.1843137254901961, 0.30980392156862746, 0.30980392156862746, 1.0), 'darkturquoise': (0.0, 0.807843137254902, 0.8196078431372549, 1.0), 'darkviolet': (0.5803921568627451, 0.0, 0.8274509803921568, 1.0), 'deeppink': (1.0, 0.0784313725490196, 0.5764705882352941, 1.0), 'deepskyblue': (0.0, 0.7490196078431373, 1.0, 1.0), 'dimgray': (0.4117647058823529, 0.4117647058823529, 0.4117647058823529, 1.0), 'dimgrey': (0.4117647058823529, 0.4117647058823529, 0.4117647058823529, 1.0), 'dodgerblue': (0.11764705882352941, 0.5647058823529412, 1.0, 1.0), 'firebrick': (0.6980392156862745, 0.13333333333333333, 0.13333333333333333, 1.0), 'floralwhite': (1.0, 0.9803921568627451, 0.9411764705882353, 1.0), 'forestgreen': (0.13333333333333333, 0.5450980392156862, 0.13333333333333333, 1.0), 'fuchsia': (1.0, 0.0, 1.0, 1.0), 'gainsboro': (0.8627450980392157, 0.8627450980392157, 0.8627450980392157, 1.0), 'ghostwhite': (0.9725490196078431, 0.9725490196078431, 1.0, 1.0), 'gold': (1.0, 0.8431372549019608, 0.0, 1.0), 'goldenrod': (0.8549019607843137, 0.6470588235294118, 0.12549019607843137, 1.0), 'gray': (0.5019607843137255, 0.5019607843137255, 0.5019607843137255, 1.0), 'green': (0.0, 0.5019607843137255, 0.0, 1.0), 'greenyellow': (0.6784313725490196, 1.0, 0.1843137254901961, 1.0), 'grey': (0.5019607843137255, 0.5019607843137255, 0.5019607843137255, 1.0), 'honeydew': (0.9411764705882353, 1.0, 0.9411764705882353, 1.0), 'hotpink': (1.0, 0.4117647058823529, 0.7058823529411765, 1.0), 'indianred': (0.803921568627451, 0.3607843137254902, 0.3607843137254902, 1.0), 'indigo': (0.29411764705882354, 0.0, 0.5098039215686274, 1.0), 'ivory': (1.0, 1.0, 0.9411764705882353, 1.0), 'khaki': (0.9411764705882353, 0.9019607843137255, 0.5490196078431373, 1.0), 'lavender': (0.9019607843137255, 0.9019607843137255, 0.9803921568627451, 1.0), 'lavenderblush': (1.0, 0.9411764705882353, 0.9607843137254902, 1.0), 'lawngreen': (0.48627450980392156, 0.9882352941176471, 0.0, 1.0), 'lemonchiffon': (1.0, 0.9803921568627451, 0.803921568627451, 1.0), 'lightblue': (0.6784313725490196, 0.8470588235294118, 0.9019607843137255, 1.0), 'lightcoral': (0.9411764705882353, 0.5019607843137255, 0.5019607843137255, 1.0), 'lightcyan': (0.8784313725490196, 1.0, 1.0, 1.0), 'lightgoldenrodyellow': (0.9803921568627451, 0.9803921568627451, 0.8235294117647058, 1.0), 'lightgray': (0.8274509803921568, 0.8274509803921568, 0.8274509803921568, 1.0), 'lightgreen': (0.5647058823529412, 0.9333333333333333, 0.5647058823529412, 1.0), 'lightgrey': (0.8274509803921568, 0.8274509803921568, 0.8274509803921568, 1.0), 'lightpink': (1.0, 0.7137254901960784, 0.7568627450980392, 1.0), 'lightsalmon': (1.0, 0.6274509803921569, 0.47843137254901963, 1.0), 'lightseagreen': (0.12549019607843137, 0.6980392156862745, 0.6666666666666666, 1.0), 'lightskyblue': (0.5294117647058824, 0.807843137254902, 0.9803921568627451, 1.0), 'lightslategray': (0.4666666666666667, 0.5333333333333333, 0.6, 1.0), 'lightslategrey': (0.4666666666666667, 0.5333333333333333, 0.6, 1.0), 'lightsteelblue': (0.6901960784313725, 0.7686274509803922, 0.8705882352941177, 1.0), 'lightyellow': (1.0, 1.0, 0.8784313725490196, 1.0), 'lime': (0.0, 1.0, 0.0, 1.0), 'limegreen': (0.19607843137254902, 0.803921568627451, 0.19607843137254902, 1.0), 'linen': (0.9803921568627451, 0.9411764705882353, 0.9019607843137255, 1.0), 'magenta': (1.0, 0.0, 1.0, 1.0), 'maroon': (0.5019607843137255, 0.0, 0.0, 1.0), 'mediumaquamarine': (0.4, 0.803921568627451, 0.6666666666666666, 1.0), 'mediumblue': (0.0, 0.0, 0.803921568627451, 1.0), 'mediumorchid': (0.7294117647058823, 0.3333333333333333, 0.8274509803921568, 1.0), 'mediumpurple': (0.5764705882352941, 0.4392156862745098, 0.8588235294117647, 1.0), 'mediumseagreen': (0.23529411764705882, 0.7019607843137254, 0.44313725490196076, 1.0), 'mediumslateblue': (0.4823529411764706, 0.40784313725490196, 0.9333333333333333, 1.0), 'mediumspringgreen': (0.0, 0.9803921568627451, 0.6039215686274509, 1.0), 'mediumturquoise': (0.2823529411764706, 0.8196078431372549, 0.8, 1.0), 'mediumvioletred': (0.7803921568627451, 0.08235294117647059, 0.5215686274509804, 1.0), 'midnightblue': (0.09803921568627451, 0.09803921568627451, 0.4392156862745098, 1.0), 'mintcream': (0.9607843137254902, 1.0, 0.9803921568627451, 1.0), 'mistyrose': (1.0, 0.8941176470588236, 0.8823529411764706, 1.0), 'moccasin': (1.0, 0.8941176470588236, 0.7098039215686275, 1.0), 'navajowhite': (1.0, 0.8705882352941177, 0.6784313725490196, 1.0), 'navy': (0.0, 0.0, 0.5019607843137255, 1.0), 'oldlace': (0.9921568627450981, 0.9607843137254902, 0.9019607843137255, 1.0), 'olive': (0.5019607843137255, 0.5019607843137255, 0.0, 1.0), 'olivedrab': (0.4196078431372549, 0.5568627450980392, 0.13725490196078433, 1.0), 'orange': (1.0, 0.6470588235294118, 0.0, 1.0), 'orangered': (1.0, 0.27058823529411763, 0.0, 1.0), 'orchid': (0.8549019607843137, 0.4392156862745098, 0.8392156862745098, 1.0), 'palegoldenrod': (0.9333333333333333, 0.9098039215686274, 0.6666666666666666, 1.0), 'palegreen': (0.596078431372549, 0.984313725490196, 0.596078431372549, 1.0), 'paleturquoise': (0.6862745098039216, 0.9333333333333333, 0.9333333333333333, 1.0), 'palevioletred': (0.8588235294117647, 0.4392156862745098, 0.5764705882352941, 1.0), 'papayawhip': (1.0, 0.9372549019607843, 0.8352941176470589, 1.0), 'peachpuff': (1.0, 0.8549019607843137, 0.7254901960784313, 1.0), 'peru': (0.803921568627451, 0.5215686274509804, 0.24705882352941178, 1.0), 'pink': (1.0, 0.7529411764705882, 0.796078431372549, 1.0), 'plum': (0.8666666666666667, 0.6274509803921569, 0.8666666666666667, 1.0), 'powderblue': (0.6901960784313725, 0.8784313725490196, 0.9019607843137255, 1.0), 'purple': (0.5019607843137255, 0.0, 0.5019607843137255, 1.0), 'rebeccapurple': (0.4, 0.2, 0.6, 1.0), 'red': (1.0, 0.0, 0.0, 1.0), 'rosybrown': (0.7372549019607844, 0.5607843137254902, 0.5607843137254902, 1.0), 'royalblue': (0.2549019607843137, 0.4117647058823529, 0.8823529411764706, 1.0), 'saddlebrown': (0.5450980392156862, 0.27058823529411763, 0.07450980392156863, 1.0), 'salmon': (0.9803921568627451, 0.5019607843137255, 0.4470588235294118, 1.0), 'sandybrown': (0.9568627450980393, 0.6431372549019608, 0.3764705882352941, 1.0), 'seagreen': (0.1803921568627451, 0.5450980392156862, 0.3411764705882353, 1.0), 'seashell': (1.0, 0.9607843137254902, 0.9333333333333333, 1.0), 'sienna': (0.6274509803921569, 0.3215686274509804, 0.17647058823529413, 1.0), 'silver': (0.7529411764705882, 0.7529411764705882, 0.7529411764705882, 1.0), 'skyblue': (0.5294117647058824, 0.807843137254902, 0.9215686274509803, 1.0), 'slateblue': (0.41568627450980394, 0.35294117647058826, 0.803921568627451, 1.0), 'slategray': (0.4392156862745098, 0.5019607843137255, 0.5647058823529412, 1.0), 'slategrey': (0.4392156862745098, 0.5019607843137255, 0.5647058823529412, 1.0), 'snow': (1.0, 0.9803921568627451, 0.9803921568627451, 1.0), 'springgreen': (0.0, 1.0, 0.4980392156862745, 1.0), 'steelblue': (0.27450980392156865, 0.5098039215686274, 0.7058823529411765, 1.0), 'tan': (0.8235294117647058, 0.7058823529411765, 0.5490196078431373, 1.0), 'teal': (0.0, 0.5019607843137255, 0.5019607843137255, 1.0), 'thistle': (0.8470588235294118, 0.7490196078431373, 0.8470588235294118, 1.0), 'tomato': (1.0, 0.38823529411764707, 0.2784313725490196, 1.0), 'turquoise': (0.25098039215686274, 0.8784313725490196, 0.8156862745098039, 1.0), 'violet': (0.9333333333333333, 0.5098039215686274, 0.9333333333333333, 1.0), 'wheat': (0.9607843137254902, 0.8705882352941177, 0.7019607843137254, 1.0), 'white': (1.0, 1.0, 1.0, 1.0), 'whitesmoke': (0.9607843137254902, 0.9607843137254902, 0.9607843137254902, 1.0), 'yellow': (1.0, 1.0, 0.0, 1.0), 'yellowgreen': (0.6039215686274509, 0.803921568627451, 0.19607843137254902, 1.0), 'b': (0.0, 0.0, 1.0, 1), 'g': (0.0, 0.5, 0.0, 1), 'r': (1.0, 0.0, 0.0, 1), 'c': (0.0, 0.75, 0.75, 1), 'm': (0.75, 0.0, 0.75, 1), 'y': (0.75, 0.75, 0.0, 1), 'k': (0.0, 0.0, 0.0, 1), 'w': (1.0, 1.0, 1.0, 1)}
    _tab={'blue': (0.12156862745098039, 0.4666666666666667, 0.7058823529411765, 1.0), 'orange': (1.0, 0.4980392156862745, 0.054901960784313725, 1.0), 'green': (0.17254901960784313, 0.6274509803921569, 0.17254901960784313, 1.0), 'red': (0.8392156862745098, 0.15294117647058825, 0.1568627450980392, 1.0), 'purple': (0.5803921568627451, 0.403921568627451, 0.7411764705882353, 1.0), 'brown': (0.5490196078431373, 0.33725490196078434, 0.29411764705882354, 1.0), 'pink': (0.8901960784313725, 0.4666666666666667, 0.7607843137254902, 1.0), 'gray': (0.4980392156862745, 0.4980392156862745, 0.4980392156862745, 1.0), 'olive': (0.7372549019607844, 0.7411764705882353, 0.13333333333333333, 1.0), 'cyan': (0.09019607843137255, 0.7450980392156863, 0.8117647058823529, 1.0), 'grey': (0.4980392156862745, 0.4980392156862745, 0.4980392156862745, 1.0)}
    _xkcd={'cloudy blue': (0.6745098039215687, 0.7607843137254902, 0.8509803921568627, 1.0), 'dark pastel green': (0.33725490196078434, 0.6823529411764706, 0.3411764705882353, 1.0), 'dust': (0.6980392156862745, 0.6, 0.43137254901960786, 1.0), 'electric lime': (0.6588235294117647, 1.0, 0.01568627450980392, 1.0), 'fresh green': (0.4117647058823529, 0.8470588235294118, 0.30980392156862746, 1.0), 'light eggplant': (0.5372549019607843, 0.27058823529411763, 0.5215686274509804, 1.0), 'nasty green': (0.4392156862745098, 0.6980392156862745, 0.24705882352941178, 1.0), 'really light blue': (0.8313725490196079, 1.0, 1.0, 1.0), 'tea': (0.396078431372549, 0.6705882352941176, 0.48627450980392156, 1.0), 'warm purple': (0.5843137254901961, 0.1803921568627451, 0.5607843137254902, 1.0), 'yellowish tan': (0.9882352941176471, 0.9882352941176471, 0.5058823529411764, 1.0), 'cement': (0.6470588235294118, 0.6392156862745098, 0.5686274509803921, 1.0), 'dark grass green': (0.2196078431372549, 0.5019607843137255, 0.01568627450980392, 1.0), 'dusty teal': (0.2980392156862745, 0.5647058823529412, 0.5215686274509804, 1.0), 'grey teal': (0.3686274509803922, 0.6078431372549019, 0.5411764705882353, 1.0), 'macaroni and cheese': (0.9372549019607843, 0.7058823529411765, 0.20784313725490197, 1.0), 'pinkish tan': (0.8509803921568627, 0.6078431372549019, 0.5098039215686274, 1.0), 'spruce': (0.0392156862745098, 0.37254901960784315, 0.2196078431372549, 1.0), 'strong blue': (0.047058823529411764, 0.023529411764705882, 0.9686274509803922, 1.0), 'toxic green': (0.3803921568627451, 0.8705882352941177, 0.16470588235294117, 1.0), 'windows blue': (0.21568627450980393, 0.47058823529411764, 0.7490196078431373, 1.0), 'blue blue': (0.13333333333333333, 0.25882352941176473, 0.7803921568627451, 1.0), 'blue with a hint of purple': (0.3254901960784314, 0.23529411764705882, 0.7764705882352941, 1.0), 'booger': (0.6078431372549019, 0.7098039215686275, 0.23529411764705882, 1.0), 'bright sea green': (0.0196078431372549, 1.0, 0.6509803921568628, 1.0), 'dark green blue': (0.12156862745098039, 0.38823529411764707, 0.3411764705882353, 1.0), 'deep turquoise': (0.00392156862745098, 0.45098039215686275, 0.4549019607843137, 1.0), 'green teal': (0.047058823529411764, 0.7098039215686275, 0.4666666666666667, 1.0), 'strong pink': (1.0, 0.027450980392156862, 0.5372549019607843, 1.0), 'bland': (0.6862745098039216, 0.6588235294117647, 0.5450980392156862, 1.0), 'deep aqua': (0.03137254901960784, 0.47058823529411764, 0.4980392156862745, 1.0), 'lavender pink': (0.8666666666666667, 0.5215686274509804, 0.8431372549019608, 1.0), 'light moss green': (0.6509803921568628, 0.7843137254901961, 0.4588235294117647, 1.0), 'light seafoam green': (0.6549019607843137, 1.0, 0.7098039215686275, 1.0), 'olive yellow': (0.7607843137254902, 0.7176470588235294, 0.03529411764705882, 1.0), 'pig pink': (0.9058823529411765, 0.5568627450980392, 0.6470588235294118, 1.0), 'deep lilac': (0.5882352941176471, 0.43137254901960786, 0.7411764705882353, 1.0), 'desert': (0.8, 0.6784313725490196, 0.3764705882352941, 1.0), 'dusty lavender': (0.6745098039215687, 0.5254901960784314, 0.6588235294117647, 1.0), 'purpley grey': (0.5803921568627451, 0.49411764705882355, 0.5803921568627451, 1.0), 'purply': (0.596078431372549, 0.24705882352941178, 0.6980392156862745, 1.0), 'candy pink': (1.0, 0.38823529411764707, 0.9137254901960784, 1.0), 'light pastel green': (0.6980392156862745, 0.984313725490196, 0.6470588235294118, 1.0), 'boring green': (0.38823529411764707, 0.7019607843137254, 0.396078431372549, 1.0), 'kiwi green': (0.5568627450980392, 0.8980392156862745, 0.24705882352941178, 1.0), 'light grey green': (0.7176470588235294, 0.8823529411764706, 0.6313725490196078, 1.0), 'orange pink': (1.0, 0.43529411764705883, 0.3215686274509804, 1.0), 'tea green': (0.7411764705882353, 0.9725490196078431, 0.6392156862745098, 1.0), 'very light brown': (0.8274509803921568, 0.7137254901960784, 0.5137254901960784, 1.0), 'egg shell': (1.0, 0.9882352941176471, 0.7686274509803922, 1.0), 'eggplant purple': (0.2627450980392157, 0.0196078431372549, 0.2549019607843137, 1.0), 'powder pink': (1.0, 0.6980392156862745, 0.8156862745098039, 1.0), 'reddish grey': (0.6, 0.4588235294117647, 0.4392156862745098, 1.0), 'baby shit brown': (0.6784313725490196, 0.5647058823529412, 0.050980392156862744, 1.0), 'liliac': (0.7686274509803922, 0.5568627450980392, 0.9921568627450981, 1.0), 'stormy blue': (0.3137254901960784, 0.4823529411764706, 0.611764705882353, 1.0), 'ugly brown': (0.49019607843137253, 0.44313725490196076, 0.011764705882352941, 1.0), 'custard': (1.0, 0.9921568627450981, 0.47058823529411764, 1.0), 'darkish pink': (0.8549019607843137, 0.27450980392156865, 0.49019607843137253, 1.0), 'deep brown': (0.2549019607843137, 0.00784313725490196, 0.0, 1.0), 'greenish beige': (0.788235294117647, 0.8196078431372549, 0.4745098039215686, 1.0), 'manilla': (1.0, 0.9803921568627451, 0.5254901960784314, 1.0), 'off blue': (0.33725490196078434, 0.5176470588235295, 0.6823529411764706, 1.0), 'battleship grey': (0.4196078431372549, 0.48627450980392156, 0.5215686274509804, 1.0), 'browny green': (0.43529411764705883, 0.4235294117647059, 0.0392156862745098, 1.0), 'bruise': (0.49411764705882355, 0.25098039215686274, 0.44313725490196076, 1.0), 'kelley green': (0.0, 0.5764705882352941, 0.21568627450980393, 1.0), 'sickly yellow': (0.8156862745098039, 0.8941176470588236, 0.1607843137254902, 1.0), 'sunny yellow': (1.0, 0.9764705882352941, 0.09019607843137255, 1.0), 'azul': (0.11372549019607843, 0.36470588235294116, 0.9254901960784314, 1.0), 'darkgreen': (0.0196078431372549, 0.28627450980392155, 0.027450980392156862, 1.0), 'green/yellow': (0.7098039215686275, 0.807843137254902, 0.03137254901960784, 1.0), 'lichen': (0.5607843137254902, 0.7137254901960784, 0.4823529411764706, 1.0), 'light light green': (0.7843137254901961, 1.0, 0.6901960784313725, 1.0), 'pale gold': (0.9921568627450981, 0.8705882352941177, 0.4235294117647059, 1.0), 'sun yellow': (1.0, 0.8745098039215686, 0.13333333333333333, 1.0), 'tan green': (0.6627450980392157, 0.7450980392156863, 0.4392156862745098, 1.0), 'burple': (0.40784313725490196, 0.19607843137254902, 0.8901960784313725, 1.0), 'butterscotch': (0.9921568627450981, 0.6941176470588235, 0.2784313725490196, 1.0), 'toupe': (0.7803921568627451, 0.6745098039215687, 0.49019607843137253, 1.0), 'dark cream': (1.0, 0.9529411764705882, 0.6039215686274509, 1.0), 'indian red': (0.5215686274509804, 0.054901960784313725, 0.01568627450980392, 1.0), 'light lavendar': (0.9372549019607843, 0.7529411764705882, 0.996078431372549, 1.0), 'poison green': (0.25098039215686274, 0.9921568627450981, 0.0784313725490196, 1.0), 'baby puke green': (0.7137254901960784, 0.7686274509803922, 0.023529411764705882, 1.0), 'bright yellow green': (0.615686274509804, 1.0, 0.0, 1.0), 'charcoal grey': (0.23529411764705882, 0.2549019607843137, 0.25882352941176473, 1.0), 'squash': (0.9490196078431372, 0.6705882352941176, 0.08235294117647059, 1.0), 'cinnamon': (0.6745098039215687, 0.30980392156862746, 0.023529411764705882, 1.0), 'light pea green': (0.7686274509803922, 0.996078431372549, 0.5098039215686274, 1.0), 'radioactive green': (0.17254901960784313, 0.9803921568627451, 0.12156862745098039, 1.0), 'raw sienna': (0.6039215686274509, 0.3843137254901961, 0.0, 1.0), 'baby purple': (0.792156862745098, 0.6078431372549019, 0.9686274509803922, 1.0), 'cocoa': (0.5294117647058824, 0.37254901960784315, 0.25882352941176473, 1.0), 'light royal blue': (0.22745098039215686, 0.1803921568627451, 0.996078431372549, 1.0), 'orangeish': (0.9921568627450981, 0.5529411764705883, 0.28627450980392155, 1.0), 'rust brown': (0.5450980392156862, 0.19215686274509805, 0.011764705882352941, 1.0), 'sand brown': (0.796078431372549, 0.6470588235294118, 0.3764705882352941, 1.0), 'swamp': (0.4117647058823529, 0.5137254901960784, 0.2235294117647059, 1.0), 'tealish green': (0.047058823529411764, 0.8627450980392157, 0.45098039215686275, 1.0), 'burnt siena': (0.7176470588235294, 0.3215686274509804, 0.011764705882352941, 1.0), 'camo': (0.4980392156862745, 0.5607843137254902, 0.3058823529411765, 1.0), 'dusk blue': (0.14901960784313725, 0.3254901960784314, 0.5529411764705883, 1.0), 'fern': (0.38823529411764707, 0.6627450980392157, 0.3137254901960784, 1.0), 'old rose': (0.7843137254901961, 0.4980392156862745, 0.5372549019607843, 1.0), 'pale light green': (0.6941176470588235, 0.9882352941176471, 0.6, 1.0), 'peachy pink': (1.0, 0.6039215686274509, 0.5411764705882353, 1.0), 'rosy pink': (0.9647058823529412, 0.40784313725490196, 0.5568627450980392, 1.0), 'light bluish green': (0.4627450980392157, 0.9921568627450981, 0.6588235294117647, 1.0), 'light bright green': (0.3254901960784314, 0.996078431372549, 0.3607843137254902, 1.0), 'light neon green': (0.3058823529411765, 0.9921568627450981, 0.32941176470588235, 1.0), 'light seafoam': (0.6274509803921569, 0.996078431372549, 0.7490196078431373, 1.0), 'tiffany blue': (0.4823529411764706, 0.9490196078431372, 0.8549019607843137, 1.0), 'washed out green': (0.7372549019607844, 0.9607843137254902, 0.6509803921568628, 1.0), 'browny orange': (0.792156862745098, 0.4196078431372549, 0.00784313725490196, 1.0), 'nice blue': (0.06274509803921569, 0.47843137254901963, 0.6901960784313725, 1.0), 'sapphire': (0.12941176470588237, 0.2196078431372549, 0.6705882352941176, 1.0), 'greyish teal': (0.44313725490196076, 0.6235294117647059, 0.5686274509803921, 1.0), 'orangey yellow': (0.9921568627450981, 0.7254901960784313, 0.08235294117647059, 1.0), 'parchment': (0.996078431372549, 0.9882352941176471, 0.6862745098039216, 1.0), 'straw': (0.9882352941176471, 0.9647058823529412, 0.4745098039215686, 1.0), 'very dark brown': (0.11372549019607843, 0.00784313725490196, 0.0, 1.0), 'terracota': (0.796078431372549, 0.40784313725490196, 0.2627450980392157, 1.0), 'ugly blue': (0.19215686274509805, 0.4, 0.5411764705882353, 1.0), 'clear blue': (0.1411764705882353, 0.47843137254901963, 0.9921568627450981, 1.0), 'creme': (1.0, 1.0, 0.7137254901960784, 1.0), 'foam green': (0.5647058823529412, 0.9921568627450981, 0.6627450980392157, 1.0), 'grey/green': (0.5254901960784314, 0.6313725490196078, 0.49019607843137253, 1.0), 'light gold': (0.9921568627450981, 0.8627450980392157, 0.3607843137254902, 1.0), 'seafoam blue': (0.47058823529411764, 0.8196078431372549, 0.7137254901960784, 1.0), 'topaz': (0.07450980392156863, 0.7333333333333333, 0.6862745098039216, 1.0), 
        'violet pink': (0.984313725490196, 0.37254901960784315, 0.9882352941176471, 1.0), 'wintergreen': (0.12549019607843137, 0.9764705882352941, 0.5254901960784314, 1.0), 'yellow tan': (1.0, 0.8901960784313725, 0.43137254901960786, 1.0), 'dark fuchsia': (0.615686274509804, 0.027450980392156862, 0.34901960784313724, 1.0), 'indigo blue': (0.22745098039215686, 0.09411764705882353, 0.6941176470588235, 1.0), 'light yellowish green': (0.7607843137254902, 1.0, 0.5372549019607843, 1.0), 'pale magenta': (0.8431372549019608, 0.403921568627451, 0.6784313725490196, 1.0), 'rich purple': (0.4470588235294118, 0.0, 0.34509803921568627, 1.0), 'sunflower yellow': (1.0, 0.8549019607843137, 0.011764705882352941, 1.0), 'green/blue': (0.00392156862745098, 0.7529411764705882, 0.5529411764705883, 1.0), 'leather': (0.6745098039215687, 0.4549019607843137, 0.20392156862745098, 1.0), 'racing green': (0.00392156862745098, 0.27450980392156865, 0.0, 1.0), 'vivid purple': (0.6, 0.0, 0.9803921568627451, 1.0), 'dark royal blue': (0.00784313725490196, 0.023529411764705882, 0.43529411764705883, 1.0), 'hazel': (0.5568627450980392, 0.4627450980392157, 0.09411764705882353, 1.0), 'muted pink': (0.8196078431372549, 0.4627450980392157, 0.5607843137254902, 1.0), 'booger green': (0.5882352941176471, 0.7058823529411765, 0.011764705882352941, 1.0), 'canary': (0.9921568627450981, 1.0, 0.38823529411764707, 1.0), 'cool grey': (0.5843137254901961, 0.6392156862745098, 0.6509803921568628, 1.0), 'dark taupe': (0.4980392156862745, 0.40784313725490196, 0.3058823529411765, 1.0), 'darkish purple': (0.4588235294117647, 0.09803921568627451, 0.45098039215686275, 1.0), 'true green': (0.03137254901960784, 0.5803921568627451, 0.01568627450980392, 1.0), 'coral pink': (1.0, 0.3803921568627451, 0.38823529411764707, 1.0), 'dark sage': (0.34901960784313724, 0.5215686274509804, 0.33725490196078434, 1.0), 'dark slate blue': (0.12941176470588237, 0.2784313725490196, 0.3803921568627451, 1.0), 'flat blue': (0.23529411764705882, 0.45098039215686275, 0.6588235294117647, 1.0), 'mushroom': (0.7294117647058823, 0.6196078431372549, 0.5333333333333333, 1.0), 'rich blue': (0.00784313725490196, 0.10588235294117647, 0.9764705882352941, 1.0), 'dirty purple': (0.45098039215686275, 0.2901960784313726, 0.396078431372549, 1.0), 'greenblue': (0.13725490196078433, 0.7686274509803922, 0.5450980392156862, 1.0), 'icky green': (0.5607843137254902, 0.6823529411764706, 0.13333333333333333, 1.0), 'light khaki': (0.9019607843137255, 0.9490196078431372, 0.6352941176470588, 1.0), 'warm blue': (0.29411764705882354, 0.3411764705882353, 0.8588235294117647, 1.0), 'dark hot pink': (0.8509803921568627, 0.00392156862745098, 0.4, 1.0), 'deep sea blue': (0.00392156862745098, 0.32941176470588235, 0.5098039215686274, 1.0), 'carmine': (0.615686274509804, 0.00784313725490196, 0.08627450980392157, 1.0), 'dark yellow green': (0.4470588235294118, 0.5607843137254902, 0.00784313725490196, 1.0), 'pale peach': (1.0, 0.8980392156862745, 0.6784313725490196, 1.0), 'plum purple': (0.3058823529411765, 0.0196078431372549, 0.3137254901960784, 1.0), 'golden rod': (0.9764705882352941, 0.7372549019607844, 0.03137254901960784, 1.0), 'neon red': (1.0, 0.027450980392156862, 0.22745098039215686, 1.0), 'old pink': (0.7803921568627451, 0.4745098039215686, 0.5254901960784314, 1.0), 'very pale blue': (0.8392156862745098, 1.0, 0.996078431372549, 1.0), 'blood orange': (0.996078431372549, 0.29411764705882354, 0.011764705882352941, 1.0), 'grapefruit': (0.9921568627450981, 0.34901960784313724, 0.33725490196078434, 1.0), 'sand yellow': (0.9882352941176471, 0.8823529411764706, 0.4, 1.0), 'clay brown': (0.6980392156862745, 0.44313725490196076, 0.23921568627450981, 1.0), 'dark blue grey': (0.12156862745098039, 0.23137254901960785, 0.30196078431372547, 1.0), 'flat green': (0.4117647058823529, 0.615686274509804, 0.2980392156862745, 1.0), 'light green blue': (0.33725490196078434, 0.9882352941176471, 0.6352941176470588, 1.0), 'warm pink': (0.984313725490196, 0.3333333333333333, 0.5058823529411764, 1.0), 'dodger blue': (0.24313725490196078, 0.5098039215686274, 0.9882352941176471, 1.0), 'gross green': (0.6274509803921569, 0.7490196078431373, 0.08627450980392157, 1.0), 'ice': (0.8392156862745098, 1.0, 0.9803921568627451, 1.0), 'metallic blue': (0.30980392156862746, 0.45098039215686275, 0.5568627450980392, 1.0), 'pale salmon': (1.0, 0.6941176470588235, 0.6039215686274509, 1.0), 'sap green': (0.3607843137254902, 0.5450980392156862, 0.08235294117647059, 1.0), 'algae': (0.32941176470588235, 0.6745098039215687, 0.40784313725490196, 1.0), 'bluey grey': (0.5372549019607843, 0.6274509803921569, 0.6901960784313725, 1.0), 'greeny grey': (0.49411764705882355, 0.6274509803921569, 0.47843137254901963, 1.0), 'highlighter green': (0.10588235294117647, 0.9882352941176471, 0.023529411764705882, 1.0), 'light light blue': (0.792156862745098, 1.0, 0.984313725490196, 1.0), 'light mint': (0.7137254901960784, 1.0, 0.7333333333333333, 1.0), 'raw umber': (0.6549019607843137, 0.3686274509803922, 0.03529411764705882, 1.0), 'vivid blue': (0.08235294117647059, 0.1803921568627451, 1.0, 1.0), 'deep lavender': (0.5529411764705883, 0.3686274509803922, 0.7176470588235294, 1.0), 'dull teal': (0.37254901960784315, 0.6196078431372549, 0.5607843137254902, 1.0), 'light greenish blue': (0.38823529411764707, 0.9686274509803922, 0.7058823529411765, 1.0), 'mud green': (0.3764705882352941, 0.4, 0.00784313725490196, 1.0), 'pinky': (0.9882352941176471, 0.5254901960784314, 0.6666666666666666, 1.0), 'red wine': (0.5490196078431373, 0.0, 0.20392156862745098, 1.0), 'shit green': (0.4588235294117647, 0.5019607843137255, 0.0, 1.0), 'tan brown': (0.6705882352941176, 0.49411764705882355, 0.2980392156862745, 1.0), 'darkblue': (0.011764705882352941, 0.027450980392156862, 0.39215686274509803, 1.0), 'rosa': (0.996078431372549, 0.5254901960784314, 0.6431372549019608, 1.0), 'lipstick': (0.8352941176470589, 0.09019607843137255, 0.3058823529411765, 1.0), 'pale mauve': (0.996078431372549, 0.8156862745098039, 0.9882352941176471, 1.0), 'claret': (0.40784313725490196, 0.0, 0.09411764705882353, 1.0), 'dandelion': (0.996078431372549, 0.8745098039215686, 0.03137254901960784, 1.0), 'orangered': (0.996078431372549, 0.25882352941176473, 0.058823529411764705, 1.0), 'poop green': (0.43529411764705883, 0.48627450980392156, 0.0, 1.0), 'ruby': (0.792156862745098, 0.00392156862745098, 0.2784313725490196, 1.0), 'dark': (0.10588235294117647, 0.1411764705882353, 0.19215686274509805, 1.0), 'greenish turquoise': (0.0, 0.984313725490196, 0.6901960784313725, 1.0), 'pastel red': (0.8588235294117647, 0.34509803921568627, 0.33725490196078434, 1.0), 'piss yellow': (0.8666666666666667, 0.8392156862745098, 0.09411764705882353, 1.0), 'bright cyan': (0.2549019607843137, 0.9921568627450981, 0.996078431372549, 1.0), 'dark coral': (0.8117647058823529, 0.3215686274509804, 0.3058823529411765, 1.0), 'algae green': (0.12941176470588237, 0.7647058823529411, 0.43529411764705883, 1.0), 'darkish red': (0.6627450980392157, 0.011764705882352941, 0.03137254901960784, 1.0), 'reddy brown': (0.43137254901960786, 0.06274509803921569, 0.0196078431372549, 1.0), 'blush pink': (0.996078431372549, 0.5098039215686274, 0.5490196078431373, 1.0), 'camouflage green': (0.29411764705882354, 0.3803921568627451, 0.07450980392156863, 1.0), 'lawn green': (0.30196078431372547, 0.6431372549019608, 0.03529411764705882, 1.0), 'putty': (0.7450980392156863, 0.6823529411764706, 0.5411764705882353, 1.0), 'vibrant blue': (0.011764705882352941, 0.2235294117647059, 0.9725490196078431, 1.0), 'dark sand': (0.6588235294117647, 0.5607843137254902, 0.34901960784313724, 1.0), 'purple/blue': (0.36470588235294116, 0.12941176470588237, 0.8156862745098039, 1.0), 'saffron': (0.996078431372549, 0.6980392156862745, 0.03529411764705882, 1.0), 'twilight': (0.3058823529411765, 0.3176470588235294, 0.5450980392156862, 1.0), 'warm brown': (0.5882352941176471, 0.3058823529411765, 0.00784313725490196, 1.0), 'bluegrey': (0.5215686274509804, 0.6392156862745098, 0.6980392156862745, 1.0), 'bubble gum pink': (1.0, 0.4117647058823529, 0.6862745098039216, 1.0), 'duck egg blue': (0.7647058823529411, 0.984313725490196, 0.9568627450980393, 1.0), 'greenish cyan': (0.16470588235294117, 0.996078431372549, 0.7176470588235294, 1.0), 'petrol': (0.0, 0.37254901960784315, 0.41568627450980394, 1.0), 'royal': (0.047058823529411764, 0.09019607843137255, 0.5764705882352941, 1.0), 'butter': (1.0, 1.0, 0.5058823529411764, 1.0), 'dusty orange': (0.9411764705882353, 0.5137254901960784, 0.22745098039215686, 1.0), 'off yellow': (0.9450980392156862, 0.9529411764705882, 0.24705882352941178, 1.0), 'pale olive green': (0.6941176470588235, 0.8235294117647058, 0.4823529411764706, 1.0), 'orangish': (0.9882352941176471, 0.5098039215686274, 0.2901960784313726, 1.0), 'leaf': (0.44313725490196076, 0.6666666666666666, 0.20392156862745098, 1.0), 'light blue grey': (0.7176470588235294, 0.788235294117647, 0.8862745098039215, 1.0), 'dried blood': (0.29411764705882354, 0.00392156862745098, 0.00392156862745098, 1.0), 'lightish purple': (0.6470588235294118, 0.3215686274509804, 0.9019607843137255, 1.0), 'rusty red': (0.6862745098039216, 0.1843137254901961, 0.050980392156862744, 1.0), 'lavender blue': (0.5450980392156862, 0.5333333333333333, 0.9725490196078431, 1.0), 'light grass green': (0.6039215686274509, 0.9686274509803922, 0.39215686274509803, 1.0), 'light mint green': (0.6509803921568628, 0.984313725490196, 0.6980392156862745, 1.0), 'sunflower': (1.0, 0.7725490196078432, 0.07058823529411765, 1.0), 'velvet': (0.4588235294117647, 0.03137254901960784, 0.3176470588235294, 1.0), 'brick orange': (0.7568627450980392, 0.2901960784313726, 0.03529411764705882, 1.0), 'lightish red': (0.996078431372549, 0.1843137254901961, 0.2901960784313726, 1.0), 'pure blue': (0.00784313725490196, 0.011764705882352941, 0.8862745098039215, 1.0), 'twilight blue': (0.0392156862745098, 0.2627450980392157, 0.47843137254901963, 1.0), 'violet red': (0.6470588235294118, 0.0, 0.3333333333333333, 1.0), 'yellowy brown': (0.6823529411764706, 0.5450980392156862, 0.047058823529411764, 1.0), 'carnation': (0.9921568627450981, 0.4745098039215686, 0.5607843137254902, 1.0), 'muddy yellow': (0.7490196078431373, 0.6745098039215687, 0.0196078431372549, 1.0), 'dark seafoam green': (0.24313725490196078, 0.6862745098039216, 0.4627450980392157, 1.0), 'deep rose': (0.7803921568627451, 0.2784313725490196, 0.403921568627451, 1.0), 
        'dusty red': (0.7254901960784313, 0.2823529411764706, 0.3058823529411765, 1.0), 'grey/blue': (0.39215686274509803, 0.49019607843137253, 0.5568627450980392, 1.0), 'lemon lime': (0.7490196078431373, 0.996078431372549, 0.1568627450980392, 1.0), 'purple/pink': (0.8431372549019608, 0.1450980392156863, 0.8705882352941177, 1.0), 'brown yellow': (0.6980392156862745, 0.592156862745098, 0.0196078431372549, 1.0), 'purple brown': (0.403921568627451, 0.22745098039215686, 0.24705882352941178, 1.0), 'wisteria': (0.6588235294117647, 0.49019607843137253, 0.7607843137254902, 1.0), 'banana yellow': (0.9803921568627451, 0.996078431372549, 0.29411764705882354, 1.0), 'lipstick red': (0.7529411764705882, 0.00784313725490196, 0.1843137254901961, 1.0), 'water blue': (0.054901960784313725, 0.5294117647058824, 0.8, 1.0), 'brown grey': (0.5529411764705883, 0.5176470588235295, 0.40784313725490196, 1.0), 'vibrant purple': (0.6784313725490196, 0.011764705882352941, 0.8705882352941177, 1.0), 'baby green': (0.5490196078431373, 1.0, 0.6196078431372549, 1.0), 'barf green': (0.5803921568627451, 0.6745098039215687, 0.00784313725490196, 1.0), 'eggshell blue': (0.7686274509803922, 1.0, 0.9686274509803922, 1.0), 'sandy yellow': (0.9921568627450981, 0.9333333333333333, 0.45098039215686275, 1.0), 'cool green': (0.2, 0.7215686274509804, 0.39215686274509803, 1.0), 'pale': (1.0, 0.9764705882352941, 0.8156862745098039, 1.0), 'blue/grey': (0.4588235294117647, 0.5529411764705883, 0.6392156862745098, 1.0), 'hot magenta': (0.9607843137254902, 0.01568627450980392, 0.788235294117647, 1.0), 'greyblue': (0.4666666666666667, 0.6313725490196078, 0.7098039215686275, 1.0), 'purpley': (0.5294117647058824, 0.33725490196078434, 0.8941176470588236, 1.0), 'baby shit green': (0.5333333333333333, 0.592156862745098, 0.09019607843137255, 1.0), 'brownish pink': (0.7607843137254902, 0.49411764705882355, 0.4745098039215686, 1.0), 'dark aquamarine': (0.00392156862745098, 0.45098039215686275, 0.44313725490196076, 1.0), 'diarrhea': (0.6235294117647059, 0.5137254901960784, 0.011764705882352941, 1.0), 'light mustard': (0.9686274509803922, 0.8352941176470589, 0.3764705882352941, 1.0), 'pale sky blue': (0.7411764705882353, 0.9647058823529412, 0.996078431372549, 1.0), 'turtle green': (0.4588235294117647, 0.7215686274509804, 0.30980392156862746, 1.0), 'bright olive': (0.611764705882353, 0.7333333333333333, 0.01568627450980392, 1.0), 'dark grey blue': (0.1607843137254902, 0.27450980392156865, 0.3568627450980392, 1.0), 'greeny brown': (0.4117647058823529, 0.3764705882352941, 0.023529411764705882, 1.0), 'lemon green': (0.6784313725490196, 0.9725490196078431, 0.00784313725490196, 1.0), 'light periwinkle': (0.7568627450980392, 0.7764705882352941, 0.9882352941176471, 1.0), 'seaweed green': (0.20784313725490197, 0.6784313725490196, 0.4196078431372549, 1.0), 'sunshine yellow': (1.0, 0.9921568627450981, 0.21568627450980393, 1.0), 'ugly purple': (0.6431372549019608, 0.25882352941176473, 0.6274509803921569, 1.0), 'medium pink': (0.9529411764705882, 0.3803921568627451, 0.5882352941176471, 1.0), 'puke brown': (0.5803921568627451, 0.4666666666666667, 0.023529411764705882, 1.0), 'very light pink': (1.0, 0.9568627450980393, 0.9490196078431372, 1.0), 'viridian': (0.11764705882352941, 0.5686274509803921, 0.403921568627451, 1.0), 'bile': (0.7098039215686275, 0.7647058823529411, 0.023529411764705882, 1.0), 'faded yellow': (0.996078431372549, 1.0, 0.4980392156862745, 1.0), 'very pale green': (0.8117647058823529, 0.9921568627450981, 0.7372549019607844, 1.0), 'vibrant green': (0.0392156862745098, 0.8666666666666667, 0.03137254901960784, 1.0), 'bright lime': (0.5294117647058824, 0.9921568627450981, 0.0196078431372549, 1.0), 'spearmint': (0.11764705882352941, 0.9725490196078431, 0.4627450980392157, 1.0), 'light aquamarine': (0.4823529411764706, 0.9921568627450981, 0.7803921568627451, 1.0), 'light sage': (0.7372549019607844, 0.9254901960784314, 0.6745098039215687, 1.0), 'yellowgreen': (0.7333333333333333, 0.9764705882352941, 0.058823529411764705, 1.0), 'baby poo': (0.6705882352941176, 0.5647058823529412, 0.01568627450980392, 1.0), 'dark seafoam': (0.12156862745098039, 0.7098039215686275, 0.47843137254901963, 1.0), 'deep teal': (0.0, 0.3333333333333333, 0.35294117647058826, 1.0), 'heather': (0.6431372549019608, 0.5176470588235295, 0.6745098039215687, 1.0), 'rust orange': (0.7686274509803922, 0.3333333333333333, 0.03137254901960784, 1.0), 'dirty blue': (0.24705882352941178, 0.5098039215686274, 0.615686274509804, 1.0), 'fern green': (0.32941176470588235, 0.5529411764705883, 0.26666666666666666, 1.0), 'bright lilac': (0.788235294117647, 0.3686274509803922, 0.984313725490196, 1.0), 'weird green': (0.22745098039215686, 0.8980392156862745, 0.4980392156862745, 1.0), 'peacock blue': (0.00392156862745098, 0.403921568627451, 0.5843137254901961, 1.0), 'avocado green': (0.5294117647058824, 0.6627450980392157, 0.13333333333333333, 1.0), 'faded orange': (0.9411764705882353, 0.5803921568627451, 0.30196078431372547, 1.0), 'grape purple': (0.36470588235294116, 0.0784313725490196, 0.3176470588235294, 1.0), 'hot green': (0.1450980392156863, 1.0, 0.1607843137254902, 1.0), 'lime yellow': (0.8156862745098039, 0.996078431372549, 0.11372549019607843, 1.0), 'mango': (1.0, 0.6509803921568628, 0.16862745098039217, 1.0), 'shamrock': (0.00392156862745098, 0.7058823529411765, 0.2980392156862745, 1.0), 'bubblegum': (1.0, 0.4235294117647059, 0.7098039215686275, 1.0), 'purplish brown': (0.4196078431372549, 0.25882352941176473, 0.2784313725490196, 1.0), 'vomit yellow': (0.7803921568627451, 0.7568627450980392, 0.047058823529411764, 1.0), 'pale cyan': (0.7176470588235294, 1.0, 0.9803921568627451, 1.0), 'key lime': (0.6823529411764706, 1.0, 0.43137254901960786, 1.0), 'tomato red': (0.9254901960784314, 0.17647058823529413, 0.00392156862745098, 1.0), 'lightgreen': (0.4627450980392157, 1.0, 0.4823529411764706, 1.0), 'merlot': (0.45098039215686275, 0.0, 0.2235294117647059, 1.0), 'night blue': (0.01568627450980392, 0.011764705882352941, 0.2823529411764706, 1.0), 'purpleish pink': (0.8745098039215686, 0.3058823529411765, 0.7843137254901961, 1.0), 'apple': (0.43137254901960786, 0.796078431372549, 0.23529411764705882, 1.0), 'baby poop green': (0.5607843137254902, 0.596078431372549, 0.0196078431372549, 1.0), 'green apple': (0.3686274509803922, 0.8627450980392157, 0.12156862745098039, 1.0), 'heliotrope': (0.8509803921568627, 0.30980392156862746, 0.9607843137254902, 1.0), 'yellow/green': (0.7843137254901961, 0.9921568627450981, 0.23921568627450981, 1.0), 'almost black': (0.027450980392156862, 0.050980392156862744, 0.050980392156862744, 1.0), 'cool blue': (0.28627450980392155, 0.5176470588235295, 0.7215686274509804, 1.0), 'leafy green': (0.3176470588235294, 0.7176470588235294, 0.23137254901960785, 1.0), 'mustard brown': (0.6745098039215687, 0.49411764705882355, 0.01568627450980392, 1.0), 'dusk': (0.3058823529411765, 0.32941176470588235, 0.5058823529411764, 1.0), 'dull brown': (0.5294117647058824, 0.43137254901960786, 0.29411764705882354, 1.0), 'frog green': (0.34509803921568627, 0.7372549019607844, 0.03137254901960784, 1.0), 'vivid green': (0.1843137254901961, 0.9372549019607843, 0.06274509803921569, 1.0), 'bright light green': (0.17647058823529413, 0.996078431372549, 0.32941176470588235, 1.0), 'fluro green': (0.0392156862745098, 1.0, 0.00784313725490196, 1.0), 'kiwi': (0.611764705882353, 0.9372549019607843, 0.2627450980392157, 1.0), 'seaweed': (0.09411764705882353, 0.8196078431372549, 0.4823529411764706, 1.0), 'navy green': (0.20784313725490197, 0.3254901960784314, 0.0392156862745098, 1.0), 'ultramarine blue': (0.09411764705882353, 0.0196078431372549, 0.8588235294117647, 1.0), 'iris': (0.3843137254901961, 0.34509803921568627, 0.7686274509803922, 1.0), 'pastel orange': (1.0, 0.5882352941176471, 0.30980392156862746, 1.0), 'yellowish orange': (1.0, 0.6705882352941176, 0.058823529411764705, 1.0), 'perrywinkle': (0.5607843137254902, 0.5490196078431373, 0.9058823529411765, 1.0), 'tealish': (0.1411764705882353, 0.7372549019607844, 0.6588235294117647, 1.0), 'dark plum': (0.24705882352941178, 0.00392156862745098, 0.17254901960784313, 1.0), 'pear': (0.796078431372549, 0.9725490196078431, 0.37254901960784315, 1.0), 'pinkish orange': (1.0, 0.4470588235294118, 0.2980392156862745, 1.0), 'midnight purple': (0.1568627450980392, 0.00392156862745098, 0.21568627450980393, 1.0), 'light urple': (0.7019607843137254, 0.43529411764705883, 0.9647058823529412, 1.0), 'dark mint': (0.2823529411764706, 0.7529411764705882, 0.4470588235294118, 1.0), 'greenish tan': (0.7372549019607844, 0.796078431372549, 0.47843137254901963, 1.0), 'light burgundy': (0.6588235294117647, 0.2549019607843137, 0.3568627450980392, 1.0), 'turquoise blue': (0.023529411764705882, 0.6941176470588235, 0.7686274509803922, 1.0), 'ugly pink': (0.803921568627451, 0.4588235294117647, 0.5176470588235295, 1.0), 'sandy': (0.9450980392156862, 0.8549019607843137, 0.47843137254901963, 1.0), 'electric pink': (1.0, 0.01568627450980392, 0.5647058823529412, 1.0), 'muted purple': (0.5019607843137255, 0.3568627450980392, 0.5294117647058824, 1.0), 'mid green': (0.3137254901960784, 0.6549019607843137, 0.2784313725490196, 1.0), 'greyish': (0.6588235294117647, 0.6431372549019608, 0.5843137254901961, 1.0), 'neon yellow': (0.8117647058823529, 1.0, 0.01568627450980392, 1.0), 'banana': (1.0, 1.0, 0.49411764705882355, 1.0), 'carnation pink': (1.0, 0.4980392156862745, 0.6549019607843137, 1.0), 'tomato': (0.9372549019607843, 0.25098039215686274, 0.14901960784313725, 1.0), 'sea': (0.23529411764705882, 0.6, 0.5725490196078431, 1.0), 'muddy brown': (0.5333333333333333, 0.40784313725490196, 0.023529411764705882, 1.0), 'turquoise green': (0.01568627450980392, 0.9568627450980393, 0.5372549019607843, 1.0), 'buff': (0.996078431372549, 0.9647058823529412, 0.6196078431372549, 1.0), 'fawn': (0.8117647058823529, 0.6862745098039216, 0.4823529411764706, 1.0), 'muted blue': (0.23137254901960785, 0.44313725490196076, 0.6235294117647059, 1.0), 'pale rose': (0.9921568627450981, 0.7568627450980392, 0.7725490196078432, 1.0), 'dark mint green': (0.12549019607843137, 0.7529411764705882, 0.45098039215686275, 1.0), 'amethyst': (0.6078431372549019, 0.37254901960784315, 0.7529411764705882, 1.0), 'blue/green': (0.058823529411764705, 0.6078431372549019, 0.5568627450980392, 1.0), 'chestnut': (0.4549019607843137, 0.1568627450980392, 0.00784313725490196, 1.0), 'sick green': (0.615686274509804, 0.7254901960784313, 0.17254901960784313, 1.0), 
        'pea': (0.6431372549019608, 0.7490196078431373, 0.12549019607843137, 1.0), 'rusty orange': (0.803921568627451, 0.34901960784313724, 0.03529411764705882, 1.0), 'stone': (0.6784313725490196, 0.6470588235294118, 0.5294117647058824, 1.0), 'rose red': (0.7450980392156863, 0.00392156862745098, 0.23529411764705882, 1.0), 'pale aqua': (0.7215686274509804, 1.0, 0.9215686274509803, 1.0), 'deep orange': (0.8627450980392157, 0.30196078431372547, 0.00392156862745098, 1.0), 'earth': (0.6352941176470588, 0.396078431372549, 0.24313725490196078, 1.0), 'mossy green': (0.38823529411764707, 0.5450980392156862, 0.15294117647058825, 1.0), 'grassy green': (0.2549019607843137, 0.611764705882353, 0.011764705882352941, 1.0), 'pale lime green': (0.6941176470588235, 1.0, 0.396078431372549, 1.0), 'light grey blue': (0.615686274509804, 0.7372549019607844, 0.8313725490196079, 1.0), 'pale grey': (0.9921568627450981, 0.9921568627450981, 0.996078431372549, 1.0), 'asparagus': (0.4666666666666667, 0.6705882352941176, 0.33725490196078434, 1.0), 'blueberry': (0.27450980392156865, 0.2549019607843137, 0.5882352941176471, 1.0), 'purple red': (0.6, 0.00392156862745098, 0.2784313725490196, 1.0), 'pale lime': (0.7450980392156863, 0.9921568627450981, 0.45098039215686275, 1.0), 'greenish teal': (0.19607843137254902, 0.7490196078431373, 0.5176470588235295, 1.0), 'caramel': (0.6862745098039216, 0.43529411764705883, 0.03529411764705882, 1.0), 'deep magenta': (0.6274509803921569, 0.00784313725490196, 0.3607843137254902, 1.0), 'light peach': (1.0, 0.8470588235294118, 0.6941176470588235, 1.0), 'milk chocolate': (0.4980392156862745, 0.3058823529411765, 0.11764705882352941, 1.0), 'ocher': (0.7490196078431373, 0.6078431372549019, 0.047058823529411764, 1.0), 'off green': (0.4196078431372549, 0.6392156862745098, 0.3254901960784314, 1.0), 'purply pink': (0.9411764705882353, 0.4588235294117647, 0.9019607843137255, 1.0), 'lightblue': (0.4823529411764706, 0.7843137254901961, 0.9647058823529412, 1.0), 'dusky blue': (0.2784313725490196, 0.37254901960784315, 0.5803921568627451, 1.0), 'golden': (0.9607843137254902, 0.7490196078431373, 0.011764705882352941, 1.0), 'light beige': (1.0, 0.996078431372549, 0.7137254901960784, 1.0), 'butter yellow': (1.0, 0.9921568627450981, 0.4549019607843137, 1.0), 'dusky purple': (0.5372549019607843, 0.3568627450980392, 0.4823529411764706, 1.0), 'french blue': (0.2627450980392157, 0.4196078431372549, 0.6784313725490196, 1.0), 'ugly yellow': (0.8156862745098039, 0.7568627450980392, 0.00392156862745098, 1.0), 'greeny yellow': (0.7764705882352941, 0.9725490196078431, 0.03137254901960784, 1.0), 'orangish red': (0.9568627450980393, 0.21176470588235294, 0.0196078431372549, 1.0), 'shamrock green': (0.00784313725490196, 0.7568627450980392, 0.30196078431372547, 1.0), 'orangish brown': (0.6980392156862745, 0.37254901960784315, 0.011764705882352941, 1.0), 'tree green': (0.16470588235294117, 0.49411764705882355, 0.09803921568627451, 1.0), 'deep violet': (0.28627450980392155, 0.023529411764705882, 0.2823529411764706, 1.0), 'gunmetal': (0.3254901960784314, 0.3843137254901961, 0.403921568627451, 1.0), 'blue/purple': (0.35294117647058826, 0.023529411764705882, 0.9372549019607843, 1.0), 'cherry': (0.8117647058823529, 0.00784313725490196, 0.20392156862745098, 1.0), 'sandy brown': (0.7686274509803922, 0.6509803921568628, 0.3803921568627451, 1.0), 'warm grey': (0.592156862745098, 0.5411764705882353, 0.5176470588235295, 1.0), 'dark indigo': (0.12156862745098039, 0.03529411764705882, 0.32941176470588235, 1.0), 'midnight': (0.011764705882352941, 0.00392156862745098, 0.17647058823529413, 1.0), 'bluey green': (0.16862745098039217, 0.6941176470588235, 0.4745098039215686, 1.0), 'grey pink': (0.7647058823529411, 0.5647058823529412, 0.6078431372549019, 1.0), 'soft purple': (0.6509803921568628, 0.43529411764705883, 0.7098039215686275, 1.0), 'blood': (0.4666666666666667, 0.0, 0.00392156862745098, 1.0), 'brown red': (0.5725490196078431, 0.16862745098039217, 0.0196078431372549, 1.0), 'medium grey': (0.49019607843137253, 0.4980392156862745, 0.48627450980392156, 1.0), 'berry': (0.6, 0.058823529411764705, 0.29411764705882354, 1.0), 'poo': (0.5607843137254902, 0.45098039215686275, 0.011764705882352941, 1.0), 'purpley pink': (0.7843137254901961, 0.23529411764705882, 0.7254901960784313, 1.0), 'light salmon': (0.996078431372549, 0.6627450980392157, 0.5764705882352941, 1.0), 'snot': (0.6745098039215687, 0.7333333333333333, 0.050980392156862744, 1.0), 'easter purple': (0.7529411764705882, 0.44313725490196076, 0.996078431372549, 1.0), 'light yellow green': (0.8, 0.9921568627450981, 0.4980392156862745, 1.0), 'dark navy blue': (0.0, 0.00784313725490196, 0.1803921568627451, 1.0), 'drab': (0.5098039215686274, 0.5137254901960784, 0.26666666666666666, 1.0), 'light rose': (1.0, 0.7725490196078432, 0.796078431372549, 1.0), 'rouge': (0.6705882352941176, 0.07058823529411765, 0.2235294117647059, 1.0), 'purplish red': (0.6901960784313725, 0.0196078431372549, 0.29411764705882354, 1.0), 'slime green': (0.6, 0.8, 0.01568627450980392, 1.0), 'baby poop': (0.5764705882352941, 0.48627450980392156, 0.0, 1.0), 'irish green': (0.00392156862745098, 0.5843137254901961, 0.1607843137254902, 1.0), 'pink/purple': (0.9372549019607843, 0.11372549019607843, 0.9058823529411765, 1.0), 'dark navy': (0.0, 0.01568627450980392, 0.20784313725490197, 1.0), 'greeny blue': (0.25882352941176473, 0.7019607843137254, 0.5843137254901961, 1.0), 'light plum': (0.615686274509804, 0.3411764705882353, 0.5137254901960784, 1.0), 'pinkish grey': (0.7843137254901961, 0.6745098039215687, 0.6627450980392157, 1.0), 'dirty orange': (0.7843137254901961, 0.4627450980392157, 0.023529411764705882, 1.0), 'rust red': (0.6666666666666666, 0.15294117647058825, 0.01568627450980392, 1.0), 'pale lilac': (0.8941176470588236, 0.796078431372549, 1.0, 1.0), 'orangey red': (0.9803921568627451, 0.25882352941176473, 0.1411764705882353, 1.0), 'primary blue': (0.03137254901960784, 0.01568627450980392, 0.9764705882352941, 1.0), 'kermit green': (0.3607843137254902, 0.6980392156862745, 0.0, 1.0), 'brownish purple': (0.4627450980392157, 0.25882352941176473, 0.3058823529411765, 1.0), 'murky green': (0.4235294117647059, 0.47843137254901963, 0.054901960784313725, 1.0), 'wheat': (0.984313725490196, 0.8666666666666667, 0.49411764705882355, 1.0), 'very dark purple': (0.16470588235294117, 0.00392156862745098, 0.20392156862745098, 1.0), 'bottle green': (0.01568627450980392, 0.2901960784313726, 0.0196078431372549, 1.0), 'watermelon': (0.9921568627450981, 0.27450980392156865, 0.34901960784313724, 1.0), 'deep sky blue': (0.050980392156862744, 0.4588235294117647, 0.9725490196078431, 1.0), 'fire engine red': (0.996078431372549, 0.0, 0.00784313725490196, 1.0), 'yellow ochre': (0.796078431372549, 0.615686274509804, 0.023529411764705882, 1.0), 'pumpkin orange': (0.984313725490196, 0.49019607843137253, 0.027450980392156862, 1.0), 'pale olive': (0.7254901960784313, 0.8, 0.5058823529411764, 1.0), 'light lilac': (0.9294117647058824, 0.7843137254901961, 1.0, 1.0), 'lightish green': (0.3803921568627451, 0.8823529411764706, 0.3764705882352941, 1.0), 'carolina blue': (0.5411764705882353, 0.7215686274509804, 0.996078431372549, 1.0), 'mulberry': (0.5725490196078431, 0.0392156862745098, 0.3058823529411765, 1.0), 'shocking pink': (0.996078431372549, 0.00784313725490196, 0.6352941176470588, 1.0), 'auburn': (0.6039215686274509, 0.18823529411764706, 0.00392156862745098, 1.0), 'bright lime green': (0.396078431372549, 0.996078431372549, 0.03137254901960784, 1.0), 'celadon': (0.7450980392156863, 0.9921568627450981, 0.7176470588235294, 1.0), 'pinkish brown': (0.6941176470588235, 0.4470588235294118, 0.3803921568627451, 1.0), 'poo brown': (0.5333333333333333, 0.37254901960784315, 0.00392156862745098, 1.0), 'bright sky blue': (0.00784313725490196, 0.8, 0.996078431372549, 1.0), 'celery': (0.7568627450980392, 0.9921568627450981, 0.5843137254901961, 1.0), 'dirt brown': (0.5137254901960784, 0.396078431372549, 0.2235294117647059, 1.0), 'strawberry': (0.984313725490196, 0.1607843137254902, 0.2627450980392157, 1.0), 'dark lime': (0.5176470588235295, 0.7176470588235294, 0.00392156862745098, 1.0), 'copper': (0.7137254901960784, 0.38823529411764707, 0.1450980392156863, 1.0), 'medium brown': (0.4980392156862745, 0.3176470588235294, 0.07058823529411765, 1.0), 'muted green': (0.37254901960784315, 0.6274509803921569, 0.3215686274509804, 1.0), "robin's egg": (0.42745098039215684, 0.9294117647058824, 0.9921568627450981, 1.0), 'bright aqua': (0.043137254901960784, 0.9764705882352941, 0.9176470588235294, 1.0), 'bright lavender': (0.7803921568627451, 0.3764705882352941, 1.0, 1.0), 'ivory': (1.0, 1.0, 0.796078431372549, 1.0), 'very light purple': (0.9647058823529412, 0.807843137254902, 0.9882352941176471, 1.0), 'light navy': (0.08235294117647059, 0.3137254901960784, 0.5176470588235295, 1.0), 'pink red': (0.9607843137254902, 0.0196078431372549, 0.30980392156862746, 1.0), 'olive brown': (0.39215686274509803, 0.32941176470588235, 0.011764705882352941, 1.0), 'poop brown': (0.47843137254901963, 0.34901960784313724, 0.00392156862745098, 1.0), 'mustard green': (0.6588235294117647, 0.7098039215686275, 0.01568627450980392, 1.0), 'ocean green': (0.23921568627450981, 0.6, 0.45098039215686275, 1.0), 'very dark blue': (0.0, 0.00392156862745098, 0.2, 1.0), 'dusty green': (0.4627450980392157, 0.6627450980392157, 0.45098039215686275, 1.0), 'light navy blue': (0.1803921568627451, 0.35294117647058826, 0.5333333333333333, 1.0), 'minty green': (0.043137254901960784, 0.9686274509803922, 0.49019607843137253, 1.0), 'adobe': (0.7411764705882353, 0.4235294117647059, 0.2823529411764706, 1.0), 'barney': (0.6745098039215687, 0.11372549019607843, 0.7215686274509804, 1.0), 'jade green': (0.16862745098039217, 0.6862745098039216, 0.41568627450980394, 1.0), 'bright light blue': (0.14901960784313725, 0.9686274509803922, 0.9921568627450981, 1.0), 'light lime': (0.6823529411764706, 0.9921568627450981, 0.4235294117647059, 1.0), 'dark khaki': (0.6078431372549019, 0.5607843137254902, 0.3333333333333333, 1.0), 'orange yellow': (1.0, 0.6784313725490196, 0.00392156862745098, 1.0), 'ocre': (0.7764705882352941, 0.611764705882353, 0.01568627450980392, 1.0), 'maize': (0.9568627450980393, 0.8156862745098039, 0.32941176470588235, 1.0), 'faded pink': (0.8705882352941177, 0.615686274509804, 0.6745098039215687, 1.0), 'british racing green': (0.0196078431372549, 0.2823529411764706, 0.050980392156862744, 1.0), 
        'sandstone': (0.788235294117647, 0.6823529411764706, 0.4549019607843137, 1.0), 'mud brown': (0.3764705882352941, 0.27450980392156865, 0.058823529411764705, 1.0), 'light sea green': (0.596078431372549, 0.9647058823529412, 0.6901960784313725, 1.0), 'robin egg blue': (0.5411764705882353, 0.9450980392156862, 0.996078431372549, 1.0), 'aqua marine': (0.1803921568627451, 0.9098039215686274, 0.7333333333333333, 1.0), 'dark sea green': (0.06666666666666667, 0.5294117647058824, 0.36470588235294116, 1.0), 'soft pink': (0.9921568627450981, 0.6901960784313725, 0.7529411764705882, 1.0), 'orangey brown': (0.6941176470588235, 0.3764705882352941, 0.00784313725490196, 1.0), 'cherry red': (0.9686274509803922, 0.00784313725490196, 0.16470588235294117, 1.0), 'burnt yellow': (0.8352941176470589, 0.6705882352941176, 0.03529411764705882, 1.0), 'brownish grey': (0.5254901960784314, 0.4666666666666667, 0.37254901960784315, 1.0), 'camel': (0.7764705882352941, 0.6235294117647059, 0.34901960784313724, 1.0), 'purplish grey': (0.47843137254901963, 0.40784313725490196, 0.4980392156862745, 1.0), 'marine': (0.01568627450980392, 0.1803921568627451, 0.3764705882352941, 1.0), 'greyish pink': (0.7843137254901961, 0.5529411764705883, 0.5803921568627451, 1.0), 'pale turquoise': (0.6470588235294118, 0.984313725490196, 0.8352941176470589, 1.0), 'pastel yellow': (1.0, 0.996078431372549, 0.44313725490196076, 1.0), 'bluey purple': (0.3843137254901961, 0.2549019607843137, 0.7803921568627451, 1.0), 'canary yellow': (1.0, 0.996078431372549, 0.25098039215686274, 1.0), 'faded red': (0.8274509803921568, 0.28627450980392155, 0.3058823529411765, 1.0), 'sepia': (0.596078431372549, 0.3686274509803922, 0.16862745098039217, 1.0), 'coffee': (0.6509803921568628, 0.5058823529411764, 0.2980392156862745, 1.0), 'bright magenta': (1.0, 0.03137254901960784, 0.9098039215686274, 1.0), 'mocha': (0.615686274509804, 0.4627450980392157, 0.3176470588235294, 1.0), 'ecru': (0.996078431372549, 1.0, 0.792156862745098, 1.0), 'purpleish': (0.596078431372549, 0.33725490196078434, 0.5529411764705883, 1.0), 'cranberry': (0.6196078431372549, 0.0, 0.22745098039215686, 1.0), 'darkish green': (0.1568627450980392, 0.48627450980392156, 0.21568627450980393, 1.0), 'brown orange': (0.7254901960784313, 0.4117647058823529, 0.00784313725490196, 1.0), 'dusky rose': (0.7294117647058823, 0.40784313725490196, 0.45098039215686275, 1.0), 'melon': (1.0, 0.47058823529411764, 0.3333333333333333, 1.0), 'sickly green': (0.5803921568627451, 0.6980392156862745, 0.10980392156862745, 1.0), 'silver': (0.7725490196078432, 0.788235294117647, 0.7803921568627451, 1.0), 'purply blue': (0.4, 0.10196078431372549, 0.9333333333333333, 1.0), 'purpleish blue': (0.3803921568627451, 0.25098039215686274, 0.9372549019607843, 1.0), 'hospital green': (0.6078431372549019, 0.8980392156862745, 0.6666666666666666, 1.0), 'shit brown': (0.4823529411764706, 0.34509803921568627, 0.01568627450980392, 1.0), 'mid blue': (0.15294117647058825, 0.41568627450980394, 0.7019607843137254, 1.0), 'amber': (0.996078431372549, 0.7019607843137254, 0.03137254901960784, 1.0), 'easter green': (0.5490196078431373, 0.9921568627450981, 0.49411764705882355, 1.0), 'soft blue': (0.39215686274509803, 0.5333333333333333, 0.9176470588235294, 1.0), 'cerulean blue': (0.0196078431372549, 0.43137254901960786, 0.9333333333333333, 1.0), 'golden brown': (0.6980392156862745, 0.47843137254901963, 0.00392156862745098, 1.0), 'bright turquoise': (0.058823529411764705, 0.996078431372549, 0.9764705882352941, 1.0), 'red pink': (0.9803921568627451, 0.16470588235294117, 0.3333333333333333, 1.0), 'red purple': (0.5098039215686274, 0.027450980392156862, 0.2784313725490196, 1.0), 'greyish brown': (0.47843137254901963, 0.41568627450980394, 0.30980392156862746, 1.0), 'vermillion': (0.9568627450980393, 0.19607843137254902, 0.047058823529411764, 1.0), 'russet': (0.6313725490196078, 0.2235294117647059, 0.0196078431372549, 1.0), 'steel grey': (0.43529411764705883, 0.5098039215686274, 0.5411764705882353, 1.0), 'lighter purple': (0.6470588235294118, 0.35294117647058826, 0.9568627450980393, 1.0), 'bright violet': (0.6784313725490196, 0.0392156862745098, 0.9921568627450981, 1.0), 'prussian blue': (0.0, 0.27058823529411763, 0.4666666666666667, 1.0), 'slate green': (0.396078431372549, 0.5529411764705883, 0.42745098039215684, 1.0), 'dirty pink': (0.792156862745098, 0.4823529411764706, 0.5019607843137255, 1.0), 'dark blue green': (0.0, 0.3215686274509804, 0.28627450980392155, 1.0), 'pine': (0.16862745098039217, 0.36470588235294116, 0.20392156862745098, 1.0), 'yellowy green': (0.7490196078431373, 0.9450980392156862, 0.1568627450980392, 1.0), 'dark gold': (0.7098039215686275, 0.5803921568627451, 0.06274509803921569, 1.0), 'bluish': (0.1607843137254902, 0.4627450980392157, 0.7333333333333333, 1.0), 'darkish blue': (0.00392156862745098, 0.2549019607843137, 0.5098039215686274, 1.0), 'dull red': (0.7333333333333333, 0.24705882352941178, 0.24705882352941178, 1.0), 'pinky red': (0.9882352941176471, 0.14901960784313725, 0.2784313725490196, 1.0), 'bronze': (0.6588235294117647, 0.4745098039215686, 0.0, 1.0), 'pale teal': (0.5098039215686274, 0.796078431372549, 0.6980392156862745, 1.0), 'military green': (0.4, 0.48627450980392156, 0.24313725490196078, 1.0), 'barbie pink': (0.996078431372549, 0.27450980392156865, 0.6470588235294118, 1.0), 'bubblegum pink': (0.996078431372549, 0.5137254901960784, 0.8, 1.0), 'pea soup green': (0.5803921568627451, 0.6509803921568628, 0.09019607843137255, 1.0), 'dark mustard': (0.6588235294117647, 0.5372549019607843, 0.0196078431372549, 1.0), 'shit': (0.4980392156862745, 0.37254901960784315, 0.0, 1.0), 'medium purple': (0.6196078431372549, 0.2627450980392157, 0.6352941176470588, 1.0), 'very dark green': (0.023529411764705882, 0.1803921568627451, 0.011764705882352941, 1.0), 'dirt': (0.5411764705882353, 0.43137254901960786, 0.27058823529411763, 1.0), 'dusky pink': (0.8, 0.47843137254901963, 0.5450980392156862, 1.0), 'red violet': (0.6196078431372549, 0.00392156862745098, 0.40784313725490196, 1.0), 'lemon yellow': (0.9921568627450981, 1.0, 0.2196078431372549, 1.0), 'pistachio': (0.7529411764705882, 0.9803921568627451, 0.5450980392156862, 1.0), 'dull yellow': (0.9333333333333333, 0.8627450980392157, 0.3568627450980392, 1.0), 'dark lime green': (0.49411764705882355, 0.7411764705882353, 0.00392156862745098, 1.0), 'denim blue': (0.23137254901960785, 0.3568627450980392, 0.5725490196078431, 1.0), 'teal blue': (0.00392156862745098, 0.5333333333333333, 0.6235294117647059, 1.0), 'lightish blue': (0.23921568627450981, 0.47843137254901963, 0.9921568627450981, 1.0), 'purpley blue': (0.37254901960784315, 0.20392156862745098, 0.9058823529411765, 1.0), 'light indigo': (0.42745098039215684, 0.35294117647058826, 0.8117647058823529, 1.0), 'swamp green': (0.4549019607843137, 0.5215686274509804, 0.0, 1.0), 'brown green': (0.4392156862745098, 0.4235294117647059, 0.06666666666666667, 1.0), 'dark maroon': (0.23529411764705882, 0.0, 0.03137254901960784, 1.0), 'hot purple': (0.796078431372549, 0.0, 0.9607843137254902, 1.0), 'dark forest green': (0.0, 0.17647058823529413, 0.01568627450980392, 1.0), 'faded blue': (0.396078431372549, 0.5490196078431373, 0.7333333333333333, 1.0), 'drab green': (0.4549019607843137, 0.5843137254901961, 0.3176470588235294, 1.0), 'light lime green': (0.7254901960784313, 1.0, 0.4, 1.0), 'snot green': (0.615686274509804, 0.7568627450980392, 0.0, 1.0), 'yellowish': (0.9803921568627451, 0.9333333333333333, 0.4, 1.0), 'light blue green': (0.49411764705882355, 0.984313725490196, 0.7019607843137254, 1.0), 'bordeaux': (0.4823529411764706, 0.0, 0.17254901960784313, 1.0), 'light mauve': (0.7607843137254902, 0.5725490196078431, 0.6313725490196078, 1.0), 'ocean': (0.00392156862745098, 0.4823529411764706, 0.5725490196078431, 1.0), 'marigold': (0.9882352941176471, 0.7529411764705882, 0.023529411764705882, 1.0), 'muddy green': (0.396078431372549, 0.4549019607843137, 0.19607843137254902, 1.0), 'dull orange': (0.8470588235294118, 0.5254901960784314, 0.23137254901960785, 1.0), 'steel': (0.45098039215686275, 0.5215686274509804, 0.5843137254901961, 1.0), 'electric purple': (0.6666666666666666, 0.13725490196078433, 1.0, 1.0), 'fluorescent green': (0.03137254901960784, 1.0, 0.03137254901960784, 1.0), 'yellowish brown': (0.6078431372549019, 0.47843137254901963, 0.00392156862745098, 1.0), 'blush': (0.9490196078431372, 0.6196078431372549, 0.5568627450980392, 1.0), 'soft green': (0.43529411764705883, 0.7607843137254902, 0.4627450980392157, 1.0), 'bright orange': (1.0, 0.3568627450980392, 0.0, 1.0), 'lemon': (0.9921568627450981, 1.0, 0.3215686274509804, 1.0), 'purple grey': (0.5254901960784314, 0.43529411764705883, 0.5215686274509804, 1.0), 'acid green': (0.5607843137254902, 0.996078431372549, 0.03529411764705882, 1.0), 'pale lavender': (0.9333333333333333, 0.8117647058823529, 0.996078431372549, 1.0), 'violet blue': (0.3176470588235294, 0.0392156862745098, 0.788235294117647, 1.0), 'light forest green': (0.30980392156862746, 0.5686274509803921, 0.3254901960784314, 1.0), 'burnt red': (0.6235294117647059, 0.13725490196078433, 0.0196078431372549, 1.0), 'khaki green': (0.4470588235294118, 0.5254901960784314, 0.2235294117647059, 1.0), 'cerise': (0.8705882352941177, 0.047058823529411764, 0.3843137254901961, 1.0), 'faded purple': (0.5686274509803921, 0.43137254901960786, 0.6, 1.0), 'apricot': (1.0, 0.6941176470588235, 0.42745098039215684, 1.0), 'dark olive green': (0.23529411764705882, 0.30196078431372547, 0.011764705882352941, 1.0), 'grey brown': (0.4980392156862745, 0.4392156862745098, 0.3254901960784314, 1.0), 'green grey': (0.4666666666666667, 0.5725490196078431, 0.43529411764705883, 1.0), 'true blue': (0.00392156862745098, 0.058823529411764705, 0.8, 1.0), 'pale violet': (0.807843137254902, 0.6823529411764706, 0.9803921568627451, 1.0), 'periwinkle blue': (0.5607843137254902, 0.6, 0.984313725490196, 1.0), 'light sky blue': (0.7764705882352941, 0.9882352941176471, 1.0, 1.0), 'blurple': (0.3333333333333333, 0.2235294117647059, 0.8, 1.0), 'green brown': (0.32941176470588235, 0.3058823529411765, 0.011764705882352941, 1.0), 'bluegreen': (0.00392156862745098, 0.47843137254901963, 0.4745098039215686, 1.0), 'bright teal': (0.00392156862745098, 0.9764705882352941, 0.7764705882352941, 1.0), 'brownish yellow': (0.788235294117647, 0.6901960784313725, 0.011764705882352941, 1.0), 'pea soup': (0.5725490196078431, 0.6, 0.00392156862745098, 1.0), 
        'forest': (0.043137254901960784, 0.3333333333333333, 0.03529411764705882, 1.0), 'barney purple': (0.6274509803921569, 0.01568627450980392, 0.596078431372549, 1.0), 'ultramarine': (0.12549019607843137, 0.0, 0.6941176470588235, 1.0), 'purplish': (0.5803921568627451, 0.33725490196078434, 0.5490196078431373, 1.0), 'puke yellow': (0.7607843137254902, 0.7450980392156863, 0.054901960784313725, 1.0), 'bluish grey': (0.4549019607843137, 0.5450980392156862, 0.592156862745098, 1.0), 'dark periwinkle': (0.4, 0.37254901960784315, 0.8196078431372549, 1.0), 'dark lilac': (0.611764705882353, 0.42745098039215684, 0.6470588235294118, 1.0), 'reddish': (0.7686274509803922, 0.25882352941176473, 0.25098039215686274, 1.0), 'light maroon': (0.6352941176470588, 0.2823529411764706, 0.3411764705882353, 1.0), 'dusty purple': (0.5098039215686274, 0.37254901960784315, 0.5294117647058824, 1.0), 'terra cotta': (0.788235294117647, 0.39215686274509803, 0.23137254901960785, 1.0), 'avocado': (0.5647058823529412, 0.6941176470588235, 0.20392156862745098, 1.0), 'marine blue': (0.00392156862745098, 0.2196078431372549, 0.41568627450980394, 1.0), 'teal green': (0.1450980392156863, 0.6392156862745098, 0.43529411764705883, 1.0), 'slate grey': (0.34901960784313724, 0.396078431372549, 0.42745098039215684, 1.0), 'lighter green': (0.4588235294117647, 0.9921568627450981, 0.38823529411764707, 1.0), 'electric green': (0.12941176470588237, 0.9882352941176471, 0.050980392156862744, 1.0), 'dusty blue': (0.35294117647058826, 0.5254901960784314, 0.6784313725490196, 1.0), 'golden yellow': (0.996078431372549, 0.7764705882352941, 0.08235294117647059, 1.0), 'bright yellow': (1.0, 0.9921568627450981, 0.00392156862745098, 1.0), 'light lavender': (0.8745098039215686, 0.7725490196078432, 0.996078431372549, 1.0), 'umber': (0.6980392156862745, 0.39215686274509803, 0.0, 1.0), 'poop': (0.4980392156862745, 0.3686274509803922, 0.0, 1.0), 'dark peach': (0.8705882352941177, 0.49411764705882355, 0.36470588235294116, 1.0), 'jungle green': (0.01568627450980392, 0.5098039215686274, 0.2627450980392157, 1.0), 'eggshell': (1.0, 1.0, 0.8313725490196079, 1.0), 'denim': (0.23137254901960785, 0.38823529411764707, 0.5490196078431373, 1.0), 'yellow brown': (0.7176470588235294, 0.5803921568627451, 0.0, 1.0), 'dull purple': (0.5176470588235295, 0.34901960784313724, 0.49411764705882355, 1.0), 'chocolate brown': (0.2549019607843137, 0.09803921568627451, 0.0, 1.0), 'wine red': (0.4823529411764706, 0.011764705882352941, 0.13725490196078433, 1.0), 'neon blue': (0.01568627450980392, 0.8509803921568627, 1.0, 1.0), 'dirty green': (0.4, 0.49411764705882355, 0.17254901960784313, 1.0), 'light tan': (0.984313725490196, 0.9333333333333333, 0.6745098039215687, 1.0), 'ice blue': (0.8431372549019608, 1.0, 0.996078431372549, 1.0), 'cadet blue': (0.3058823529411765, 0.4549019607843137, 0.5882352941176471, 1.0), 'dark mauve': (0.5294117647058824, 0.2980392156862745, 0.3843137254901961, 1.0), 'very light blue': (0.8352941176470589, 1.0, 1.0, 1.0), 'grey purple': (0.5098039215686274, 0.42745098039215684, 0.5490196078431373, 1.0), 'pastel pink': (1.0, 0.7294117647058823, 0.803921568627451, 1.0), 'very light green': (0.8196078431372549, 1.0, 0.7411764705882353, 1.0), 'dark sky blue': (0.26666666666666666, 0.5568627450980392, 0.8941176470588236, 1.0), 'evergreen': (0.0196078431372549, 0.2784313725490196, 0.16470588235294117, 1.0), 'dull pink': (0.8352941176470589, 0.5254901960784314, 0.615686274509804, 1.0), 'aubergine': (0.23921568627450981, 0.027450980392156862, 0.20392156862745098, 1.0), 'mahogany': (0.2901960784313726, 0.00392156862745098, 0.0, 1.0), 'reddish orange': (0.9725490196078431, 0.2823529411764706, 0.10980392156862745, 1.0), 'deep green': (0.00784313725490196, 0.34901960784313724, 0.058823529411764705, 1.0), 'vomit green': (0.5372549019607843, 0.6352941176470588, 0.011764705882352941, 1.0), 'purple pink': (0.8784313725490196, 0.24705882352941178, 0.8470588235294118, 1.0), 'dusty pink': (0.8352941176470589, 0.5411764705882353, 0.5803921568627451, 1.0), 'faded green': (0.4823529411764706, 0.6980392156862745, 0.4549019607843137, 1.0), 'camo green': (0.3215686274509804, 0.396078431372549, 0.1450980392156863, 1.0), 'pinky purple': (0.788235294117647, 0.2980392156862745, 0.7450980392156863, 1.0), 'pink purple': (0.8588235294117647, 0.29411764705882354, 0.8549019607843137, 1.0), 'brownish red': (0.6196078431372549, 0.21176470588235294, 0.13725490196078433, 1.0), 'dark rose': (0.7098039215686275, 0.2823529411764706, 0.36470588235294116, 1.0), 'mud': (0.45098039215686275, 0.3607843137254902, 0.07058823529411765, 1.0), 'brownish': (0.611764705882353, 0.42745098039215684, 0.3411764705882353, 1.0), 'emerald green': (0.00784313725490196, 0.5607843137254902, 0.11764705882352941, 1.0), 'pale brown': (0.6941176470588235, 0.5686274509803921, 0.43137254901960786, 1.0), 'dull blue': (0.28627450980392155, 0.4588235294117647, 0.611764705882353, 1.0), 'burnt umber': (0.6274509803921569, 0.27058823529411763, 0.054901960784313725, 1.0), 'medium green': (0.2235294117647059, 0.6784313725490196, 0.2823529411764706, 1.0), 'clay': (0.7137254901960784, 0.41568627450980394, 0.3137254901960784, 1.0), 'light aqua': (0.5490196078431373, 1.0, 0.8588235294117647, 1.0), 'light olive green': (0.6431372549019608, 0.7450980392156863, 0.3607843137254902, 1.0), 'brownish orange': (0.796078431372549, 0.4666666666666667, 0.13725490196078433, 1.0), 'dark aqua': (0.0196078431372549, 0.4117647058823529, 0.4196078431372549, 1.0), 'purplish pink': (0.807843137254902, 0.36470588235294116, 0.6823529411764706, 1.0), 'dark salmon': (0.7843137254901961, 0.35294117647058826, 0.3254901960784314, 1.0), 'greenish grey': (0.5882352941176471, 0.6823529411764706, 0.5529411764705883, 1.0), 'jade': (0.12156862745098039, 0.6549019607843137, 0.4549019607843137, 1.0), 'ugly green': (0.47843137254901963, 0.592156862745098, 0.011764705882352941, 1.0), 'dark beige': (0.6745098039215687, 0.5764705882352941, 0.3843137254901961, 1.0), 'emerald': (0.00392156862745098, 0.6274509803921569, 0.28627450980392155, 1.0), 'pale red': (0.8509803921568627, 0.32941176470588235, 0.30196078431372547, 1.0), 'light magenta': (0.9803921568627451, 0.37254901960784315, 0.9686274509803922, 1.0), 'sky': (0.5098039215686274, 0.792156862745098, 0.9882352941176471, 1.0), 'light cyan': (0.6745098039215687, 1.0, 0.9882352941176471, 1.0), 'yellow orange': (0.9882352941176471, 0.6901960784313725, 0.00392156862745098, 1.0), 'reddish purple': (0.5686274509803921, 0.03529411764705882, 0.3176470588235294, 1.0), 'reddish pink': (0.996078431372549, 0.17254901960784313, 0.32941176470588235, 1.0), 'orchid': (0.7843137254901961, 0.4588235294117647, 0.7686274509803922, 1.0), 'dirty yellow': (0.803921568627451, 0.7725490196078432, 0.0392156862745098, 1.0), 'orange red': (0.9921568627450981, 0.2549019607843137, 0.11764705882352941, 1.0), 'deep red': (0.6039215686274509, 0.00784313725490196, 0.0, 1.0), 'orange brown': (0.7450980392156863, 0.39215686274509803, 0.0, 1.0), 'cobalt blue': (0.011764705882352941, 0.0392156862745098, 0.6549019607843137, 1.0), 'neon pink': (0.996078431372549, 0.00392156862745098, 0.6039215686274509, 1.0), 'rose pink': (0.9686274509803922, 0.5294117647058824, 0.6039215686274509, 1.0), 'greyish purple': (0.5333333333333333, 0.44313725490196076, 0.5686274509803921, 1.0), 'raspberry': (0.6901960784313725, 0.00392156862745098, 0.28627450980392155, 1.0), 'aqua green': (0.07058823529411765, 0.8823529411764706, 0.5764705882352941, 1.0), 'salmon pink': (0.996078431372549, 0.4823529411764706, 0.48627450980392156, 1.0), 'tangerine': (1.0, 0.5803921568627451, 0.03137254901960784, 1.0), 'brownish green': (0.41568627450980394, 0.43137254901960786, 0.03529411764705882, 1.0), 'red brown': (0.5450980392156862, 0.1803921568627451, 0.08627450980392157, 1.0), 'greenish brown': (0.4117647058823529, 0.3803921568627451, 0.07058823529411765, 1.0), 'pumpkin': (0.8823529411764706, 0.4666666666666667, 0.00392156862745098, 1.0), 'pine green': (0.0392156862745098, 0.2823529411764706, 0.11764705882352941, 1.0), 'charcoal': (0.20392156862745098, 0.2196078431372549, 0.21568627450980393, 1.0), 'baby pink': (1.0, 0.7176470588235294, 0.807843137254902, 1.0), 'cornflower': (0.41568627450980394, 0.4745098039215686, 0.9686274509803922, 1.0), 'blue violet': (0.36470588235294116, 0.023529411764705882, 0.9137254901960784, 1.0), 'chocolate': (0.23921568627450981, 0.10980392156862745, 0.00784313725490196, 1.0), 'greyish green': (0.5098039215686274, 0.6509803921568628, 0.49019607843137253, 1.0), 'scarlet': (0.7450980392156863, 0.00392156862745098, 0.09803921568627451, 1.0), 'green yellow': (0.788235294117647, 1.0, 0.15294117647058825, 1.0), 'dark olive': (0.21568627450980393, 0.24313725490196078, 0.00784313725490196, 1.0), 'sienna': (0.6627450980392157, 0.33725490196078434, 0.11764705882352941, 1.0), 'pastel purple': (0.792156862745098, 0.6274509803921569, 1.0, 1.0), 'terracotta': (0.792156862745098, 0.4, 0.2549019607843137, 1.0), 'aqua blue': (0.00784313725490196, 0.8470588235294118, 0.9137254901960784, 1.0), 'sage green': (0.5333333333333333, 0.7019607843137254, 0.47058823529411764, 1.0), 'blood red': (0.596078431372549, 0.0, 0.00784313725490196, 1.0), 'deep pink': (0.796078431372549, 0.00392156862745098, 0.3843137254901961, 1.0), 'grass': (0.3607843137254902, 0.6745098039215687, 0.17647058823529413, 1.0), 'moss': (0.4627450980392157, 0.6, 0.34509803921568627, 1.0), 'pastel blue': (0.6352941176470588, 0.7490196078431373, 0.996078431372549, 1.0), 'bluish green': (0.06274509803921569, 0.6509803921568628, 0.4549019607843137, 1.0), 'green blue': (0.023529411764705882, 0.7058823529411765, 0.5450980392156862, 1.0), 'dark tan': (0.6862745098039216, 0.5333333333333333, 0.2901960784313726, 1.0), 'greenish blue': (0.043137254901960784, 0.5450980392156862, 0.5294117647058824, 1.0), 'pale orange': (1.0, 0.6549019607843137, 0.33725490196078434, 1.0), 'vomit': (0.6352941176470588, 0.6431372549019608, 0.08235294117647059, 1.0), 'forrest green': (0.08235294117647059, 0.26666666666666666, 0.023529411764705882, 1.0), 'dark lavender': (0.5215686274509804, 0.403921568627451, 0.596078431372549, 1.0), 'dark violet': (0.20392156862745098, 0.00392156862745098, 0.24705882352941178, 1.0), 'purple blue': (0.38823529411764707, 0.17647058823529413, 0.9137254901960784, 1.0), 'dark cyan': (0.0392156862745098, 0.5333333333333333, 0.5411764705882353, 1.0), 
        'olive drab': (0.43529411764705883, 0.4627450980392157, 0.19607843137254902, 1.0), 'pinkish': (0.8313725490196079, 0.41568627450980394, 0.49411764705882355, 1.0), 'cobalt': (0.11764705882352941, 0.2823529411764706, 0.5607843137254902, 1.0), 'neon purple': (0.7372549019607844, 0.07450980392156863, 0.996078431372549, 1.0), 'light turquoise': (0.49411764705882355, 0.9568627450980393, 0.8, 1.0), 'apple green': (0.4627450980392157, 0.803921568627451, 0.14901960784313725, 1.0), 'dull green': (0.4549019607843137, 0.6509803921568628, 0.3843137254901961, 1.0), 'wine': (0.5019607843137255, 0.00392156862745098, 0.24705882352941178, 1.0), 'powder blue': (0.6941176470588235, 0.8196078431372549, 0.9882352941176471, 1.0), 'off white': (1.0, 1.0, 0.8941176470588236, 1.0), 'electric blue': (0.023529411764705882, 0.3215686274509804, 1.0, 1.0), 'dark turquoise': (0.01568627450980392, 0.3607843137254902, 0.35294117647058826, 1.0), 'blue purple': (0.3411764705882353, 0.1607843137254902, 0.807843137254902, 1.0), 'azure': (0.023529411764705882, 0.6039215686274509, 0.9529411764705882, 1.0), 'bright red': (1.0, 0.0, 0.050980392156862744, 1.0), 'pinkish red': (0.9450980392156862, 0.047058823529411764, 0.27058823529411763, 1.0), 'cornflower blue': (0.3176470588235294, 0.4392156862745098, 0.8431372549019608, 1.0), 'light olive': (0.6745098039215687, 0.7490196078431373, 0.4117647058823529, 1.0), 'grape': (0.4235294117647059, 0.20392156862745098, 0.3803921568627451, 1.0), 'greyish blue': (0.3686274509803922, 0.5058823529411764, 0.615686274509804, 1.0), 'purplish blue': (0.3764705882352941, 0.11764705882352941, 0.9764705882352941, 1.0), 'yellowish green': (0.6901960784313725, 0.8666666666666667, 0.08627450980392157, 1.0), 'greenish yellow': (0.803921568627451, 0.9921568627450981, 0.00784313725490196, 1.0), 'medium blue': (0.17254901960784313, 0.43529411764705883, 0.7333333333333333, 1.0), 'dusty rose': (0.7529411764705882, 0.45098039215686275, 0.47843137254901963, 1.0), 'light violet': (0.8392156862745098, 0.7058823529411765, 0.9882352941176471, 1.0), 'midnight blue': (0.00784313725490196, 0.0, 0.20784313725490197, 1.0), 'bluish purple': (0.4392156862745098, 0.23137254901960785, 0.9058823529411765, 1.0), 'red orange': (0.9921568627450981, 0.23529411764705882, 0.023529411764705882, 1.0), 'dark magenta': (0.5882352941176471, 0.0, 0.33725490196078434, 1.0), 'greenish': (0.25098039215686274, 0.6392156862745098, 0.40784313725490196, 1.0), 'ocean blue': (0.011764705882352941, 0.44313725490196076, 0.611764705882353, 1.0), 'coral': (0.9882352941176471, 0.35294117647058826, 0.3137254901960784, 1.0), 'cream': (1.0, 1.0, 0.7607843137254902, 1.0), 'reddish brown': (0.4980392156862745, 0.16862745098039217, 0.0392156862745098, 1.0), 'burnt sienna': (0.6901960784313725, 0.3058823529411765, 0.058823529411764705, 1.0), 'brick': (0.6274509803921569, 0.21176470588235294, 0.13725490196078433, 1.0), 'sage': (0.5294117647058824, 0.6823529411764706, 0.45098039215686275, 1.0), 'grey green': (0.47058823529411764, 0.6078431372549019, 0.45098039215686275, 1.0), 'white': (1.0, 1.0, 1.0, 1.0), "robin's egg blue": (0.596078431372549, 0.9372549019607843, 0.9764705882352941, 1.0), 'moss green': (0.396078431372549, 0.5450980392156862, 0.2196078431372549, 1.0), 'steel blue': (0.35294117647058826, 0.49019607843137253, 0.6039215686274509, 1.0), 'eggplant': (0.2196078431372549, 0.03137254901960784, 0.20784313725490197, 1.0), 'light yellow': (1.0, 0.996078431372549, 0.47843137254901963, 1.0), 'leaf green': (0.3607843137254902, 0.6627450980392157, 0.01568627450980392, 1.0), 'light grey': (0.8470588235294118, 0.8627450980392157, 0.8392156862745098, 1.0), 'puke': (0.6470588235294118, 0.6470588235294118, 0.00784313725490196, 1.0), 'pinkish purple': (0.8392156862745098, 0.2823529411764706, 0.8431372549019608, 1.0), 'sea blue': (0.01568627450980392, 0.4549019607843137, 0.5843137254901961, 1.0), 'pale purple': (0.7176470588235294, 0.5647058823529412, 0.8313725490196079, 1.0), 'slate blue': (0.3568627450980392, 0.48627450980392156, 0.6, 1.0), 'blue grey': (0.3764705882352941, 0.48627450980392156, 0.5568627450980392, 1.0), 'hunter green': (0.043137254901960784, 0.25098039215686274, 0.03137254901960784, 1.0), 'fuchsia': (0.9294117647058824, 0.050980392156862744, 0.8509803921568627, 1.0), 'crimson': (0.5490196078431373, 0.0, 0.058823529411764705, 1.0), 'pale yellow': (1.0, 1.0, 0.5176470588235295, 1.0), 'ochre': (0.7490196078431373, 0.5647058823529412, 0.0196078431372549, 1.0), 'mustard yellow': (0.8235294117647058, 0.7411764705882353, 0.0392156862745098, 1.0), 'light red': (1.0, 0.2784313725490196, 0.2980392156862745, 1.0), 'cerulean': (0.01568627450980392, 0.5215686274509804, 0.8196078431372549, 1.0), 'pale pink': (1.0, 0.8117647058823529, 0.8627450980392157, 1.0), 'deep blue': (0.01568627450980392, 0.00784313725490196, 0.45098039215686275, 1.0), 'rust': (0.6588235294117647, 0.23529411764705882, 0.03529411764705882, 1.0), 'light teal': (0.5647058823529412, 0.8941176470588236, 0.7568627450980392, 1.0), 'slate': (0.3176470588235294, 0.396078431372549, 0.4470588235294118, 1.0), 'goldenrod': (0.9803921568627451, 0.7607843137254902, 0.0196078431372549, 1.0), 'dark yellow': (0.8352941176470589, 0.7137254901960784, 0.0392156862745098, 1.0), 'dark grey': (0.21176470588235294, 0.21568627450980393, 0.21568627450980393, 1.0), 'army green': (0.29411764705882354, 0.36470588235294116, 0.08627450980392157, 1.0), 'grey blue': (0.4196078431372549, 0.5450980392156862, 0.6431372549019608, 1.0), 'seafoam': (0.5019607843137255, 0.9764705882352941, 0.6784313725490196, 1.0), 'puce': (0.6470588235294118, 0.49411764705882355, 0.3215686274509804, 1.0), 'spring green': (0.6627450980392157, 0.9764705882352941, 0.44313725490196076, 1.0), 'dark orange': (0.7764705882352941, 0.3176470588235294, 0.00784313725490196, 1.0), 'sand': (0.8862745098039215, 0.792156862745098, 0.4627450980392157, 1.0), 'pastel green': (0.6901960784313725, 1.0, 0.615686274509804, 1.0), 'mint': (0.6235294117647059, 0.996078431372549, 0.6901960784313725, 1.0), 'light orange': (0.9921568627450981, 0.6666666666666666, 0.2823529411764706, 1.0), 'bright pink': (0.996078431372549, 0.00392156862745098, 0.6941176470588235, 1.0), 'chartreuse': (0.7568627450980392, 0.9725490196078431, 0.0392156862745098, 1.0), 'deep purple': (0.21176470588235294, 0.00392156862745098, 0.24705882352941178, 1.0), 'dark brown': (0.20392156862745098, 0.10980392156862745, 0.00784313725490196, 1.0), 'taupe': (0.7254901960784313, 0.6352941176470588, 0.5058823529411764, 1.0), 'pea green': (0.5568627450980392, 0.6705882352941176, 0.07058823529411765, 1.0), 'puke green': (0.6039215686274509, 0.6823529411764706, 0.027450980392156862, 1.0), 'kelly green': (0.00784313725490196, 0.6705882352941176, 0.1803921568627451, 1.0), 'seafoam green': (0.47843137254901963, 0.9764705882352941, 0.6705882352941176, 1.0), 'blue green': (0.07450980392156863, 0.49411764705882355, 0.42745098039215684, 1.0), 'khaki': (0.6666666666666666, 0.6509803921568628, 0.3843137254901961, 1.0), 'burgundy': (0.3803921568627451, 0.0, 0.13725490196078433, 1.0), 'dark teal': (0.00392156862745098, 0.30196078431372547, 0.3058823529411765, 1.0), 'brick red': (0.5607843137254902, 0.0784313725490196, 0.00784313725490196, 1.0), 'royal purple': (0.29411764705882354, 0.0, 0.43137254901960786, 1.0), 'plum': (0.34509803921568627, 0.058823529411764705, 0.2549019607843137, 1.0), 'mint green': (0.5607843137254902, 1.0, 0.6235294117647059, 1.0), 'gold': (0.8588235294117647, 0.7058823529411765, 0.047058823529411764, 1.0), 'baby blue': (0.6352941176470588, 0.8117647058823529, 0.996078431372549, 1.0), 'yellow green': (0.7529411764705882, 0.984313725490196, 0.17647058823529413, 1.0), 'bright purple': (0.7450980392156863, 0.011764705882352941, 0.9921568627450981, 1.0), 'dark red': (0.5176470588235295, 0.0, 0.0, 1.0), 'pale blue': (0.8156862745098039, 0.996078431372549, 0.996078431372549, 1.0), 'grass green': (0.24705882352941178, 0.6078431372549019, 0.043137254901960784, 1.0), 'navy': (0.00392156862745098, 0.08235294117647059, 0.24313725490196078, 1.0), 'aquamarine': (0.01568627450980392, 0.8470588235294118, 0.6980392156862745, 1.0), 'burnt orange': (0.7529411764705882, 0.3058823529411765, 0.00392156862745098, 1.0), 'neon green': (0.047058823529411764, 1.0, 0.047058823529411764, 1.0), 'bright blue': (0.00392156862745098, 0.396078431372549, 0.9882352941176471, 1.0), 'rose': (0.8117647058823529, 0.3843137254901961, 0.4588235294117647, 1.0), 'light pink': (1.0, 0.8196078431372549, 0.8745098039215686, 1.0), 'mustard': (0.807843137254902, 0.7019607843137254, 0.00392156862745098, 1.0), 'indigo': (0.2196078431372549, 0.00784313725490196, 0.5098039215686274, 1.0), 'lime': (0.6666666666666666, 1.0, 0.19607843137254902, 1.0), 'sea green': (0.3254901960784314, 0.9882352941176471, 0.6313725490196078, 1.0), 'periwinkle': (0.5568627450980392, 0.5098039215686274, 0.996078431372549, 1.0), 'dark pink': (0.796078431372549, 0.2549019607843137, 0.4196078431372549, 1.0), 'olive green': (0.403921568627451, 0.47843137254901963, 0.01568627450980392, 1.0), 'peach': (1.0, 0.6901960784313725, 0.48627450980392156, 1.0), 'pale green': (0.7803921568627451, 0.9921568627450981, 0.7098039215686275, 1.0), 'light brown': (0.6784313725490196, 0.5058823529411764, 0.3137254901960784, 1.0), 'hot pink': (1.0, 0.00784313725490196, 0.5529411764705883, 1.0), 'black': (0.0, 0.0, 0.0, 1.0), 'lilac': (0.807843137254902, 0.6352941176470588, 0.9921568627450981, 1.0), 'navy blue': (0.0, 0.06666666666666667, 0.27450980392156865, 1.0), 'royal blue': (0.0196078431372549, 0.01568627450980392, 0.6666666666666666, 1.0), 'beige': (0.9019607843137255, 0.8549019607843137, 0.6509803921568628, 1.0), 'salmon': (1.0, 0.4745098039215686, 0.4235294117647059, 1.0), 'olive': (0.43137254901960786, 0.4588235294117647, 0.054901960784313725, 1.0), 'maroon': (0.396078431372549, 0.0, 0.12941176470588237, 1.0), 'bright green': (0.00392156862745098, 1.0, 0.027450980392156862, 1.0), 'dark purple': (0.20784313725490197, 0.023529411764705882, 0.24313725490196078, 1.0), 'mauve': (0.6823529411764706, 0.44313725490196076, 0.5058823529411764, 1.0), 'forest green': (0.023529411764705882, 0.2784313725490196, 0.047058823529411764, 1.0), 'aqua': (0.07450980392156863, 0.9176470588235294, 0.788235294117647, 1.0), 'cyan': (0.0, 1.0, 1.0, 1.0), 'tan': (0.8196078431372549, 0.6980392156862745, 0.43529411764705883, 1.0), 
        'dark blue': (0.0, 0.011764705882352941, 0.3568627450980392, 1.0), 'lavender': (0.7803921568627451, 0.6235294117647059, 0.9372549019607843, 1.0), 'turquoise': (0.023529411764705882, 0.7607843137254902, 0.6745098039215687, 1.0), 'dark green': (0.011764705882352941, 0.20784313725490197, 0.0, 1.0), 'violet': (0.6039215686274509, 0.054901960784313725, 0.9176470588235294, 1.0), 'light purple': (0.7490196078431373, 0.4666666666666667, 0.9647058823529412, 1.0), 'lime green': (0.5372549019607843, 0.996078431372549, 0.0196078431372549, 1.0), 'grey': (0.5725490196078431, 0.5843137254901961, 0.5686274509803921, 1.0), 'sky blue': (0.4588235294117647, 0.7333333333333333, 0.9921568627450981, 1.0), 'yellow': (1.0, 1.0, 0.0784313725490196, 1.0), 'magenta': (0.7607843137254902, 0.0, 0.47058823529411764, 1.0), 'light green': (0.5882352941176471, 0.9764705882352941, 0.4823529411764706, 1.0), 'orange': (0.9764705882352941, 0.45098039215686275, 0.023529411764705882, 1.0), 'teal': (0.00784313725490196, 0.5764705882352941, 0.5254901960784314, 1.0), 'light blue': (0.5843137254901961, 0.8156862745098039, 0.9882352941176471, 1.0), 'red': (0.8980392156862745, 0.0, 0.0, 1.0), 'brown': (0.396078431372549, 0.21568627450980393, 0.0, 1.0), 'pink': (1.0, 0.5058823529411764, 0.7529411764705882, 1.0), 'blue': (0.011764705882352941, 0.2627450980392157, 0.8745098039215686, 1.0), 'green': (0.08235294117647059, 0.6901960784313725, 0.10196078431372549, 1.0), 'purple': (0.49411764705882355, 0.11764705882352941, 0.611764705882353, 1.0), 'gray teal': (0.3686274509803922, 0.6078431372549019, 0.5411764705882353, 1.0), 'purpley gray': (0.5803921568627451, 0.49411764705882355, 0.5803921568627451, 1.0), 'light gray green': (0.7176470588235294, 0.8823529411764706, 0.6313725490196078, 1.0), 'reddish gray': (0.6, 0.4588235294117647, 0.4392156862745098, 1.0), 'battleship gray': (0.4196078431372549, 0.48627450980392156, 0.5215686274509804, 1.0), 'charcoal gray': (0.23529411764705882, 0.2549019607843137, 0.25882352941176473, 1.0), 'grayish teal': (0.44313725490196076, 0.6235294117647059, 0.5686274509803921, 1.0), 'gray/green': (0.5254901960784314, 0.6313725490196078, 0.49019607843137253, 1.0), 'cool gray': (0.5843137254901961, 0.6392156862745098, 0.6509803921568628, 1.0), 'dark blue gray': (0.12156862745098039, 0.23137254901960785, 0.30196078431372547, 1.0), 'bluey gray': (0.5372549019607843, 0.6274509803921569, 0.6901960784313725, 1.0), 'greeny gray': (0.49411764705882355, 0.6274509803921569, 0.47843137254901963, 1.0), 'bluegray': (0.5215686274509804, 0.6392156862745098, 0.6980392156862745, 1.0), 'light blue gray': (0.7176470588235294, 0.788235294117647, 0.8862745098039215, 1.0), 'gray/blue': (0.39215686274509803, 0.49019607843137253, 0.5568627450980392, 1.0), 'brown gray': (0.5529411764705883, 0.5176470588235295, 0.40784313725490196, 1.0), 'blue/gray': (0.4588235294117647, 0.5529411764705883, 0.6392156862745098, 1.0), 'grayblue': (0.4666666666666667, 0.6313725490196078, 0.7098039215686275, 1.0), 'dark gray blue': (0.1607843137254902, 0.27450980392156865, 0.3568627450980392, 1.0), 'grayish': (0.6588235294117647, 0.6431372549019608, 0.5843137254901961, 1.0), 'light gray blue': (0.615686274509804, 0.7372549019607844, 0.8313725490196079, 1.0), 'pale gray': (0.9921568627450981, 0.9921568627450981, 0.996078431372549, 1.0), 'warm gray': (0.592156862745098, 0.5411764705882353, 0.5176470588235295, 1.0), 'gray pink': (0.7647058823529411, 0.5647058823529412, 0.6078431372549019, 1.0), 'medium gray': (0.49019607843137253, 0.4980392156862745, 0.48627450980392156, 1.0), 'pinkish gray': (0.7843137254901961, 0.6745098039215687, 0.6627450980392157, 1.0), 'brownish gray': (0.5254901960784314, 0.4666666666666667, 0.37254901960784315, 1.0), 'purplish gray': (0.47843137254901963, 0.40784313725490196, 0.4980392156862745, 1.0), 'grayish pink': (0.7843137254901961, 0.5529411764705883, 0.5803921568627451, 1.0), 'grayish brown': (0.47843137254901963, 0.41568627450980394, 0.30980392156862746, 1.0), 'steel gray': (0.43529411764705883, 0.5098039215686274, 0.5411764705882353, 1.0), 'purple gray': (0.5254901960784314, 0.43529411764705883, 0.5215686274509804, 1.0), 'gray brown': (0.4980392156862745, 0.4392156862745098, 0.3254901960784314, 1.0), 'green gray': (0.4666666666666667, 0.5725490196078431, 0.43529411764705883, 1.0), 'bluish gray': (0.4549019607843137, 0.5450980392156862, 0.592156862745098, 1.0), 'slate gray': (0.34901960784313724, 0.396078431372549, 0.42745098039215684, 1.0), 'gray purple': (0.5098039215686274, 0.42745098039215684, 0.5490196078431373, 1.0), 'greenish gray': (0.5882352941176471, 0.6823529411764706, 0.5529411764705883, 1.0), 'grayish purple': (0.5333333333333333, 0.44313725490196076, 0.5686274509803921, 1.0), 'grayish green': (0.5098039215686274, 0.6509803921568628, 0.49019607843137253, 1.0), 'grayish blue': (0.3686274509803922, 0.5058823529411764, 0.615686274509804, 1.0), 'gray green': (0.47058823529411764, 0.6078431372549019, 0.45098039215686275, 1.0), 'light gray': (0.8470588235294118, 0.8627450980392157, 0.8392156862745098, 1.0), 'blue gray': (0.3764705882352941, 0.48627450980392156, 0.5568627450980392, 1.0), 'dark gray': (0.21176470588235294, 0.21568627450980393, 0.21568627450980393, 1.0), 'gray blue': (0.4196078431372549, 0.5450980392156862, 0.6431372549019608, 1.0), 'gray': (0.5725490196078431, 0.5843137254901961, 0.5686274509803921, 1.0)}

    @property
    def tab(self):
        return self._tab
    @property
    def xkcd(self):
        return self._xkcd
    @property
    def x11(self):
        return self._colors
    @property
    def css4(self):
        return self._colors


    def __getitem__(self,name):
        if not ":" in name:
            try:
                return self._colors[name]
            except:
                return self._xkcd[name]
        elif "xkcd:" in name:
            return self._xkcd[name.split(':')[-1]]
        elif "tab:" in name:
            return self._tab[name.split(':')[-1]]
    
    def keys(self):
        ans=set(self._colors.keys())
        for k in self._tab.keys():
            ans.add('tab:'+k)
        for k in self._xkcd.keys():
            ans.add('xkcd:'+k)
        return ans
    def items(self):
        return ((cn,self.__getitem__(cn)) for cn in self.keys())
    def values(self):
        ans=set(self._colors.values())
        for k in self._tab.values():
            ans.add(k)
        for k in self._xkcd.values():
            ans.add(k)
        return ans

def darken_rgba(color, factor):
    """
    Darken an RGBA color by a specified factor.
    
    Args:
        color: A tuple or list of 4 floats (r, g, b, a) in range [0, 1]
        factor: A float between 0 and 1 where 0 is completely dark, 1 is no change
    
    Returns:
        A tuple of (r, g, b, a) representing the darkened color
    """
    if not (0 <= factor <= 1):
        raise ValueError("Factor must be between 0 and 1")
    
    r, g, b, a = color
    return (r * factor, g * factor, b * factor, a)  # Alpha channel remains unchanged

def brighten_rgba(color, factor):
    """
    Darken an RGBA color by a specified factor.
    
    Args:
        color: A tuple or list of 4 floats (r, g, b, a) in range [0, 1]
        factor: A float between 0 and 1 where 0 is completely dark, 1 is no change
    
    Returns:
        A tuple of (r, g, b, a) representing the darkened color
    """
    if not (0 <= factor <= 1):
        raise ValueError("Factor must be between 0 and 1")
    
    r, g, b, a = color
    return (ci if ci<=1 else 1 for ci in (r + factor, g + factor, b + factor, a))  # Alpha channel remains unchanged

colors=Colors=NamedColors()
Fonts = CaseInsensitiveDict({
    'DejaVu': 'DejaVuSans.ttf',
    'DejaVusans': 'DejaVuSans.ttf',
    'Roboto': 'Roboto-Regular.ttf',
    'Roboto it': 'Roboto-Italic.ttf',
    'Roboto b': 'Roboto-Bold.ttf',
    'Roboto itb': 'Roboto-BoldItalic.ttf',
    'Roboto bit': 'Roboto-BoldItalic.ttf',
    'Mono': 'RobotoMono-Regular.ttf',
    'Segoe UI': 'segoeui.ttf',
    'Segoe Symbol': 'seguisym.ttf',
    'Segoe UI Symbol': 'seguisym.ttf',
    'Segoe': 'segoeui.ttf',
    'Lucida Sans': 'lsans.ttf',
    'Lucida Sans it': 'lsansi.ttf',
    'Lucida Sans itb': 'LSANSDI.TTF',
    'Lucida Sans bit': 'LSANSDI.TTF',
    'Lucida Sans b': 'LSANSD.TTF',
})

def _resolve_color(c):
    if type(c) is str:
        if '#' in c:
            c = hex2rgb(c, alpha=255, vmax=1)
        else:
            c = Colors[c]

    return c

def resolve_color(v):
    if isinstance(v,str):
        if not '#' in v:
            try:
                v=Colors[v]
            except:
                raise ValueError(f"Invalid color string \"{v}\".\nValid colors are:{Colors.keys()}")
        else:
            try:
                v=hex2rgb(v, alpha=255, vmax=1)
            except:
                raise ValueError(f"Invalid color string \"{v}\"")
    elif isinstance(v,dict):
        for k,val in v.items():
            v[k]=rgba2hex(resolve_color(val))
    return v

def resolve_relative_pos_hint(
    widget_relative,to_this_widget,hint='same',
    keep_inside_window=True
    ):
    # from kvWidgets import get_kvWindow
    kvWindow = __getattr__('Window')
    location=list(to_this_widget.to_window(*to_this_widget.pos))
    if hint=='same':
        location[0]+=to_this_widget.width/2
        location[1]+=to_this_widget.height/2
    elif hint=='bellow':
        location[0]+=to_this_widget.width/2
        location[1]+=-widget_relative.height/2
    elif hint=='above':
        location[0]+=to_this_widget.width/2
        location[1]+=to_this_widget.height+widget_relative.height/2    
    elif hint=='right':
        location[0]+=to_this_widget.width+widget_relative.width/2
        location[1]+=to_this_widget.height/2
    elif hint=='left':
        location[0]+=-widget_relative.width/2
        location[1]+=to_this_widget.height/2

    if keep_inside_window:
        outside_left=location[0]-widget_relative.width/2
        outside_right=location[0]+widget_relative.width/2-kvWindow.width
        outside_top=location[1]+widget_relative.height/2-kvWindow.height
        outside_btm=location[1]-widget_relative.height/2
        if outside_left<0:
            location[0]+=-outside_left
        if outside_right>0:
            location[0]+=-outside_right
        if outside_top>0:
            location[1]+=-outside_top
        if outside_btm<0:
            location[1]+=-outside_btm

    # print(location,outside_btm)
    
    pos_hint={'center_x': 0.5, 'center_y': 0.5}
        # location=_resolve_size(location)
    if not location[1] is None:
        # pos_hint['y']=location[1] /  self.kvWindow.height
        pos_hint['center_y'] = location[1] / kvWindow.height
    if not location[0] is None:
        # pos_hint['x']=location[0] /  self.kvWindow.width
        pos_hint['center_x'] = location[0] / kvWindow.width
    return pos_hint

def _resolve_font_name(f):
    try:
        f = Fonts[f]
    except:
        pass
    return f


def hex2rgb(hex, alpha=None, vmax=255):
    hex = hex.lstrip('#')
    rgb = list(int(hex[i:i + 2], 16) for i in (0, 2, 4))
    if not alpha is None:
        rgb.append(alpha)

    if vmax != 255:
        rgb = [c / (255 / vmax) for c in rgb]

    return tuple(rgb)


def rgb2rgba_max(rgb, alpha=255, vmax=1):
    rgb = list(rgb[:3])
    if not alpha is None:
        rgb.append(alpha)

    if vmax != 255:
        rgb = [c / (255 / vmax) for c in rgb]
    return tuple(rgb)


def rgb2hex(rgb):
    if type(rgb) == tuple or type(rgb) == list and False not in[0 <= c <= 255 for c in rgb]:
        if len(rgb) == 3:
            hex_ = '#%02x%02x%02x' % tuple([int(i) for i in rgb])
        elif len(rgb) > 3:
            hex_ = '#%02x%02x%02x' % tuple([int(i) for i in rgb[0:3]])
        elif len(rgb) == 2:
            hex_ = '#%02x%02x00' % tuple([int(i) for i in rgb[0:2]])
        elif len(rgb) == 1:
            hex_ = '#%02x0000' % tuple(int(rgb))
    elif type(rgb) == int and 0 <= rgb <= 255:
        hex_ = '#%02x%02x%02x' % (rgb, rgb, rgb)
    else:
        hex_ = '#000000'
    return hex_
def rgba2hex(rgba):
    return rgb2hex(rgba[:-1])


def hex2str(s):
    val = int(s, 16)
    return chr(val)

def markup_href(url,text=None,color='1B95E0'):
    if text==None:
        text=url
    color=color.lstrip('#')
        
    return f"[color={color}][ref={url}][u]{text}[/u][/ref][/color]"


def markup_str(s, font='', size=None, color='', list_tags=[], dic_tags={}, is_hex=False):
    if is_hex:
        # s=s[1:] if '#'==s[0]  else s
        s = hex2str(s.strip('#'))
    if font:
        font = _resolve_font_name(font)
        s = '[font=' + font + ']' + s + '[/font]'
    if size:
        s = '[size=' + str(size) + ']' + s + '[/size]'
# bold=False,italic=False,underlined=False,strike=False,subscript=False,superscript=False,
    # if bold:
    #     s='[b]'+s+'[/b]'
    # if italic:
    #     s='[i]'+s+'[/i]'
    # if underlined:
    #     s='[u]'+s+'[/u]'
    # if strike:
    #     s='[s]'+s+'[/s]'
    if color:
        if not type(color) is str:
            if any(i > 1 for i in color):
                color = rgb2hex(color)
            else:
                color = rgb2hex([int(c * 255 + .5) for c in color])
        elif '#' not in color:
            color = rgb2hex([int(c * 255 + .5) for c in Colors[color]])
        s = '[color=' + color + ']' + s + '[/color]'

    for l in list_tags:
        s = '[' + l + ']' + s + '[/' + l + ']'
    for k in dic_tags:
        s = '[' + k + '=' + dic_tags[k] + ']' + s + '[/' + k + ']'

    return s
class IconFont:

    def __init__(self, ttf_families={},
                 # You only need one, but  you can use css and fontd
                 css_dir=None, fontd_dir=None, fontd=None,prepend='',default_font_size=None):
        self._initprops=ttf_families,css_dir,fontd_dir,fontd,prepend
        if type(ttf_families) is str:
            self.ttf_families = {'regular': ttf_families}
        elif type(ttf_families) in [list, tuple]:
            self.ttf_families = {}
            c = 0
            for f in ttf_families:
                self.ttf_families[0] = f
                c += 1
        else:
            self.ttf_families = ttf_families

        self.prepend=prepend
        self.default_font_size=default_font_size
        # self.ttf_dir=os.path.abspath(ttf_dir)
        self.ttf_dir = os.path.abspath(list(self.ttf_families.values())[0])
        self.css_dir = css_dir
        self.css = None

        if fontd:
            self.fontd = fontd
        elif fontd_dir:
            with open(fontd_dir, 'r', encoding='utf-8') as fid:
                fontd = eval(fid.read())
            self.fontd = fontd
        elif css_dir:
            with open(css_dir, 'r', encoding='utf-8') as fid:
                pass
                self.css = fid.read().replace('\r', '').replace('\n', ' ')
            self.fontd = {}
        else:
            self.fontd = {}

    # def __getitem__(self, key):
    #     # if not self.css:
    #     # if key in self.fontd:
    #     try:
    #         val=self.fontd[key]
    #         if type(val)==str:
    #             val=int(s.strip('#'), 16)
    #             self.fontd[key]=val
    #         # val=chr(val)
    #     # else:
    #     except:
    #         # print(self.css)
    #         val=self.css.split(key+':')[1].split('}')[0]
    #         for p in 'before { } : \" \' \\ ; content'.split():
    #             val=val.replace(p,'')

    #         val=int(val.strip(), 16)
    #         self.fontd[key]=val

        # return '[font='+self.ttf_dir+']'+chr(val)+'[/font]'
        # return markup_str(chr(val),font=self.ttf_dir)
    def __call__(self, key, size=None, color='', list_tags=[], dic_tags={}, font_size=None,
        # bold=False
        ):
        key=self.prepend+key
        if not size:
            size = font_size
        if not size:
            size=self.default_font_size

        if ' ' in key:
            family, key = key.split()
            try:
                ttf_dir = self.ttf_families[family]
            except:
                family=family.split('-')[-1]
                ttf_dir = self.ttf_families[family]
        else:
            ttf_dir = self.ttf_dir

        try:
            val = self.fontd[key]
            if type(val) == str:
                val = int(val.strip('#'), 16)
                self.fontd[key] = val
            # val=chr(val)
        # else:
        except KeyError:
            val = self.get_val_from_css(key)
            if val is None:
                # return key
                return markup_str(key, font=ttf_dir, size=size, color=color, list_tags=list_tags, dic_tags=dic_tags)
            # try:
            #     # print(self.css)
            #     val=self.css.split(key+':')[1].split('}')[0]
            #     for p in 'before { } : \" \' \\ ; content'.split():
            #         val=val.replace(p,'')

            #     val=int(val.strip(), 16)
            #     self.fontd[key]=val
            # except:
            #     print('KeyError: key \"',key,'\"',' could not be found',sep='')
            #     return key
        ans=markup_str(chr(val), font=ttf_dir, size=size, color=color, list_tags=list_tags, dic_tags=dic_tags)
        # if bold:
        #     ans='[b]'+ans+'[/b]'
        return ans

    def get_val_from_css(self, key):
        try:
            # print(self.css)
            val = self.css.split(key + ':')[1].split('}')[0]
            for p in 'before { } : \" \' \\ ; content'.split():
                val = val.replace(p, '')
            # print(val)
            val = int(val.strip(), 16)
            self.fontd[key] = val
            return val
        except:
            print('KeyError: key \"', key, '\"', ' could not be found in ' +
                  self.css_dir + ', key returned', sep='')
            return
    def copy(self):
        return IconFont(*self._initprops)
# icons_material=infinite()
mdi= IconFont({
    'regular': os.path.join(SK_PATH,'skdata/fonts/mdi/fonts/materialdesignicons-webfont.ttf')
    },
    css_dir=os.path.join(SK_PATH,'skdata/fonts/mdi/css/materialdesignicons.css')
    )
mdi.prepend=('mdi-')
# print('hell')


class FileCategory:

    def __init__(self, icon, extensions, size=20):
        self._exts = set()
        self._edef = {}
        self._resolved = {}
        self.size = size
        self.icon = icon
        for e in extensions:
            if isinstance(e, str):
                self._exts.add(e)
            else:
                self._edef[e[0]] = e[1:]
                self._exts.add(e[0])

    def __contains__(self, v):
        return v in self._exts

    def __getitem__(self, v):
        try:
            return self._edef[v]
        except:
            if v in self._exts:
                return self.icon
            else:
                raise ValueError

    def get(self, k):
        iargs = self.__getitem__(k)
        if iargs in self._resolved:
            return self._resolved[iargs]
        if isinstance(iargs, str):
            ic = mdi(iargs, size=self.size)
        else:
            ic = mdi(iargs[0], color=iargs[1], size=self.size)
        self._resolved[iargs] = ic
        return ic


class FileIconFinder:
    _resolved = {}

    def __init__(self, default_icon, size=None):
        if size == None:
            try:
                size = re.search(r"size[ ]*=[ ]*[\d]+", default_icon).group()
                # print(size)
                size = int(re.search(r"[\d]+", size).group())
            except:
                pass
        self.size = size
        self.default_icon = default_icon
        # Define your icon categories and subcategories here
        self.icon_categories = {
            "common_paths":FileCategory(
                icon=('folder','#FFD96C'),
                extensions=(
                    ('folder','folder','#FFD96C'),
                    ('user','account-box',"#0174CD"),
                    ('home','home-account',"#0174CD"),
                    ('root','harddisk','#E1E3E6'),
                    ('storage','harddisk','#E1E3E6'),
                    ('usb','usb-flash-drive','#E1E3E6'),
                    ('desktop','monitor-dashboard','#1A93CA'),
                    ('documents','file-document','#738FAC'),
                    ('downloads','download',"#1CB49A"),
                    ('pictures','image',"#148ED7"),
                    ('videos','filmstrip',(1.0, 0.3, 0.7)),
                    ('music','music-box',(0.5, 0.8, 1.0)),
                    ('books','bookshelf','#BC8447'),

                    )
                ),
            # Images
            "raster_images": FileCategory(
                extensions=(
                    # Standard formats (lossy)
                    ".jpg",
                    ".jpeg",
                    ".jpe",
                    ".jfif",
                    ".pjpeg",
                    ".pjp",
                    ".png",
                    # Standard formats (lossless)
                    ".bmp",
                    ".dib",
                    ".rle",
                    # Web formats
                    ".webp",
                    ".avif",
                    # Animation (single-layer)
                    ".gif",
                    ".apng",
                    # Camera formats
                    ".heic",
                    ".heif",
                    ".avci",
                    ".avcs",
                    # Raw formats (technically unprocessed but single-layer)
                    ".raw",
                    ".cr2",
                    ".cr3",
                    ".nef",
                    ".arw",
                    ".sr2",
                    ".dng",
                    ".raf",
                    ".orf",
                    ".rw2",
                    ".pef",
                    ".srf",
                    ".dcr",
                    ".kdc",
                    ".mos",
                    ".mrw",
                    ".nrw",
                    ".ptx",
                    ".x3f",
                    ".erf",
                    # HDR/other
                    ".hdr",
                    ".exr",
                    ".ppm",
                    ".pgm",
                    ".pbm",
                    ".pnm",
                    ".pfm",
                ),
                # icon=("image-outline",(0.95, 0.65, 0.25)),  # Simple image icon
                icon=("image-outline","#148ED7"),  # Simple image icon
            ),
            "layered_images": FileCategory(
                extensions=(
                    # Professional editors
                    ".psd",
                    ".psb",
                    ".psdt",  # Photoshop
                    ".xcf",  # GIMP
                    ".kra",  # Krita
                    ".ora",  # OpenRaster
                    ".clip",
                    ".lip",  # Clip Studio Paint
                    ".sai",  # PaintTool SAI
                    ".csp",  # Clip Studio (older)
                    ".afphoto",  # Affinity Photo
                    ".procreate",  # Procreate (iOS)
                    # TIFF/EXR (can be multilayer)
                    ".tif",
                    ".tiff",
                    ".exr",
                    # Other editors
                    ".pdn",  # Paint.NET
                    ".pix",  # PIXLR
                    ".pde",  # Pixelmator
                    ".webp",  # (Can have layers in some apps)
                ),
                # icon=("layers-triple",(0.85, 0.5, 0.95)),  # Stacked layers icon
                # icon=("image-edit",(0.85, 0.5, 0.95)),  # Stacked layers icon
                icon=("image-edit","#148ED7")
            ),
            "vector_images": FileCategory(
                extensions=(
                    # Standard vector formats
                    ".svg",
                    ".svgz",
                    # Adobe formats
                    ".ai",
                    ".ait",
                    ".eps",
                    # ".pdf",  # (PDF can be vector-based)
                    # Corel/CAD
                    ".cdr",
                    ".cmx",
                    ".afdesign",
                    ".fh",
                    ".fh7",
                    ".fh8",
                    ".fh9",
                    ".fh10",
                    ".fh11",
                    # Other editors
                    ".sketch",
                    ".fig",
                    ".xd",
                    ".epsf",
                    ".ps",
                    ".swf",
                    ".wmf",
                    ".emf",
                    # # 3D vector formats
                    # ".dxf",
                    # ".dwg",
                    # ".iges",
                    # ".step",
                ),
                icon=("vector-arrange-above",(0.3, 0.8, 1.0)),  # Vector/path icon
            ),
            # CAD (Expanded)
            "cad": FileCategory(
                extensions=(
                    ".dwg",
                    ".dxf",
                    ".stp",
                    ".step",
                    ".iges",
                    ".igs",
                    ".x_t",
                    ".x_b",
                    ".sldprt",
                    ".sldasm",
                    ".slddrw",
                    ".prt",
                    ".asm",
                    ".drw",
                    ".ipt",
                    ".iam",
                    ".idw",
                    ".f3d",
                    ".catpart",
                    ".catproduct",
                    ".cgr",
                    ".3dxml",
                    ".jt",
                    ".par",
                    ".psm",
                    ".model",
                    ".session",
                    ".dlv",
                    ".exp",
                    ".plmxml",
                    ".prt",
                    ".neu",
                    ".mf1",
                    ".scdoc",
                    ".skp",
                    ".3dm",
                    ".3ds",
                    ".blend",
                ),
                # icon="vector-square",
                icon=("cube-outline",(0.0, 0.75, 0.95)),
            ),
            # CAM & 3D Printing
            "cam": FileCategory(
                extensions=(
                    ".gcode",
                    ".nc",
                    ".tap",
                    ".cnc",
                    ".ncc",
                    ".dnc",
                    ".eia",
                    ".ptp",
                    ".3mf",
                    ".amf",
                    ".stl",
                    ".obj",
                    ".ply",
                    ".wrl",
                    ".x3d",
                    ".vrml",
                    ".sla",
                    ".slc",
                    ".cl",
                    ".ol",
                    ".rol",
                    ".inp",
                    ".mtt",
                    ".pcd",
                    ".vda",
                ),
                icon=("printer-3d",(0.0, 0.7, 0.8)),
            ),
            # CAE & Simulation
            "cae": FileCategory(
                extensions=(
                    ".inp",
                    ".dat",
                    ".odb",
                    ".sim",
                    ".fem",
                    ".cae",
                    ".ans",
                    ".cdb",
                    ".mud",
                    ".unv",
                    ".bdf",
                    ".nas",
                    ".pch",
                    ".rst",
                    ".rth",
                    ".rfl",
                    ".dyn",
                    ".key",
                    ".d3plot",
                    ".mod",
                    ".f06",
                    ".frd",
                    ".pch",
                    ".mnf",
                    ".op2",
                    ".op4",
                    ".wrl",
                    ".pvtu",
                    ".vtu",
                    ".msh",
                    ".cas",
                    ".cgns",
                ),
                icon=("chart-line",(0.4, 0.7, 1.0)),
            ),
            
            # PLM & PDM
            "plm": FileCategory(
                extensions=(
                    ".wgm",
                    ".wht",
                    ".whtx",
                    ".whtxx",
                    ".whtxxx",
                    ".whtxxxx",
                    ".whtxxxxx",
                    ".whtxxxxxx",
                    ".whtxxxxxxx",
                    ".whtxxxxxxxx",
                    ".whtxxxxxxxxx",
                    ".whtxxxxxxxxxx",
                ),
                icon=("database-cog",(0.2, 0.6, 0.8)),
            ),
            # Mesh & Point Cloud
            "mesh": FileCategory(
                extensions=(
                    ".ply",
                    ".pcd",
                    ".xyz",
                    ".pts",
                    ".ptx",
                    ".las",
                    ".laz",
                    ".e57",
                    ".obj",
                    ".fbx",
                    ".3ds",
                    ".dae",
                    ".off",
                    ".smf",
                    ".wrl",
                    ".x3d",
                    ".stl",
                    ".3mf",
                    ".amf",
                    ".vrml",
                    ".iv",
                    ".vtu",
                    ".msh",
                    ".mesh",
                    ".med",
                    ".bdf",
                    ".nas",
                    ".unv",
                    ".neu",
                    ".mf1",
                    ".scdoc",
                    ".3dm",
                ),
                icon=("grid",(0.6, 0.6, 1.0)),
            ),
            # Documents (General)
            "documents": FileCategory(
                extensions=(
                    ".doc",
                    ".docx",
                    ".odt",
                    ".rtf",
                    ".tex",
                    ".wpd",
                    ".pages",
                    ".fodt",
                    ".dot",
                    ".dotx",
                    ".docm",
                    ".dotm",
                    ".odm",
                    ".ott",
                    ".stw",
                    ".sxw",
                    ".uot",
                    ".vor",
                    ".wps",
                    ".wpt",
                    # ".xml",
                    ".wri",
                    ".kwd",
                    ".abw",
                    ".zabw",
                    # ".csv",
                    # ".tsv",
                    # ".txt",
                    ".md",
                    ".markdown",
                    ".rst",
                    (".org","file-document",'#77AA99'),
                    
                ),
                icon=("file-document",(0.3, 0.6, 0.95)),
            ),
            # PDFs
            "pdfs": FileCategory(
                extensions=(
                    ".pdf",
                    ".fdf",
                    ".xfdf",
                    ".pdx",
                    ".pd",
                    ".pmd",
                    # PDF-like
                    ".ai",
                    ".indd",
                ),
                icon=("file-document",(1.0, 0.3, 0.3)),
            ),
            # Spreadsheets
            "spreadsheets": FileCategory(
                extensions=(
                    ".xls",
                    ".xlsx",
                    ".ods",
                    ".csv",
                    ".tsv",
                    ".fods",
                    ".xlt",
                    ".xltx",
                    ".xlsm",
                    ".xltm",
                    ".xlw",
                    ".xlr",
                    ".numbers",
                    ".gnumeric",
                    ".uos",
                    ".sxc",
                    ".stc",
                    ".sdc",
                    ".dif",
                    ".slk",
                    ".prn",
                    ".dbf",
                    ".qpw",
                    ".wb1",
                    ".wb2",
                    ".wb3",
                    ".123",
                    ".wk1",
                    ".wk3",
                    ".wk4",
                    ".wks",
                    ".wq1",
                    ".wq2",
                    ".xlk",
                    ".xlsb",
                    ".xlam",
                    ".xla",
                    ".xll",
                    ".xlm",
                ),
                icon=("file-table",(0.3, 0.85, 0.5)),
            ),
            # Presentations
            "presentations": FileCategory(
                extensions=(
                    ".ppt",
                    ".pptx",
                    ".odp",
                    ".key",
                    ".fodp",
                    ".pot",
                    ".potx",
                    ".pps",
                    ".ppsx",
                    ".pptm",
                    ".potm",
                    ".ppsm",
                    ".sxi",
                    ".sti",
                    ".sxd",
                    ".std",
                    ".show",
                    ".shw",
                    ".prz",
                    ".pez",
                    ".odg",
                    ".otp",
                    ".uop",
                    ".wmf",
                    ".emf",
                    ".gslides",
                    ".nb",
                    ".pez",
                    ".thmx",
                    ".ppam",
                    ".pptx",
                    ".ppa",
                ),
                icon=("shape",(1.0, 0.5, 0.4)),
            ),
            'plugins': FileCategory(
                extensions=(
                    '.vsix',
                    ),
                icon=('puzzle',(.8,.8,.8))
                ),
            'disk_image_archives': FileCategory(
                extensions=(
                    # CD/DVD/Blu-ray Images
                    '.iso', '.bin', '.cue', '.mdf', '.mds', '.img', '.ccd', '.sub', '.nrg',
                    # # Floppy/Virtual Disk Images
                    # '.dmg', '.toast', '.vfd', '.ima', '.dsk', '.vhd', '.vhdx', '.vdi', '.vmdk',
                    # # Game Console Images
                    # '.nds', '.3ds', '.cia', '.cci', '.cso', '.gb', '.gba', '.n64', '.sfc', '.smc',
                    # # Forensic/System Images
                    # '.dd', '.raw', '.aff', '.afm', '.afd', '.e01', '.l01', '.s01', '.vmdk', '.vmem',
                    # Optical Disc Formats
                    '.b5t', '.b6t', '.bwt', '.cdi', '.dmg', '.dmgpart', '.dvdr', '.gi', '.pdi',
                    # Legacy Formats
                    '.ashdisc', '.daa', '.fcd', '.gcd', '.gi', '.p01', '.pqi', '.udf', '.xmd'
                ),
                icon=('disc',(0.65, 0.75, 0.9))
            ),
            
            # Archives
            "archives": FileCategory(
                extensions=(
                    ".rar",
                    (".zip","folder-zip",(0.8, 0.6, 0.3)),
                    ".7z",
                    ".tar",
                    ".gz",
                    ".bz2",
                    ".xz",
                    # ".iso",
                    ".dmg",
                    # ".pkg",
                    ".deb",
                    ".rpm",
                    ".cab",
                    # ".msi",
                    # ".apk",
                    # ".jar",
                    ".war",
                    ".ear",
                    ".sar",
                    ".a",
                    ".ar",
                    ".cpio",
                    ".shar",
                    ".lbr",
                    ".mar",
                    ".sbx",
                    ".bz",
                    ".lz",
                    ".lzma",
                    ".lzo",
                    ".rz",
                    ".sfark",
                    ".sz",
                    ".xz",
                    ".z",
                    ".Z",
                    ".zst",
                    ".zipx",
                    ".zz",
                    ".arc",
                    ".ark",
                    ".cdx",
                    ".ha",
                    ".hki",
                    ".ice",
                    ".pak",
                    ".pit",
                    ".sit",
                    ".sitx",
                    ".sqx",
                    ".tar.gz",
                    ".tgz",
                    ".tbz2",
                    ".tlz",
                    ".txz",
                    ".tzst",
                    ".uc2",
                    ".uha",
                    ".wim",
                    ".xar",
                    ".zoo",
                    ".zip",
                    ".zpaq",
                    ".zz",
                ),
                icon=("zip-box",(0.8, 0.6, 0.3)),
            ),
            # Shortcuts & Links
            "shortcuts": FileCategory(
                extensions=(
                    (".url",'link-variant',(0.9, 0.9, 0.9)),
                    ".lnk",
                    ".desktop",
                    ".webloc",
                    ".alias",
                    ".appref-ms",
                    ".website",
                    ".bkf",
                    ".favorite",
                    ".library-ms",
                ),
                icon=("open-in-new",(0.9, 0.9, 0.9)),
            ),
            # Add more categories as needed...
            # (Previous categories for audio, video, code, etc. can be included similarly)
            "audio": FileCategory(
                extensions=(
                    ".mp3",
                    ".wav",
                    ".aiff",
                    ".aif",
                    ".flac",
                    ".alac",
                    ".ogg",
                    ".wma",
                    ".aac",
                    ".m4a",
                    ".opus",
                    ".ac3",
                    ".amr",
                    ".au",
                    ".mid",
                    ".midi",
                    ".kar",
                    ".rmi",
                    ".xm",
                    ".mod",
                    ".s3m",
                    ".it",
                    ".mtm",
                    ".umx",
                    ".mo3",
                    ".spx",
                    ".tta",
                    ".ape",
                    ".wv",
                    ".dts",
                    ".dsd",
                    ".dsf",
                    ".mka",
                    ".webm",
                    ".m3u",
                    ".pls",
                    ".asx",
                    ".cue",
                    ".aup",
                    ".band",
                    ".daw",
                    ".ses",
                    ".als",
                    ".flp",
                    ".ptf",
                    ".rpp",
                    ".logic",
                    ".garageband",
                    ".reason",
                    ".npr",
                    ".nms",
                    ".nki",
                    ".sf2",
                    ".sfz",
                    ".gig",
                    ".dls",
                    ".exs",
                    ".kontakt",
                    ".omnisphere",
                    ".mx6",
                    ".als",
                    ".ableton",
                    ".alp",
                    ".adg",
                    ".adv",
                    ".agr",
                    ".ams",
                    ".cpr",
                    ".dwp",
                    ".npr",
                    ".rpp",
                    ".ptx",
                    ".sng",
                    ".sfl",
                    ".sfap0",
                    ".sfk",
                    ".sfpack",
                ),
                icon=("file-music",(0.5, 0.8, 1.0)),
            ),
            "video": FileCategory(
                extensions=(
                    ".mp4",
                    ".avi",
                    ".mov",
                    ".mkv",
                    ".wmv",
                    ".flv",
                    ".webm",
                    ".m4v",
                    ".mpg",
                    ".mpeg",
                    ".3gp",
                    ".3g2",
                    ".m2ts",
                    ".mts",
                    ".ts",
                    ".vob",
                    ".ogv",
                    ".divx",
                    ".f4v",
                    ".h264",
                    ".m2v",
                    ".m4p",
                    ".m4v",
                    ".mxf",
                    ".nsv",
                    ".rm",
                    ".rmvb",
                    ".svi",
                    ".tod",
                    ".trp",
                    ".vp6",
                    ".vp7",
                    ".vp8",
                    ".vp9",
                    ".yuv",
                    ".gifv",
                    ".m1v",
                    ".m2v",
                    ".m4e",
                    ".mj2",
                    ".mpv",
                    ".mpe",
                    ".qt",
                    ".ram",
                    ".smk",
                    ".swf",
                    ".viv",
                    ".y4m",
                    ".264",
                    ".265",
                    ".hevc",
                    ".av1",
                    ".dav",
                    ".gcs",
                    ".ivf",
                    ".k3g",
                    ".mjp",
                    ".mjpg",
                    ".mod",
                    ".moflex",
                    ".mp4v",
                    ".mse",
                    ".mvc",
                    ".mxg",
                    ".nuv",
                    ".pva",
                    ".rcv",
                    ".rcd",
                    ".rec",
                    ".rv",
                    ".rrc",
                    ".sdp",
                    ".seq",
                    ".sml",
                    ".ssif",
                    ".str",
                    ".vro",
                    ".xesc",
                ),
                icon=("file-video",(1.0, 0.3, 0.7)),
            ),
            # Engineering Documents
            "engineering_docs": FileCategory(
                extensions=(
                    ".idw",
                    ".dwt",
                    ".ipj",
                    ".idcl",
                    ".idcx",
                    ".dwf",
                    ".dwfx",
                    ".edrw",
                    ".eprt",
                    ".edrw",
                    ".easm",
                    ".p2s",
                    ".p2a",
                    ".p3s",
                    ".p3a",
                    ".p4s",
                    ".p4a",
                    ".pc3",
                    ".pc4",
                    ".pc5",
                    # ".pdf",
                    ".pln",
                    ".prt",
                    ".prw",
                    ".psm",
                    ".pwd",
                    ".pwx",
                    ".rpt",
                    ".slddrw",
                    ".slddrt",
                    ".sldprt",
                    ".sldasm",
                    ".std",
                    ".tpl",
                    ".vda",
                    ".vrml",
                    ".wrl",
                    ".xgl",
                    ".zgl",
                ),
                icon=("file-cog",(0.1, 0.6, 0.85)),
            ),
            "virtualization": FileCategory(
                extensions=(
                    ".vmdk",
                    ".vdi",
                    ".vhd",
                    ".vhdx",
                    ".ova",
                    ".ovf",
                    ".nvram",
                    ".vmem",
                    ".vmsd",
                    ".vmsn",
                    ".vmss",
                    ".vmtm",
                    ".vmx",
                    ".vmxf",
                    ".pvm",
                    ".hdd",
                    ".qcow",
                    ".qcow2",
                    ".qed",
                    ".vfd",
                    ".vfd",
                    ".vhd",
                    ".avhd",
                    ".avhdx",
                    ".vsv",
                    ".bin",
                    ".iso",
                    ".img",
                    ".dmg",
                    ".toast",
                    ".nrg",
                    ".daa",
                    ".ima",
                    ".dsk",
                    ".hdd",
                    ".hds",
                    ".hdx",
                    ".vmdk",
                    ".vmem",
                    ".vmsn",
                    ".vmss",
                    ".vmtm",
                    ".vmx",
                    ".vmxf",
                    ".nvram",
                    ".pvs",
                    ".vbox",
                    ".vbox-extpack",
                ),
                icon=("server",(0.4, 0.9, 0.8)),
            ),
            "fonts": FileCategory(
                extensions=(
                    ".ttf",
                    ".otf",
                    ".woff",
                    ".woff2",
                    ".eot",
                    ".pfb",
                    ".pfm",
                    ".afm",
                    ".dfont",
                    ".sfd",
                    ".bdf",
                    ".pcf",
                    ".ttc",
                    ".fon",
                    ".fnt",
                    ".chr",
                    ".suit",
                    ".xfn",
                    ".gf",
                    ".pk",
                    ".mf",
                    ".tfm",
                    ".vf",
                    ".vpl",
                    ".map",
                    ".enc",
                    ".cid",
                    ".cef",
                    ".otb",
                    ".pfa",
                    ".pcf.gz",
                    ".ttx",
                    ".ufo",
                    ".svg",
                    ".eot",
                    ".woff",
                    ".woff2",
                ),
                icon=("format-font",(1.0, 0.8, 0.4)),
            ),
            "ebooks": FileCategory(
                extensions=(
                    ".epub",
                    ".mobi",
                    ".azw",
                    ".azw3",
                    ".kfx",
                    ".kpf",
                    ".prc",
                    ".fb2",
                    ".ibooks",
                    ".pdb",
                    ".lit",
                    ".chm",
                    ".djvu",
                    ".djv",
                    ".pdf",
                    ".oxps",
                    ".xps",
                    ".cbz",
                    ".cbr",
                    ".cb7",
                    ".cbt",
                    ".cba",
                    ".ceb",
                    ".pdg",
                    ".tr2",
                    ".tr3",
                    ".snb",
                    ".xeb",
                    ".pep",
                    ".baf",
                    ".aeh",
                    ".bok",
                    ".dnl",
                    ".ebk",
                    ".edn",
                    ".etd",
                    ".flip",
                    ".htmlz",
                    ".imp",
                    ".inf",
                    ".kbk",
                    ".lrf",
                    ".lrx",
                    ".man",
                    ".mmp",
                    ".opf",
                    # ".pkg",
                    ".ps",
                    ".rtf",
                    ".tk3",
                    ".tpz",
                    ".vbk",
                    ".webz",
                    ".zno",
                    ".ztxt",
                ),
                icon=("book-open-variant",(0.7, 0.5, 0.95)),
            ),
            "temp": FileCategory(
                extensions=(
                    ".tmp",
                    ".temp",
                    ".bak",
                    ".backup",
                    ".old",
                    ".new",
                    ".part",
                    ".crdownload",
                    ".download",
                    ".partial",
                    ".swp",
                    ".swo",
                    ".swn",
                    ".spl",
                    ".lock",
                    ".lck",
                    ".pid",
                    ".state",
                    ".autosave",
                    ".~",
                    ".dmp",
                    ".hprof",
                    ".core",
                    ".stackdump",
                    ".crash",
                    ".minidump",
                    ".mdmp",
                    ".wer",
                    ".recycle",
                    ".trash",
                    ".pending",
                    ".pending-rename",
                    ".pending-delete",
                    ".pending-move",
                    ".pending-copy",
                    ".pending-merge",
                ),
                icon=("file-clock-outline",(0.8, 0.8, 0.8)),
            ),
            "logs": FileCategory(
                extensions=(
                    ".log",
                    ".txt",
                    ".err",
                    ".out",
                    ".debug",
                    ".info",
                    ".warn",
                    ".error",
                    ".trace",
                    ".audit",
                    ".history",
                    ".journal",
                    ".dump",
                    ".diag",
                    ".report",
                    ".crash",
                    ".stacktrace",
                    ".stderr",
                    ".stdout",
                    ".syslog",
                    ".eventlog",
                    ".evtx",
                    ".etl",
                    ".wevt",
                    ".evt",
                    ".evtx",
                    ".evtc",
                    ".evtl",
                    ".evtm",
                    ".evtr",
                    ".evts",
                    ".evtx",
                    ".evt_",
                    ".evtx_",
                    ".evtc_",
                    ".evtl_",
                    ".evtm_",
                    ".evtr_",
                    ".evts_",
                    ".evtx_",
                ),
                icon=("text-box",(0.7, 0.7, 0.7)),
            ),
            # General code
            "code":FileCategory(
                extensions=(
                    ".ees"
                    ),
                icon=('file-code',(0.25, 0.8, 1.0))
                ),
            # Python
            'python': FileCategory(
                extensions=('.py', '.pyc', '.pyo', '.pyd', '.pyi', '.pyw', '.pyz', '.pyzw', '.pyt', '.whl', '.egg'),
                icon=('language-python','#519ABA')
            ),

            # JavaScript/TypeScript
            'javascript': FileCategory(
                extensions=('.js', '.jsx', '.mjs', '.cjs', '.ts', '.tsx', '.mts', '.cts', '.es', '.es6', '.pac'),
                icon='language-javascript'
            ),

            # Java/Kotlin/Scala (JVM)
            'jvm': FileCategory(
                extensions=('.java', '.class', '.jar', '.war', '.ear', '.jmod', '.jks', '.kt', '.kts', '.scala', '.sc'),
                icon='language-java'
            ),

            # C/C++
            'cpp': FileCategory(
                extensions=('.c', '.h', '.cpp', '.hpp', '.cc', '.cxx', '.hxx', '.ii', '.inl', '.ipp', '.ixx', '.c++', '.h++', '.cu', '.cuh'),
                icon='language-cpp'
            ),

            # Rust
            'rust': FileCategory(
                extensions=('.rs', '.rlib', '.rustc', '.toml'),  # Cargo.toml is included here
                icon='language-rust'
            ),

            # Go
            'go': FileCategory(
                extensions=('.go', '.mod', '.sum', '.work'),
                icon='language-go'
            ),

            # Ruby
            'ruby': FileCategory(
                extensions=('.rb', '.rbw', '.gemspec', '.rake', '.ru', '.erb', '.rbs'),
                icon='language-ruby'
            ),

            # PHP
            'php': FileCategory(
                extensions=('.php', '.phtml', '.php3', '.php4', '.php5', '.php7', '.phps', '.phar', '.inc'),
                icon='language-php'
            ),

            # Swift
            'swift': FileCategory(
                extensions=('.swift', '.swiftinterface', '.swiftmodule', '.swiftsourceinfo'),
                icon='language-swift'
            ),

            # R
            'r': FileCategory(
                extensions=('.r', '.R', '.Rdata', '.Rds', '.Rda', '.Rhistory', '.Rprofile', '.Renviron'),
                icon='language-r'
            ),

            # Haskell
            'haskell': FileCategory(
                extensions=('.hs', '.lhs', '.cabal', '.hsc'),
                icon='lambda'
            ),
            # HTML
            "html": FileCategory(
                extensions=(
                    ".html",
                    ".htm",
                    ".xhtml",
                    ".shtml",
                    ".jhtml",
                    ".chtml",
                    ".dhtml",
                    ".mhtml",
                ),
                # icon=("web-box",(1.0, 0.6, 0.2)),
                icon=('web','#0078D7')
            ),
            # CSS/Sass
            "css": FileCategory(
                extensions=(
                    ".css",
                    ".scss",
                    ".sass",
                    ".less",
                    ".styl",
                    ".pcss",
                    ".postcss",
                ),
                icon=("language-css3",(0.3, 0.8, 1.0)),
            ),
            # Web Templates
            "templates": FileCategory(
                extensions=(
                    ".ejs",
                    ".pug",
                    ".jade",
                    ".hbs",
                    ".handlebars",
                    ".mustache",
                    ".twig",
                    ".liquid",
                    ".njk",
                ),
                icon=("file-document-outline",(0.7, 0.9, 1.0)),
            ),
            # Package Managers
            "packages": FileCategory(
                extensions=(
                    ".json",
                    ".lock",
                    ".toml",
                    ".yaml",
                    ".yml",
                    ".xml",
                    # ".ini",
                    ".cfg",
                    ".conf",
                ),
                icon=("package-variant",(0.95, 0.7, 0.3)),
            ),
            # Build Tools
            "build": FileCategory(
                extensions=(
                    ".gradle",
                    ".pom",
                    ".build",
                    ".bzl",
                    ".bazel",
                    ".cmake",
                    ".makefile",
                    ".mk",
                    ".ninja",
                ),
                icon=("hammer-wrench",(0.8, 0.5, 0.2)),
            ),
            # CI/CD
            "ci": FileCategory(
                extensions=(
                    ".yml",
                    ".yaml",
                    ".travis.yml",
                    ".gitlab-ci.yml",
                    ".circleci",
                    ".drone.yml",
                    ".appveyor.yml",
                    ".azure-pipelines.yml",
                ),
                icon=("git",(0.4, 0.95, 0.7)),
            ),
            # SQL
            "sql": FileCategory(
                extensions=(
                    ".sql",
                    ".ddl",
                    ".dml",
                    ".pgsql",
                    ".psql",
                    ".plpgsql",
                    ".plsql",
                    ".pkb",
                    ".pks",
                    ".tab",
                    ".udf",
                    ".viw",
                    ".prc",
                    ".fnc",
                    ".trg",
                ),
                icon=("database",(0.9, 0.7, 1.0)),
            ),
            # Shell Scripts
            "shell": FileCategory(
                extensions=(
                    ".sh",
                    ".bash",
                    ".zsh",
                    ".fish",
                    ".ps1",
                    ".psm1",
                    ".psd1",
                    ".bat",
                    ".cmd",
                    ".vbs",
                ),
                # icon=("console",(1.0, 1.0, 0.5)),
                icon=("console",(1.0, 1.0, 1.0)),
            ),
            # Notebooks
            "notebooks": FileCategory(
                extensions=(
                    ".ipynb",
                    ".rmd",
                    ".sc",
                    ".sage",
                    ".zcml",
                    ".qlikview",
                    ".qvw",
                    ".twb",
                    ".tde",
                ),
                icon=("notebook",(1.0, 0.6, 0.8)),
            ),
            # Assembly
            "assembly": FileCategory(
                extensions=(
                    ".asm",
                    ".s",
                    ".S",
                    ".inc",
                    ".mac",
                    ".lst",
                    ".obj",
                    ".o",
                    ".ko",
                ),
                icon=("chip",(0.8, 0.3, 0.8)),
            ),
            # Embedded
            "embedded": FileCategory(
                extensions=(
                    ".hex",
                    ".bin",
                    ".elf",
                    ".map",
                    ".ld",
                    ".sv",
                    ".v",
                    ".vhdl",
                    ".vhd",
                    ".ucf",
                    ".qsf",
                    ".sdc",
                    ".bit",
                    ".mcs",
                    ".pof",
                ),
                icon=("microcontroller",(0.4, 0.8, 0.5)),
            ),
            # Dotfiles/Configs
            "config": FileCategory(
                extensions=(
                    ".env",
                    ".gitignore",
                    ".gitattributes",
                    ".editorconfig",
                    ".dockerignore",
                    ".npmignore",
                    ".htaccess",
                    ".properties",
                    ".reg",
                ),
                icon=("cog",(0.6, 0.85, 1.0)),
            ),
            # Containers/VMs
            "containers": FileCategory(
                extensions=(
                    ".dockerfile",
                    ".dockerignore",
                    ".compose.yml",
                    ".vagrantfile",
                    ".box",
                    ".ova",
                    ".ovf",
                ),
                icon=("docker",(0.3, 0.95, 0.95)),
            ),
            "apps": FileCategory(
                extensions=(
                    # Windows
                    ".exe",
                    ".com",
                    ".scr",
                    ".cpl",
                    ".msc",
                    ".jar",
                    ".appref-ms",
                    ".wsf",
                    ".ps1",
                    ".psm1",
                    # macOS/Linux
                    ".app",
                    ".run",
                    ".out",
                    ".elf",
                    ".bin",
                    ".so",
                    ".dylib",
                    ".bundle",
                    ".sh",
                    ".command",
                    # Cross-platform
                    ".py",
                    ".rb",
                    ".pl",
                    ".lua",
                    ".ahk",
                    ".scpt",
                    ".js",
                    ".php",
                    ".bat",
                    ".cmd",
                    ".vbs",
                ),
                icon=("application-export",(0.2, 0.9, 0.6)),  # or 'application' for a simpler icon
            ),
            "installers": FileCategory(
                extensions=(
                    # Windows
                    ".msi",
                    ".msix",
                    ".msixbundle",
                    ".appx",
                    ".appxbundle",
                    ".exe",
                    ".msp",
                    ".mst",
                    # macOS
                    ".dmg",
                    (".pkg","package-variant","#CF925E"),
                    ".mpkg",
                    ".app",
                    ".prefpane",
                    ".kext",
                    # Linux
                    ".deb",
                    ".rpm",
                    ".snap",
                    ".flatpak",
                    ".AppImage",
                    ".pacman",
                    ".pkg.tar.zst",
                    # Mobile
                    ".apk",
                    ".ipa",
                    ".xap",
                    ".appx",
                    ".aab",
                    # Generic
                    ".zip",
                    ".tar.gz",
                    ".7z",
                    ".iso",
                    ".img",
                ),
                icon=("package-down",(0.8, 0.4, 0.8)),
            ),
            "system_libs": FileCategory(
                extensions=(
                    ".dll",
                    ".so",
                    ".dylib",
                    ".a",
                    ".lib",
                    ".ko",
                    ".sys",
                    ".drv",
                    ".ocx",
                    ".vxd",
                    ".efi",
                    ".acm",
                    ".ax",
                    ".tsp",
                    ".ime",
                    ".cpl",
                    ".mui",
                    ".mun",
                    ".nlp",
                    ".scr",
                    ".vbx",
                    ".xll",
                    ".olb",
                    ".tlb",
                    ".winmd",
                ),
                icon=("file-cog-outline",'#D4E7FC'),
            ),
            "disk_images": FileCategory(
                extensions=(
                    ".iso",
                    ".img",
                    ".dmg",
                    ".toast",
                    ".vfd",
                    ".nrg",
                    ".daa",
                    ".bin",
                    ".cue",
                    ".ima",
                    ".dsk",
                    ".vhd",
                    ".vhdx",
                    ".avhd",
                    ".vmdk",
                    ".vdi",
                    ".qcow",
                    ".qcow2",
                    ".hdd",
                    ".hds",
                    ".vfd",
                    ".mem",
                    ".dmp",
                    ".hprof",
                    ".core",
                    ".crash",
                    ".minidump",
                    ".mdmp",
                    ".raw",
                    ".img",
                ),
                icon=("harddisk",(0.7, 0.7, 0.8)),
            ),
            "system_config": FileCategory(
                extensions=(
                    ".reg",
                    ".inf",
                    ".ini",
                    ".cfg",
                    ".conf",
                    ".plist",
                    ".json",
                    ".xml",
                    ".yaml",
                    ".toml",
                    ".log",
                    ".tmp",
                    ".bak",
                    ".old",
                    ".part",
                    ".pid",
                    ".lock",
                    ".lck",
                    ".swp",
                    ".dmp",
                    ".evtx",
                    ".etl",
                    ".syslog",
                    ".journal",
                    ".diag",
                    ".report",
                    ".crash",
                    ".audit",
                ),
                icon=("cog-sync",(0.7, 0.7, 1.0)),
            ),
            "firmware": FileCategory(
                extensions=(
                    ".rom",
                    ".bin",
                    ".hex",
                    ".uf2",
                    ".dfu",
                    ".cap",
                    ".bio",
                    ".fd",
                    ".flash",
                    ".eep",
                    # ".pkg",
                    ".bios",
                    ".frm",
                    ".fdt",
                    ".dtb",
                    ".aml",
                    ".acpi",
                    ".uefi",
                    ".efi",
                    ".tef",
                    # ".pkg",
                    ".rbf",
                    ".bit",
                    ".mcs",
                ),
                icon=("chip",(0.4, 0.4, 0.9)),
            ),
            "cursors": FileCategory(
                icon=('button-cursor'),
                extensions=('.cur')
                )
            
        }
        for v in self.icon_categories.values():
            v.size = self.size

    def get(self, v):
        v = v.lower()
        try:
            return self._resolved[v]
        except:
            for k, cat in self.icon_categories.items():
                if v in cat:
                    ic = cat.get(v)
                    self._resolved[v] = ic
                    return ic
            return self.default_icon


def remove_duplicates_fast(lst):
    seen = set()        # Set to keep track of seen elements
    unique_values = []  # List to collect unique values in order

    for item in lst:
        if item not in seen:
            seen.add(item)
            unique_values.append(item)

    return unique_values

class BrowserHistory:
    def __init__(self):
        self.history = []  # List to store browsing history
        self.current_page = None  # Variable to keep track of current page index

    def visit(self, url):
        """Visit a new URL, adding it to history"""
        # If we are currently on a page and it's not the last in history, truncate history
        if self.current_page is not None and self.current_page < len(self.history) - 1:
            self.history = self.history[:self.current_page + 1]

        self.history.append(url)
        self.history=remove_duplicates_fast(self.history)
        self.current_page = len(self.history) - 1  # Update current page index

    def back(self):
        """Go back one page in history"""
        if self.current_page is not None and self.current_page > 0:
            self.current_page -= 1
            return self.history[self.current_page]
        else:
            print("No previous page available")

    def forward(self):
        """Go forward one page in history"""
        if self.current_page is not None and self.current_page < len(self.history) - 1:
            self.current_page += 1
            return self.history[self.current_page]
        else:
            print("No next page available")

    def current_url(self):
        """Get the current URL"""
        if self.current_page is not None:
            return self.history[self.current_page]
        else:
            return None
    def print(self):
        print(self.history)

class NavigationHistory:
    def __init__(self, max_size=50):
        self.back_stack = []       # Stack for backward navigation
        self.current = None        # Current location
        self.forward_stack = []    # Stack for forward navigation
        self.max_size = max_size   # Maximum history size
        self.is_navigating = False # Flag to track navigation vs new visits
    
    def visit(self, location, is_navigation=False):
        """Add a new location to history"""
        if self.current == location:
            return  # Don't do anything if same location
        
        if not is_navigation and self.current is not None:
            # Only add to back stack if this is a new visit (not navigation)
            self.back_stack.append(self.current)
        
        if not is_navigation:
            # Clear forward stack only for new visits
            self.forward_stack = []
        
        self.current = location
        self.is_navigating = False
        
        # Enforce max size
        if len(self.back_stack) > self.max_size:
            self.back_stack.pop(0)
    
    def back(self):
        """Go to previous location in history"""
        if not self.can_go_back():
            return None
        
        self.forward_stack.append(self.current)
        self.current = self.back_stack.pop()
        self.is_navigating = True
        return self.current
    
    def forward(self):
        """Go to next location in history"""
        if not self.can_go_forward():
            return None
        
        self.back_stack.append(self.current)
        self.current = self.forward_stack.pop()
        self.is_navigating = True
        return self.current
    
    def can_go_back(self):
        """Check if back navigation is possible"""
        return len(self.back_stack) > 0
    
    def can_go_forward(self):
        """Check if forward navigation is possible"""
        return len(self.forward_stack) > 0
    
    def get_current(self):
        """Get current location"""
        return self.current
    
    def get_history_state(self):
        """Get complete navigation state"""
        return {
            'back_stack': self.back_stack.copy(),
            'current': self.current,
            'forward_stack': self.forward_stack.copy(),
            'can_go_back': self.can_go_back(),
            'can_go_forward': self.can_go_forward()
        }
    
    def clear(self):
        """Clear all history"""
        self.back_stack = []
        self.current = None
        self.forward_stack = []

import random
from collections import deque

class PlaylistManager:
    def __init__(self):
        self.playlist_set = set()        # Set to store unique elements (e.g., music tracks)
        self.playlist_order = deque()    # Deque to maintain the order of playlist elements
        self.current_track = None        # Pointer to the current track

    def insert(self, track):
        """Insert a new track into the playlist (if not already present)"""
        if track not in self.playlist_set:
            self.playlist_set.add(track)
            self.playlist_order.append(track)
            if self.current_track is None:
                self.current_track = track

    def add_to_queue(self, track):
        """Add a track to the end of the playlist queue"""
        if track not in self.playlist_set:
            self.playlist_set.add(track)
            self.playlist_order.append(track)

    def add_after_current(self, track):
        """Add a track after the current track in the playlist"""
        if track not in self.playlist_set:
            if self.current_track is not None and self.current_track in self.playlist_set:
                current_index = self.playlist_order.index(self.current_track)
                self.playlist_order.insert(current_index + 1, track)
                self.playlist_set.add(track)

    def remove(self, track):
        """Remove a track from the playlist"""
        if track in self.playlist_set:
            self.playlist_set.remove(track)
            self.playlist_order.remove(track)

    def get_current_track(self):
        """Get the current track"""
        return self.current_track

    def set_current_track(self, track):
        """Set the current track"""
        if track in self.playlist_set:
            self.current_track = track

    def shuffle(self):
        """Shuffle the playlist order"""
        random.shuffle(self.playlist_order)

    def unshuffle(self):
        """Restore the playlist order to its original state"""
        self.playlist_order = deque(sorted(self.playlist_order, key=lambda x: self.playlist_order.index(x)))

    def next_track(self):
        """Move to the next track in the playlist"""
        if self.current_track is not None and self.current_track in self.playlist_set:
            try:
                current_index = self.playlist_order.index(self.current_track)
                next_track = self.playlist_order[current_index + 1]
                self.current_track = next_track
                return next_track
            except IndexError:
                print("End of playlist reached.")
        else:
            print("No current track set.")

    def prev_track(self):
        """Move to the previous track in the playlist"""
        if self.current_track is not None and self.current_track in self.playlist_set:
            try:
                current_index = self.playlist_order.index(self.current_track)
                prev_track = self.playlist_order[current_index - 1]
                self.current_track = prev_track
                return prev_track
            except IndexError:
                print("Start of playlist reached.")
        else:
            print("No current track set.")

    def print_playlist(self):
        """Print the current playlist order"""
        print("Playlist Order:")
        for idx, track in enumerate(self.playlist_order, start=1):
            print(f"{idx}. {track}")

def get_common_paths():
    """Returns a list of common paths available on the current platform."""
    paths = []
    home = os.path.expanduser("~")
    
    # Root storage (varies by platform)
    root = None
    if sys.platform == "win32":
        root = os.path.abspath(os.sep)  # Usually C:\
    else:
        root = os.path.abspath(os.sep)  # /
    if root:
        paths.append(root)
    
    # Platform-specific paths
    platform_paths = {
        "win32": {
            "desktop": os.path.join(home, "Desktop"),
            "documents": os.path.join(home, "Documents"),
            "downloads": os.path.join(home, "Downloads"),
            "images": os.path.join(home, "Pictures"),
            "videos": os.path.join(home, "Videos"),
            "music": os.path.join(home, "Music"),
            "books": os.path.join(home, "Documents"),  # Windows doesn't have a standard Books folder
        },
        "darwin": {  # macOS
            "desktop": os.path.join(home, "Desktop"),
            "documents": os.path.join(home, "Documents"),
            "downloads": os.path.join(home, "Downloads"),
            "images": os.path.join(home, "Pictures"),
            "videos": os.path.join(home, "Movies"),
            "music": os.path.join(home, "Music"),
            "books": os.path.join(home, "Library", "Containers", "com.apple.BKAgentService", "Data", "Documents", "iBooks"),
        },
        "linux": {
            "desktop": os.path.join(home, "Desktop"),
            "documents": os.path.join(home, "Documents"),
            "downloads": os.path.join(home, "Downloads"),
            "images": os.path.join(home, "Pictures"),
            "videos": os.path.join(home, "Videos"),
            "music": os.path.join(home, "Music"),
            "books": os.path.join(home, "Documents"),  # Linux doesn't have a standard Books folder
        }
    }
    
    # Get paths for current platform
    current_platform = sys.platform
    platform_specific = platform_paths.get("win32" if current_platform == "win32" else "linux")  # Default to Linux-style for unknown platforms
    
    if current_platform == "darwin":
        platform_specific = platform_paths["darwin"]
    
    # Add user home directory
    paths.append(home)
    
    # Add platform-specific paths if they exist
    for name, path in platform_specific.items():
        if os.path.exists(path):
            paths.append(path)
    
    # Remove duplicates while preserving order
    # seen = set()
    unique_paths = {root:'root',home:'home'}
    for path in paths:
        if path not in unique_paths:
            # unique_paths.append(path)
            unique_paths[path]=os.path.basename(path)
    
    return unique_paths

# # Example usage:
# playlist = PlaylistManager()

# # Insert tracks into the playlist
# playlist.insert("Track 1")
# playlist.insert("Track 2")
# playlist.insert("Track 3")
# playlist.insert("Track 2")  # Won't be added again due to uniqueness

# # Add more tracks
# playlist.add_to_queue("Track 4")
# playlist.add_to_queue("Track 5")

# # Print current playlist
# playlist.print_playlist()

# # Shuffle the playlist
# playlist.shuffle()
# playlist.print_playlist()

# # Move to next and previous tracks
# print("Current Track:", playlist.get_current_track())
# playlist.next_track()
# print("Current Track:", playlist.get_current_track())
# playlist.prev_track()
# print("Current Track:", playlist.get_current_track())

# # Set current track to "Track 3"
# playlist.set_current_track("Track 3")
# playlist.add_after_current("Track X")

# # Print updated playlist
# playlist.print_playlist()


def getFiles(path,files_ext=''):
    #if path[-1] != '/':path+='/'
    import os
    filelist=[]
    files_here=os.listdir(path)
    
    #print(files_ext,files_here)
    for file in files_here:
        # if '.' not in os.path.basename(file):
        #     continue

        ext=os.path.splitext(file)[-1].replace('.','')
        
        if files_ext:
            # if os.path.isfile(file) and ext in files_ext:
            if ext in files_ext:
                f=os.path.join(path, file)
                if os.path.isdir(f):
                    continue
                filelist.append(f)
        else:
            file_path=os.path.join(path, file)
            if os.path.isfile(file_path):
                filelist.append(file_path)
    
    #filelist=[f.replace('/','\\') for f in filelist]
    # filelist=sorti(filelist)
    return filelist
def ensure_folder_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
def get_folders(*directories):
    '''
    Get the folders in one or more directories. Skips empty strings.
    '''
    files = []

    for directory in directories:
        if not directory or not os.path.exists(directory):
            continue
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if not os.path.isfile(filepath):
                files.append(filepath.replace('\\','/'))
    return files
def get_files(*directories):
    '''
    Get the files in one or more directories. Skips empty strings.
    '''
    files = []
    for directory in directories:
        if not directory or not os.path.exists(directory):
            continue
        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                files.append(filepath.replace('\\','/'))
    return files
def text_between(string,first_delimiter,last_delimiter):
    btw=re.search(f'{first_delimiter}(.*){last_delimiter}', string)
    if btw:
        return btw.group()
    else:
        return ''
def md2markdown(t):
    nt=''
    for l in t.splitlines():
        if l:
            if '#'==l[0]:
                l=markup_str( l[1:].strip(),size=20,list_tags=['b'])
        nt+=l+'\n'
    t=nt.strip()
    btw=True
    while btw:
        btw=text_between(t,r'\*\*',r'\*\*')
        # print(btw)
        if btw:
            t=t.replace(btw,f'[b]{btw[2:-2]}[/b]')
    btw=True
    while btw:
        btw=text_between(t,r'\<',r'\>')
        # print(btw)
        if btw:
            t=t.replace(btw,markup_href(btw[1:-1]))
    return t





# with open('_internal/notes.md','r',encoding='utf-8') as fid:
#     ans=md2markdown(fid.read())
#     with open('_internal/notes.rst','w',encoding='utf-8') as f2:
#         f2.write(ans)
#     print(ans)

# match platform:
#     case 'win':
#         # import os
#         # os.system('cls')
#         import time
#         import clr
#         # Add necessary .NET references
#         clr.AddReference("System.Windows.Forms")
#         clr.AddReference("System.Drawing")
#         clr.AddReference("System")
#         # clr.AddReference("System.Widows.Forms.FormBorderStyle")

#         from System import String

#         # Import all required components
#         from System.Windows.Forms import (
#             Application, Form, Label, Cursor, Timer,
#             FormBorderStyle, FormStartPosition, AnchorStyles
#         )
#         from System.Drawing import (
#             Color, Point, Font, FontStyle, Size
#         )
#         from System.Windows.Forms import Padding

#         class Tooltip(Form):
#             def __init__(self, message):
#                 super().__init__()
                
#                 # Form setup
                
#                 self.StartPosition = FormStartPosition.Manual
#                 self.ShowInTaskbar = False
#                 self.TopMost = True
#                 # self.ControlBox = False
#                 # self.Text = String.Empty
#                 self.FormBorderStyle = getattr(FormBorderStyle,'None')
                
#                 # Get cursor position
#                 time.sleep(.5)
#                 cursor_pos = Cursor.Position
#                 self.Location = Point(cursor_pos.X + 8, cursor_pos.Y + 8)  # Offset from cursor
                
#                 # Store initial mouse position
#                 self.initial_mouse_pos = Cursor.Position
                
#                 # Create the message label
#                 self.lbl = Label()
                
#                 self.lbl.Text = message
#                 self.lbl.AutoSize = True
#                 self.lbl.Font = Font("Segoe UI", 10, FontStyle.Regular)
#                 self.lbl.BackColor = Color.FromArgb(45, 45, 45)  # Dark gray background
#                 self.lbl.ForeColor = Color.White  # White text
#                 self.lbl.Padding = Padding(0)
                
                
#                 # Form appearance
#                 # self.BackColor = Color.FromArgb(255, 0, 0)  # Slightly lighter border
#                 self.BackColor = self.lbl.BackColor  # Slightly lighter border
#                 self.Padding = Padding(0)
                
#                 # Add to form
#                 self.Controls.Add(self.lbl)
                
#                 # Set form size based on label
#                 self.ClientSize = Size(
#                     self.lbl.PreferredWidth + self.lbl.Padding.Horizontal,
#                     self.lbl.PreferredHeight + self.lbl.Padding.Vertical
#                 )

#                 # print(self.lbl.Text.Size)
#                 # self.lbl.AutoSize = False
#                 self.lbl.Anchor = getattr(AnchorStyles,'None')

                

#                 # # Center the label vertically
#                 # self.lbl.Location = Point(
#                 #     self.lbl.Padding.Left,  # Horizontal position (keep left padding)
#                 #     (self.ClientSize.Height - self.lbl.Height) // 2  # Vertical center
#                 # )
                
#                 # print(self.lbl.MinimumSize)
                
#                 # Timer to check mouse movement
#                 self.timer = Timer()
#                 self.timer.Interval = 100  # Check every 100ms
#                 self.timer.Tick += self.check_mouse_movement
#                 self.timer.Start()
                
#                 # Track when to close
#                 self.start_time = time.time()
#                 # self.max_duration = 5  # Max seconds to show (safety)
            
#             def check_mouse_movement(self, sender, event):
#                 self.TopMost = False
#                 # Close if mouse has moved significantly from initial position
#                 current_pos = Cursor.Position
#                 if (abs(current_pos.X - self.initial_mouse_pos.X) > 1 or 
#                     abs(current_pos.Y - self.initial_mouse_pos.Y) > 1):
#                     self.close_form()
                
#                 # Safety close after max duration
#                 # if time.time() - self.start_time > self.max_duration:
#                 #     self.close_form()
            
#             def close_form(self):
#                 if self.timer is not None:
#                     self.timer.Stop()
#                     self.timer.Dispose()
#                 self.Close()

#         def tooltip(message='this is a tooltip'):
#             form = Tooltip(message)
#             Application.Run(form)




def replace_module_imports(root_dir, old_module, new_module):
    """
    Recursively replaces all imports of old_module with new_module in all .py files.
    
    Args:
        root_dir (str): Root directory to search for .py files
        old_module (str): The module name to be replaced (e.g., 'xmodule')
        new_module (str): The new module name to use (e.g., 'ymodule')
    """
    # Compile regex patterns for different import styles
    patterns = [
        # Pattern for 'import xmodule' or 'import xmodule as alias'
        re.compile(rf'^( *import +){old_module}((?: +as +\w+)?\s*$)', re.MULTILINE),
        # Pattern for 'from xmodule import ...' or 'from xmodule.sub import ...'
        re.compile(rf'^( *from +){old_module}((?:\.\w+)* +import +\w+(?: +as +\w+)?\s*$)', re.MULTILINE),
        # Pattern for 'import xmodule.sub' or 'import xmodule.sub as alias'
        re.compile(rf'^( *import +){old_module}(\.\w+(?: +as +\w+)?\s*$)', re.MULTILINE)
    ]
    
    replacement = rf'\1{new_module}\2'
    
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                file_path = Path(root) / file
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    modified = False
                    for pattern in patterns:
                        new_content, count = pattern.subn(replacement, content)
                        if count > 0:
                            content = new_content
                            modified = True
                    
                    if modified:
                        with open(file_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Updated imports in {file_path}")
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")

# Example usage:
# replace_module_imports(r"C:\Users\migue\.conda\envs\app\Lib\site-packages\sk_webview", 'webview', 'sk_webview')
# print(time.time()-t0)