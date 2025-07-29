import sys
import os

kvw = sys.modules[__name__]
import re
from . import kvBehaviors as kvb
# from .utils import *
from . import utils
from .utils import colors,abc,resolve_color,pos_hints

def __getattr__(name):
    match name:
        case 'kvInput':
            return utils.TextInput
        case 'Camera':
            return utils.Camera
        case 'DropDownB':
#             Builder.load_string("""
# <DropDownB>:
#     bcolor: 0, 0, 0, 0
#     lcolor: 1, 1, 1, 0
#     lwidth: 1
#     canvas.before:
#         Color:
#             rgba: self.bcolor
#         Rectangle:
#             pos: self.pos
#             size: self.size

#         Color:
#             rgba: self.lcolor
#         Line:
#             width: self.lwidth
#             rectangle: (self.x, self.y, self.width, self.height)""")

#             class DropDownB(utils.DropDown):
#                 bcolor = ListProperty([0, 0, 0, 0])
#                 lcolor = ListProperty([1, 1, 1, 0])
#                 lwidth = NumericProperty(1)
#                 # pos_hint = ObjectProperty({'center_x':0.5,'center_y':0.5,})
#                 pass
#             return DropDownB
            class DropDownB(BgLine,utils.DropDown):
                pass
            return DropDownB
        case _:
            raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


from .utils import CaseInsensitiveDict

import traceback
import copy

from kivy.lang import Builder
from .kvBehaviors import TouchBehavior
from kivy.uix.recycleview import RecycleView
from kivy.uix.progressbar import ProgressBar
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.behaviors.focus import FocusBehavior
from kivy.uix.scatter import Scatter

from kivy.uix.pagelayout import PageLayout
# sys.exit()
# from kivy.uix.spinner import SpinnerOption

from kivy.uix.scrollview import ScrollView

from kivy.properties import BooleanProperty,NumericProperty,StringProperty,ListProperty,ObjectProperty,BoundedNumericProperty,OptionProperty,AliasProperty,VariableListProperty, Property
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.behaviors import FocusBehavior

class ColorProperty(Property):
    """Custom property for handling colors as RGBA lists"""
    
    def __init__(self, defaultvalue=None, **kwargs):
        if defaultvalue == None:
            defaultvalue = [1, 1, 1, 1]  # default white
        super().__init__(defaultvalue, **kwargs)
    
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


from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.stacklayout import StackLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.behaviors import ButtonBehavior, ToggleButtonBehavior, TouchRippleButtonBehavior,TouchRippleBehavior

from kivy.graphics import Ellipse,Color,Rectangle,Line,RoundedRectangle,SmoothRoundedRectangle,SmoothLine

# print('hell'*50)
from kivy.uix.label import Label as _Label

# print('hell'*50)

# from kivy.uix.textinput import TextInput as kvInput
# from .modkvWidgets import TextInput as kvInput
# print('hell'*50)


from kivy.uix.button import Button as kvButton
from kivy.uix.togglebutton import ToggleButton as kvToggleButton

from kivy.uix.gridlayout import GridLayout

from kivy.uix.tabbedpanel import TabbedPanel,TabbedPanelItem
# print('hell'*50)

# from kivy.uix.spinner import Spinner as _Spinner
# sys.exit()
from kivy.uix.screenmanager import ScreenManager, Screen
# print('hell'*50)

from kivy.clock import Clock

from kivy.uix.widget import Widget
from kivy.uix.checkbox import CheckBox
# from kivy.metrics import dp





class Button(kvButton):
    # def _get_background_color_down(self):
    #     rgba=self.bcolor_normal
    #     return [r,g,b,a*.5]
    # def _set_background_color_down(self,val):
    #     self.background_color=resolve_color(val)
    bcolor_down=ColorProperty([1,1,1, 1])
    # bcolor_down=AliasProperty(_get_background_color_down,_set_background_color_down)
    bcolor_normal = ColorProperty([1,1,1,1])
    # bcolor=AliasProperty(_get_background_color,_set_background_color,bind=['background_color'])
    bcolor=ColorProperty([1,1,1,1])
    # def _set_background_color_down(self,ins,bcolor_normal):
    #     r,g,b,a=bcolor_normal
    #     self.bcolor_down=[r,g,b,1]
    def __init__(self,**kwargs):
        # self.bind(bcolor_normal=self.setter('background_color'))
        # self.bind(bcolor_normal=self._set_background_color_down)
        self.bind(bcolor=self.setter('background_color'))
        super(Button,self).__init__(**kwargs)
        # self.bcolor_normal
        self.bcolor=self.bcolor_normal

        
    
class ToggleButtonB(kvToggleButton):
    def _get_background_color(self):
        return self.background_color
    def _set_background_color(self,val):
        self.background_color=val
    bcolor=AliasProperty(_get_background_color,_set_background_color,bind=['background_color'],cache=True)


class ScrollbarMirror(Widget):
    """
    A custom widget that mirrors the vertical scrollbar of a ScrollView.
    - Shows a draggable rectangle representing the visible portion
    - Updates when ScrollView scrolls
    - Allows dragging to control ScrollView position
    """
    
    scroll_view = ObjectProperty(None)
    bar_width = NumericProperty(20)
    handle_color = ColorProperty([161/255,161/255,161/255, 1])
    bar_color = ColorProperty([31/255, 31/255, 31/255, 1])
    min_handle_height = NumericProperty(30)
    
    def __init__(self, scroll_view=None, **kwargs):
        super(ScrollbarMirror, self).__init__(**kwargs)
    def connect_to(self,scroll_view):
        self._updating = False
        self._touch_down = False
        self._handle_pos = 0
        self._handle_height = 0
        
        self.bind(
            size=self._update_graphics,
            pos=self._update_graphics
        )
        
        with self.canvas:
            self.bar_color_obj = Color(*self.bar_color)
            self.bar_rect = Rectangle()
            self.handle_color_obj = Color(*self.handle_color)
            self.handle_rect = Rectangle()
        
        if scroll_view:
            self.set_scroll_view(scroll_view)
    
    def set_scroll_view(self, scroll_view):
        """Set the ScrollView to mirror"""
        if self.scroll_view:
            self.scroll_view.unbind(
                scroll_y=self._update_from_scroll,
                size=self._update_graphics,
                scroll_pos=self._update_from_scroll
            )
        
        self.scroll_view = scroll_view
        
        if scroll_view:
            scroll_view.bind(
                scroll_y=self._update_from_scroll,
                size=self._update_graphics
            )
            
            if hasattr(scroll_view, 'content'):
                scroll_view.content.bind(
                    size=self._update_graphics,
                    pos=self._update_graphics
                )
            else:
                scroll_view.content=scroll_view.children[0]
                scroll_view.content.bind(
                    size=self._update_graphics,
                    pos=self._update_graphics
                )
        
        self._update_graphics()
    
    def _update_graphics(self, *args):
        """Update the visual representation"""
        if not self.scroll_view or not self.scroll_view.children:
            return
            
        # Update background bar
        self.bar_rect.pos = self.pos
        self.bar_rect.size = (self.bar_width, self.height)
        
        # Calculate handle position and size
        content = self.scroll_view.content
        viewport_height = self.scroll_view.height
        content_height = content.height
        
        if content_height <= viewport_height:
            # All content is visible
            self.handle_rect.size = (self.bar_width, self.height)
            self.handle_rect.pos = self.pos
            return
        
        # Calculate handle height based on viewport ratio
        ratio = viewport_height / content_height
        self._handle_height = max(self.min_handle_height, self.height * ratio)
        
        # Calculate handle position based on scroll position
        scroll_y = self.scroll_view.scroll_y
        available_space = self.height - self._handle_height
        self._handle_pos = ( scroll_y) * available_space
        
        # Update handle rectangle
        self.handle_rect.pos = (self.x, self.y + self._handle_pos)
        self.handle_rect.size = (self.bar_width, self._handle_height)
    
    def _update_from_scroll(self, *args):
        """Update handle position when ScrollView scrolls"""
        if self._updating or self._touch_down:
            self._update_graphics()
            return
            
        self._updating = True
        self._update_graphics()
        self._updating = False
    
    def on_touch_down(self, touch):
        """Handle touch events on the mirror scrollbar"""
        if not self.collide_point(*touch.pos) or not self.scroll_view:
            return super(ScrollbarMirror, self).on_touch_down(touch)
            
        if hasattr(self.scroll_view, 'content'):
            content = self.scroll_view.content
            viewport_height = self.scroll_view.height
            content_height = content.height
            
            if content_height <= viewport_height:
                return True
                
            # Check if touch is on the handle
            handle_top = self.y + self._handle_pos + self._handle_height
            handle_bottom = self.y + self._handle_pos
            
            if touch.y <= handle_top and touch.y >= handle_bottom:
                # Touched the handle - prepare for drag
                self._touch_down = True
                self._touch_offset = touch.y - (self.y + self._handle_pos)
                return True
            else:
                # Jump to clicked position
                self._updating = True
                new_pos = (touch.y - self.y) / self.height
                self.scroll_view.scroll_y = new_pos
                self._updating = False
                return True
                
        return super(ScrollbarMirror, self).on_touch_down(touch)
    
    def on_touch_move(self, touch):
        """Handle dragging the scrollbar handle"""
        try:
            if not self._touch_down or not self.scroll_view:
                return super(ScrollbarMirror, self).on_touch_move(touch)
        except:
            pass
            
        if hasattr(self.scroll_view, 'content'):
            content = self.scroll_view.content
            viewport_height = self.scroll_view.height
            content_height = content.height
            
            if content_height > viewport_height:
                self._updating = True
                
                # Calculate new position
                new_handle_pos = touch.y - self.y - self._touch_offset
                available_space = self.height - self._handle_height
                normalized = max(0, min(1, new_handle_pos / available_space))
                
                # Update ScrollView position
                self.scroll_view.scroll_y = normalized
                self._updating = False
                self._update_graphics()
                return True
                
        return super(ScrollbarMirror, self).on_touch_move(touch)
    
    def on_touch_up(self, touch):
        """Handle touch release"""
        self._touch_down = False
        return super(ScrollbarMirror, self).on_touch_up(touch)
    
    # def on_bar_color(self, instance, value):
    #     """Update bar color"""
    #     self.bar_color_obj.rgba = value
    
    # def on_handle_color(self, instance, value):
    #     """Update handle color"""
    #     self.handle_color_obj.rgba = value


Builder.load_string("""
<LabelA>:
    bcolor: 0, 0, 0, 0
    lcolor: 1, 1, 1, 0
    lwidth: 1
    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size

        Color:
            rgba: self.lcolor
        Line:
            width: self.lwidth
            rectangle: (self.x, self.y, self.width, self.height)
""")

class LabelA(_Label):
    bcolor = ColorProperty([0, 0, 0, 0])
    lcolor = ColorProperty([1, 1, 1, 0])
    lwidth=NumericProperty(1)
    # pos_hint = ObjectProperty({'center_x':0.5,'center_y':0.5,})
    pass



# Builder.load_string("""
# <LabelB>:
#     bcolor: 0, 0, 0, 0
#     lcolor: 1, 1, 1, 0
#     lwidth: 1
#     text_size: self.size
#     canvas.before:
#         Color:
#             rgba: self.bcolor
#         Rectangle:
#             pos: self.pos
#             size: self.size

#         Color:
#             rgba: self.lcolor
#         Line:
#             width: self.lwidth
#             rectangle: (self.x, self.y, self.width, self.height)
# """)

# class LabelB(_Label):
#     bcolor = ListProperty([0, 0, 0, 0])
#     lcolor = ListProperty([1, 1, 1, 0])
#     lwidth=NumericProperty(1)
#     # pos_hint = ObjectProperty({'center_x':0.5,'center_y':0.5,})
#     pass


