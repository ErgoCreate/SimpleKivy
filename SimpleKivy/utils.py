from kivy.clock import Clock
import time
import re
import os
import re
from pathlib import Path
from kivy.resources import resource_paths, resource_add_path, resource_remove_path
from kivy.utils import platform

class DotDict:
    def __init__(self,**kwargs):
        self._orignal=kwargs
        for k,v in kwargs.items():
            setattr(self,k,v)
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
pos_hints=DotDict(
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

def auto_config(size=(800,600),exit_on_escape=False,desktop=True,resizable=True,multitouch_emulation=False,**kwargs):
    from kivy.config import Config
    Config.set('kivy', 'exit_on_escape', int(exit_on_escape))
    Config.set('kivy', 'desktop', int(desktop))
    Config.set('graphics', 'resizable', int(resizable))
    Config.set('graphics', 'multisamples', 0)
    if not multitouch_emulation:
        Config.set('input', 'mouse', 'mouse,disable_multitouch')
    if size[0]:
        Config.set('graphics', 'width', size[0])
    if size[1]:
        Config.set('graphics', 'height', size[1])

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


# colors = [
#         (31, 119, 180),   # Blue
#         (158, 218, 229),  # Light Blue
#         (255, 127, 14),   # Orange
#         (255, 187, 120),  # Light Orange
#         (44, 160, 44),    # Green
#         (152, 223, 138),  # Light Green
#         (214, 39, 40),    # Red
#         (255, 152, 150),  # Light Red
#         (148, 103, 189),  # Purple
#         (197, 176, 213),  # Light Purple
#         (140, 86, 75),    # Brown
#         (196, 156, 148),  # Light Brown
#         (227, 119, 194),  # Pink
#         (247, 182, 210),  # Light Pink
#         (127, 127, 127),  # Gray
#         (199, 199, 199),  # Light Gray
#         (188, 189, 34),   # Yellow
#         (219, 219, 141),  # Light Yellow
#         (23, 190, 207),   # Cyan
#         (158, 218, 229),  # Light Cyan
#     ]

# # Scale the RGB values to the range [0, 1]
# colors = [(r / 255, g / 255, b / 255) for (r, g, b) in colors]
# print(colors)

# colors=[(0.12156862745098039, 0.4666666666666667, 0.7058823529411765), (0.6196078431372549, 0.8549019607843137, 0.8980392156862745), (1.0, 0.4980392156862745, 0.054901960784313725), (1.0, 0.7333333333333333, 0.47058823529411764), (0.17254901960784313, 0.6274509803921569, 0.17254901960784313), (0.596078431372549, 0.8745098039215686, 0.5411764705882353), (0.8392156862745098, 0.15294117647058825, 0.1568627450980392), (1.0, 0.596078431372549, 0.5882352941176471), (0.5803921568627451, 0.403921568627451, 0.7411764705882353), (0.7725490196078432, 0.6901960784313725, 0.8352941176470589), (0.5490196078431373, 0.33725490196078434, 0.29411764705882354), (0.7686274509803922, 0.611764705882353, 0.5803921568627451), (0.8901960784313725, 0.4666666666666667, 0.7607843137254902), (0.9686274509803922, 0.7137254901960784, 0.8235294117647058), (0.4980392156862745, 0.4980392156862745, 0.4980392156862745), (0.7803921568627451, 0.7803921568627451, 0.7803921568627451), (0.7372549019607844, 0.7411764705882353, 0.13333333333333333), (0.8588235294117647, 0.8588235294117647, 0.5529411764705883), (0.09019607843137255, 0.7450980392156863, 0.8117647058823529), (0.6196078431372549, 0.8549019607843137, 0.8980392156862745)]
Colors = {'': (0, 0, 0, 0), 'clear': (0, 0, 0, 0), 'b': (0, 0, 1, 1), 'g': (0, 0.5, 0, 1), 'r': (1, 0, 0, 1), 'c': (0, 0.75, 0.75, 1), 'm': (0.75, 0, 0.75, 1), 'y': (0.75, 0.75, 0, 1), 'k': (0, 0, 0, 1), 'w': (1, 1, 1, 1), 'aliceblue': (0.9411764705882353, 0.9725490196078431, 1.0, 1.0), 'antiquewhite': (0.9803921568627451, 0.9215686274509803, 0.8431372549019608, 1.0), 'aqua': (0.0, 1.0, 1.0, 1.0), 'aquamarine': (0.4980392156862745, 1.0, 0.8313725490196079, 1.0), 'azure': (0.9411764705882353, 1.0, 1.0, 1.0), 'beige': (0.9607843137254902, 0.9607843137254902, 0.8627450980392157, 1.0), 'bisque': (1.0, 0.8941176470588236, 0.7686274509803922, 1.0), 'black': (0.0, 0.0, 0.0, 1.0), 'blanchedalmond': (1.0, 0.9215686274509803, 0.803921568627451, 1.0), 'blue': (0.0, 0.0, 1.0, 1.0), 'blueviolet': (0.5411764705882353, 0.16862745098039217, 0.8862745098039215, 1.0), 'brown': (0.6470588235294118, 0.16470588235294117, 0.16470588235294117, 1.0), 'burlywood': (0.8705882352941177, 0.7215686274509804, 0.5294117647058824, 1.0), 'cadetblue': (0.37254901960784315, 0.6196078431372549, 0.6274509803921569, 1.0), 'chartreuse': (0.4980392156862745, 1.0, 0.0, 1.0), 'chocolate': (0.8235294117647058, 0.4117647058823529, 0.11764705882352941, 1.0), 'coral': (1.0, 0.4980392156862745, 0.3137254901960784, 1.0), 'cornflowerblue': (0.39215686274509803, 0.5843137254901961, 0.9294117647058824, 1.0), 'cornsilk': (1.0, 0.9725490196078431, 0.8627450980392157, 1.0), 'crimson': (0.8627450980392157, 0.0784313725490196, 0.23529411764705882, 1.0), 'cyan': (0.0, 1.0, 1.0, 1.0), 'darkblue': (0.0, 0.0, 0.5450980392156862, 1.0), 'darkcyan': (0.0, 0.5450980392156862, 0.5450980392156862, 1.0), 'darkgoldenrod': (0.7215686274509804, 0.5254901960784314, 0.043137254901960784, 1.0), 'darkgray': (0.6627450980392157, 0.6627450980392157, 0.6627450980392157, 1.0), 'darkgreen': (0.0, 0.39215686274509803, 0.0, 1.0), 'darkgrey': (0.6627450980392157, 0.6627450980392157, 0.6627450980392157, 1.0), 'darkkhaki': (0.7411764705882353, 0.7176470588235294, 0.4196078431372549, 1.0), 'darkmagenta': (0.5450980392156862, 0.0, 0.5450980392156862, 1.0), 'darkolivegreen': (0.3333333333333333, 0.4196078431372549, 0.1843137254901961, 1.0), 'darkorange': (1.0, 0.5490196078431373, 0.0, 1.0), 'darkorchid': (0.6, 0.19607843137254902, 0.8, 1.0), 'darkred': (0.5450980392156862, 0.0, 0.0, 1.0), 'darksalmon': (0.9137254901960784, 0.5882352941176471, 0.47843137254901963, 1.0), 'darkseagreen': (0.5607843137254902, 0.7372549019607844, 0.5607843137254902, 1.0), 'darkslateblue': (0.2823529411764706, 0.23921568627450981, 0.5450980392156862, 1.0), 'darkslategray': (0.1843137254901961, 0.30980392156862746, 0.30980392156862746, 1.0), 'darkslategrey': (0.1843137254901961, 0.30980392156862746, 0.30980392156862746, 1.0), 'darkturquoise': (0.0, 0.807843137254902, 0.8196078431372549, 1.0), 'darkviolet': (0.5803921568627451, 0.0, 0.8274509803921568, 1.0), 'deeppink': (1.0, 0.0784313725490196, 0.5764705882352941, 1.0), 'deepskyblue': (0.0, 0.7490196078431373, 1.0, 1.0), 'dimgray': (0.4117647058823529, 0.4117647058823529, 0.4117647058823529, 1.0), 'dimgrey': (0.4117647058823529, 0.4117647058823529, 0.4117647058823529, 1.0), 'dodgerblue': (0.11764705882352941, 0.5647058823529412, 1.0, 1.0), 'firebrick': (0.6980392156862745, 0.13333333333333333, 0.13333333333333333, 1.0), 'floralwhite': (1.0, 0.9803921568627451, 0.9411764705882353, 1.0), 'forestgreen': (0.13333333333333333, 0.5450980392156862, 0.13333333333333333, 1.0), 'fuchsia': (1.0, 0.0, 1.0, 1.0), 'gainsboro': (0.8627450980392157, 0.8627450980392157, 0.8627450980392157, 1.0), 'ghostwhite': (0.9725490196078431, 0.9725490196078431, 1.0, 1.0), 'gold': (1.0, 0.8431372549019608, 0.0, 1.0), 'goldenrod': (0.8549019607843137, 0.6470588235294118, 0.12549019607843137, 1.0), 'gray': (0.5019607843137255, 0.5019607843137255, 0.5019607843137255, 1.0), 'green': (0.0, 0.5019607843137255, 0.0, 1.0), 'greenyellow': (0.6784313725490196, 1.0, 0.1843137254901961, 1.0), 'grey': (0.5019607843137255, 0.5019607843137255, 0.5019607843137255, 1.0), 'honeydew': (0.9411764705882353, 1.0, 0.9411764705882353, 1.0), 'hotpink': (1.0, 0.4117647058823529, 0.7058823529411765, 1.0), 'indianred': (0.803921568627451, 0.3607843137254902, 0.3607843137254902, 1.0), 'indigo': (0.29411764705882354, 0.0, 0.5098039215686274, 1.0), 'ivory': (1.0, 1.0, 0.9411764705882353, 1.0), 'khaki': (0.9411764705882353, 0.9019607843137255, 0.5490196078431373, 1.0), 'lavender': (0.9019607843137255, 0.9019607843137255, 0.9803921568627451, 1.0), 'lavenderblush': (1.0, 0.9411764705882353, 0.9607843137254902, 1.0), 'lawngreen': (0.48627450980392156, 0.9882352941176471, 0.0, 1.0), 'lemonchiffon': (1.0, 0.9803921568627451, 0.803921568627451, 1.0), 'lightblue': (0.6784313725490196, 0.8470588235294118, 0.9019607843137255, 1.0), 'lightcoral': (0.9411764705882353, 0.5019607843137255, 0.5019607843137255, 1.0), 'lightcyan': (0.8784313725490196, 1.0, 1.0, 1.0), 'lightgoldenrodyellow': (0.9803921568627451, 0.9803921568627451, 0.8235294117647058, 1.0), 'lightgray': (0.8274509803921568, 0.8274509803921568, 0.8274509803921568, 1.0), 'lightgreen': (0.5647058823529412, 0.9333333333333333, 0.5647058823529412, 1.0), 'lightgrey': (
    0.8274509803921568, 0.8274509803921568, 0.8274509803921568, 1.0), 'lightpink': (1.0, 0.7137254901960784, 0.7568627450980392, 1.0), 'lightsalmon': (1.0, 0.6274509803921569, 0.47843137254901963, 1.0), 'lightseagreen': (0.12549019607843137, 0.6980392156862745, 0.6666666666666666, 1.0), 'lightskyblue': (0.5294117647058824, 0.807843137254902, 0.9803921568627451, 1.0), 'lightslategray': (0.4666666666666667, 0.5333333333333333, 0.6, 1.0), 'lightslategrey': (0.4666666666666667, 0.5333333333333333, 0.6, 1.0), 'lightsteelblue': (0.6901960784313725, 0.7686274509803922, 0.8705882352941177, 1.0), 'lightyellow': (1.0, 1.0, 0.8784313725490196, 1.0), 'lime': (0.0, 1.0, 0.0, 1.0), 'limegreen': (0.19607843137254902, 0.803921568627451, 0.19607843137254902, 1.0), 'linen': (0.9803921568627451, 0.9411764705882353, 0.9019607843137255, 1.0), 'magenta': (1.0, 0.0, 1.0, 1.0), 'maroon': (0.5019607843137255, 0.0, 0.0, 1.0), 'mediumaquamarine': (0.4, 0.803921568627451, 0.6666666666666666, 1.0), 'mediumblue': (0.0, 0.0, 0.803921568627451, 1.0), 'mediumorchid': (0.7294117647058823, 0.3333333333333333, 0.8274509803921568, 1.0), 'mediumpurple': (0.5764705882352941, 0.4392156862745098, 0.8588235294117647, 1.0), 'mediumseagreen': (0.23529411764705882, 0.7019607843137254, 0.44313725490196076, 1.0), 'mediumslateblue': (0.4823529411764706, 0.40784313725490196, 0.9333333333333333, 1.0), 'mediumspringgreen': (0.0, 0.9803921568627451, 0.6039215686274509, 1.0), 'mediumturquoise': (0.2823529411764706, 0.8196078431372549, 0.8, 1.0), 'mediumvioletred': (0.7803921568627451, 0.08235294117647059, 0.5215686274509804, 1.0), 'midnightblue': (0.09803921568627451, 0.09803921568627451, 0.4392156862745098, 1.0), 'mintcream': (0.9607843137254902, 1.0, 0.9803921568627451, 1.0), 'mistyrose': (1.0, 0.8941176470588236, 0.8823529411764706, 1.0), 'moccasin': (1.0, 0.8941176470588236, 0.7098039215686275, 1.0), 'navajowhite': (1.0, 0.8705882352941177, 0.6784313725490196, 1.0), 'navy': (0.0, 0.0, 0.5019607843137255, 1.0), 'oldlace': (0.9921568627450981, 0.9607843137254902, 0.9019607843137255, 1.0), 'olive': (0.5019607843137255, 0.5019607843137255, 0.0, 1.0), 'olivedrab': (0.4196078431372549, 0.5568627450980392, 0.13725490196078433, 1.0), 'orange': (1.0, 0.6470588235294118, 0.0, 1.0), 'orangered': (1.0, 0.27058823529411763, 0.0, 1.0), 'orchid': (0.8549019607843137, 0.4392156862745098, 0.8392156862745098, 1.0), 'palegoldenrod': (0.9333333333333333, 0.9098039215686274, 0.6666666666666666, 1.0), 'palegreen': (0.596078431372549, 0.984313725490196, 0.596078431372549, 1.0), 'paleturquoise': (0.6862745098039216, 0.9333333333333333, 0.9333333333333333, 1.0), 'palevioletred': (0.8588235294117647, 0.4392156862745098, 0.5764705882352941, 1.0), 'papayawhip': (1.0, 0.9372549019607843, 0.8352941176470589, 1.0), 'peachpuff': (1.0, 0.8549019607843137, 0.7254901960784313, 1.0), 'peru': (0.803921568627451, 0.5215686274509804, 0.24705882352941178, 1.0), 'pink': (1.0, 0.7529411764705882, 0.796078431372549, 1.0), 'plum': (0.8666666666666667, 0.6274509803921569, 0.8666666666666667, 1.0), 'powderblue': (0.6901960784313725, 0.8784313725490196, 0.9019607843137255, 1.0), 'purple': (0.5019607843137255, 0.0, 0.5019607843137255, 1.0), 'rebeccapurple': (0.4, 0.2, 0.6, 1.0), 'red': (1.0, 0.0, 0.0, 1.0), 'rosybrown': (0.7372549019607844, 0.5607843137254902, 0.5607843137254902, 1.0), 'royalblue': (0.2549019607843137, 0.4117647058823529, 0.8823529411764706, 1.0), 'saddlebrown': (0.5450980392156862, 0.27058823529411763, 0.07450980392156863, 1.0), 'salmon': (0.9803921568627451, 0.5019607843137255, 0.4470588235294118, 1.0), 'sandybrown': (0.9568627450980393, 0.6431372549019608, 0.3764705882352941, 1.0), 'seagreen': (0.1803921568627451, 0.5450980392156862, 0.3411764705882353, 1.0), 'seashell': (1.0, 0.9607843137254902, 0.9333333333333333, 1.0), 'sienna': (0.6274509803921569, 0.3215686274509804, 0.17647058823529413, 1.0), 'silver': (0.7529411764705882, 0.7529411764705882, 0.7529411764705882, 1.0), 'skyblue': (0.5294117647058824, 0.807843137254902, 0.9215686274509803, 1.0), 'slateblue': (0.41568627450980394, 0.35294117647058826, 0.803921568627451, 1.0), 'slategray': (0.4392156862745098, 0.5019607843137255, 0.5647058823529412, 1.0), 'slategrey': (0.4392156862745098, 0.5019607843137255, 0.5647058823529412, 1.0), 'snow': (1.0, 0.9803921568627451, 0.9803921568627451, 1.0), 'springgreen': (0.0, 1.0, 0.4980392156862745, 1.0), 'steelblue': (0.27450980392156865, 0.5098039215686274, 0.7058823529411765, 1.0), 'tan': (0.8235294117647058, 0.7058823529411765, 0.5490196078431373, 1.0), 'teal': (0.0, 0.5019607843137255, 0.5019607843137255, 1.0), 'thistle': (0.8470588235294118, 0.7490196078431373, 0.8470588235294118, 1.0), 'tomato': (1.0, 0.38823529411764707, 0.2784313725490196, 1.0), 'turquoise': (0.25098039215686274, 0.8784313725490196, 0.8156862745098039, 1.0), 'violet': (0.9333333333333333, 0.5098039215686274, 0.9333333333333333, 1.0), 'wheat': (0.9607843137254902, 0.8705882352941177, 0.7019607843137254, 1.0), 'white': (1.0, 1.0, 1.0, 1.0), 'whitesmoke': (0.9607843137254902, 0.9607843137254902, 0.9607843137254902, 1.0), 'yellow': (1.0, 1.0, 0.0, 1.0), 'yellowgreen': (0.6039215686274509, 0.803921568627451, 0.19607843137254902, 1.0)}
colors=Colors
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


import os
import re
from pathlib import Path

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