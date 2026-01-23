import os
os.environ['HAS_GRADIENT']='1'
from .utils import resolve_color
from kivy.graphics.texture import Texture
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.relativelayout import RelativeLayout
from kivy.properties import StringProperty, ObjectProperty, ListProperty, AliasProperty, OptionProperty
from kivy.graphics import Rectangle
from kivy.clock import Clock
import traceback
from kivy.uix.widget import Widget
from kivy.lang import Builder
# from ._gradient_fast_pure import Gradient as _Gradient
# from ._gradient_np import Gradient as _Gradient
try:
    from ._gradient_np import Gradient as _Gradient
except ImportError:
    from ._gradient_fast_pure import Gradient as _Gradient



Builder.load_string("""
#:import Gradient kivy_gradient.Gradient
<kvGradientBox>:
    gradient_type: root.gradient_type
    gradient_args: root.gradient_args
    gradient: root.gradient

    canvas:
        Rectangle:
            size: self.size
            pos: self.pos
            # texture: self._get_texture()
            texture: Gradient.horizontal(get_color_from_hex("E91E63"), get_color_from_hex("FCE4EC"),[0,0,0,1])
""")


class kvGradientBox(BoxLayout):
    def __init__(self, **kwargs):
        gradient=kwargs.pop('gradient',None)
        if gradient:
            self.gradient_type,self.gradient_args=gradient
        super().__init__(**kwargs)
    gradient= ListProperty(None)
    def _get_texture(self,*x):
        self._pre_grad()
        print(self.buff_size)
        tex = Texture.create(size=self.buff_size)
        tex.blit_buffer(self._get_buffer(), colorfmt='rgba', bufferfmt='ubyte')
        tex.wrap = 'clamp_to_edge'
        return tex
    def _pre_grad(self):
        _parsed_colors=[]
        for item in self.gradient_args['colors']:
            if isinstance(item, (list, tuple)) and len(item) == 2 and isinstance(item[1], (int, float)):
                _parsed_colors.append([resolve_color(item[0]),item[1]])
            else:
                _parsed_colors.append(resolve_color(item))
        self.gradient_args['colors']=_parsed_colors
        
        size=self.gradient_args.pop('size',None)
        if size==None:
            lc=len(self.gradient_args.get('colors'))
            cmul=48
            if self.gradient_type=='linear-gradient':
                c=cmul*lc
            elif self.gradient_type=='radial-gradient':
                if lc<4:
                    cmul=96
                c=cmul*lc
            elif self.gradient_type=='conic-gradient':
                if lc<4:
                    cmul=96
                c=cmul*lc
            # ratio=self.height/self.width
            try:
                ratio=self.height/self.width
            except:
                ratio=1
            if ratio>1:
                size=int(c*1/ratio),c
            else:
                size=c,int(c*ratio)
        else:
            size=tuple(size)
        self.buff_size=size
        self._parsed_colors=_parsed_colors
    def _get_buffer(self):
        # print(self.gradient_type,self.gradient_args)
        buff = _Gradient.create(
            self.gradient_type,
            size=self.buff_size,
            **self.gradient_args,
        )
        return buff