class BgLine(object):
    # _bcolor=[0, 0, 0, 0]
    bcolor=ColorProperty([0, 0, 0, 0])
    

    # def _get_bcolor(self):
    #     return self._bcolor
    # def _set_bcolor(self,v):
    #     self._bcolor=resolve_color(v)
    #     return True

    # _lcolor=[1,1,1,0]
    # def _get_lcolor(self):
    #     return self._lcolor
    # def _set_lcolor(self,v):
    #     self._lcolor=resolve_color(v)
    #     return True
    lcolor=ColorProperty([1,1,1,0])

    # bcolor = AliasProperty(_get_bcolor,_set_bcolor)  # background color
    # lcolor = AliasProperty(_get_lcolor,_set_lcolor)  # line color
    lwidth = NumericProperty(1)          # line width

    # bcolor = ListProperty([0, 0, 0, 0])  # background color
    # lcolor = ListProperty([1, 1, 1, 0])  # line color
    # lwidth = NumericProperty(1)          # line width
    
    def __init__(self, **kwargs):
        # kwargs['bcolor']=resolve_color(kwargs.get('bcolor',self.bcolor))
        # kwargs['lcolor']=resolve_color(kwargs.get('lcolor',self.lcolor))
        super(BgLine, self).__init__(**kwargs)
        Clock.schedule_once(self._init)
    def _init(self,dt):
        # Initial canvas setup
        with self.canvas.before:
            self.bg_color = Color(rgba= resolve_color( self.bcolor ))
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        with self.canvas.after:
            # print(resolve_color(self.lcolor))
            self.line_color = Color(rgba=self.lcolor)
            self.line = Line(width=self.lwidth, rectangle=(
                self.x, self.y, self.width, self.height
            ))
        
        # Bind properties to update visuals
        self.bind(
            pos=self._update_canvas,
            size=self._update_canvas,
            bcolor=self._update_bcolor,
            lcolor=self._update_lcolor,
            lwidth=self._update_lwidth
        )
    
    def _update_canvas(self, *args):
        """Update the canvas elements when position or size changes"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.line.rectangle = (self.x, self.y, self.width, self.height)
        self.text_size = self.size
    
    def _update_bcolor(self, instance, value):
        """Update background color"""
        # print("""Update background color""",value)
        # self.bg_color.rgba = resolve_color( value)
        self.bg_color.rgba = value
        

    
    def _update_lcolor(self, instance, value):
        """Update line color"""
        # self.line_color.rgba = resolve_color( value)
        self.line_color.rgba = value
    
    def _update_lwidth(self, instance, value):
        """Update line width"""
        self.line.width = value


class BgLineState(object):
    # _bcolor=[0, 0, 0, 0]
    # _lcolor=[1,1,1,0]
    # _bcolor_normal = [0, 0, 0, 0]
    # _bcolor_down = [.2, .64, .8, 1]

    bcolor=ColorProperty([0, 0, 0, 0])
    lcolor=ColorProperty([1,1,1,0])
    bcolor_normal = ColorProperty([0, 0, 0, 0])
    bcolor_down = ColorProperty([.2, .64, .8, 0])

    # def _get_bcolor(self):
    #     return self._bcolor
    # def _set_bcolor(self,v):
    #     self._bcolor=resolve_color(v)
    #     return True
    # def _get_bcolor_down(self):
    #     return self._bcolor
    # def _set_bcolor_down(self,v):
    #     self._bcolor_down=resolve_color(v)
    #     return True
    # def _get_bcolor_normal(self):
    #     return self._bcolor_normal
    # def _set_bcolor_normal(self,v):
    #     self._bcolor_normal=resolve_color(v)
    #     return True
        
    # def _get_lcolor(self):
    #     return self._lcolor
    # def _set_lcolor(self,v):
    #     self._lcolor=resolve_color(v)
    #     return True

    # bcolor = AliasProperty(_get_bcolor,_set_bcolor)  # background color
    # bcolor_down = AliasProperty(_get_bcolor_down,_set_bcolor_down)  # background color
    # bcolor_normal = AliasProperty(_get_bcolor_normal,_set_bcolor_normal)  # background color
    # lcolor = AliasProperty(_get_lcolor,_set_lcolor)  # line color
    lwidth = NumericProperty(1)          # line width

    # bcolor = ListProperty([0, 0, 0, 0])  # background color
    # lcolor = ListProperty([1, 1, 1, 0])  # line color
    # lwidth = NumericProperty(1)          # line width

    state=OptionProperty('normal',options=('normal','down'))
    def on_state(self,instance, value):
        # print(value,self.bcolor_normal,self.bcolor_down)
        if value == 'down':
            self.bcolor=self.bcolor_down
        else:
            self.bcolor=self.bcolor_normal
    
    def __init__(self, **kwargs):
        # kwargs['bcolor']=resolve_color(kwargs.get('bcolor',self.bcolor))
        # kwargs['lcolor']=resolve_color(kwargs.get('lcolor',self.lcolor))
        super(BgLineState, self).__init__(**kwargs)
        # Clock.schedule_once(self._init)
    # def _init(self,dt):
        # Initial canvas setup
        with self.canvas.before:
            self.bg_color = Color(rgba= resolve_color( self.bcolor ))
            self.bg_rect = Rectangle(pos=self.pos, size=self.size)
        with self.canvas.after:
            self.line_color = Color(rgba=resolve_color( self.lcolor))
            self.line = Line(width=self.lwidth, rectangle=(
                self.x, self.y, self.width, self.height
            ))
        
        # Bind properties to update visuals
        self.bind(
            pos=self._update_canvas,
            size=self._update_canvas,
            bcolor=self._update_bcolor,
            lcolor=self._update_lcolor,
            lwidth=self._update_lwidth
        )
    
    def _update_canvas(self, *args):
        """Update the canvas elements when position or size changes"""
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size
        self.line.rectangle = (self.x, self.y, self.width, self.height)
        self.text_size = self.size
    
    def _update_bcolor(self, instance, value):
        """Update background color"""
        # print("""Update background color""",value)
        # self.bg_color.rgba = resolve_color( value)
        self.bg_color.rgba = value
        

    
    def _update_lcolor(self, instance, value):
        """Update line color"""
        # self.line_color.rgba = resolve_color( value)
        self.line_color.rgba = value
    
    def _update_lwidth(self, instance, value):
        """Update line width"""
        self.line.width = value


class RoundBgLineState(object):
    r=NumericProperty(8)
    segments=NumericProperty(30)
    lwidth=NumericProperty(1)

    lcolor=ColorProperty([.345, .345, .345,1])
    bcolor=ColorProperty([.345, .345, .345, 0])
    bcolor_normal = ColorProperty([.345, .345, .345, 1])
    bcolor_down = ColorProperty([.2, .64, .8, 1])

    # _bcolor=[.345, .345, .345, 0]
    # _lcolor=[.345, .345, .345,1]
    # _bcolor_normal = [.345, .345, .345, 1]
    # _bcolor_down = [.2, .64, .8, 1]

    # def _get_bcolor(self):
    #     return self._bcolor
    # def _set_bcolor(self,v):
    #     self._bcolor=resolve_color(v)
    #     return True
    # def _get_bcolor_down(self):
    #     return self._bcolor_down
    # def _set_bcolor_down(self,v):
    #     self._bcolor_down=resolve_color(v)
    #     return True
    # def _get_bcolor_normal(self):
    #     return self._bcolor_normal
    # def _set_bcolor_normal(self,v):
    #     self._bcolor_normal=resolve_color(v)
    #     return True
        
    # def _get_lcolor(self):
    #     return self._lcolor
    # def _set_lcolor(self,v):
    #     self._lcolor=resolve_color(v)
    #     return True

    # bcolor = AliasProperty(_get_bcolor,_set_bcolor,cache=True)  # background color
    # bcolor_down = AliasProperty(_get_bcolor_down,_set_bcolor_down,cache=True)  # background color
    # bcolor_normal = AliasProperty(_get_bcolor_normal,_set_bcolor_normal,cache=True)  # background color
    # lcolor = AliasProperty(_get_lcolor,_set_lcolor,cache=True)  # line color
    state=OptionProperty('normal',options=('normal','down'))
    def on_state(self,instance, value):
        # print(value,self.bcolor_normal,self.bcolor_down)
        if value == 'down':
            self.bcolor=self.bcolor_down
        else:
            self.bcolor=self.bcolor_normal

    def __init__(self,**kwargs):
        # print(kwargs)
        # kwargs['bcolor']=resolve_color(kwargs.get('bcolor',self.bcolor))
        # kwargs['bcolor_normal']=resolve_color(kwargs.get('bcolor_normal',self.bcolor_normal))
        # kwargs['bcolor_down']=resolve_color(kwargs.get('bcolor_down',self.bcolor_down))
        # kwargs['lcolor']=resolve_color(kwargs.get('lcolor',self.lcolor))
        kwargs['state']=kwargs.get('state',self.state)

        super(RoundBgLineState,self).__init__(**kwargs)

        # with self.canvas.before:
        #     # kwargs['bcolor']=resolve_color(kwargs.get('bcolor',self.bcolor))
        #     self.bg_color=Color(rgba=self.bcolor)
        #     self.bg_rect = SmoothRoundedRectangle(
        #         pos=self.pos,
        #         size=self.size,
        #         radius=[(self.r, self.r)]*4,
        #     )
        # self.bind(pos=lambda obj, pos: setattr(self.bg_rect, "pos", pos))
        # self.bind(size=lambda obj, size: setattr(self.bg_rect, "size", size))
        # Clock.schedule_once(self._create)
    # def _create(self,dt):
        with self.canvas.before:
            self.bg_color=Color(rgba=self.bcolor)
            self.bg_rect = SmoothRoundedRectangle(
                # pos=self.pos,
                size=self.size,
                pos_hint=pos_hints.center,
                radius=[(self.r, self.r)]*4,
                segments=self.segments,
            )
        with self.canvas.after:
            self.line_color = Color(rgba=self.lcolor)
            self.line = SmoothLine(
                size=self.size,
                width=self.lwidth,
                pos_hint=pos_hints.center,
                rounded_rectangle=(
                self.x, self.y, self.width, self.height, self.r, self.r, self.r, self.r, self.segments
                )
                )

        # Bind properties to update visuals
        self.bind(
            pos=self._update_canvas,
            size=self._update_canvas,
            bcolor=self._update_bcolor,
            lcolor=self._update_lcolor,
            lwidth=self._update_lwidth
        )
        Clock.schedule_once(lambda dt:self.on_state(self,self.state))
    
    def _update_canvas(self, *args):
        """Update the canvas elements when position or size changes"""
        # self.bg_rect.pos=self.pos
        # self.bg_rect.pos = (self.pos[0]-self.r/2,self.pos[1]-self.r/2)
        self.bg_rect.size = self.size
        self.bg_rect.segments = self.segments
        self.line.rounded_rectangle=(
                # self.x, self.y+self.height,
                # self.x+self.width, self.y+self.width,
                # self.x+self.width, self.y,
                # self.x, self.y,

                # 1
                # 0,0,0,100,100,100,100,0,
                # 10
                self.x, self.y, self.width, self.height, self.r, self.r, self.r, self.r, self.segments

                )
        # self.text_size = self.size

    def _update_bcolor(self, instance, value):
        """Update background color"""
        # print("""Update background color""",value)
        # self.bg_color.rgba = resolve_color( value)
        self.bg_color.rgba = value
        

    
    def _update_lcolor(self, instance, value):
        """Update line color"""
        # self.line_color.rgba = resolve_color( value)
        self.line_color.rgba = value
    
    def _update_lwidth(self, instance, value):
        """Update line width"""
        self.line.width = value
    

class RoundBgLine(object):
    r=NumericProperty(8)
    segments=NumericProperty(30)
    lwidth=NumericProperty(1)

    # _bcolor=[.345, .345, .345, 0]
    # _lcolor=[.345, .345, .345,1]
    bcolor=ColorProperty([.345, .345, .345, 0])
    lcolor=ColorProperty([.345, .345, .345,1])

    # def _get_bcolor(self):
    #     return self._bcolor
    # def _set_bcolor(self,v):
    #     self._bcolor=resolve_color(v)
    #     return True
    # def _get_bcolor_down(self):
    #     return self._bcolor
    # def _set_bcolor_down(self,v):
    #     self._bcolor_down=resolve_color(v)
    #     return True
    # def _get_bcolor_normal(self):
    #     return self._bcolor_normal
    # def _set_bcolor_normal(self,v):
    #     self._bcolor_normal=resolve_color(v)
    #     return True
        
    # def _get_lcolor(self):
    #     return self._lcolor
    # def _set_lcolor(self,v):
    #     self._lcolor=resolve_color(v)
    #     return True

    # bcolor = AliasProperty(_get_bcolor,_set_bcolor)  # background color
    # bcolor_down = AliasProperty(_get_bcolor_down,_set_bcolor_down)  # background color
    # bcolor_normal = AliasProperty(_get_bcolor_normal,_set_bcolor_normal)  # background color
    # lcolor = AliasProperty(_get_lcolor,_set_lcolor)  # line color


    def __init__(self,**kwargs):
        # kwargs['bcolor']=resolve_color(kwargs.get('bcolor',self._bcolor))
        # kwargs['lcolor']=resolve_color(kwargs.get('lcolor',self._lcolor))

        super(RoundBgLine,self).__init__(**kwargs)

        # with self.canvas.before:
        #     # kwargs['bcolor']=resolve_color(kwargs.get('bcolor',self.bcolor))
        #     self.bg_color=Color(rgba=self.bcolor)
        #     self.bg_rect = SmoothRoundedRectangle(
        #         pos=self.pos,
        #         size=self.size,
        #         radius=[(self.r, self.r)]*4,
        #     )
        # self.bind(pos=lambda obj, pos: setattr(self.bg_rect, "pos", pos))
        # self.bind(size=lambda obj, size: setattr(self.bg_rect, "size", size))
        # Clock.schedule_once(self._create)
    # def _create(self,dt):
        with self.canvas.before:
            self.bg_color=Color(rgba=self.bcolor)
            self.bg_rect = SmoothRoundedRectangle(
                # pos=self.pos,
                size=self.size,
                pos_hint=pos_hints.center,
                radius=[(self.r, self.r)]*4,
                segments=self.segments,
            )
        with self.canvas.after:
            self.line_color = Color(rgba=self.lcolor)
            self.line = SmoothLine(
                size=self.size,
                width=self.lwidth,
                pos_hint=pos_hints.center,
                rounded_rectangle=(
                self.x, self.y, self.width, self.height, self.r, self.r, self.r, self.r, self.segments
                )
                )
        
        # Bind properties to update visuals
        self.bind(
            pos=self._update_canvas,
            size=self._update_canvas,
            bcolor=self._update_bcolor,
            lcolor=self._update_lcolor,
            lwidth=self._update_lwidth
        )
    
    def _update_canvas(self, *args):
        """Update the canvas elements when position or size changes"""
        # self.bg_rect.pos=self.pos
        # self.bg_rect.pos = (self.pos[0]-self.r/2,self.pos[1]-self.r/2)
        self.bg_rect.size = self.size
        self.bg_rect.segments = self.segments
        self.line.rounded_rectangle=(
                # self.x, self.y+self.height,
                # self.x+self.width, self.y+self.width,
                # self.x+self.width, self.y,
                # self.x, self.y,

                # 1
                # 0,0,0,100,100,100,100,0,
                # 10
                self.x, self.y, self.width, self.height, self.r, self.r, self.r, self.r, self.segments

                )
        # self.text_size = self.size

    def _update_bcolor(self, instance, value):
        """Update background color"""
        # print("""Update background color""",value)
        # self.bg_color.rgba = resolve_color( value)
        self.bg_color.rgba = value
        

    
    def _update_lcolor(self, instance, value):
        """Update line color"""
        # self.line_color.rgba = resolve_color( value)
        self.line_color.rgba = value
    
    def _update_lwidth(self, instance, value):
        """Update line width"""
        self.line.width = value


Builder.load_string("""
<LabelB>:
    text_size: self.size
""")

class LabelB(_Label,BgLine):
    pass


Builder.load_string("""
<LabelC>:
    bcolor: 0, 0, 0, 0



    lcolor: 1, 1, 1, 0
    lwidth: 1
    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size

        Color:
            rgba: self.lcolor
        Line:
            width: self.lwidth
            rectangle: (self.x, self.y, self.width, self.height)
""")

class LabelC(_Label):
    bcolor = ColorProperty([0, 0, 0, 0])
    lcolor = ColorProperty([1, 1, 1, 0])
    lwidth=NumericProperty(1)
    pass


class FocusLabelB(kvb.FocusBehavior,kvw.LabelB):
    pass

Builder.load_string("""
<BBoxLayout>:
    bcolor_normal: 0, 0, 0, 0
    bcolor_down: .2, .64, .8, 1
    bcolor: self.bcolor_normal

    lcolor: 1, 1, 1, 0
    lwidth: 1
    
    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size

        Color:
            rgba: self.lcolor
        Line:
            width: self.lwidth
            rectangle: (self.x, self.y, self.width, self.height)
