from kivy.clock import Clock
from .utils import Colors
from kivy.properties import BooleanProperty,NumericProperty,StringProperty,ListProperty,ObjectProperty
from kivy.graphics import Ellipse,Color,Rectangle,Line

# from .utils import get_kvWindow
from . import utils
from .utils import resolve_color
from kivy.uix.behaviors import ButtonBehavior as _ButtonBehavior
#--------------------------------------------------------------------------------------------------------------------------------
# hi=0
_other_highlighted=None
_other_highlighted_pos=(-1,-1)
class HoverHighlightBehavior(object):
    hovered = BooleanProperty(False)
    border_point= ObjectProperty(None)
    bcolor_normal = ListProperty([0, 0, 0, 0])
    bcolor_down = ListProperty([.2, .64, .8, 1])
    bcolor = ListProperty([0, 0, 0, 0])
    tooltip_text=StringProperty('')
    tooltip_args=ObjectProperty({})
    _higlight_color=[1,1,1,1]
    do_highlight=BooleanProperty(True)


    def __init__(self, **kwargs):
        self.kvWindow=utils.Window
        self.bind(bcolor_down=self._set_highlight_color)
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        to_parent=kwargs.pop('to_parent',False)
        self.bcolor_normal=kwargs.get('bcolor_normal',kwargs.get('bcolor',self.bcolor_normal))
        self.kvWindow.bind(mouse_pos=self.on_mouse_pos_parent)
        # if to_parent:
        #     self.kvWindow.bind(mouse_pos=self.on_mouse_pos_parent)
        # else:
        #     self.kvWindow.bind(mouse_pos=self.on_mouse_pos_widget)
        super(HoverHighlightBehavior, self).__init__(**kwargs)
        self._set_highlight_color(self,self.bcolor_down)
    def _set_highlight_color(self,ins,bcolor_down):
        self._higlight_color=utils.darken_rgba(bcolor_down,.66)

    def on_mouse_pos_widget(self, *args):
        # print(self,self.to_widget(*self.pos),self.to_local(*self.pos),self.to_window(*self.pos),self.to_parent(*self.pos))
        if not self.get_root_window():
            return
        
        pos = args[1]
        # inside = self.collide_point(*self.to_widget(*pos))
        inside = self.collide_point(*self.to_widget(*self.kvWindow.mouse_pos))

        if self.hovered == inside:
            return
        self.border_point = pos
        self.hovered = inside
        
        if self.tooltip_text:
            
            if inside:
                Clock.schedule_once(self._on_tooltip,.5)
                self.dispatch('on_enter')
            else:
                self.dispatch('on_leave')
                Clock.unschedule(self._on_tooltip)
        else:

            if inside:
                self.dispatch('on_enter')
            else:
                self.dispatch('on_leave')
    def on_mouse_pos_parent(self, *args):
        global _other_highlighted,_other_highlighted_pos

        if not self.get_root_window():
            return
        
        pos = args[1]
        try:
            inside = self.collide_point(*self.parent.to_widget(*pos))
        except:
            inside = self.collide_point(*self.to_widget(*pos))
        # inside = self.collide_point(*self.to_widget(*self.kvWindow.mouse_pos))

        if self.hovered == inside:
            return
        # print('here',inside,hi)
        # hi+=1
        self.border_point = pos
        self.hovered = inside
        
        if self.tooltip_text:
            
            if inside:
                Clock.schedule_once(self._on_tooltip,.5)
                # self.dispatch('on_enter')

                if _other_highlighted:
                    _other_highlighted.on_mouse_pos_parent(*(None,(-1,-1)))
                self.dispatch('on_enter')
                _other_highlighted=self
                _other_highlighted_pos=self.to_window(*self.pos)

            else:
                self.dispatch('on_leave')
                Clock.unschedule(self._on_tooltip)
        else:

            if inside:
                # self.dispatch('on_enter')

                if _other_highlighted:
                    _other_highlighted.on_mouse_pos_parent(*(None,(-1,-1)))
                self.dispatch('on_enter')
                _other_highlighted=self
                _other_highlighted_pos=self.to_window(*self.pos)

            else:
                self.dispatch('on_leave')
    def _on_tooltip(self,dt):
        _app=utils.get_kvApp()
        _app._tooltip(self.tooltip_text,**self.tooltip_args)

    def on_enter(self):
        # self.bcolor=self.bcolor_down[:3]+[self.bcolor_down[-1]/2]
        # print('entering:',self)
        if self.do_highlight:
            self.bcolor=self._higlight_color
        
    

    def on_leave(self):
        global _other_highlighted,_other_highlighted_pos
        # print('leaving:',self)
        # self.bcolor=self.bcolor_normal
        wpos=self.to_window(*self.pos)
        if _other_highlighted_pos==wpos:
        # if _other_highlighted==self:
            _other_highlighted=None
            _other_highlighted_pos=(-1,-1)
            # Clock.schedule_once(lambda dt:setattr(HoverHighlightBehavior,'_other_highlighted',None))

        if self.do_highlight:
            if getattr(self,'selected',False):
                self.bcolor=getattr(self,'selected_color',self.bcolor_normal)
            else:
                self.bcolor=self.bcolor_normal