class GradientBox(BoxLayout):
    # gradient_type = StringProperty("linear-gradient")
    gradient_type = OptionProperty('linear-gradient',options=["linear-gradient", "radial-gradient", "conic-gradient"])
    gradient_args = ObjectProperty(dict(colors=[[1,1,1,1],[0,0,0,1]]))
    gradient= ListProperty(None)
    def on_gradient(self,ins,val):
        self.gradient_type,self.gradient_args=val
        self._create_rect()

    # def _ggradient_type(self):
    #   return self.graient[0]
    # def _ggradient_args(self):
    #   return self.graient[1]
    # def _sgradient_type(self,val):
    #   if not isinstance(val,str):
    #       raise TypeError(f'Gradient "{val}" of type "{type(val)}" must be one of the following strings: "linear-gradient", "radial-gradient", "conic-gradient"')
    #   if not val in Gradient.registry:
    #       raise ValueError(f'Gradient "{val}" must be one of the following: "linear-gradient", "radial-gradient", "conic-gradient"')
    #   self.graient[0]=val
    #   return True
    # def _sgradient_args(self,val):
    #   if not isinstance(val,dict):
    #       raise TypeError(f'Gradient args "{val}" of type "{type(val)}" must be a dict object with valid gradient properties.')
    #   self.graient[1]=val
    #   return True

    # gradient_type = AliasProperty(_ggradient_type,_sgradient_type)
    # gradient_args = AliasProperty(_ggradient_args,_sgradient_args)

    def __init__(self, **kwargs):
        gradient=kwargs.pop('gradient',None)
        if gradient:
            self.gradient_type,self.gradient_args=gradient
        super().__init__(**kwargs)

        self._create_rect()
        self.bind(
            size=self._update_canvas,
            pos=self._update_canvas,
          )
    def _create_rect(self):
        with self.canvas:
            self.bg_rect=Rectangle(pos=self.pos, size=self.size)
            self._pre_grad()
            tex = Texture.create(size=self.buff_size)
            tex.blit_buffer(self._get_buffer(), colorfmt='rgba', bufferfmt='ubyte')
            tex.wrap = 'clamp_to_edge'
            self.bg_rect.texture=tex

    def _pre_grad(self):
        _parsed_colors=[]
        for item in self.gradient_args['colors']:
            if isinstance(item, (list, tuple)) and len(item) == 2 and isinstance(item[1], (int, float)):
                _parsed_colors.append([resolve_color(item[0]),item[1]])
            else:
                _parsed_colors.append(resolve_color(item))
        self.gradient_args['colors']=_parsed_colors
        
        size=self.gradient_args.pop('size',None)
        if size==None:
            lc=len(self.gradient_args.get('colors'))
            cmul=48
            if self.gradient_type=='linear-gradient':
                c=cmul*lc
            elif self.gradient_type=='radial-gradient':
                if lc<4:
                    cmul=96
                c=cmul*lc
            elif self.gradient_type=='conic-gradient':
                if lc<4:
                    cmul=96
                c=cmul*lc
            try:
                ratio=self.height/self.width
            except:
                ratio=1
            if ratio>1:
                size=int(c*1/ratio),c
            else:
                size=c,int(c*ratio)
        else:
            size=tuple(size)
        self.buff_size=size
        self._parsed_colors=_parsed_colors
    def _get_buffer(self):
        # print(self.gradient_type,self.gradient_args)
        buff = _Gradient.create(
            self.gradient_type,
            size=self.buff_size,
            **self.gradient_args,
        )
        return buff

    def _update_canvas(self, *args):
        # print('hell')
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

        # # self.canvas.clear()
        # with self.canvas.before:
        #     buff,buff_size=self.get_buffer()
        #     tex = Texture.create(size=buff_size)
        #     tex.blit_buffer(buff, colorfmt='rgba', bufferfmt='ubyte')
        #     tex.wrap = 'clamp_to_edge'
        #     # print(buff,buff_size)
        #     self.bg_rect=Rectangle(texture=tex,pos=self.pos, size=self.size)