""")


class BBoxLayout(ButtonBehavior,BgLineState,BoxLayout):
    pass
    # bcolor_normal = ListProperty([0, 0, 0, 0])
    # bcolor_down = ListProperty([.2, .64, .8, 1])
    # bcolor = ListProperty([0, 0, 0, 0])
    # lcolor = ListProperty([1, 1, 1, 0])
    # lwidth=NumericProperty(1)

    # # background_down:'atlas://data/images/defaulttheme/button_pressed'
    # def on_state(self,instance, value):
    #     if value == 'down':
    #         self.bcolor=self.bcolor_down
    #     else:
    #         self.bcolor=self.bcolor_normal

# Builder.load_string("""
# <TBBoxLayout>:
#     bcolor_normal: 0, 0, 0, 0
#     bcolor_down: .2, .64, .8, 1
#     bcolor: self.bcolor_normal

#     lcolor: 1, 1, 1, 0
#     lwidth: 1


#     canvas.before:
#         Color:
#             rgba: self.bcolor
#         Rectangle:
#             pos: self.pos
#             size: self.size

#         Color:
#             rgba: self.lcolor
#         Line:
#             width: self.lwidth
#             rectangle: (self.x, self.y, self.width, self.height)
# """)


class TBBoxLayout(kvb.ToggleButtonBehavior2,BgLineState,BoxLayout):
    pass
    # bcolor_normal = ListProperty([0, 0, 0, 0])
    # bcolor_down = ListProperty([.2, .64, .8, 1])
    # bcolor = ListProperty([0, 0, 0, 0])

    # lcolor = ListProperty([1, 1, 1, 0])
    # lwidth=NumericProperty(1)

    # def __init__(self,**kwargs):
    #     self.register_event_type('on_option')
    #     super(TBBoxLayout, self).__init__(**kwargs)
    
    # def __do_press(self):
    #     if (not self.allow_no_selection and
    #             self.group and self.state == 'down'):
    #         return

    #     self._release_group(self)
    #     self.state = 'normal' if self.state == 'down' else 'down'

    # def _do_press(self):
    #     # print(self.last_touch)
    #     if self.last_touch:
    #         if self.last_touch.button=='left':
    #             return self.__do_press()
    #             # if (not self.allow_no_selection and
    #             #         self.group and self.state == 'down'):
    #             #     return
    #             # self._release_group(self)
    #             # self.state = 'normal' if self.state == 'down' else 'down'
    #         if self.last_touch.button=='right':
    #             self.dispatch('on_option')
    #     else:
    #         return self.__do_press()
    #         # if self.state==''
    #         # self.state='normal'
    # def on_option(self):
    #     pass
    # def on_state(self,instance, value):
    #     if value == 'down':
    #         self.bcolor=self.bcolor_down
    #     else:
    #         self.bcolor=self.bcolor_normal

Builder.load_string("""
<SplitterV2>:
    bcolor_normal: 0, 0, 0, 0
    bcolor_down: .2, .64, .8, 1
    bcolor: self.bcolor_normal
    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size
""")


# Builder.load_string('''
# <FlatButton>:
#     ripple_color: 0.8, 0.8, 0.8, 0.5
#     background_color: 0, 0, 0, 0
#     lcolor: 1,1,1,1
#     color: 1,1,1,1
#     lwidth: 1

#     canvas.before:
#         Color:
#             rgba: self.lcolor
#         Line:
#             width: self.lwidth
#             rectangle: (self.x, self.y, self.width, self.height)

#     # Label:
#     #     id: _label
#     #     text: root.text
#     #     halign: root.halign
#     #     text: root.text
#     #     center: root.center
#     #     markup: root.markup
#     #     font_size: root.font_size
# ''')
# class FlatButton(TouchRippleButtonBehavior,BgLineState, kvButton):
#     halign=OptionProperty('center',options=('auto','left','center','right','justify'))
#     valign=OptionProperty('middle',options=('bottom','middle','center','top'))
#     text=StringProperty()
#     font_size=NumericProperty(15)
#     markup=BooleanProperty(False)
#     # halign=StringProperty('center')

#     def __init__(self, **kwargs):
        
#         # self.primary_color= primary_color
#         super(FlatButton, self).__init__(**kwargs)
    
#     def on_press(self):
#         touch=self.last_touch
#         collide_point = self.collide_point(touch.x, touch.y)
#         if collide_point:
#             # touch.grab(self)
#             self.ripple_show(touch)
#             return True
#         return False
#     def on_release(self):
#         touch=self.last_touch
#         if touch.grab_current is self:
#             # touch.ungrab(self)
#             self.ripple_fade()
#             return True
#         return False

Builder.load_string("""
<FlatButtonTouch>:
    bcolor_normal: self.bcolor_normal
    bcolor_down: self.bcolor_down
    bcolor: self.bcolor_normal
    ripple_color: self.bcolor_down
    background_color: self.bcolor
    lcolor: self.lcolor
    lwidth: self.lwidth
    text_color: self.text_color


    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: self.lcolor
        Line:
            width: self.lwidth
            rectangle: (self.x, self.y, self.width, self.height)

    Label:
        id: _label
        text: root.text
        color: root.text_color
        center: root.center
        markup: root.markup
        halign: root.halign
        valign: root.valign
        shorten: root.shorten
        font_name: root.font_name
        shorten_from: root.shorten_from
        line_height: root.line_height
        text_size: root.size
        font_size: root.font_size


""")


class FlatButtonTouch(TouchRippleButtonBehavior,BoxLayout):
    bcolor_normal = ListProperty([.345, .345, .345, 1])
    
    bcolor_down = ListProperty([.2, .64, .8, 1])
    bcolor = ListProperty([.345, .345, .345, 1])
    # background_color=bcolor
    
    valign=OptionProperty('middle',options=('bottom','middle','center','top'))
    shorten=BooleanProperty(False)
    shorten_from=OptionProperty('center',options=('left','center','right'))
    line_height=NumericProperty(1.0)
    font_name=StringProperty('Roboto')

    text=StringProperty()
    font_size=NumericProperty(15)
    markup=BooleanProperty(False)
    halign=OptionProperty('center',options=('auto','left','center','right','justify'))
    

    text_color=ListProperty([1, 1, 1, 1])

    lcolor = ListProperty([1, 1, 1, 0.5])
    lwidth=NumericProperty(1)


    # background_down:'atlas://data/images/defaulttheme/button_pressed'
    def on_state(self,instance, value):
        if value == 'down':
            self.bcolor=self.bcolor_down
        else:
            self.bcolor=self.bcolor_normal

Builder.load_string("""
<FlatButtonAngle>:
    bcolor_normal: self.bcolor_normal
    bcolor_down: self.bcolor_down
    bcolor: self.bcolor_normal
    lcolor: self.lcolor
    lwidth: self.lwidth

    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: self.lcolor
        Line:
            width: self.lwidth
            rectangle: (self.x, self.y, self.width, self.height)

    Label:
        id: _label
        text: root.text
        text_size: root.size
        halign: root.halign
        valign: root.valign
        shorten: root.shorten
        font_name: root.font_name
        shorten_from: root.shorten_from
        line_height: root.line_height
        angle: root.angle
        text: root.text
        center: root.center
        # bcolor: [0.1,0,0,0.5]

        #text_size: root.width-(self.padding[0]+self.padding[2]),root.height-(self.padding[1]+self.padding[3])
        canvas.before:
            PushMatrix
            Rotate:
                angle: root.angle
                origin: root.center
        canvas.after:
            PopMatrix


""")


class FlatButtonAngle(ButtonBehavior,BoxLayout):
    bcolor_normal = ListProperty([.345, .345, .345, 1])
    
    bcolor_down = ListProperty([.2, .64, .8, 1])
    bcolor = ListProperty([.345, .345, .345, 1])
    angle=NumericProperty(90)
    
    text=StringProperty('')
    halign=OptionProperty('center',options=('auto','left','center','right','justify'))
    valign=OptionProperty('middle',options=('bottom','middle','center','top'))
    shorten=BooleanProperty(False)
    shorten_from=OptionProperty('center',options=('left','center','right'))
    line_height=NumericProperty(1.0)
    font_name=StringProperty('Roboto')

    lcolor = ListProperty([1, 1, 1, 0.5])
    lwidth=NumericProperty(1)

    # background_down:'atlas://data/images/defaulttheme/button_pressed'
    def on_state(self,instance, value):
        if value == 'down':
            self.bcolor=self.bcolor_down
        else:
            self.bcolor=self.bcolor_normal

dyn_class_record={}
def add_parent(cls,added_parent_class='ButtonBehavior'):
    global dyn_class_record

    key=(cls,added_parent_class)

    try:
        return dyn_class_record[key]
    except:
        if isinstance(added_parent_class,str):
            added_parent_class=globals()[added_parent_class]

        class new_class(added_parent_class,cls):
            pass
        dyn_class_record[key]=new_class

    return new_class



Builder.load_string("""
<FlatTButtonAngle>:
    bcolor_normal: self.bcolor_normal
    bcolor_down: self.bcolor_down
    bcolor: self.bcolor_normal
    lcolor: self.lcolor
    lwidth: self.lwidth

    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: self.lcolor
        Line:
            width: self.lwidth
            rectangle: (self.x, self.y, self.width, self.height)

    Label:
        id: _label
        text: root.text
        markup: root.markup
        halign: root.halign
        valign: root.valign
        shorten: root.shorten
        font_name: root.font_name
        shorten_from: root.shorten_from
        line_height: root.line_height
        angle: root.angle
        text: root.text
        center: root.center
        # bcolor: [0.1,0,0,0.5]

        #text_size: root.width-(self.padding[0]+self.padding[2]),root.height-(self.padding[1]+self.padding[3])
        canvas.before:
            PushMatrix
            Rotate:
                angle: root.angle
                origin: root.center
        canvas.after:
            PopMatrix


""")


class FlatTButtonAngle(ToggleButtonBehavior,BoxLayout):
    bcolor_normal = ListProperty([.345, .345, .345, 1])
    
    bcolor_down = ListProperty([.2, .64, .8, 1])
    bcolor = ListProperty([.345, .345, .345, 1])
    angle=NumericProperty(90)
    
    text=StringProperty('')
    halign=OptionProperty('center',options=('auto','left','center','right','justify'))
    valign=OptionProperty('middle',options=('bottom','middle','center','top'))
    shorten=BooleanProperty(False)
    shorten_from=OptionProperty('center',options=('left','center','right'))
    line_height=NumericProperty(1.0)
    font_name=StringProperty('Roboto')

    lcolor = ListProperty([1, 1, 1, 0.5])
    lwidth=NumericProperty(1)
    markup=BooleanProperty(False)
    # state=StringProperty('normal')

    # background_down:'atlas://data/images/defaulttheme/button_pressed'
    def on_state(self,instance, value):
        if value == 'down':
            self.bcolor=self.bcolor_down
        else:
            self.bcolor=self.bcolor_normal








Builder.load_string("""
<FlatTButton>:
    bcolor_normal: self.bcolor_normal
    bcolor_down: self.bcolor_down
    bcolor: self.bcolor_normal
    lcolor: self.lcolor
    lwidth: self.lwidth

    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: self.lcolor
        Line:
            width: self.lwidth
            rectangle: (self.x, self.y, self.width, self.height)

    Label:
        id: _label
        text: root.text
        font_size: root.font_size
        markup: root.markup
        halign: root.halign
        valign: root.valign
        shorten: root.shorten
        font_name: root.font_name
        shorten_from: root.shorten_from
        line_height: root.line_height
        text_size: root.size
        center: root.center


""")


class FlatTButton(ToggleButtonBehavior,BoxLayout):
    bcolor_normal = ListProperty([.345, .345, .345, 1])
    
    bcolor_down = ListProperty([.2, .64, .8, 1])
    bcolor = ListProperty([.345, .345, .345, 1])
    
    text=StringProperty('')
    # halign=StringProperty('center')
    halign=OptionProperty('center',options=('auto','left','center','right','justify'))
    
    valign=OptionProperty('middle',options=('bottom','middle','center','top'))
    shorten=BooleanProperty(False)
    shorten_from=OptionProperty('center',options=('left','center','right'))
    line_height=NumericProperty(1.0)
    font_name=StringProperty('Roboto')

    font_size=NumericProperty(15)

    lcolor = ListProperty([1, 1, 1, 0.5])
    lwidth=NumericProperty(1)
    markup=BooleanProperty(False)
    # state=StringProperty('normal')

    # background_down:'atlas://data/images/defaulttheme/button_pressed'

    def __init__(self,**kwargs):
        self.register_event_type('on_state_down')
        super(FlatTButton, self).__init__(**kwargs)

    def on_state(self,instance, value):
        if value == 'down':
            self.bcolor=self.bcolor_down
            self.dispatch('on_state_down',self,value)
            if self.group!=None:
                for w in self.get_widgets(self.group):
                    if w==self:
                        continue
                    setattr(w,'state','normal')

        else:
            self.bcolor=self.bcolor_normal
    def on_state_down(self,instance, value):
        pass
    # def group_comply(self):
    #     for w in self.get_widgets(self.group):
    #         print(w)











Builder.load_string("""
<FlatButtonA>:
    bcolor_normal: self.bcolor_normal
    bcolor_down: self.bcolor_down
    bcolor: self.bcolor_normal
    background_color: self.bcolor
    lcolor: self.lcolor
    lwidth: self.lwidth
    text_color: self.text_color


    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size
        Color:
            rgba: self.lcolor
        Line:
            width: self.lwidth
            rectangle: (self.x, self.y, self.width, self.height)

    Label:
        id: _label
        text: root.text
        color: root.text_color
        center: root.center
        markup: root.markup
        halign: root.halign
        valign: root.valign
        shorten: root.shorten
        font_name: root.font_name
        shorten_from: root.shorten_from
        line_height: root.line_height
        text_size: root.size
        font_size: root.font_size
        padding: root.padding


""")