class HoverBehavior(object):
    hovered = BooleanProperty(False)
    border_point= ObjectProperty(None)
    tooltip_text=StringProperty('')
    tooltip_args=ObjectProperty({})
    _other_highlighted=None
    def __init__(self, **kwargs):
        self.kvWindow=utils.Window
        self.register_event_type('on_enter')
        self.register_event_type('on_leave')
        # self.register_event_type('on_over')
        self.kvWindow.bind(mouse_pos=self.on_mouse_pos_parent)
        # super(HoverHighlightBehavior, self).__init__(**kwargs)
        super(HoverBehavior, self).__init__(**kwargs)
    def on_mouse_pos_parent(self, *args):
        global _other_highlighted
        if not self.get_root_window():
            return
        
        pos = args[1]
        # inside = self.collide_point(*self.to_widget(*self.kvWindow.mouse_pos))
        try:
            inside = self.collide_point(*self.parent.to_widget(*pos))
        except:
            inside = self.collide_point(*self.to_widget(*pos))
        if self.hovered == inside:
            return
        self.border_point = pos
        self.hovered = inside
        
        if self.tooltip_text:
            
            if inside:
                Clock.schedule_once(self._on_tooltip,.5)
                # self.dispatch('on_enter')

                # if _other_highlighted:
                #     _other_highlighted.on_mouse_pos_parent(*(None,(-1,-1)))
                self.dispatch('on_enter')
                # _other_highlighted=self
                # _other_highlighted_pos=self.to_window(*self.pos)

            else:
                Clock.unschedule(self._on_tooltip)
                self.dispatch('on_leave')
        else:

            if inside:
                # self.dispatch('on_enter')

                # if _other_highlighted:
                #     _other_highlighted.on_mouse_pos_parent(*(None,(-1,-1)))
                self.dispatch('on_enter')
                # _other_highlighted=self
                # _other_highlighted_pos=self.to_window(*self.pos)

            else:
                self.dispatch('on_leave')
    def on_mouse_pos(self, *args):
        if not self.get_root_window():
            return
        
        pos = args[1]
        # inside = self.collide_point(*self.to_widget(*pos))
        inside = self.collide_point(*self.to_widget(*self.kvWindow.mouse_pos))
        # if inside:
        #     self.dispatch('on_over')
        # print('pos')
        if self.hovered == inside:
            return
        self.border_point = pos
        self.hovered = inside
        
        if self.tooltip_text:
            
            if inside:
                self.dispatch('on_enter')
                Clock.schedule_once(self._on_tooltip,.5)
                
            else:
                self.dispatch('on_leave')
                Clock.unschedule(self._on_tooltip)
        else:

            if inside:
                self.dispatch('on_enter')
            else:
                self.dispatch('on_leave')
    def _on_tooltip(self,dt):
        _app=utils.get_kvApp()
        _app._tooltip(self.tooltip_text,**self.tooltip_args)

    def on_enter(self):
        pass
    # def on_over(self):
    #     pass

    def on_leave(self):
        pass
        # global _other_highlighted,_other_highlighted_pos
        # wpos=self.to_window(*self.pos)
        # # if _other_highlighted==self:
        # if _other_highlighted_pos==wpos:
        #     _other_highlighted=None
        #     _other_highlighted_pos=(-1,-1)


from kivy.uix.behaviors import ToggleButtonBehavior




class ToggleButtonBehavior2(ToggleButtonBehavior):

    def __init__(self,**kwargs):
        self.register_event_type('on_option')
        super(ToggleButtonBehavior2, self).__init__(**kwargs)
    
    def __do_press(self):
        if (not self.allow_no_selection and
                self.group and self.state == 'down'):
            return

        self._release_group(self)
        self.state = 'normal' if self.state == 'down' else 'down'

    def _do_press(self):
        if self.last_touch:
            if self.last_touch.button=='left':
                return self.__do_press()
            if self.last_touch.button=='right':
                self.dispatch('on_option')
        else:
            return self.__do_press()
    def on_option(self):
        pass
    def on_state(self,instance, value):
        if value == 'down':
            self.bcolor=self.bcolor_down
        else:
            self.bcolor=self.bcolor_normal