class GradientBehavior(object):
# class GradientBehavior(Widget):
    # gradient_type = OptionProperty('linear-gradient',options=["linear-gradient", "radial-gradient", "conic-gradient"])
    # gradient_args = ObjectProperty(dict(colors=[[1,1,1,1],[0,0,0,1]]))
    gradient_type = OptionProperty('linear-gradient',options=["linear-gradient", "radial-gradient", "conic-gradient"])
    gradient_args = ObjectProperty(dict(colors=[[1,1,1,0],[0,0,0,0]],size=(2,2)))
    gradient= ListProperty(None)
    def on_gradient(self,ins,val):
        self.gradient_type,self.gradient_args=val
        self._create_rect()

    def __init__(self, **kwargs):
        gradient=kwargs.pop('gradient',None)
        if gradient:
            self.gradient_type,self.gradient_args=gradient
        super().__init__(**kwargs)

        self._create_rect()
        self.bind(
            size=self._update_canvas,
            pos=self._update_canvas,
          )
    def _create_rect(self):
        with self.canvas:
            self.bg_rect=Rectangle(pos=self.pos, size=self.size)
            self._pre_grad()
            tex = Texture.create(size=self.buff_size)
            tex.blit_buffer(self._get_buffer(), colorfmt='rgba', bufferfmt='ubyte')
            tex.wrap = 'clamp_to_edge'
            self.bg_rect.texture=tex

    def _pre_grad(self):
        _parsed_colors=[]
        for item in self.gradient_args['colors']:
            if isinstance(item, (list, tuple)) and len(item) == 2 and isinstance(item[1], (int, float)):
                _parsed_colors.append([resolve_color(item[0]),item[1]])
            else:
                _parsed_colors.append(resolve_color(item))
        self.gradient_args['colors']=_parsed_colors
        
        size=self.gradient_args.pop('size',None)
        if size==None:
            lc=len(self.gradient_args.get('colors'))
            cmul=48
            if self.gradient_type=='linear-gradient':
                c=cmul*lc
            elif self.gradient_type=='radial-gradient':
                if lc<4:
                    cmul=96
                c=cmul*lc
            elif self.gradient_type=='conic-gradient':
                if lc<4:
                    cmul=96
                c=cmul*lc
            # ratio=self.height/self.width
            try:
                ratio=self.height/self.width
            except:
                ratio=1

            if ratio>1:
                size=int(c*1/ratio),c
            else:
                size=c,int(c*ratio)
        else:
            size=tuple(size)
        self.buff_size=size
        self._parsed_colors=_parsed_colors
    def _get_buffer(self):
        buff = _Gradient.create(
            self.gradient_type,
            size=self.buff_size,
            **self.gradient_args,
        )
        return buff

    def _update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class GradientRelative(GradientBehavior,GridLayout):
    pass
class GradientGrid(GradientBehavior,GridLayout):
    pass
    # gradient_type = StringProperty("linear-gradient")
    # gradient_type = OptionProperty('linear-gradient',options=["linear-gradient", "radial-gradient", "conic-gradient"])
    # gradient_args = ObjectProperty(dict(colors=[[1,1,1,1],[0,0,0,1]]))
    # gradient= ListProperty(None)
    # def on_gradient(self,ins,val):
    #     self.gradient_type,self.gradient_args=val
    #     self._create_rect()

    # def __init__(self, **kwargs):
    #     gradient=kwargs.pop('gradient',None)
    #     if gradient:
    #         self.gradient_type,self.gradient_args=gradient
    #     super().__init__(**kwargs)

    #     self._create_rect()
    #     self.bind(
    #         size=self._update_canvas,
    #         pos=self._update_canvas,
    #       )
    # def _create_rect(self):
    #     with self.canvas:
    #         self.bg_rect=Rectangle(pos=self.pos, size=self.size)
    #         self._pre_grad()
    #         tex = Texture.create(size=self.buff_size)
    #         tex.blit_buffer(self._get_buffer(), colorfmt='rgba', bufferfmt='ubyte')
    #         tex.wrap = 'clamp_to_edge'
    #         self.bg_rect.texture=tex

    # def _pre_grad(self):
    #     _parsed_colors=[]
    #     for item in self.gradient_args['colors']:
    #         if isinstance(item, (list, tuple)) and len(item) == 2 and isinstance(item[1], (int, float)):
    #             _parsed_colors.append([resolve_color(item[0]),item[1]])
    #         else:
    #             _parsed_colors.append(resolve_color(item))
    #     self.gradient_args['colors']=_parsed_colors
        
    #     size=self.gradient_args.pop('size',None)
    #     if size==None:
    #         lc=len(self.gradient_args.get('colors'))
    #         cmul=48
    #         if self.gradient_type=='linear-gradient':
    #             c=cmul*lc
    #         elif self.gradient_type=='radial-gradient':
    #             if lc<4:
    #                 cmul=96
    #             c=cmul*lc
    #         elif self.gradient_type=='conic-gradient':
    #             if lc<4:
    #                 cmul=96
    #             c=cmul*lc
    #         ratio=self.height/self.width
    #         if ratio>1:
    #             size=int(c*1/ratio),c
    #         else:
    #             size=c,int(c*ratio)
    #     else:
    #         size=tuple(size)
    #     self.buff_size=size
    #     self._parsed_colors=_parsed_colors
    # def _get_buffer(self):
    #     buff = _Gradient.create(
    #         self.gradient_type,
    #         size=self.buff_size,
    #         **self.gradient_args,
    #     )
    #     return buff

    # def _update_canvas(self, *args):
    #     self.bg_rect.pos = self.pos
    #     self.bg_rect.size = self.size