class FlatButtonA(ButtonBehavior,BoxLayout):
    bcolor_normal = ListProperty([.345, .345, .345, 1])
    
    bcolor_down = ListProperty([.2, .64, .8, 1])
    bcolor = ListProperty([.345, .345, .345, 1])
    # background_color=bcolor
    
    valign=OptionProperty('middle',options=('bottom','middle','center','top'))
    shorten=BooleanProperty(False)
    shorten_from=OptionProperty('center',options=('left','center','right'))
    line_height=NumericProperty(1.0)
    font_name=StringProperty('Roboto')

    text=StringProperty()
    font_size=NumericProperty(15)
    markup=BooleanProperty(False)
    halign=OptionProperty('center',options=('auto','left','center','right','justify'))
    

    text_color=ListProperty([1, 1, 1, 1])

    lcolor = ListProperty([1, 1, 1, 0.5])
    lwidth=NumericProperty(1)


    # background_down:'atlas://data/images/defaulttheme/button_pressed'
    def on_state(self,instance, value):
        if value == 'down':
            self.bcolor=self.bcolor_down
        else:
            self.bcolor=self.bcolor_normal


# Builder.load_string("""
# <FlatRoundButtonA>:
#     bcolor_normal: self.bcolor_normal
#     bcolor_down: self.bcolor_down
#     bcolor: self.bcolor_normal
#     background_color: self.bcolor
#     lcolor: self.lcolor
#     lwidth: self.lwidth
#     text_color: self.text_color

#     Label:
#         id: _label
#         text: root.text
#         color: root.text_color
#         center: root.center
#         markup: root.markup
#         halign: root.halign
#         valign: root.valign
#         shorten: root.shorten
#         font_name: root.font_name
#         shorten_from: root.shorten_from
#         line_height: root.line_height
#         text_size: root.size
#         font_size: root.font_size


# """)





# class FlatButtonA(ButtonBehavior,BgLineState,BoxLayout):
#     # bcolor_normal = ListProperty([.345, .345, .345, 1])
#     # _bcolor_normal=[.345, .345, .345, 1]
#     # _bcolor=_bcolor_normal
#     # _bcolor_down=[.2, .64, .8, 1]
#     # _lcolor=[1, 1, 1, 0.5]
    
#     # bcolor_down = ListProperty([.2, .64, .8, 1])
#     # bcolor = ListProperty([.345, .345, .345, 1])
#     # background_color=AliasProperty(BgLineState._get_bcolor,BgLineState._set_bcolor)
    
#     valign=OptionProperty('middle',options=('bottom','middle','center','top'))
#     shorten=BooleanProperty(False)
#     shorten_from=OptionProperty('center',options=('left','center','right'))
#     line_height=NumericProperty(1.0)
#     font_name=StringProperty('Roboto')

#     text=StringProperty()
#     font_size=NumericProperty(15)
#     markup=BooleanProperty(False)
#     halign=OptionProperty('center',options=('auto','left','center','right','justify'))
    
#     # text_color=ListProperty([1, 1, 1, 1])
#     _text_color=[1,1,1,1]
#     def _get_text_color(self):
#         return self._text_color
#     def _set_text_color(self,v):
#         self._text_color=resolve_color(v)
#         return True
#     text_color=AliasProperty(_get_text_color,_set_text_color)

#     # lcolor = ListProperty([1, 1, 1, 0.5])
#     # lwidth=NumericProperty(1)

#     def __init__(self,**kwargs):
#         super(FlatButtonA,self).__init__(**kwargs)

#     # background_down:'atlas://data/images/defaulttheme/button_pressed'
#     def on_state(self,instance, value):
#         # print(self.bcolor)
#         if value == 'down':
#             self.bcolor=self.bcolor_down
#         else:
#             self.bcolor=self.bcolor_normal


class SplitterV2(ButtonBehavior,BoxLayout):
    bcolor_normal = ListProperty([0, 0, 0, 0])
    bcolor_down = ListProperty([.2, .64, .8, 1])
    bcolor = ListProperty([0, 0, 0, 0])
    _moving=False
    _offset=[0,0]

    # background_down:'atlas://data/images/defaulttheme/button_pressed'
    # def on_state(self,instance, value):
    #     if value == 'down':
    #         self.bcolor=self.bcolor_down
    #     else:
    #         self.bcolor=self.bcolor_normal

    def on_touch_down(self, touch):
        # print(self.bcolor)
        # print("\nCustomLabel.on_touch_down:")

        if self.collide_point(*touch.pos):
            self._moving=True
            # print("\ttouch.pos =", touch.pos)
            self.touch_x, self.touch_y = touch.spos[0], touch.spos[1]

            return True
        self._moving=False
        return super(SplitterV2, self).on_touch_down(touch)
    def on_touch_up(self, touch):
        self._moving=False
        return touch

    def on_touch_move(self, touch):
        # print("\nCustomLabel.on_touch_move:")

        if self._moving or self.collide_point(*touch.pos):
            # self._moving=True

        # if True:
            try:
                
                # self.kvWindow.left -= self.touch_x * \
                #         self.kvWindow.size[0] - touch.spos[0]*self.kvWindow.size[0]+self._offset[0]
                # self.kvWindow.top += self.touch_y * \
                #         self.kvWindow.size[1] - touch.spos[1]*self.kvWindow.size[1]+self._offset[1]

                # print(f"{touch.spos =}")
                
                # print()
                # print(f"{touch.pos =}")
                dx=touch.pos[0]-self.pos[0]
                nwidth= self.parent.width+dx
                if nwidth<1:
                    return True

                pwidth=self.parent.parent.size[0]
                # print(f"{dx =}")
                hl=self.parent.children[1]
                # print(hl.width,hl.size_hint_x)

                # print(dx/pwidth)

                # self.parent.size_hint_x=self.parent.size_hint_x*(1+dx/pwidth)
                # print(self.parent.size,self.parent.size_hint)
                self.parent.width=nwidth
                hlabel=self.parent.children[1]
                ht=hlabel.text.lower()
                # print(hlabel.text)
                # start=False
                
                # for k,child in self.parent.parent.children_dict.items():
                #     # print(k)
                #     if ht in k:
                #         child.width=self.parent.width

                return True
            except:
                traceback.print_exc()
        return super(SplitterV2, self).on_touch_move(touch)