class GridNavigationBehavior(ToggleButtonBehavior,object):
    last_index=NumericProperty(None)
    selected=ObjectProperty(None)
    soft_selected=ObjectProperty(None)
    navigable=True
    # _prev_colors={}

    color_soft=ListProperty([0.31, 160/255, 76/255, .3])  # line color
    color_sel=ListProperty([0.31, 160/255, 76/255, 1])  # line color
    _lcolor = ListProperty([1, 0, 0, 0])  # line color
    _lwidth = NumericProperty(2)          # line width
    # _line=None

    def __init__(self, **kwargs):
        self.kvWindow=utils.Window
        self.register_event_type('on_select')
        # self.register_event_type('on_leave')
        # self.kvWindow.bind(mouse_pos=self.on_mouse_pos)
        super(GridNavigationBehavior, self).__init__(**kwargs)
        
            # print('here hja')
            # self._do_press()
            # self._do_release()
        # self.on_state(self,self.state)
        # if self.state=='down':
        #     Clock.schedule_once(lambda dt: self.on_state(self,self.state))
            # Clock.schedule_once(lambda dt: self._do_release(),.1)
        
        Clock.schedule_once(self._init)
    # @property
    # def line(self):
    #     if not self._line:
    #         with self.canvas.after:

    #             self.line_color = Color(self.color_soft)
    #             self._line = Line(width=self._lwidth, rectangle=(
    #                 self.x, self.y, 0, 0
    #             ))
    #     return self._line

    def _init(self,dt):
        
        
        self.bind(selected=self._update_canvas_sel)
        self.bind(soft_selected=self._update_canvas_soft)
        
        # Bind properties to update visuals
        self.bind(
            _lcolor=self._update_lcolor,
            _lwidth=self._update_lwidth,
        )
        # self._ensure_keyboard()
        # Clock.schedule_once(lambda dt: self.on_state(self,self.state))
        if self.state=='down':
            setattr(self,'lcolor',(.5,.5,.5,.5))
            Clock.schedule_once(lambda dt: self._update_canvas_soft(self,self.soft_selected))


    def _update_canvas_sel(self, ins,w):
        """Update the canvas elements when position or size changes"""
        if w and self.state=='down':
            self._lcolor=self.color_sel
        else:
            self._lcolor=self.color_soft
            # self.line.rectangle = (w.x, w.y, w.width, w.height)
    # def _update_rect(self,dt):
    #     self.line.rectangle = (w.x, w.y, w.width, w.height)
    def _update_canvas_soft(self,ins,w):
        # print(f"{w =}")
        if w:
            if not hasattr(self,'line'):
                with self.canvas.after:
                    self.line_color = Color()
                    self.line_color.rgba=resolve_color( self.color_soft)
                    self.line = Line(width=self._lwidth, rectangle=(
                        w.x, w.y, w.width, w.height
                    ))
            else:
                self._lcolor=self.color_soft
                self.line.rectangle = (w.x, w.y, w.width, w.height)
            # Clock.schedule_once(lambda dt:setattr(self.line,'rectangle',(w.x, w.y, w.width, w.height)))
        else:
            self._lcolor=[0,0,0,0]

    
    def _update_lcolor(self, instance, value):
        """Update line color"""
        if hasattr(self,'line_color'):
            self.line_color.rgba = resolve_color( value)
        else:
            self.line_color = Color(self.color_soft)
            self.line_color.rgba = resolve_color( value)
    
    def _update_lwidth(self, instance, value):
        """Update line width"""
        self.line.width = value


    def on_select_action(self):
        self.set_group_siblings(state='normal')
        self.state='down'

    def set_group_siblings(self,state):
        for w in self.get_widgets(self.group):
            w.state='normal'
    def _ensure_keyboard(self):
        self._keyboard=self.kvWindow.request_keyboard(
            self._keyboard_closed, self, 'text')
        
    def _keyboard_closed(self):
        # print('My keyboard have been closed!')
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None
    def soft_select(self,index):
        # print(f"soft_select: {index}")
        if index==None:
            index=-1
        # print('called:',index)
        lc=len(self.children)
        if index<0:
            index=lc+index
        elif index>=lc:
            index=index-lc
        # print('final index:',index,f'{lc = }')
        w=self.children[index]
        # self._prev_colors[index]={'b':getattr(w,'bcolor',[0,0,0,0]),'l':getattr(w,'lcolor',[0,0,0,0])}

        # setattr(w,'bcolor',(41/255,41/255,41/255,.5))
        # setattr(w,'lcolor',(41/255,41/255,41/255,.75))
        self.soft_selected=w
        
        if index!=self.last_index:
            self.soft_unselect(self.last_index)

        # print(f"{self.last_index = }, {index = }")
        

        self.last_index=index
    def select(self,index=None):
        if index==None:
            index=self.last_index
        w=self.children[index]
        
        # self._prev_colors[index]={'b':getattr(w,'bcolor',[0,0,0,0]),'l':getattr(w,'lcolor',[0,0,0,0])}

        # setattr(w,'bcolor',(41/255,41/255,41/255,.5))
        # setattr(w,'lcolor',(1,1,1,1))
        self.selected=w
        self.dispatch('on_select',index)
        if hasattr(w,'on_select_action'):
            w.on_select_action()
        elif hasattr(w,'focus'):
            w.focus=True
            def on_defocus(ins,val):
                if not val:
                    w.unbind(focus=on_defocus)
                    self.on_select_action()
            w.bind(focus=on_defocus)
        elif hasattr(w,'trigger_action'):
            w.trigger_action()
    
    def soft_unselect(self,index):
        if index!=None:
            lw=self.children[index]
            # self.selected=False
            # setattr(lw,'bcolor',(41/255,41/255,41/255,0))
            # setattr(lw,'lcolor',(41/255,41/255,41/255,0))
            
            # setattr(lw,'bcolor',self._prev_colors.get(index,[0,0,0,0])['b'])
            # setattr(lw,'lcolor',self._prev_colors.get(index,[0,0,0,0])['l'])


    def on_state(self, widget, value):
        self._ensure_keyboard()
        if value=='down':
            setattr(self,'lcolor',(.5,.5,.5,.5))
            self._lcolor=self.color_soft
            
            # self.soft_select(self.last_index)
            Clock.schedule_once(lambda dt: self.soft_select(self.last_index))

            self._keyboard.bind(on_key_down=self._on_keyboard_down)
            
        else:
            setattr(self,'lcolor',(.5,.5,.5,0))
            self._lcolor=[0,0,0,0]
            self._keyboard.unbind(on_key_down=self._on_keyboard_down)
            self.soft_unselect(self.last_index)

    def on_select(self,index):
        pass
    def prev_navigable(self):
        wids=self.get_widgets(self.group)
        lwids=len(wids)
        myi=wids.index(self)
        # print(myi)
        previ=myi-1
        if previ>=lwids:
            previ=previ-lwids
        self.state='normal'
        wids[previ].state='down'

        del wids
    def next_navigable(self):
        wids=self.get_widgets(self.group)
        lwids=len(wids)
        myi=wids.index(self)
        nexti=myi+1
        if nexti>=lwids:
            nexti=nexti-lwids
        self.state='normal'
        wids[nexti].state='down'
        del wids
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # print('The key', keycode, 'have been pressed')
        # print(' - modifiers are %r' % modifiers)

        # print(self.rows,self.cols)
        lc=len(self.children)
        
        if keycode[1]=='right':
            self.soft_select(self.last_index-1)
        elif keycode[1]=='left':
            self.soft_select(self.last_index+1)
        elif keycode[1]=='up':
            if self.rows:
                self.soft_select(self.last_index+lc//self.rows)
        elif keycode[1]=='down':
            if self.rows:
                self.soft_select(self.last_index-lc//self.rows)
        elif keycode[1] in ('enter','spacebar'):
            self.select(self.last_index)
        elif keycode[1] =='tab':
            if 'shift' in modifiers:
                self.prev_navigable()
            else:
                self.next_navigable()
        elif keycode[1]=='escape':
            # self.soft_unselect(self.last_index)
            self.selected=False
            if self.parent:
                if getattr(self.parent,'navigable',False):
                    self._lcolor=[0,0,0,0]
                    self.lcolor=[0,0,0,0]
                    self.parent.state='normal'
                    self.parent._do_press()

                    # self.parent._do_release()
                    # self.parent.selected=False

            

            # del wids


        return True



#--------------------------------------------------------------------------------------------------------------------------------

class TouchBehavior:
    duration_long_touch = NumericProperty(0.4)
    """
    Time for a long touch.

    :attr:`duration_long_touch` is an :class:`~kivy.properties.NumericProperty`
    and defaults to `0.4`.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ntouchs=0
        self.bind(
            # on_touch_down=self.create_clock,
            # on_touch_up=self.delete_clock,
            # on_touch_up=self.create_clock,
            # on_touch_up=self.delete_clock,
            on_release=self.create_clock,
        )
        self.event = Clock.schedule_once(self.return_to_0,0.25)
    def return_to_0(self,*args):
        self.ntouchs=0

    def create_clock(self, *args):
    # def create_clock(self, widget, touch, *args):
        # if self.collide_point(touch.x, touch.y):
        #     if "event" not in touch.ud:
        #         callback = partial(self.on_long_touch, touch)
        #         Clock.schedule_once(callback, self.duration_long_touch)
        #         touch.ud["event"] = callback
        # print(self,widget)
        # print(touch.pos)

        self.ntouchs+=1

        self.event()
        # print(self.ntouchs)

        if self.ntouchs>=2:
            self.on_double_tap(*args)
        elif self.ntouchs==1:
            self.on_single_tap(*args)
        # if touch.is_triple_tap:
        #     self.on_triple_tap(touch, *args)

    def delete_clock(self, widget, touch, *args):
        """Removes a key event from `touch.ud`."""

        # if self.collide_point(touch.x, touch.y):
        #     if "event" in touch.ud:
        #         Clock.unschedule(touch.ud["event"])
        #         del touch.ud["event"]

    def on_long_touch(self, touch, *args):
        """Fired when the widget is pressed for a long time."""

    def on_double_tap(self, touch, *args):
        """Fired by double-clicking on the widget."""
    def on_single_tap(self, touch, *args):
        """Fired by double-clicking on the widget."""

    def on_triple_tap(self, touch, *args):
        """Fired by triple clicking on the widget."""




























'''
Focus Behavior
==============

The :class:`~kivy.uix.behaviors.FocusBehavior`
`mixin <https://en.wikipedia.org/wiki/Mixin>`_ class provides
keyboard focus behavior. When combined with other
FocusBehavior widgets it allows one to cycle focus among them by pressing
tab. In addition, upon gaining focus, the instance will automatically
receive keyboard input.

Focus, very different from selection, is intimately tied with the keyboard;
each keyboard can focus on zero or one widgets, and each widget can only
have the focus of one keyboard. However, multiple keyboards can focus
simultaneously on different widgets. When escape is hit, the widget having
the focus of that keyboard will de-focus.

Managing focus
--------------

In essence, focus is implemented as a doubly linked list, where each
node holds a (weak) reference to the instance before it and after it,
as visualized when cycling through the nodes using tab (forward) or
shift+tab (backward). If a previous or next widget is not specified,
:attr:`focus_next` and :attr:`focus_previous` defaults to `None`. This
means that the :attr:`~kivy.uix.widget.Widget.children` list and
:attr:`parents <kivy.uix.widget.Widget.parent>` are
walked to find the next focusable widget, unless :attr:`focus_next` or
:attr:`focus_previous` is set to the `StopIteration` class, in which case
focus stops there.

For example, to cycle focus between :class:`~kivy.uix.button.Button`
elements of a :class:`~kivy.uix.gridlayout.GridLayout`::

    class FocusButton(FocusBehavior, Button):
      pass

    grid = GridLayout(cols=4)
    for i in range(40):
        grid.add_widget(FocusButton(text=str(i)))
    # clicking on a widget will activate focus, and tab can now be used
    # to cycle through

When using a software keyboard, typical on mobile and touch devices, the
keyboard display behavior is determined by the
:attr:`~kivy.core.window.WindowBase.softinput_mode` property. You can use
this property to ensure the focused widget is not covered or obscured by the
keyboard.

Initializing focus
------------------

Widgets needs to be visible before they can receive the focus. This means that
setting their *focus* property to True before they are visible will have no
effect. To initialize focus, you can use the 'on_parent' event::

    from kivy.app import App
    from kivy.uix.textinput import TextInput

    class MyTextInput(TextInput):
        def on_parent(self, widget, parent):
            self.focus = True

    class SampleApp(App):
        def build(self):
            return MyTextInput()

    SampleApp().run()

If you are using a :class:`~kivy.uix.popup`, you can use the 'on_open' event.

For an overview of behaviors, please refer to the :mod:`~kivy.uix.behaviors`
documentation.

.. warning::

    This code is still experimental, and its API is subject to change in a
    future version.
'''

__all__ = ('FocusBehavior', )

from kivy.properties import OptionProperty, ObjectProperty, BooleanProperty, \
    AliasProperty
from kivy.config import Config
from kivy.base import EventLoop

# When we are generating documentation, Config doesn't exist
_is_desktop = False
_keyboard_mode = 'system'
if Config:
    _is_desktop = Config.getboolean('kivy', 'desktop')
    _keyboard_mode = Config.get('kivy', 'keyboard_mode')


class FocusBehavior(object):
    '''Provides keyboard focus behavior. When combined with other
    FocusBehavior widgets it allows one to cycle focus among them by pressing
    tab. Please see the
    :mod:`focus behavior module documentation <kivy.uix.behaviors.focus>`
    for more information.

    .. versionadded:: 1.9.0

    '''

    _requested_keyboard = False
    _keyboard = ObjectProperty(None, allownone=True)
    _keyboards = {}

    ignored_touch = []
    '''A list of touches that should not be used to defocus. After on_touch_up,
    every touch that is not in :attr:`ignored_touch` will defocus all the
    focused widgets if the config keyboard mode is not multi. Touches on
    focusable widgets that were used to focus are automatically added here.

    Example usage::

        class Unfocusable(Widget):

            def on_touch_down(self, touch):
                if self.collide_point(*touch.pos):
                    FocusBehavior.ignored_touch.append(touch)

    Notice that you need to access this as a class, not an instance variable.
    '''

    def _set_keyboard(self, value):
        focus = self.focus
        keyboard = self._keyboard
        keyboards = FocusBehavior._keyboards
        if keyboard:
            self.focus = False    # this'll unbind
            if self._keyboard:  # remove assigned keyboard from dict
                del keyboards[keyboard]
        if value and value not in keyboards:
            keyboards[value] = None
        self._keyboard = value
        self.focus = focus

    def _get_keyboard(self):
        return self._keyboard
    keyboard = AliasProperty(_get_keyboard, _set_keyboard,
                             bind=('_keyboard', ))
    '''The keyboard to bind to (or bound to the widget) when focused.

    When None, a keyboard is requested and released whenever the widget comes
    into and out of focus. If not None, it must be a keyboard, which gets
    bound and unbound from the widget whenever it's in or out of focus. It is
    useful only when more than one keyboard is available, so it is recommended
    to be set to None when only one keyboard is available.

    If more than one keyboard is available, whenever an instance gets focused
    a new keyboard will be requested if None. Unless the other instances lose
    focus (e.g. if tab was used), a new keyboard will appear. When this is
    undesired, the keyboard property can be used. For example, if there are
    two users with two keyboards, then each keyboard can be assigned to
    different groups of instances of FocusBehavior, ensuring that within
    each group, only one FocusBehavior will have focus, and will receive input
    from the correct keyboard. See `keyboard_mode` in :mod:`~kivy.config` for
    more information on the keyboard modes.

    **Keyboard and focus behavior**

    When using the keyboard, there are some important default behaviors you
    should keep in mind.

    * When Config's `keyboard_mode` is multi, each new touch is considered
      a touch by a different user and will set the focus (if clicked on a
      focusable) with a new keyboard. Already focused elements will not lose
      their focus (even if an unfocusable widget is touched).

    * If the keyboard property is set, that keyboard will be used when the
      instance gets focused. If widgets with different keyboards are linked
      through :attr:`focus_next` and :attr:`focus_previous`, then as they are
      tabbed through, different keyboards will become active. Therefore,
      typically it's undesirable to link instances which are assigned
      different keyboards.

    * When a widget has focus, setting its keyboard to None will remove its
      keyboard, but the widget will then immediately try to get
      another keyboard. In order to remove its keyboard, rather set its
      :attr:`focus` to False.

    * When using a software keyboard, typical on mobile and touch devices, the
      keyboard display behavior is determined by the
      :attr:`~kivy.core.window.WindowBase.softinput_mode` property. You can use
      this property to ensure the focused widget is not covered or obscured.

    :attr:`keyboard` is an :class:`~kivy.properties.AliasProperty` and defaults
    to None.

    .. warning:

        When assigning a keyboard, the keyboard must not be released while
        it is still assigned to an instance. Similarly, the keyboard created
        by the instance on focus and assigned to :attr:`keyboard` if None,
        will be released by the instance when the instance loses focus.
        Therefore, it is not safe to assign this keyboard to another instance's
        :attr:`keyboard`.
    '''

    is_focusable = BooleanProperty(_is_desktop)
    '''Whether the instance can become focused. If focused, it'll lose focus
    when set to False.

    :attr:`is_focusable` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to True on a desktop (i.e. `desktop` is True in
    :mod:`~kivy.config`), False otherwise.
    '''

    focus = BooleanProperty(False)
    '''Whether the instance currently has focus.

    Setting it to True will bind to and/or request the keyboard, and input
    will be forwarded to the instance. Setting it to False will unbind
    and/or release the keyboard. For a given keyboard, only one widget can
    have its focus, so focusing one will automatically unfocus the other
    instance holding its focus.

    When using a software keyboard, please refer to the
    :attr:`~kivy.core.window.WindowBase.softinput_mode` property to determine
    how the keyboard display is handled.

    :attr:`focus` is a :class:`~kivy.properties.BooleanProperty` and defaults
    to False.
    '''

    focused = focus
    '''An alias of :attr:`focus`.

    :attr:`focused` is a :class:`~kivy.properties.BooleanProperty` and defaults
    to False.

    .. warning::
        :attr:`focused` is an alias of :attr:`focus` and will be removed in
        2.0.0.
    '''

    keyboard_suggestions = BooleanProperty(True)
    '''If True provides auto suggestions on top of keyboard.
    This will only work if :attr:`input_type` is set to `text`, `url`, `mail` or
    `address`.

    .. warning::
        On Android, `keyboard_suggestions` relies on
        `InputType.TYPE_TEXT_FLAG_NO_SUGGESTIONS` to work, but some keyboards
        just ignore this flag. If you want to disable suggestions at all on
        Android, you can set `input_type` to `null`, which will request the
        input method to run in a limited "generate key events" mode.

    .. versionadded:: 2.1.0

    :attr:`keyboard_suggestions` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to True
    '''

    def _set_on_focus_next(self, instance, value):
        '''If changing focus, ensure your code does not create an infinite loop.
        eg:
        ```python
        widget.focus_next = widget
        widget.focus_previous = widget
        ```
        '''
        next_ = self._old_focus_next
        if next_ is value:   # prevent infinite loop
            return

        if isinstance(next_, FocusBehavior):
            next_.focus_previous = None
        self._old_focus_next = value
        if value is None or value is StopIteration:
            return
        if not isinstance(value, FocusBehavior):
            raise ValueError('focus_next accepts only objects based on'
                             ' FocusBehavior, or the `StopIteration` class.')
        value.focus_previous = self

    focus_next = ObjectProperty(None, allownone=True)
    '''The :class:`FocusBehavior` instance to acquire focus when
    tab is pressed and this instance has focus, if not `None` or
    `StopIteration`.

    When tab is pressed, focus cycles through all the :class:`FocusBehavior`
    widgets that are linked through :attr:`focus_next` and are focusable. If
    :attr:`focus_next` is `None`, it instead walks the children lists to find
    the next focusable widget. Finally, if :attr:`focus_next` is
    the `StopIteration` class, focus won't move forward, but end here.

    .. note:

        Setting :attr:`focus_next` automatically sets :attr:`focus_previous`
        of the other instance to point to this instance, if not None or
        `StopIteration`. Similarly, if it wasn't None or `StopIteration`, it
        also sets the :attr:`focus_previous` property of the instance
        previously in :attr:`focus_next` to `None`. Therefore, it is only
        required to set one of the :attr:`focus_previous` or
        :attr:`focus_next` links since the other side will be set
        automatically.

    :attr:`focus_next` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    '''

    def _set_on_focus_previous(self, instance, value):
        prev = self._old_focus_previous
        if prev is value:
            return

        if isinstance(prev, FocusBehavior):
            prev.focus_next = None
        self._old_focus_previous = value
        if value is None or value is StopIteration:
            return
        if not isinstance(value, FocusBehavior):
            raise ValueError('focus_previous accepts only objects based'
                             'on FocusBehavior, or the `StopIteration` class.')
        value.focus_next = self

    focus_previous = ObjectProperty(None, allownone=True)
    '''The :class:`FocusBehavior` instance to acquire focus when
    shift+tab is pressed on this instance, if not None or `StopIteration`.

    When shift+tab is pressed, focus cycles through all the
    :class:`FocusBehavior` widgets that are linked through
    :attr:`focus_previous` and are focusable. If :attr:`focus_previous` is
    `None`, it instead walks the children tree to find the
    previous focusable widget. Finally, if :attr:`focus_previous` is the
    `StopIteration` class, focus won't move backward, but end here.

    .. note:

        Setting :attr:`focus_previous` automatically sets :attr:`focus_next`
        of the other instance to point to this instance, if not None or
        `StopIteration`. Similarly, if it wasn't None or `StopIteration`, it
        also sets the :attr:`focus_next` property of the instance previously in
        :attr:`focus_previous` to `None`. Therefore, it is only required
        to set one of the :attr:`focus_previous` or :attr:`focus_next`
        links since the other side will be set automatically.

    :attr:`focus_previous` is an :class:`~kivy.properties.ObjectProperty` and
    defaults to `None`.
    '''

    keyboard_mode = OptionProperty('auto', options=('auto', 'managed'))
    '''Determines how the keyboard visibility should be managed. 'auto' will
    result in the standard behavior of showing/hiding on focus. 'managed'
    requires setting the keyboard visibility manually, or calling the helper
    functions :meth:`show_keyboard` and :meth:`hide_keyboard`.

    :attr:`keyboard_mode` is an :class:`~kivy.properties.OptionsProperty` and
    defaults to 'auto'. Can be one of 'auto' or 'managed'.
    '''

    input_type = OptionProperty('null', options=('null', 'text', 'number',
                                                 'url', 'mail', 'datetime',
                                                 'tel', 'address'))
    '''The kind of input keyboard to request.

    .. versionadded:: 1.8.0

    .. versionchanged:: 2.1.0
        Changed default value from `text` to `null`. Added `null` to options.

        .. warning::
            As the default value has been changed, you may need to adjust
            `input_type` in your code.

    :attr:`input_type` is an :class:`~kivy.properties.OptionsProperty` and
    defaults to 'null'. Can be one of 'null', 'text', 'number', 'url', 'mail',
    'datetime', 'tel' or 'address'.
    '''

    unfocus_on_touch = BooleanProperty(_keyboard_mode not in
                                       ('multi', 'systemandmulti'))
    '''Whether a instance should lose focus when clicked outside the instance.

    When a user clicks on a widget that is focus aware and shares the same
    keyboard as this widget (which in the case with only one keyboard),
    then as the other widgets gain focus, this widget loses focus. In addition
    to that, if this property is `True`, clicking on any widget other than this
    widget, will remove focus from this widget.

    :attr:`unfocus_on_touch` is a :class:`~kivy.properties.BooleanProperty` and
    defaults to `False` if the `keyboard_mode` in :attr:`~kivy.config.Config`
    is `'multi'` or `'systemandmulti'`, otherwise it defaults to `True`.
    '''

    focus_color=ListProperty(Colors['r'])

    def __init__(self, **kwargs):
        self._old_focus_next = None
        self._old_focus_previous = None
        super(FocusBehavior, self).__init__(**kwargs)

        self._keyboard_mode = _keyboard_mode
        fbind = self.fbind
        fbind('focus', self._on_focus)
        fbind('disabled', self._on_focusable)
        fbind('is_focusable', self._on_focusable)
        fbind('focus_next', self._set_on_focus_next)
        fbind('focus_previous', self._set_on_focus_previous)

    def _on_focusable(self, instance, value):
        if self.disabled or not self.is_focusable:
            self.focus = False
    def on_parent(self,widget,parent):
        self._lastcolor=getattr(self,'lcolor',None)

    def _on_focus(self, instance, value, *largs):
        
        if value:
            self.lcolor=self.focus_color

        else:
            self.lcolor=getattr(self,'_lastcolor',None)

        if self.keyboard_mode == 'auto':
            if value:
                self._bind_keyboard()
            else:
                self._unbind_keyboard()

    def _ensure_keyboard(self):
        if self._keyboard is None:
            self._requested_keyboard = True
            keyboard = self._keyboard = EventLoop.window.request_keyboard(
                self._keyboard_released,
                self,
                input_type=self.input_type,
                keyboard_suggestions=self.keyboard_suggestions,
            )
            keyboards = FocusBehavior._keyboards
            if keyboard not in keyboards:
                keyboards[keyboard] = None

    def _bind_keyboard(self):
        self._ensure_keyboard()
        keyboard = self._keyboard

        if not keyboard or self.disabled or not self.is_focusable:
            self.focus = False
            return
        keyboards = FocusBehavior._keyboards
        old_focus = keyboards[keyboard]  # keyboard should be in dict
        if old_focus:
            old_focus.focus = False
            # keyboard shouldn't have been released here, see keyboard warning
        keyboards[keyboard] = self
        keyboard.bind(on_key_down=self.keyboard_on_key_down,
                      on_key_up=self.keyboard_on_key_up,
                      on_textinput=self.keyboard_on_textinput)

    def _unbind_keyboard(self):
        keyboard = self._keyboard
        if keyboard:
            keyboard.unbind(on_key_down=self.keyboard_on_key_down,
                            on_key_up=self.keyboard_on_key_up,
                            on_textinput=self.keyboard_on_textinput)
            if self._requested_keyboard:
                keyboard.release()
                self._keyboard = None
                self._requested_keyboard = False
                del FocusBehavior._keyboards[keyboard]
            else:
                FocusBehavior._keyboards[keyboard] = None

    def keyboard_on_textinput(self, window, text):
        pass

    def _keyboard_released(self):
        self.focus = False

    def on_touch_down(self, touch):
        if not self.collide_point(*touch.pos):
            return
        if (not self.disabled and self.is_focusable and
            ('button' not in touch.profile or
             not touch.button.startswith('scroll'))):
            self.focus = True
            FocusBehavior.ignored_touch.append(touch)
        return super(FocusBehavior, self).on_touch_down(touch)

    @staticmethod
    def _handle_post_on_touch_up(touch):
        ''' Called by window after each touch has finished.
        '''
        touches = FocusBehavior.ignored_touch
        if touch in touches:
            touches.remove(touch)
            return
        if 'button' in touch.profile and touch.button in\
                ('scrollup', 'scrolldown', 'scrollleft', 'scrollright'):
            return
        for focusable in list(FocusBehavior._keyboards.values()):
            if focusable is None or not focusable.unfocus_on_touch:
                continue
            focusable.focus = False

    def _get_focus_next(self, focus_dir):
        current = self
        walk_tree = 'walk' if focus_dir == 'focus_next' else 'walk_reverse'

        while 1:
            # if we hit a focusable, walk through focus_xxx
            while getattr(current, focus_dir) is not None:
                current = getattr(current, focus_dir)
                if current is self or current is StopIteration:
                    return None  # make sure we don't loop forever
                if current.is_focusable and not current.disabled:
                    return current

            # hit unfocusable, walk widget tree
            itr = getattr(current, walk_tree)(loopback=True)
            if focus_dir == 'focus_next':
                next(itr)  # current is returned first  when walking forward
            for current in itr:
                if isinstance(current, FocusBehavior):
                    break
            # why did we stop
            if isinstance(current, FocusBehavior):
                if current is self:
                    return None
                if current.is_focusable and not current.disabled:
                    return current
            else:
                return None

    def get_focus_next(self):
        '''Returns the next focusable widget using either :attr:`focus_next`
           or the :attr:`children` similar to the order when tabbing forwards
           with the ``tab`` key.
        '''
        return self._get_focus_next('focus_next')

    def get_focus_previous(self):
        '''Returns the previous focusable widget using either
           :attr:`focus_previous` or the :attr:`children` similar to the
           order when the ``tab`` + ``shift`` keys are triggered together.
        '''
        return self._get_focus_next('focus_previous')

    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        '''The method bound to the keyboard when the instance has focus.

        When the instance becomes focused, this method is bound to the
        keyboard and will be called for every input press. The parameters are
        the same as :meth:`kivy.core.window.WindowBase.on_key_down`.

        When overwriting the method in the derived widget, super should be
        called to enable tab cycling. If the derived widget wishes to use tab
        for its own purposes, it can call super after it has processed the
        character (if it does not wish to consume the tab).

        Similar to other keyboard functions, it should return True if the
        key was consumed.
        '''
        if keycode[1] == 'tab':  # deal with cycle
            modifiers = set(modifiers)
            if {'ctrl', 'alt', 'meta', 'super', 'compose'} & modifiers:
                return False
            if 'shift' in modifiers:
                next = self.get_focus_previous()
            else:
                next = self.get_focus_next()
            if next:
                self.focus = False

                next.focus = True

            return True
        elif keycode[1] in ('right','down'):  # deal with cycle
            modifiers = set(modifiers)
            if {'ctrl','shift', 'alt', 'meta', 'super', 'compose'} & modifiers:
                return False
            next = self.get_focus_next()
            if next:
                self.focus = False

                next.focus = True

            return True
        elif keycode[1] in ('left','up'):  # deal with cycle
            modifiers = set(modifiers)
            if {'ctrl','shift', 'alt', 'meta', 'super', 'compose'} & modifiers:
                return False
            next = self.get_focus_previous()
            if next:
                self.focus = False

                next.focus = True

            return True
        return False

    def keyboard_on_key_up(self, window, keycode):
        '''The method bound to the keyboard when the instance has focus.

        When the instance becomes focused, this method is bound to the
        keyboard and will be called for every input release. The parameters are
        the same as :meth:`kivy.core.window.WindowBase.on_key_up`.

        When overwriting the method in the derived widget, super should be
        called to enable de-focusing on escape. If the derived widget wishes
        to use escape for its own purposes, it can call super after it has
        processed the character (if it does not wish to consume the escape).

        See :meth:`keyboard_on_key_down`
        '''
        if keycode[1] == 'escape':
            self.focus = False
            return True
        return False

    def show_keyboard(self):
        '''
        Convenience function to show the keyboard in managed mode.
        '''
        if self.keyboard_mode == 'managed':
            self._bind_keyboard()

    def hide_keyboard(self):
        '''
        Convenience function to hide the keyboard in managed mode.
        '''
        if self.keyboard_mode == 'managed':
            self._unbind_keyboard()




class ButtonBehavior(_ButtonBehavior):
    is_held = BooleanProperty(False)
    repeat_delay = 0.5  # seconds before repeating starts
    repeat_interval = 0.1  # seconds between repeats
    
    def __init__(self, **kwargs):
        self.register_event_type('on_repeat')
        super(ButtonBehavior, self).__init__(**kwargs)
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