Builder.load_string('''
<SelectableLabel>:
    
    # halign: root.halign
    # valign: root.valign
    # markup: root.markup
    # text_size: root.width,root.height
    # on_pos: lambda *x:setattr(self,'text_size',self.size)
    # on_size: self.setter("text_size")

    # # Draw a background to indicate selection
    # canvas.before:
    #     Color:
    #         rgba: root._set_selected_color()
    #     Rectangle:
    #         pos: self.pos
    #         size: self.size
    
<RV>:
    scroll_type: ['bars','content']
    bar_width: 8
    bar_color: [.4, .4, .4, .9]
    bar_inactive_color: [.4, .4, .4, .6]
    viewclass: 'SelectableLabel'
    SelectableRecycleBoxLayout:
        padding: self.parent.padding
        spacing: self.parent.spacing
        default_size: None, dp(56)
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: True
''')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behavior to the view. '''
    selected_color=ListProperty([.5, 0.5, .5, .3])

    def on_parent(self,ins,parent):
        if parent:
            self.selected_color=parent.selected_color


# class SelectableLabel(RecycleDataViewBehavior, LabelB):
#     ''' Add selection support to the Label '''
#     index = None
#     selected = BooleanProperty(False)
#     selectable = BooleanProperty(True)
#     # lcolor = ListProperty(Colors['gray'])

#     def refresh_view_attrs(self, rv, index, data):
#         ''' Catch and handle the view changes '''
#         self.index = index
#         return super(SelectableLabel, self).refresh_view_attrs(
#             rv, index, data)

#     def on_touch_down(self, touch):
#         ''' Add selection on touch down '''
#         if super(SelectableLabel, self).on_touch_down(touch):
#             return True
#         if self.collide_point(*touch.pos) and self.selectable:
#             return self.parent.select_with_touch(self.index, touch)

#     def apply_selection(self, rv, index, is_selected):
#         ''' Respond to the selection of items in the view. '''
#         self.selected = is_selected
#         if is_selected:
#             # print("selection changed to {0}".format(rv.data[index]))
#             pass
#         else:
#             # print("selection removed for {0}".format(rv.data[index]))
#             pass

class  SelectableLabel(RecycleDataViewBehavior,LabelB):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)
    markup = BooleanProperty(False)
    meta = ObjectProperty(None)

    valign=OptionProperty('bottom',options=('bottom','middle','center','top'))
    halign=OptionProperty('left',options=('auto','left','center','right','justify'))

    option_selected=BooleanProperty(False)
    touch_button=OptionProperty('',options=('','left','right'))

    selected_color=ListProperty([.5, 0.5, .5, .3])

    def on_parent(self,ins,parent):
        # print(ins,parent)
        if parent:
            self.selected_color=parent.selected_color

    def on_selected(self,ins,v):
        # print(self.parent.parent)
        # try:
        #     grandparent=self.parent.parent
        # except:
        #     print('massive error',v)
        #     grandparent=None
        if v :
            # print(grandparent)
            self.bcolor=self.selected_color
        else:
            try:
                self.bcolor=self.parent.parent.data[self.index].get('bcolor',(0,0,0,0))
            except:
                self.bcolor=(0,0,0,0)
        # self.canvas.before.clear()
        # with self.canvas.before:
        #     Color(self.bcolor)
        #     Rectangle(pos=self.pos, 
        #         size=self.size, 
        #         size_hint=self.size_hint
        #         )
        # print(a)

    # lcolor = ListProperty(Colors['gray'])

    # def _set_selected_color(self,*a):
        # if self.selected:
        #     try:
        #         print(self.root)
        #         return self.selected_color
        #     except:
        #         print(self.parent)
        #         return self.selected_color
        # else:
        #     return 
        # print(a)
        # try:
        #     print('parent:',self.parent)
        #     return self.parent.parent.selected_color if self.selected else (0, 0, 0, 1)
        # except:
        #     return self.selected_color


    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        # if rv.option_selected:
        #     data['option_selected']=True
        # else:
        #     data['option_selected']=False
        data['lcolor']=data.get('lcolor','gray')
        for k,v in data.items():
            if 'color' in k:
                data[k]=resolve_color(v)
            elif k== 'font_name':
                data[k]=utils.Fonts.get(v,v)

        data['valign']=data.get('valign','middle')
        data['halign']=data.get('halign','left')
        data['padding']=data.get('padding',4)

        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data
            )

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        
        if touch.button=='left':
            if super(SelectableLabel, self).on_touch_down(touch):
                return True
            if self.collide_point(*touch.pos) and self.selectable:
                self.touch_button='left'
                self.option_selected=False
                return self.parent.select_with_touch(self.index, touch)
        elif touch.button=='right':
            if super(SelectableLabel, self).on_touch_down(touch):
                return True
            if self.collide_point(*touch.pos) and self.selectable:
                self.touch_button='right'
                # return self.parent.select_with_touch(self.index, touch)
                # self.option_selected=True
                self.parent.parent.index_option_selected=self.index
                self.parent.parent.widget_option_selected=self
                # self.parent.parent._purge_other_options(self.index)
                #Clock.schedule_once(lambda dt: self.parent.parent._purge_other_options(self.index) )
                # self.parent.parent.dispatch('on_purge_other_options',self.index)
                self.parent.parent.dispatch('on_option_selection',self.index)
        else:
            self.option_selected=False
            self.touch_button=''


    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        # if self.touch_button=='left':
        #     print('selected')
        #     self.selected = is_selected
        # elif self.touch_button=='right':
        #     self.option_selected
        #     print('o-selected')
        # else:
        #     print('none-selected')
        #     self.selected=False
        #     self.option_selected=False
        if is_selected:
            # print("selection changed to {0}".format(rv.data[index]))
            # self.parent.parent.dispatch('on_selection',index,rv.data[index])            
            pass
        else:
            # print("selection removed for {0}".format(rv.data[index]))
            pass
    def on_ref_press(self,refvalue):
        pass
        # self.parent.parent.on_ref_press()
        self.parent.parent.index_ref_pressed
        self.parent.parent.dispatch('on_ref_press',refvalue)


class RV(RecycleView,BgLine):
    data_selected=ListProperty([])
    index_selected=ListProperty([])
    # selected_color=ListProperty([.0, 0.9, .1, .3])
    selected_color=ListProperty([.5, 0.5, .5, .3])
    # option_selected_color=ListProperty([.5, 0.5, .5, .6])
    option_selected_color=ListProperty([.5, 0, 0, .6])
    widget_option_selected=ObjectProperty(None)
    index_option_selected=NumericProperty()
    index_ref_pressed=NumericProperty()
    padding=VariableListProperty([0, 0, 0, 0])
    spacing=NumericProperty(0)

    lwidth=NumericProperty(1)
    
    lcolor=ListProperty([0,0,0,0])
    
    bcolor=ListProperty([0,0,0, 0])



    def __init__(self,data,keyboard_scroll=True, **kwargs):

        self.register_event_type('on_ref_press')
        self.register_event_type('on_selection')
        self.register_event_type('on_option_selection')
        # self.register_event_type('on_purge_other_options')

        super(RV, self).__init__(**kwargs)
        # SelectableLabel.selected_color.defaultvalue=self.selected_color
        
        self.data=data
        self.layout_manager.bind(selected_nodes=self._select)
    # def on_selected_color(self,ins,v):
    #     SelectableLabel.selected_color.defaultvalue=utils.resolve_color(v)

    # ########################
    # def __init__(self,data,keyboard_scroll=True, **kwargs):
    #     super(RV, self).__init__(**kwargs)
    #     self.data=data
    # ########################


        # self.keyboard_scroll=keyboard_scroll
    #     self._keyboard = None
    # # def on_touch_down(self, touch):
    #     if keyboard_scroll:
    #         from kivy.core.window import Window
    #         self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    #         self._keyboard.bind(on_key_down=self._on_keyboard_down)
    #         self._keyboard.bind(on_key_up=self._on_keyboard_up)
    #         print('Keyboard Opened')
    #         # return True
    #     # return False
    # # def on_focus(self,*_):
    # #     print(_)
    # #     # if keyboard_scroll:
    #     #     from kivy.core.window import Window
    #     #     # Window.request_keyboard(self._keyboard_closed, self)
    #     #     self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
    #     #     self._keyboard.bind(on_key_down=self._on_keyboard_down)
    #     #     self._keyboard.bind(on_key_up=self._on_keyboard_up)
    #     #     print('Keyboard Opened')
    # def _keyboard_closed(self):
    #     print('Keyboard Closed')
    #     # self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    #     # self._keyboard.unbind(on_key_up=self._on_keyboard_up)
    #     # self._keyboard = None
    # def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #     key = keycode[1]
    #     print(f'{key} pressed')
    #     if key in ['left', 'right', 'up', 'spacebar']:
    #         pass
    #         # app = App.get_running_app()
    #         # app.root.ids[key].down_opacity = .5

    # def _on_keyboard_up(self, keyboard, keycode):
    #     key = keycode[1]
    #     print(f'{key} released')
    #     if key in ['left', 'right', 'up', 'spacebar']:
    #         pass
    #         # app = App.get_running_app()
    #         # app.root.ids[key].down_opacity = 0

    def on_ref_press(self, refvalue):
        # print(self,instance, refvalue)
        pass
    def _select(self,*largs):
        # print(largs)
        if largs[1]:
            self.index_selected=largs[1]
            
            self.data_selected=[]
            # oscount=0
            for s in largs[1]:
                # print(self.data[s])
                # if s['option_selected']:
                #     oscount+=1
                self.data_selected.append(self.data[s])
            self.dispatch('on_selection',*largs)


    def on_selection(self,*largs):
        pass
    def on_option_selection(self,*largs):
        pass

    def scroll(self,val):
        self.scroll_y=val
    def scroll_top(self,val=1):
        self.scroll_y=val
    def scroll_bottom(self,val=0):
        self.scroll_y=val
    def scroll_into_view(self,index):
        ld=len(self.data)
        sv=1-(index)/(ld-1)
        self.scroll_y=sv


    def select(self,index):
        self.children[0].select_node(index)

    def deselect(self,index):
        self.children[0].deselect_node(index)
    def select_all(self):
        for i in range(len(self.data)):
            self.children[0].select_node(i)
    def deselect_all(self):
        for i in range(len(self.data)):
            self.children[0].deselect_node(i)
    def clear_selection(self):
        self.children[0].clear_selection()



class CalcGridLayout(kvw.GridLayout):
    dpos=StringProperty('A1')
    cval=ObjectProperty(0)
    _data_num=CaseInsensitiveDict()
    _exec_code='import math\nimport statistics\n'
    exec_vars={}
    error=''
    selected=None
    headers=CaseInsensitiveDict()
    columns=CaseInsensitiveDict()
    children_dict=CaseInsensitiveDict()
    def compile_ecode(self):
        self.exec_vars={}
        exec(self._exec_code,self.exec_vars)
    def force_color_selected(self):
        wid=self.children_dict[self.dpos]
        self.selected=wid
        wid.lcolor=(103/255,216/255,239/255,1)
    def hide_widget(self,widget):
        widget.height, widget.size_hint_y, widget.opacity, widget.disabled = 0, None, 0, True
    def show_widget(self,on_widget,top_widget):
        # print(on_widget.pos,on_widget.size)
        top_widget.pos=  on_widget.pos
        top_widget.size=  on_widget.size
        top_widget.opacity= 1
        top_widget.disabled= False
        top_widget.focus=True
    def update_data_num(self,do_clear=False):
        if do_clear:
            self._data_num.clear()
        self._data_num.update(self.exec_vars)
        for k,wid in self.children_dict.items():
            self._data_num[k]=self.eval(wid,wid._text)
    def eval(self,wid,s):
        wid.error=''
        s=s.strip()
        v_=s
        if s and s[0]=='=':
            ls=re.findall(r"[a-z][0-9]+:[a-z][0-9]+",v_,flags=re.IGNORECASE)
            for li in ls:
                l,r=li.split(':')
                tl=re.sub(r"\d", "", l)
                il=re.sub(r"\D", "", l)
                tr=re.sub(r"\d", "", r)
                ir=re.sub(r"\D", "", r)
                if tl==tr:
                    v_=v_.replace(li,f'[{",".join([tl+str(i) for i in range(int(il),int(ir)+1)])}]')
                if il==ir:
                    abc0=abc.index(tl.upper())
                    abc1=abc.index(tr.upper())
                    v_=v_.replace(li,f'[{",".join([abc[abci]+str(il) for abci in range(abc0,abc1+1)])}]')
                elif tl!=tr and il!=ir:
                    TABLE_matrix=False
                    
                    abc0=abc.index(tl.upper())
                    abc1=abc.index(tr.upper())
                    il=int(il)
                    ir=int(ir)
                    nl_=[]
                    if TABLE_matrix:
                        for i in range(il,ir+1):
                            nl_.append('[' + ",".join([abc[abci]+str(i) for abci in range(abc0,abc1+1)])  +']')
                        nl='['+','.join(nl_)+']'
                        v_=v_.replace(li,nl)
                    else:
                        for i in range(il,ir+1):
                            for abci in range(abc0,abc1+1):
                                nl_.append(abc[abci]+str(i))
                        nl='['+','.join(nl_)+']'
                        v_=v_.replace(li,nl)
        s=v_

        

        if s=='':
            wid.text=''
            wid.val=0
            return wid.val
        
        if s[0]=='=':
            try:
                wid.val=eval(s[1:],self._data_num)
            except Exception as e:
                wid.error=traceback.format_exc()
                wid.val=e.__class__.__name__
                
                # wid.val=traceback.format_exc(limit=12)
        else:
            try:
                try:
                    sf=float(s)
                except:
                    sf=None
                try:
                    si=int(s)
                except:
                    si=None
                if sf!=None and si!=None:
                    if sf==si:
                        wid.val=si
                    else:
                        wid.val=sf

                elif sf!=None:
                    wid.val=sf
                elif si!=None:
                    wid.val=si
                else:
                    raise ValueError
            except:
                wid.val=s

        # return f"{wid.val}"
        t=f"{wid.val}"
        tnum=utils.is_number(t)
        # try:
        #     if tnum and not '.' in t:
        #         wid.text=f"{wid.val:.0f}"
        #     elif tnum:
        #         wid.text=f"{wid.val:.6}"
        #     else:
        #         wid.text=f"{wid.val}"
        # except:
        #     wid.text=t
        # print(t,tnum)
        if tnum and not '.' in t:
            wid.text=f"{wid.val:.0f}"
        elif tnum:
            wid.text=f"{wid.val:.6}"
        else:
            wid.text=f"{wid.val}"

        # self
        return wid.val

class Cell(kvw.FlatButtonA,kvw.TouchBehavior):
    dpos=StringProperty('A1')
    _text=StringProperty()
    val=ObjectProperty(0)
    error=''
    def on_val(self,instance,new_val):
        self.parent.error=self.error
        self.parent.cval=new_val
    def on_double_tap(self, *args):
        self.parent.icell.ccell=self
        self.parent.icell.text=self._text
        self.parent.show_widget(self,self.parent.icell)
    def on_single_tap(self,*args):
        self.parent.dpos=self.dpos
        if self.parent.selected:
            self.parent.selected.lcolor=(1,1,1,1)
        self.parent.selected=self
        self.lcolor=(103/255,216/255,239/255,1)
    def on__text(self,instance,value):

        self.parent.update_data_num(do_clear=True)
        self.parent.eval(self,value)
        self.parent.update_data_num()
    def on_size(self,instance,value):
        padh=self.padding[0]+self.padding[2]
        padv=self.padding[1]+self.padding[3]
        instance.text_size=self.width-padh,self.height-padv

# def ICell(**kwargs):
#     from kivy.uix.textinput import TextInput


# Builder.load_string("""
# <BoxLayoutB>:
#     bcolor: 0, 0, 0, 0
#     lcolor: 1, 1, 1, 0
#     lwidth: 1
    
#     canvas.before:
#         Color:
#             rgba: self.bcolor
#         Rectangle:
#             pos: self.pos
#             size: self.size

#         Color:
#             rgba: self.lcolor
#         Line:
#             width: self.lwidth
#             rectangle: (self.x, self.y, self.width, self.height)
# """)


# class BoxLayoutB(BoxLayout):
#     bcolor = ListProperty([0, 0, 0, 0])
#     lcolor = ListProperty([1, 1, 1, 0])
#     lwidth=NumericProperty(1)

class BoxLayoutB(BgLine,BoxLayout):
    pass

    # def on_size_callback(self,instance):
    #     print('hell')
    #     # print('size',size)
    #     instance.width=size[0]*.5

Builder.load_string("""
<GridLayoutB>:
    bcolor: 0, 0, 0, 0
    lcolor: 1, 1, 1, 0
    lwidth: 1
    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size

        Color:
            rgba: self.lcolor
        Line:
            width: self.lwidth
            rectangle: (self.x, self.y, self.width, self.height)
""")


class GridLayoutB(GridLayout):
    bcolor = ListProperty([0, 0, 0, 0])
    lcolor = ListProperty([1, 1, 1, 0])
    lwidth=NumericProperty(1)

Builder.load_string("""
<StackLayoutB>:
    bcolor: 0, 0, 0, 0
    lcolor: 1, 1, 1, 0
    lwidth: 1
    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size

        Color:
            rgba: self.lcolor
        Line:
            width: self.lwidth
            rectangle: (self.x, self.y, self.width, self.height)
""")


class StackLayoutB(StackLayout):
    bcolor = ListProperty([0, 0, 0, 0])
    lcolor = ListProperty([1, 1, 1, 0])
    lwidth=NumericProperty(1)
####################################
Builder.load_string("""
<PageLayoutB>:
    bcolor: 0, 0, 0, 0
    lcolor: 1, 1, 1, 0
    lwidth: 1
    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size

        Color:
            rgba: self.lcolor
        Line:
            width: self.lwidth
            rectangle: (self.x, self.y, self.width, self.height)
""")


class PageLayoutB(PageLayout):
    bcolor = ListProperty([0, 0, 0, 0])
    lcolor = ListProperty([1, 1, 1, 0])
    lwidth=NumericProperty(1)
####################################

# Builder.load_string("""
# <RelativeLayoutB>:
#     bcolor: 0, 0, 0, 0
#     lcolor: 1, 1, 1, 0
#     lwidth: 1
#     canvas.before:
#         Color:
#             rgba: self.bcolor
#         Rectangle:
#             pos: self.pos
#             # pos_hint: self.pos_hint
#             size: self.size


#         Color:
#             rgba: self.lcolor
#         Line:
#             width: self.lwidth
#             rectangle: (self.x, self.y, self.width, self.height)

# """)


# class RelativeLayoutB(RelativeLayout):
#     bcolor = ListProperty([0, 0, 0, 0])
#     lcolor = ListProperty([1, 1, 1, 0])
#     lwidth=NumericProperty(1)

class RelativeLayoutB(BgLineState,RelativeLayout):
    pass


Builder.load_string("""
<ScatterB>:
    bcolor: 0, 0, 0, 0
    lcolor: 1, 1, 1, 0
    lwidth: 1
    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size

        Color:
            rgba: self.lcolor
        Line:
            width: self.lwidth
            rectangle: (self.x, self.y, self.width, self.height)
""")


class ScatterB(Scatter):
    bcolor = ListProperty([0, 0, 0, 0])
    lcolor = ListProperty([1, 1, 1, 0])
    lwidth=NumericProperty(1)



# # sk._Factory.register('KivyB', module='Separator')
# Builder.load_string("""
# <BBoxLayout>:
#     bcolor_normal: self.bcolor_normal
#     bcolor_down: self.bcolor_down
#     bcolor: self.bcolor_normal
#     canvas.before:
#         Color:
#             rgba: self.bcolor
#         Rectangle:
#             pos: self.pos
#             size: self.size
# """)


# class BBoxLayout(ButtonBehavior,BoxLayout):
#     bcolor_normal = ListProperty([0, 0, 0, 0])
#     bcolor_down = ListProperty([.2, .64, .8, 1])
#     bcolor = ListProperty([0, 0, 0, 0])

#     # background_down:'atlas://data/images/defaulttheme/button_pressed'
#     def on_state(self,instance, value):
#         if value == 'down':
#             self.bcolor=self.bcolor_down
#         else:
#             self.bcolor=self.bcolor_normal


# sk._Factory.register('KivyB', module='Separator')
Builder.load_string("""
<AngleBBoxLayout>:
    bcolor_normal: 0, 0, 0, 0
    bcolor_down: .2, .64, .8, 1
    bcolor: self.bcolor_normal

    canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            pos: self.pos
            size: self.size
    #canvas.before:
        PushMatrix
        Rotate:
            angle: root.angle
            origin: root.center
    canvas.after:
        PopMatrix
""")


class AngleBBoxLayout(ButtonBehavior,BoxLayout):
    bcolor_normal = ListProperty([0, 0, 0, 0])
    bcolor_down = ListProperty([.2, .64, .8, 1])
    bcolor = ListProperty([0, 0, 0, 0])
    angle = NumericProperty(0)  # Angle property in degrees

    def __init__(self, **kwargs):
        super(AngleBBoxLayout, self).__init__(**kwargs)
        # self.bind(angle=self.update)
        # self.size=kwargs.get('size',(100,100))
        # self.size_hint=kwargs.get('size',(1,1))

    def on_state(self,instance, value):
        # print('pressed')
        # print(f"{self.bcolor =}")
        # print(f"{self.size =}")
        # print(f"{self.size_hint =}")
        if value == 'down':
            self.bcolor=self.bcolor_down
        else:
            self.bcolor=self.bcolor_normal

    # def update(self, *args):
    #     # pass
    #     self.canvas.before.clear()
    #     with self.canvas.before:
    #         Color(self.bcolor)
    #         Rectangle(pos=self.pos, 
    #             size=self.size, 
    #             size_hint=self.size_hint
    #             )
    # def on_width(self, instance, value):
    #     if self.height != value:
    #         self.height = value

    # def on_height(self, instance, value):
    #     if self.width != value:
    #         self.width = value





class customScreenManager(kvw.ScreenManager):
    # from_goback=False

    def goback(self):
        prev=self.history.back()
        # print('--- Browse history ---')
        # print(self.history.history)
        # print(f'{prev =}')
        # print('-'*30)
        self.current=prev
    #     # for h,v in self.history.items():
    #     #     if v==1:
    #     #         # print(h)
    #     #         self.current=h
    #     #         self.history[h]=2
    #     self.from_goback=False
    #     lh=len(self.history)
        
    #     if lh>1:
    #     #     instance.history.insert(-1, instance.history.pop(1))
    #         self.from_goback=True
    #         self.current=self.history[1]
    #         # self.history.insert(1, self.history.pop(-1))
    #     #     # self.current=self.history.pop(1)
    #     #     # del self.history[0]
    #     #     # self.history.pop(0)
    #     # elif lh==1:
    #     #     pass
    #         # self.from_goback=True
    #         # self.current=self.history[0]
    #     self.from_goback=False
    #     print(self.history)
    #     # else:
    #     #     pass
    #         # self.history.append(self.current)

    #     #     self.history.pop(0)
    #         # self.history.pop(-2)

    # # def on_current(self,instance,value):
    # #     instance._history.append(value)
    # #     print(instance._history)

class ScrollLabel(ScrollView):
    bcolor = ListProperty([0, 0, 0, 0])
    lcolor = ListProperty([1, 1, 1, 0])
    lwidth=NumericProperty(1)
    text=StringProperty('')
    # label=ObjectProperty(None)
    
    def __init__(self,label=None, **kwargs):
        # print(kwargs)
        super(ScrollLabel, self).__init__(**kwargs)
        
        

        # label.bind(text=self.setter(self.text))
        # self.bind(text=lambda *largs:setattr(self.label,'text',largs[1]))
        self.bind(text=self.on_text)

        # label.size_hint=1, None

        label.bind(width=lambda *x: label.setter('text_size')(label, (label.width, None) )  )
        label.bind(texture_size=lambda *x: label.setter('height')(label, label.texture_size[1]))

        self.label=label

        self.add_widget(label)
        # self.c=0
        # self.th=0
        # self.change_background()


        

    #     self.label.bind(texture_size=lambda *largs: setattr(self.label,'height',self.label.texture_size[1]))
    #     # self.label.height=self.label.texture_size[1]

    #     self.label.bind(width=lambda *largs: setattr(self.label,'text_size',[self.label.width,None]))
    #     # self.label.text_size= self.label.width, None
    # def change_background(self, *args):
    #     self.canvas.before.clear()#<- clear previous instructions
    #     with self.canvas.before:
    #         if self.bcolor:
    #             Color(0.2, 0.2, 0.2, mode = 'rgb')
    #         else:
    #             Color(0.1, 0.1, 0.1, mode = 'rgb')
    #         Rectangle(pos = self.pos, size = self.size)

    def on_text(self,*largs):
        # print(largs)
        self.label.text=largs[1]
        self.scroll_y=1
        # self.old_height=self.label.size[1]*1
        # self.label.size_hint_y=1
        self.label.width+=1
        self.label.width+=-1
        # Clock.schedule_once(self._fix_size,0.1)
    # def _fix_size(self,*largs):
    #     pass

    def scroll(self,val):
        self.scroll_y=val
    def scroll_top(self,val=1):
        self.scroll_y=val
    def scroll_bottom(self,val=0):
        self.scroll_y=val


# class RoundCornerLayout(RelativeLayout):
#     bcolor=ListProperty([.345, .345, .345, 1])
#     r=NumericProperty(50)
#     def __init__(self,**kwargs):
#         super(RoundCornerLayout, self).__init__(**kwargs)
#         self.draw_round()
#     def on_size(self,*args):
#         try:
#             self.draw_round()
#         except:
#             pass
#     def draw_round(self,*args):
#         if self.canvas:
#             self.canvas.clear()
#         r=self.r
#         with self.canvas:
#             # Color(.3,0,3,.3)
#             Color(*self.bcolor)
#             Rectangle(pos=[0,r],size=[r,self.size[1]-2*r])
#             Rectangle(pos=[self.size[0]-r,0+r],size=[r,self.size[1]-2*r])

#             Rectangle(pos=[r,0],size=[self.size[0]-2*r,r])

#             Rectangle(pos=[r,self.size[1]-r],size=[self.size[0]-2*r,r])
            

#             # Color(0,.3,0,.5)
#             # Color(*self.bcolor)
#             Ellipse(pos=[0,0],size=[2*r,2*r])
#             Ellipse(pos=[self.size[0]-2*r,0],size=[2*r,2*r])
#             Ellipse(pos=[0,self.size[1]-2*r],size=[2*r,2*r])
#             Ellipse(pos=[self.size[0]-2*r,self.size[1]-2*r],size=[2*r,2*r])

#             # Color(1,1,1,0.1)
#             # Color(*self.bcolor)
#             self.bg=Rectangle(pos=[r,r],size=[self.size[0]-2*r,self.size[1]-2*r])


# Builder.load_string("""
# <RoundCornerLayout>:
#     bcolor: self.bcolor_normal
#     r: self.r
#     canvas.before:
#         Color:
#             rgba: self.bcolor
        
#         Rectangle:
#             pos: 0, self.r
#             size: self.r,self.height-2*self.r
#         Rectangle:
#             pos: self.width-self.r, self.r
#             size: self.r,self.height-2*self.r
#         Rectangle:
#             pos: self.r, 0
#             size: self.width-2*self.r, self.r
#         Rectangle:
#             pos: self.r, self.height-self.r
#             size: self.width-2*self.r, self.r

#         SmoothEllipse:
#             pos: 0,0
#             size: 2*self.r, 2*self.r
#             angle_start: 180
#             angle_end: 270
#         SmoothEllipse:
#             pos: self.width-self.r*2,0
#             size: 2*self.r, 2*self.r
#             angle_start: 90
#             angle_end: 180
#         SmoothEllipse:
#             pos: 0,self.height-self.r*2
#             size: 2*self.r, 2*self.r
#             angle_start: 270
#             angle_end: 360
#         SmoothEllipse:
#             pos: self.width-self.r*2, self.height-self.r*2
#             size: 2*self.r, 2*self.r
#             angle_start: 0
#             angle_end: 90

#         Rectangle:
#             pos: self.r, self.r
#             size: self.width-self.r*2, self.height-self.r*2

#         Color:
#             rgba: self.lcolor

#         SmoothLine:
#             width: self.lwidth
#             ellipse: 0,0,2*self.r, 2*self.r,180,270,5
#         SmoothLine:
#             width: self.lwidth
#             ellipse: self.width-self.r*2,0,2*self.r, 2*self.r,90,180,5
#         SmoothLine:
#             width: self.lwidth
#             ellipse: 0,self.height-self.r*2,2*self.r, 2*self.r,270,360,5
#         SmoothLine:
#             width: self.lwidth
#             ellipse: self.width-self.r*2, self.height-self.r*2,2*self.r, 2*self.r,0,90,5

#         # Color:
#         #     rgba: [1,0,0,1]

#         SmoothLine:
#             width: self.lwidth
#             points: self.r, 0,self.width-self.r,0
#         SmoothLine:
#             width: self.lwidth
#             points: self.r, self.height, self.width-self.r ,self.height
#         SmoothLine:
#             width: self.lwidth
#             points: 0, self.r, 0,self.height-self.r
#         SmoothLine:
#             width: self.lwidth
#             points: self.width, self.r, self.width,self.height-self.r
        
        
# """)

# Builder.load_string("""
# <RoundCornerLayout>:
#     bcolor: self.bcolor_normal
#     r: self.r
#     canvas.before:
#         Color:
#             rgba: self.bcolor
        


#         Color:
#             rgba: self.lcolor

        
        
# """)


# class BBoxLayout(ButtonBehavior,BoxLayout):
    

# class RoundCornerLayout(RelativeLayout):
#     # bcolor=ListProperty([.345, .345, .345, 1])
#     r=NumericProperty(15)
#     lwidth=NumericProperty(1)
#     lcolor=ListProperty([.345, .345, .345, 1])
    
#     bcolor=ListProperty([.345, .345, .345, 1])
#     bcolor_normal=bcolor


#     # def __init__(self,**kwargs):
#     #     super(RoundCornerLayout, self).__init__(**kwargs)
#         # self.draw_round()
#     # def on_size(self,*args):
#     #     try:
#     #         self.draw_round()
#     #     except:
#     #         pass

#     # def draw_round(self,*args):
#     #     pass



class RoundCornerLayout(RoundBgLine, RelativeLayout):
    pass

# Builder.load_string("""
# <RoundBLayout>:
#     bcolor_normal: self.bcolor_normal
#     bcolor_down: self.bcolor_down
#     bcolor: self.bcolor_normal
#     # canvas.before:
#     #     Color:
#     #         rgba: self.bcolor
#     #     Rectangle:
#     #         pos: self.pos
#     #         size: self.size
# """)


class RoundBLayout(RoundBgLineState,ButtonBehavior, RelativeLayout):
    pass
    # bcolor_normal = ListProperty([.345, .345, .345, 1])
    # bcolor_down = ListProperty([.2, .64, .8, 1])
    # bcolor = ListProperty([.345, .345, .345, 1])
    # _bcolor_normal = [.345, .345, .345, 1]
    # _bcolor_down = [.2, .64, .8, 1]
    # _bcolor = _bcolor_normal

    # def __init__(self,**kwargs):
    #     # print(kwargs)
    #     super(RoundBLayout,self).__init__(**kwargs)


    # background_down:'atlas://data/images/defaulttheme/button_pressed'
    # def on_state(self,instance, value):
    #     print(self.bcolor_down)
    #     if value == 'down':
    #         self.bcolor=self.bcolor_down
    #     else:
    #         self.bcolor=self.bcolor_normal
        # self.on_state(None,None)
        # self.draw_round()



class FlatRoundButtonA(RoundBLayout):
    valign=OptionProperty('middle',options=('bottom','middle','center','top'))
    shorten=BooleanProperty(False)
    shorten_from=OptionProperty('center',options=('left','center','right'))
    line_height=NumericProperty(1.0)
    font_name=StringProperty('Roboto')

    text=StringProperty()
    font_size=NumericProperty(15)
    markup=BooleanProperty(False)
    halign=OptionProperty('center',options=('auto','left','center','right','justify'))
    
    _text_color=[1,1,1,1]
    def _get_text_color(self):
        return self._text_color
    def _set_text_color(self,v):
        self._text_color=resolve_color(v)
        self._label.color=self._text_color
        return True
    text_color=AliasProperty(_get_text_color,_set_text_color)
    # text_color=ColorProperty([1,1,1,1])

    def __init__(self,**kwargs):
        # print(kwargs)
        super(FlatRoundButtonA,self).__init__(**kwargs)
        self._label=_Label(size_hint=(1,1))

        self.add_widget(self._label)
        _setter_task=dict(
            text='text',
            markup='markup',
            font_size='font_size',
            halign='halign',
            valign='valign',
            font_name='font_name',
            line_height='line_height',
            shorten='shorten',
            shorten_from='shorten_from',
            )
        for k,v in _setter_task.items():
            setattr(self._label,v,getattr(self,k))
        for k,v in _setter_task.items():
            self.bind(**{k:self._label.setter(v)})
        self._label.bind(size=self._label.setter('text_size'))

# Builder.load_string("""
# <RelativeBLayout>:
#     bcolor_normal: self.bcolor_normal
#     bcolor_down: self.bcolor_down
#     bcolor: self.bcolor_normal
# """)


# class RelativeBLayout(ButtonBehavior,RelativeLayoutB):
#     bcolor_normal = ListProperty([.345, .345, .345, 1])
#     bcolor_down = ListProperty([.2, .64, .8, 1])
#     bcolor = ListProperty([.345, .345, .345, 1])

#     def on_state(self,instance, value):
#         if value == 'down':
#             self.bcolor=self.bcolor_down
#         else:
#             self.bcolor=self.bcolor_normal
#         # self.on_state(None,None)
#         # self.draw_round()





Builder.load_string('''
<Pl_Selectable>:
    spacing: 8
    padding: 8
    
    wartist: wartist

    # Draw a background to indicate selection
    canvas.before:
        Color:
            # rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
            rgba: self.parent.parent.selected_color if self.parent and self.selected else (0, 0, 0, 0)
        Rectangle:
            pos: self.pos
            size: self.size

        # Color:
        #     #rgba: self.parent.parent.option_selected_color if self.parent and self.option_selected else (0, 0, 0, 0)
        #     # rgba: self.parent.parent.option_selected_color if self.parent and self.option_selected else (0, 0, 0, 0)
        #     rgba: self.lcolor
        # Line:
        #     width: 1
        #     rectangle: (self.x, self.y, self.width, self.height)
    
    AsyncImage:
        id: image_cover
        source: root.cover
        size_hint: None,None
        size: root.cover_size,root.cover_size
        pos_hint: {'center_x':0.5,'center_y':0.5}
    BoxLayout:
        # orientation: "vertical"
        # orientation: "horizontal"
        orientation: root.artist_orientation
        Label:
            text: root.title
            font_size: 14
            halign: "left"
            # valign: "bottom"
            valign: root.title_valign
            markup: True
            shorten: True
            shorten_from: "right"
            text_size: self.size
        Label:
            text: root.artist
            id: wartist
            font_size: 13
            color: (164/255,164/255,164/255,1)
            # halign: "left"
            halign: root.artist_halign
            valign: "middle"
            shorten: True
            shorten_from: "right"
            text_size: self.size
            markup: True,
            size_hint_y: root.artist_size_hint_y
            on_ref_press: root.on_ref_press(*args)
    Label:
        font_size: 13
        halign: "right"
        valign: "middle"
        markup: True
        text: root.duration
        size_hint_x: None
        width: root.duration_width
        text_size: self.size
        shorten: True
        shorten_from: "right"
    

<Playlist>:
    viewclass: 'Pl_Selectable'
    SelectableRecycleBoxLayout:
        # default_size: None, dp(56)
        default_size: None, 80
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: True
''')


class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behavior to the view. '''


class Pl_Selectable(RecycleDataViewBehavior, BoxLayoutB):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    option_selected=BooleanProperty(False)
    touch_button=OptionProperty('',options=('','left','right'))

    title=StringProperty('')
    artist=StringProperty('')
    duration=StringProperty('--:--')
    album=StringProperty('')
    # lcolor=ListProperty([0,0,0,0])

    cover=StringProperty('atlas://data/images/defaulttheme/player-play-overlay')
    cover_size=NumericProperty(60)
    duration_width=NumericProperty(40)
    artist_size_hint_y=NumericProperty(1)

    # image_cover=ObjectProperty(None)
    wartist=ObjectProperty(None)
    meta=ObjectProperty(None)


    title_valign=OptionProperty('bottom',options=('bottom','middle','center','top'))


    artist_halign=OptionProperty('left',options=('auto','left','center','right','justify'))
    artist_orientation=OptionProperty('vertical',options=('vertical','horizontal'))
    

    # lcolor = ListProperty(Colors['gray'])

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        # if rv.option_selected:
        #     data['option_selected']=True
        # else:
        #     data['option_selected']=False

        return super(Pl_Selectable, self).refresh_view_attrs(
            rv, index, data
            )

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        
        if touch.button=='left':
            if super(Pl_Selectable, self).on_touch_down(touch):
                return True
            if self.collide_point(*touch.pos) and self.selectable:
                self.touch_button='left'
                self.option_selected=False
                return self.parent.select_with_touch(self.index, touch)
        elif touch.button=='right':
            if super(Pl_Selectable, self).on_touch_down(touch):
                return True
            if self.collide_point(*touch.pos) and self.selectable:
                self.touch_button='right'
                # return self.parent.select_with_touch(self.index, touch)
                # self.option_selected=True
                self.parent.parent.index_option_selected=self.index
                self.parent.parent.widget_option_selected=self
                # self.parent.parent._purge_other_options(self.index)
                #Clock.schedule_once(lambda dt: self.parent.parent._purge_other_options(self.index) )
                # self.parent.parent.dispatch('on_purge_other_options',self.index)
                self.parent.parent.dispatch('on_option_selection',self.index)
        else:
            self.option_selected=False
            self.touch_button=''


    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        # if self.touch_button=='left':
        #     print('selected')
        #     self.selected = is_selected
        # elif self.touch_button=='right':
        #     self.option_selected
        #     print('o-selected')
        # else:
        #     print('none-selected')
        #     self.selected=False
        #     self.option_selected=False
        if is_selected:
            # print("selection changed to {0}".format(rv.data[index]))
            # self.parent.parent.dispatch('on_selection',index,rv.data[index])            
            pass
        else:
            # print("selection removed for {0}".format(rv.data[index]))
            pass
    def on_ref_press(self,instance, refvalue):
        pass
        # self.parent.parent.on_ref_press()
        self.parent.parent.index_ref_pressed
        self.parent.parent.dispatch('on_ref_press',refvalue)
    #     # print(args)
    #     get_kvApp().trigger_event(f"{self.parent.parent.id}/ref/{refvalue}")


class Playlist(RecycleView):
    padding=VariableListProperty([0, 0, 0, 0])
    spacing=NumericProperty(0)
    # 
    data_selected=ListProperty([])
    index_selected=ListProperty([])
    # selected_color=ListProperty([.0, 0.9, .1, .3])
    selected_color=ListProperty([.5, 0.5, .5, .3])
    # option_selected_color=ListProperty([.5, 0.5, .5, .6])
    option_selected_color=ListProperty([.5, 0, 0, .6])
    widget_option_selected=ObjectProperty(None)
    index_option_selected=NumericProperty()
    index_ref_pressed=NumericProperty()



    def __init__(self,data,keyboard_scroll=True, **kwargs):
        self.register_event_type('on_ref_press')
        self.register_event_type('on_selection')
        self.register_event_type('on_option_selection')
        # self.register_event_type('on_purge_other_options')

        super(Playlist, self).__init__(**kwargs)
        self.data=data
        self.layout_manager.bind(selected_nodes=self._select)

    def on_ref_press(self, refvalue):
        # print(self,instance, refvalue)
        pass
    def _select(self,*largs):
        # print(largs)
        if largs[1]:
            self.index_selected=largs[1]
            
            self.data_selected=[]
            # oscount=0
            for s in largs[1]:
                # print(self.data[s])
                # if s['option_selected']:
                #     oscount+=1
                self.data_selected.append(self.data[s])
            self.dispatch('on_selection',*largs)
            # if oscount:
            #     self.dispatch('on_option_selection',*largs)
            # else:
            #     self.dispatch('on_selection',*largs)
    # def on_purge_other_options(self,index):
    #     data=self.data
    #     for i,e in enumerate( self.data ):
    #         if i!=index:
    #             data[i]['option_selected']=False
    #             data[i]['lcolor']=[0,0,0,0]
    #         else:
    #             data[i]['option_selected']=True
    #             data[i]['lcolor']=self.option_selected_color
    #         # print(data[i])
    #     self.data=data

    #     print('hell')


    def on_selection(self,*largs):
        pass
    def on_option_selection(self,*largs):
        pass

    def scroll(self,val):
        self.scroll_y=val
    def scroll_top(self,val=1):
        self.scroll_y=val
    def scroll_bottom(self,val=0):
        self.scroll_y=val
    def scroll_into_view(self,index):
        ld=len(self.data)
        sv=1-(index)/(ld-1)
        self.scroll_y=sv


    def select(self,index):
        # self.soft_selected=index
        # print('selecting',index)
        self.children[0].select_node(index)

    def deselect(self,index):
        # print('deselecting',index)
        self.children[0].deselect_node(index)
    def select_all(self):
        for i in range(len(self.data)):
            self.children[0].select_node(i)
    def deselect_all(self):
        for i in range(len(self.data)):
            self.children[0].deselect_node(i)
    def clear_selection(self):
        self.children[0].clear_selection()
















Builder.load_string('''
<Al_Selectable>:
    spacing: 8
    padding: 8
    
    wartist: wartist

    # Draw a background to indicate selection
    canvas.before:
        Color:
            # rgba: (.0, 0.9, .1, .3) if self.selected else (0, 0, 0, 1)
            rgba: self.parent.parent.selected_color if self.parent and self.selected else (0, 0, 0, 0)
        Rectangle:
            pos: self.pos
            size: self.size
    
    # AsyncImage:
    #     id: image_cover
    #     source: root.cover
    #     size_hint: None,None
    #     size: root.cover_size,root.cover_size
    #     pos_hint: {'center_x':0.5,'center_y':0.5}
    # BoxLayout:
    #     orientation: "vertical"
    Label:
        color: (.5,.5,.5,1)
        font_size: 14
        halign: "center"
        valign: "middle"
        
        text: root.track
        text_size: self.size
        width: 32
        size_hint_x: None
        markup: True
        shorten: True
        shorten_from: "right"

    BoxLayout:
        orientation: 'vertical'
        Label:
            font_size: 14
            halign: "left"
            valign: "middle"
            text: root.title
            text_size: self.size
            markup: True
            shorten: True
            shorten_from: "right"
        BoxLayout:
            orientation: 'horizontal'
            Label:
                id: wartist
                font_size: 13
                color: (164/255,164/255,164/255,1)
                halign: "left"
                valign: "middle"
                text: root.artist
                text_size: self.size
                markup: True
                on_ref_press: root.on_ref_press(*args)
                shorten: True
                shorten_from: "right"

            Label:
                font_size: 14
                width: 80
                color: (.5,.5,.5,1)
                size_hint_x: None
                halign: "center"
                valign: "middle"
                text: root.plays
                text_size: self.size
                markup: True
                shorten: True
                shorten_from: "right"
    Label:
        font_size: 13
        halign: "right"
        valign: "middle"
        text: root.duration
        size_hint_x: None
        width: 40
        text_size: self.size
        markup: True
        shorten: True
        shorten_from: "right"
    

<Albumlist>:
    viewclass: 'Al_Selectable'
    SelectableRecycleBoxLayout:
        # default_size: None, dp(56)
        default_size: None, 45
        default_size_hint: 1, None
        size_hint_y: None
        height: self.minimum_height
        orientation: 'vertical'
        multiselect: False
        touch_multiselect: True
''')


# class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
#                                  RecycleBoxLayout):
#     ''' Adds selection and focus behavior to the view. '''


class Al_Selectable(RecycleDataViewBehavior, BoxLayoutB):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    option_selected=BooleanProperty(False)
    
    track=StringProperty('0')
    title=StringProperty('Song title')
    artist=StringProperty('Artist')
    plays=StringProperty('0 plays')
    duration=StringProperty('--:--')

    # cover=StringProperty('atlas://data/images/defaulttheme/player-play-overlay')
    # cover_size=NumericProperty(60)

    # image_cover=ObjectProperty(None)
    wartist=ObjectProperty(None)
    meta=ObjectProperty(None)

    # lcolor = ListProperty(Colors['gray'])

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(Al_Selectable, self).refresh_view_attrs(
            rv, index, data
            )

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if touch.button=='left':
            if super(Al_Selectable, self).on_touch_down(touch):
                return True
            if self.collide_point(*touch.pos) and self.selectable:
                self.touch_button='left'
                self.option_selected=False
                return self.parent.select_with_touch(self.index, touch)
        elif touch.button=='right':
            if super(Al_Selectable, self).on_touch_down(touch):
                return True
            if self.collide_point(*touch.pos) and self.selectable:
                self.touch_button='right'
                self.parent.parent.index_option_selected=self.index
                self.parent.parent.widget_option_selected=self
                self.parent.parent.dispatch('on_option_selection',self.index)
        else:
            self.option_selected=False
            self.touch_button=''        

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            pass
        else:
            pass
    def on_ref_press(self,instance, refvalue):
        self.parent.parent.index_ref_pressed
        self.parent.parent.dispatch('on_ref_press',refvalue)


class Albumlist(RecycleView):
    padding=VariableListProperty([0, 0, 0, 0])
    spacing=NumericProperty(0)
    # 
    data_selected=ListProperty([])
    index_selected=ListProperty([])

    selected_color=ListProperty([.5, 0.5, .5, .3])
    option_selected_color=ListProperty([.5, 0, 0, .6])
    widget_option_selected=ObjectProperty(None)
    index_option_selected=NumericProperty()
    index_ref_pressed=NumericProperty()


    def __init__(self,data,keyboard_scroll=True, **kwargs):
        self.register_event_type('on_ref_press')
        self.register_event_type('on_selection')
        self.register_event_type('on_option_selection')

        super(Albumlist, self).__init__(**kwargs)
        self.data=data
        self.layout_manager.bind(selected_nodes=self._select)

    def on_ref_press(self, refvalue):
        # print(self,instance, refvalue)
        pass
    def _select(self,*largs):
        # print(largs)
        if largs[1]:
            self.index_selected=largs[1]
            
            self.data_selected=[]
            for s in largs[1]:
                self.data_selected.append(self.data[s])
            self.dispatch('on_selection',*largs)

    def on_selection(self,*largs):
        pass
    def on_option_selection(self,*largs):
        pass
    def scroll(self,val):
        self.scroll_y=val
    def scroll_top(self,val=1):
        self.scroll_y=val
    def scroll_bottom(self,val=0):
        self.scroll_y=val
    def scroll_into_view(self,index):
        ld=len(self.data)
        sv=1-(index)/(ld-1)
        self.scroll_y=sv

    def select(self,index):
        # self.soft_selected=index
        # print('selecting',index)
        self.children[0].select_node(index)

    def deselect(self,index):
        # print('deselecting',index)
        self.children[0].deselect_node(index)
    def select_all(self):
        for i in range(len(self.data)):
            self.children[0].select_node(i)
    def deselect_all(self):
        for i in range(len(self.data)):
            self.children[0].deselect_node(i)
    def clear_selection(self):
        self.children[0].clear_selection()







Builder.load_string('''
<Arl_Selectable>:
    spacing: 8
    padding: 8

    # lcolor: (1,0,0,1)
    
    wsubtitle: wsubtitle

    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: self.parent.parent.selected_color if self.parent and self.selected else (0, 0, 0, 0)
        Rectangle:
            pos: self.pos
            size: self.size
    AsyncImage:
        id: image_cover
        source: root.cover
        size_hint: None,None
        size: root.cover_size,root.cover_size
        pos_hint: {'center_x':0.5,'center_y':0.5}
    BoxLayout:
        # orientation: "vertical"
        # orientation: "horizontal"
        orientation: root.subtitle_orientation
        LabelB:
            text: root.title
            font_name: 'DejaVuSans.ttf'
            font_size: 15
            halign: "center"
            # valign: "bottom"
            valign: root.title_valign
            markup: True
            shorten: True
            shorten_from: "right"
            text_size: self.size
            bcolor: root.title_bcolor
        Label:
            text: root.subtitle
            font_name: 'DejaVuSans.ttf'
            id: wsubtitle
            font_size: 13
            color: (164/255,164/255,164/255,1)
            # halign: "left"
            
            valign: "top"
            shorten: True
            shorten_from: "right"
            text_size: self.size
            markup: True,
            
            halign: root.subtitle_halign
            size_hint_y: root.subtitle_size_hint_y

            on_ref_press: root.on_ref_press(*args)
    # Label:
    #     font_size: 13
    #     halign: "right"
    #     valign: "middle"
    #     markup: True
    #     text: root.duration
    #     size_hint_x: None
    #     width: root.duration_width
    #     text_size: self.size
    #     shorten: True
    #     shorten_from: "right"
    

<Artistlist>:
    viewclass: 'Arl_Selectable'
    SelectableRecycleGridLayout:
        spacing: 8
        default_size: root.default_size
        default_size_hint: root.default_size_hint

        size_hint_y: None
        # size_hint_min_x: 100
        height: self.minimum_height
        width: self.minimum_width
        orientation: 'lr-tb'
        multiselect: False
        touch_multiselect: True
        cols: root.cols
        rows: root.rows

''')


class SelectableRecycleGridLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleGridLayout):
    ''' Adds selection and focus behavior to the view. '''


class Arl_Selectable(RecycleDataViewBehavior,kvb.HoverHighlightBehavior, BoxLayoutB):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    option_selected=BooleanProperty(False)
    touch_button=OptionProperty('',options=('','left','right'))

    title=StringProperty('')
    subtitle=StringProperty('')
    
    title_valign=OptionProperty('middle',options=('bottom','middle','center','top'))
    title_bcolor= ListProperty([0, 0, 0, 0])

    orientation=OptionProperty('vertical',options=('vertical','horizontal'))

    subtitle_orientation=OptionProperty('vertical',options=('vertical','horizontal'))

    subtitle_halign=OptionProperty('center',options=('auto','left','center','right','justify'))

    # album=StringProperty('')
    # lcolor=ListProperty([0,0,0,0])

    cover=StringProperty('atlas://data/images/defaulttheme/player-play-overlay')
    cover_size=NumericProperty(100)
    
    # duration=StringProperty('--:--')
    # duration_width=NumericProperty(40)
    subtitle_size_hint_y=NumericProperty(1)

    # image_cover=ObjectProperty(None)
    wsubtitle=ObjectProperty(None)
    meta=ObjectProperty(None)


    

    # lcolor = ListProperty(Colors['gray'])

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        # if rv.option_selected:
        #     data['option_selected']=True
        # else:
        #     data['option_selected']=False

        return super(Arl_Selectable, self).refresh_view_attrs(
            rv, index, data
            )

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        
        if touch.button=='left':
            if super(Arl_Selectable, self).on_touch_down(touch):
                return True
            if self.collide_point(*touch.pos) and self.selectable:
                self.touch_button='left'
                self.option_selected=False
                return self.parent.select_with_touch(self.index, touch)
        elif touch.button=='right':
            if super(Arl_Selectable, self).on_touch_down(touch):
                return True
            if self.collide_point(*touch.pos) and self.selectable:
                self.touch_button='right'
                # return self.parent.select_with_touch(self.index, touch)
                # self.option_selected=True
                self.parent.parent.index_option_selected=self.index
                self.parent.parent.widget_option_selected=self
                # self.parent.parent._purge_other_options(self.index)
                #Clock.schedule_once(lambda dt: self.parent.parent._purge_other_options(self.index) )
                # self.parent.parent.dispatch('on_purge_other_options',self.index)
                self.parent.parent.dispatch('on_option_selection',self.index)
        else:
            self.option_selected=False
            self.touch_button=''


    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        # if self.touch_button=='left':
        #     print('selected')
        #     self.selected = is_selected
        # elif self.touch_button=='right':
        #     self.option_selected
        #     print('o-selected')
        # else:
        #     print('none-selected')
        #     self.selected=False
        #     self.option_selected=False
        if is_selected:
            # print("selection changed to {0}".format(rv.data[index]))
            # self.parent.parent.dispatch('on_selection',index,rv.data[index])            
            pass
        else:
            # print("selection removed for {0}".format(rv.data[index]))
            pass
    def on_ref_press(self,instance, refvalue):
        pass
        # self.parent.parent.on_ref_press()
        self.parent.parent.index_ref_pressed=self.index
        self.parent.parent.dispatch('on_ref_press',refvalue)
    #     # print(args)
    #     get_kvApp().trigger_event(f"{self.parent.parent.id}/ref/{refvalue}")


class Artistlist(RecycleView):
    scroll_type= ['bars','content']
    # 
    data_selected=ListProperty([])
    index_selected=ListProperty([])
    # selected_color=ListProperty([.0, 0.9, .1, .3])
    selected_color=ListProperty([.5, 0.5, .5, .3])
    # option_selected_color=ListProperty([.5, 0.5, .5, .6])
    option_selected_color=ListProperty([.5, 0, 0, .6])
    widget_option_selected=ObjectProperty(None)
    index_option_selected=NumericProperty()
    index_ref_pressed=NumericProperty()

    default_size=ListProperty([None, 160])
    default_size_hint=ListProperty([1, None])

    cols=NumericProperty(None)
    rows=NumericProperty(None)



    def __init__(self,data,keyboard_scroll=True, **kwargs):
        self.register_event_type('on_ref_press')
        self.register_event_type('on_selection')
        self.register_event_type('on_option_selection')
        # self.register_event_type('on_purge_other_options')

        super(Artistlist, self).__init__(**kwargs)
        self.data=data
        self.layout_manager.bind(selected_nodes=self._select)

    def on_ref_press(self, refvalue):
        # print(self,instance, refvalue)
        pass
    def _select(self,*largs):
        # print(largs)
        if largs[1]:
            self.index_selected=largs[1]
            
            self.data_selected=[]
            # oscount=0
            for s in largs[1]:
                # print(self.data[s])
                # if s['option_selected']:
                #     oscount+=1
                self.data_selected.append(self.data[s])
            self.dispatch('on_selection',*largs)
            # if oscount:
            #     self.dispatch('on_option_selection',*largs)
            # else:
            #     self.dispatch('on_selection',*largs)
    # def on_purge_other_options(self,index):
    #     data=self.data
    #     for i,e in enumerate( self.data ):
    #         if i!=index:
    #             data[i]['option_selected']=False
    #             data[i]['lcolor']=[0,0,0,0]
    #         else:
    #             data[i]['option_selected']=True
    #             data[i]['lcolor']=self.option_selected_color
    #         # print(data[i])
    #     self.data=data

    #     print('hell')


    def on_selection(self,*largs):
        pass
    def on_option_selection(self,*largs):
        pass

    def scroll(self,val):
        self.scroll_y=val
    def scroll_top(self,val=1):
        self.scroll_y=val
    def scroll_bottom(self,val=0):
        self.scroll_y=val
    def scroll_into_view(self,index):
        ld=len(self.data)
        sv=1-(index)/(ld-1)
        self.scroll_y=sv


    def select(self,index):
        # self.soft_selected=index
        # print('selecting',index)
        self.children[0].select_node(index)

    def deselect(self,index):
        # print('deselecting',index)
        self.children[0].deselect_node(index)
    def select_all(self):
        for i in range(len(self.data)):
            self.children[0].select_node(i)
    def deselect_all(self):
        for i in range(len(self.data)):
            self.children[0].deselect_node(i)
    def clear_selection(self):
        self.children[0].clear_selection()























class HoldButton(kvButton):
    is_held = BooleanProperty(False)
    repeat_delay = 0.5  # seconds before repeating starts
    repeat_interval = 0.1  # seconds between repeats
    
    def __init__(self, **kwargs):
        self.register_event_type('on_repeat')
        super(HoldButton, self).__init__(**kwargs)
        self._repeat_clock = None
        self._initial_press_fired = False
    
    def on_press(self):
        self.is_held = True
        self._initial_press_fired = False
        
        # Fire the first event immediately
        self.dispatch('on_repeat')
        self._initial_press_fired = True
        
        # Schedule the repeating action after a delay
        self._repeat_clock = Clock.schedule_once(
            self._start_repeating, 
            self.repeat_delay
        )
    
    def on_release(self):
        self.is_held = False
        if self._repeat_clock:
            Clock.unschedule(self._repeat_clock)
            self._repeat_clock = None
        Clock.unschedule(self._repeated_action)
    
    def _start_repeating(self, dt):
        if self.is_held:
            # Start repeating at the specified interval
            self._repeat_clock = Clock.schedule_interval(
                self._repeated_action, 
                self.repeat_interval
            )
    
    def _repeated_action(self, dt):
        if self.is_held:
            self.dispatch('on_repeat')
        else:
            Clock.unschedule(self._repeated_action)
    
    def on_repeat(self):
        pass



# class FocusFlatButtonA(FocusBehavior,FlatButtonA):
#     pass


KV = """
#:import Calendar calendar.Calendar

<Day@FlatButtonA>:
    datepicker: self.parent.datepicker
    color: [1,1,1,0]
    # background_color: root.color if self.text != "" else [0,0,0,0]
    bcolor_normal: root.color if self.text != "" else [0,0,0,0]
    lcolor: [.345,.345,.345,1] if self.text != "" else [0,0,0,0]
    disabled: True if self.text == "" else False
    on_release:
        root.datepicker.picked = [int(self.text), root.datepicker.month, root.datepicker.year]
        focus: True
<Week@BoxLayout>:
    datepicker: root.parent
    weekdays: ["","","","","","",""]
    Day:
        text: str(root.weekdays[0])
    Day:
        text: str(root.weekdays[1])
    Day:
        text: str(root.weekdays[2])
    Day:
        text: str(root.weekdays[3])
    Day:
        text: str(root.weekdays[4])
    Day:
        text: str(root.weekdays[5])
    Day:
        text: str(root.weekdays[6])
<WeekDays@BoxLayout>:
    Label:
        text: "Mon"
    Label:
        text: "Tue"
    Label:
        text: "Wed"
    Label:
        text: "Thu"
    Label:
        text: "Fri"
    Label:
        text: "Sat"
    Label:
        text: "Sun"
<NavBar@BoxLayout>:
    datepicker: self.parent
    Spinner:
        background_color: [31/255,136/255,217/255,1]
        values: root.datepicker.months
        text: root.datepicker.months[root.datepicker.month-1]
        on_text:
            root.datepicker.month = root.datepicker.months.index(self.text)+1
    Spinner:
        # values: [str(i) for i in range(1970,2100)]
        values: [str(i) for i in range(root.datepicker.year+5,root.datepicker.year-20,-1)]
        text: str(root.datepicker.year)
        on_text:
            root.datepicker.year = int(self.text)
    Widget:
    HoldButton:
        text: "<"
        font_size: 20
        on_repeat:
            if root.datepicker.month == 1 and spin.text == "Month": root.datepicker.year -= 1
            if spin.text == "Month": root.datepicker.month = 12 if root.datepicker.month == 1 else root.datepicker.month - 1
            if spin.text == "Year": root.datepicker.year -= 1
    Spinner:
        id: spin
        values: ["Month","Year"]
        text: "Year"
        background_normal: 'atlas://skdata/sktheme/spinner'
        color: 0,0,0,1
        background_color: .9,.9,.9,1
    HoldButton:
        text: ">"
        font_size: 20
        on_repeat:
            if root.datepicker.month == 12 and spin.text == "Month": root.datepicker.year += 1
            if spin.text == "Month": root.datepicker.month = 1 if root.datepicker.month == 12 else root.datepicker.month + 1
            if spin.text == "Year": root.datepicker.year += 1
<DatePicker@BoxLayout>:
    # year: 2020
    # month: 1
    year: 2020
    month: 1
    padding: 8
    picked: ["","",""]
    months: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    calendar: Calendar()
    days: [(i if i > 0 else "") for i in self.calendar.itermonthdays(self.year, self.month)] + [""] * 14
    orientation: "vertical"
    NavBar:
    WeekDays:
    Week:
        weekdays: root.days[0:7]
    Week:
        weekdays: root.days[7:14]
    Week:
        weekdays: root.days[14:21]
    Week:
        weekdays: root.days[21:28]
    Week:
        weekdays: root.days[28:35]
    Week:
        weekdays: root.days[35:]
    LabelB:
        text: "" if root.picked == ["","",""] else "{}/{}-{}".format(root.picked[0], root.picked[1], root.picked[2])
        lcolor: .5,.5,.5,1
        valign: "middle"
        halign: "center"
        font_name: 'Roboto-Bold.ttf'
"""#.replace('__year__',str(current_date.year)).replace('__month__',str(current_date.month))
Builder.load_string(KV)
class DatePicker(BoxLayout):
    pass
    year=NumericProperty(2020)
    month=NumericProperty(1)
    # def on_date_selected(self,dmy):
    #     print(dmy)




# class SpinnerOptionB(SpinnerOptionB):
#     background_normal=''
#     pass

#-----------------------------------------



Builder.load_string("""
<ProgressBarB>:
    canvas:
        Color:
            rgb: 1, 1, 1
        BorderImage:
            border: (12, 12, 12, 12)
            pos: self.x, self.center_y - 12
            size: self.width, 24
            source: 'atlas://skdata/sktheme/pb_bg'
        BorderImage:
            border: [int(min(self.width * (self.value / float(self.max)) if self.max else 0, 12))] * 4
            pos: self.x, self.center_y - 12
            size: self.width * (self.value / float(self.max)) if self.max else 0, 24
            source: 'atlas://skdata/sktheme/pb_fg'
""")

class ProgressBarB(ProgressBar):
    pass

Builder.load_string("""
<ProgressBarC>:
    bcolor: .298, .298, .298, 1
    fcolor: 1, 0, .2, 1
    
    canvas:
    # canvas.before:
        Color:
            rgba: self.bcolor
        Rectangle:
            # border: (12, 12, 12, 12)
            # pos: self.x, self.center_y - 12
            pos: self.x, self.center_y - self.height/2
            # size: self.width, 24
            size: self.width, self.height

        Color:
            rgba: self.fcolor
        Rectangle:
            # border: [int(min(self.width * (self.value / float(self.max)) if self.max else 0, 12))] * 4
            # pos: self.x, self.center_y - 12
            pos: self.x, self.center_y - self.height/2
            # size: self.width * (self.value / float(self.max)) if self.max else 0, 24
            size: self.width * (self.value / float(self.max)) if self.max else 0, self.height
""")

class ProgressBarC(ProgressBar):
    bcolor= ListProperty([.298, .298, .298, 1])
    fcolor= ListProperty([1, 0, .2, 1])



#-----------------------------------------


class LabelCheck(kvw.BoxLayoutB):
    active=BooleanProperty(CheckBox.active.defaultvalue)
    group=ObjectProperty(CheckBox.group.defaultvalue)
    label_args=ObjectProperty({})
    check_args=ObjectProperty({})
    # max_lines=NumericProperty(1)

    def __init__(self,**kwargs):
        _label_args=kwargs.pop('label_args',{})
        _check_args=kwargs.pop('check_args',{})

        for k in ('text','halign','valign','markup','max_lines'):
            _label_args[k]=kwargs.pop(k,getattr(kvw.LabelA,k).defaultvalue)
        
        for k in ('active','background_checkbox_disabled_down','background_checkbox_disabled_normal',
            'background_checkbox_down','background_checkbox_normal','background_radio_disabled_down',
            'background_radio_disabled_normal','background_radio_down','background_radio_normal','group'):
            _check_args[k]=kwargs.pop(k,getattr(CheckBox,k).defaultvalue)
        

        self._label=LabelB(**_label_args)
        self._check=CheckBox(size_hint_x=None,**_check_args)


        super(LabelCheck, self).__init__(**kwargs)


        self._check.bind(active=lambda *x:self.setter('active')(*x))

        self.add_widget(self._check)
        self.add_widget(self._label)

    def on_active(self,ins,val):
        self._check.active=val

    def on_label_args(self,ins,val):
        for k,v in val.items():
            setattr(self._label,k,v)
    def on_check_args(self,ins,val):
        for k,v in val.items():
            setattr(self._check,k,v)

    def _get_text(self):
        return self._label.text
    def _set_text(self,val):
        self._label.text=val
    text=kvw.AliasProperty(_get_text,_set_text,cache=True)

    def _get_cwidth(self):
        return self._check.width
    def _set_cwidth(self,val):
        self._check.width=val
    cwidth=kvw.AliasProperty(_get_cwidth,_set_cwidth,cache=True)