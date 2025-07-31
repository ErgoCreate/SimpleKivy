import sys
import os
# package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# print(package_path)
# os.environ['PYTHONPATH'] = package_path + os.pathsep + os.environ.get('PYTHONPATH', '')
# # print(__name__)
NOTKEY=-67191210201
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
from .utils import infinite, CaseInsensitiveDict,_Void,is_number,find_letter_number_pairs, auto_config, re_search,get_kvApp
from .utils import import_from, get_transition, _event_manager, abc, mdi
from .utils import Colors,Fonts,hex2rgb, resolve_color,pos_hints,app_schedule_get_call,app_get
from .utils import BrowserHistory
from .utils import markup_str
from . import utils
import pickle
import types
from kivy.uix.widget import Widget

addcolors='r g b w y gray brown orange'.split()
iadd=-1
liadd=len(addcolors)
def __mul__Widget(self,val):
    # print(self.size,val.size,self.size_hint,val.size_hint)
    size_hint_y=self.size_hint_y
    if not val.size_hint_y:
        size_hint_y=val.size_hint_y
    # global iadd,addcolors,liadd
    # setattr(kel,'_isbox',kel.orientation)
    # if hasattr(self,'do_layout') and getattr(self,'orientation',None)=='horizontal':
    if getattr(self,'_isbox',None)=='horizontal':
        self.add_widget(val)
        return self
    # iadd+=1
    if size_hint_y:
        return BoxitH( self, val,k=NOTKEY)
    else:
        return BoxitH( self, val,size='ychildren',k=NOTKEY)

def __div__Widget(self,val):
    # print(self.size,val.size,self.size_hint,val.size_hint)
    size_hint_x=self.size_hint_x
    if not val.size_hint_x:
        size_hint_x=val.size_hint_x
    # global iadd,addcolors,liadd
    # if hasattr(self,'do_layout') and getattr(self,'orientation',None)=='vertical':
    if getattr(self,'_isbox',None)=='vertical':
        self.add_widget(val)
        return self
    # iadd+=1
    if size_hint_x:
        return BoxitV( self, val,k=NOTKEY)
    else:
        return BoxitV( self, val,size='xchildren',k=NOTKEY)
# setattr(Widget,'__mul__' , types.MethodType(__mul__Widget, Widget))
setattr(Widget,'__mul__' , __mul__Widget)
setattr(Widget,'__truediv__' , __div__Widget)

# setattr(Widget,'__add__',__mul__Widget)
from kivy.logger import Logger
from kivy.resources import resource_find
# SK_PATH_FILE = os.path.abspath(__file__)
# Logger.info('SimpleKivy: Installed at "' +
#             SK_PATH_FILE + '"')
from kivy.uix.treeview import TreeView as kvTreeView
from kivy.uix.treeview import TreeViewLabel as kvTreeViewLabel
from kivy.uix.treeview import TreeViewNode as kvTreeViewNode
import kivy
# print(kivy.__file__)
kivy.require('2.3.0')



from . import kvBehaviors as kvb

# from utils import *



import math
import time
import re

from functools import partial
from functools import reduce

from kivy.properties import BooleanProperty,NumericProperty,StringProperty,ListProperty,ObjectProperty

import traceback
from kivy.utils import platform

from kivy.app import App

from kivy.clock import Clock

from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
# print('hell'*50)

from . import kvWidgets as kvw
from . import modkvWidgets as mkvw

size=infinite()

def __getattr__(name):
    if name=='app':
        return app_get()

def app_lambda(*largs,**kwargs):
    return lambda *x:app_get()(*largs,**kwargs)

# def app_lambda(*largs,**kwargs):
#     return lambda *x:app_get()(*largs,**kwargs)

def app_setter(k,name,conversion=None):
    if conversion:
        return lambda ins,val:app_get()[k].setter(name)(ins,conversion(val))
    return lambda *x:app_get()[k].setter(name)(*x)

def android_moc():
    android=infinite()
    class Service:
        def __init__(self,name='my service',msg='running',*args,**kwargs):
            self.name=name
            print(name,msg)
            self.spath=''
            self.pid=None
            if os.path.exists('service/main.py'):
                self.spath='service/main.py'
            else:
                service_path=os.path.join('service','main.py')
                raise FileNotFoundError(f'The file "{os.path.abspath(service_path)}" was not found.')
        def start(self,msg='service started'):
            
            
            
            import subprocess
            if self.spath:
                cwd=os.path.join( os.getcwd(),'service')
                print(f"Service working directory : {cwd}")
                # print(self.spath)
                # self.pid=subprocess.Popen(["python",self.spath],stdin=None, stdout=None, stderr=None,cwd=cwd)
                self.pid=subprocess.Popen(["python",'main.py'],stdin=None, stdout=None, stderr=None,cwd=cwd)
                print(msg)
            else:
                print('Service not started')
    android.AndroidService=Service
            



    return android

if platform=='android':
    import android
else:
    # android=infinite()
    android=android_moc()



def _preproces(**kwargs):
    # if 'size' in kwargs:
    #     if isinstance()
    nkwargs={}
    for k,v in kwargs.items():
        nkwargs[k]=v
        if k=='key':
            nkwargs['k']=nkwargs.pop('key')
        elif k=='size':
            if isinstance(v,(str,infinite)):
                if isinstance(v,infinite):
                    v=v._name
                # print(v)
                # if 'children' in v:
                #     if 'y' in v:
                #         v=0
                #         for
                # print(v)
                if v.isnumeric():
                    v=f'x{v}y{v}'

                xs=re_search(r"x[0-9]+",v,flags=re.IGNORECASE)
                ys=re_search(r"y[0-9]+",v,flags=re.IGNORECASE)
                nkwargs['size']=[0,0]
                # print(xs,ys)
                if xs:
                    snum=re.sub(r"\D", "", xs)
                    nkwargs['size_hint_x']=None
                    nkwargs['size'][0]=int(snum)
                if ys:
                    snum=re.sub(r"\D", "", ys)
                    nkwargs['size_hint_y']=None
                    nkwargs['size'][1]=int(snum)
                # print(nkwargs)
            # elif isinstance(v,infinite):
            #     # print(v.name)
            #     v=v._name
            #     xs=re_search(r"x[0-9]+",v,flags=re.IGNORECASE)
            #     ys=re_search(r"y[0-9]+",v,flags=re.IGNORECASE)
            #     nkwargs['size']=[0,0]
            #     if xs:
            #         snum=re.sub(r"\D", "", xs)
            #         nkwargs['size_hint_x']=None
            #         nkwargs['size'][0]=int(snum)
            #     if ys:
            #         snum=re.sub(r"\D", "", ys)
            #         nkwargs['size_hint_y']=None
            #         nkwargs['size'][1]=int(snum)
        elif 'color' in k:
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
            # elif isinstance(v,dict):
                # for key,val in v.items():
                #     v[key]=utils.rgba2hex(utils.resolve_color(val))
                #     print(v[key])

                    
            nkwargs[k]=v
        elif 'transition' in k:
            if isinstance(v,str):
                import kivy.uix.screenmanager as smm
                # v=v.lower()
                match v:
                    case 'no':
                        v=smm.NoTransition()
                    case 'slide':
                        v=smm.SlideTransition()
                    case 'card':
                        v=smm.CardTransition()
                    case 'fade':
                        v=smm.FadeTransition()
                    case 'wipe':
                        v=smm.WipeTransition()
                    case 'swap':
                        v=smm.SwapTransition()
                    case 'fallout':
                        v=smm.FallOutTransition()
                    case 'risein':
                        v=smm.RiseInTransition()

            nkwargs[k]=v
        elif 'font_name'==k:
            nkwargs[k]=Fonts.get(v,v)
        elif 'schedule_once'==k:
            nkwargs.pop(k)
            Clock.schedule_once(v)

    return nkwargs

_future_elements=[]
def _future_process_elements(self):
    global _future_elements

    for el in _future_elements:
        _id=getattr(el,'id',None)
        if _id is None:
            while self._nk in self.ids:
                self._nk+=1
            el.id=self._nk
            self._nk+=1
        self.ids[el.id]=el
        self._ids[el]=el.id
    _future_elements=[]


_post_elements={
    'CalcSheet':[],
    'ToggleGeneral':[],
    'SizeofChildren':[],
    'LabelLike':[],
    'MaxWidth':[],
    'Playlist':[],
    'Albumlist':[],
    'Artistlist':[],
    'TitleBar':[],
    # 'AddWidgetByKey':[],
    }


def _post_process_elements(self):
    global _post_elements,_future_bind
    for wtype in _post_elements:
        if wtype=='ToggleGeneral':
            for el in _post_elements[wtype]:
                if el.state=='down':
                    el.on_state(el,el.state)
        elif wtype in ('Playlist','Albumlist','Artistlist'):
            for kel in _post_elements[wtype]:
                kel.bind(  on_ref_press=lambda instance, refvalue: self.trigger_event(f"{instance.id}/ref/{refvalue}")   )
        elif wtype=='TitleBar':
            for kel in _post_elements[wtype]:
                kel.title.text=self.title
                self.bind(title=lambda inst,val:setattr(kel.title,'text',val))

                def onic(inst,val):
                    if val:
                        kel.icon.source=val
                    else:
                        # kel.icon.source=f"{kivy.kivy_icons_dir}"
                        kel.icon.source='skdata/logo/simplekivy-icon-32.png'
                if self.icon:
                    kel.icon.source=self.icon
                else:
                    kel.icon.source='skdata/logo/simplekivy-icon-32.png'
                self.bind(icon=onic)


                def onc(*l):
                    self.trigger_event('__Close__')
                    Clock.schedule_once(lambda dt:self.close())

                kel.clo.bind(  on_release=onc)
                
                def onres(*l):
                    if self.window_is_maximized:
                        self.restore()
                        
                    else:
                        self.maximize()


                kel.res.bind(  on_release=onres   )
                kel.min.bind(  on_release=lambda *l: self.minimize()   )

                

                def onres_set(inst,val):
                    if val:
                        kel.res.text=mdi('window-restore')
                    else:
                        kel.res.text=mdi('window-maximize')
                        
                self.bind(window_is_maximized=onres_set)

                if self.window_is_maximized:
                    kel.res.text=mdi('window-restore')
                else:
                    kel.res.text=mdi('window-maximize')


                


        elif wtype=='MaxWidth':
            for kel in _post_elements[wtype]:
                def on_max_width(instance,val):
                    # print(instance.id)
                    pad=getattr(instance.parent,'padding',[0]*4)
                    # print(padding)
                    nmax=instance.maximum_width-pad[0]-pad[2]
                    if val>nmax:
                        setattr(instance,'width',nmax)
                        setattr(instance,'size_hint_x',None)
                def on_max_width_hint(instance,val):
                    if val<kel.maximum_width:
                        kel.size_hint_x=1
                kel.bind(width=on_max_width)
                kel.parent.bind(width=on_max_width_hint)
        elif wtype=='LabelLike':

            # print(_post_elements['LabelLike'])
            for kel in _post_elements[wtype]:
                # print(kel.id)
                markup=getattr(kel,'markup',False)

                if markup:
                    def on_href(ins,text):
                        if '[href=' in text:
                            text = text.replace('[href=', '[color=1B95E0][u][ref=').replace(
                                '[/href]', '[/ref][/u][/color]')
                        # return text
                        ins.text=text
                    on_href(kel,kel.text)
                    kel.bind(text=on_href)

                    # kel.on_event='on_ref_press',r'lambda instance, refvalue: self.trigger_event(f"{instance.id}/ref/{refvalue}")'
                    kel.bind(  on_ref_press=lambda instance, refvalue: self.trigger_event(f"{instance.id}/ref/{refvalue}")   )
        elif wtype=='SizeofChildren':
            for pair in _post_elements[wtype]:
                el,sz=pair
                setattr(el,'sizeofchildren',sz)
                # x,y=el.size
                # if 'x' in sz:
                #     x=0
                #     el.size_hint_x=None
                #     for child in el.children:
                #         x+=child.width
                # if 'y' in sz:
                #     y=0
                #     el.size_hint_y=None
                #     for child in el.children:
                #         y+=child.height
                # pad,spa=getattr(el,'padding',[0]*4),getattr(el,'spacing',[0]*2)
                # if isinstance(spa,(int,float)):
                #     spa=[spa]*2
                # el.size=x+pad[0]+pad[2]+spa[0],y+pad[1]+pad[3]+spa[1]

                def update_size_on_children(self,*_):
                    x,y=self.size
                    sz=getattr(self,'sizeofchildren','')
                    pad,spa=getattr(self,'padding',[0]*4),getattr(self,'spacing',[0]*2)
                    if isinstance(spa,(int,float)):
                        spa=[spa]*2
                    if isinstance(pad,(int,float)):
                        pad=[pad]*4

                    if 'xchildren' in sz:
                        x=0
                        self.size_hint_x=None
                        for child in self.children:
                            # if child.size_hint_x==None:
                            #     continue
                            x+=child.width

                        spa_plus=spa[0]*len(self.children)-1
                        if spa_plus<0:
                            spa_plus=0
                        self.width=x+pad[0]+pad[2]+spa_plus
                    elif 'xchild_max' in sz:
                        x=0
                        self.size_hint_x=None
                        for child in self.children:
                            # if child.size_hint_x==None:
                            #     continue
                            if child.width>x:
                                x=child.width

                        spa_plus=spa[0]*len(self.children)-1
                        if spa_plus<0:
                            spa_plus=0
                        self.width=x#+pad[0]+pad[2]+spa_plus


                    if 'ychildren' in sz:
                        y=0
                        self.size_hint_y=None
                        for child in self.children:
                            # if child.size_hint_y==None:
                            #     continue
                            y+=child.height

                        spa_plus=spa[1]*len(self.children)-1
                        if spa_plus<0:
                            spa_plus=0
                        self.height=y+pad[1]+pad[3]+spa_plus
                    elif 'ychild_max' in sz:
                        y=0
                        self.size_hint_y=None
                        for child in self.children:
                            # if child.size_hint_y==None:
                            #     continue
                            if child.height>y:
                                y=child.height

                        spa_plus=spa[1]*len(self.children)-1
                        if spa_plus<0:
                            spa_plus=0
                        self.height=y#+pad[1]+pad[3]+spa_plus

                el.update_size_on_children= types.MethodType(update_size_on_children, el)
                el.update_size_on_children()
                el.bind(children=lambda *_:Clock.schedule_once(el.update_size_on_children))



        elif wtype=='CalcSheet':
            for el in _post_elements[wtype]:
                # print(f"{el}, {el.id = }")
                cinpto=getattr(el,'connect_input_to',None)
                cdposto=getattr(el,'connect_dpos_to',None)
                cvalto=getattr(el,'connect_cell_value_to',None)

                if cdposto:
                    el.cdposto= self.ids[cdposto]
                    el.cdposto.text= el.sheet.dpos
                    def on_disabled(instance,value):
                        instance.rel.cdposto.text= value
                    el.sheet.bind(dpos=on_disabled)
                    if cinpto and getattr(el.cdposto,'on_text_validate',None):
                        def on_valid(instance,*args):
                            if instance.text in instance.sheet.children_dict:
                                wid=instance.sheet.children_dict[instance.text]
                                instance.sheet.icell.ccell=wid
                                instance.sheet.dpos=wid.dpos
                                # el.sheet.icell.ccell._text=el.cinpto.text
                                # el.sheet.icell.dpo=wid
                                instance.cinpto.focus=True
                            else:
                                instance.cdposto.text= el.sheet.dpos
                                # el.cdposto.focus= True
                                Clock.schedule_once(lambda dt:setattr(instance.cdposto,'focus',True))

                        el.cdposto.bind(on_text_validate=on_valid)


                if cinpto:
                    el.cinpto= self.ids[cinpto]
                    setattr(el.cinpto,'sheet',el.sheet)
                    el.cinpto.text=el.sheet.children_dict.get( el.sheet.dpos)._text
                    def on_dpos(instance,dpos):
                        wid=instance.children_dict.get(dpos)
                        instance.rel.cinpto.text= wid._text
                    el.sheet.bind(dpos=on_dpos)
                    def on_cval(instance,new_value):
                        # print(instance,new_value)
                        dpos=instance.dpos
                        wid=instance.children_dict.get(dpos)
                        instance.rel.cinpto.text= wid._text

                    el.sheet.bind(cval=on_cval)
                    def on_valid(instance,*args):
                        dpos=instance.sheet.dpos
                        wid=instance.sheet.children_dict.get(dpos)
                        wid._text= instance.text

                    el.cinpto.bind(on_text_validate=on_valid)

                if cvalto:
                    el.cvalto= self.ids[cvalto]
                    def on_cval(instance,new_value):
                        if instance.error:
                            el.cvalto.text= instance.error

                        else:
                            el.cvalto.text= f"{new_value}"
                        # el.cvalto.text= f"{new_value}"
                    def on_dpos(instance,dpos):
                        # print(args)
                        if instance.error:
                            el.cvalto.text= instance.error

                        else:
                            # el.cvalto.text= f"{new_value}"
                            new_value=instance.children_dict.get(dpos).val
                            el.cvalto.text= f"{new_value}"
                    el.sheet.bind(cval=on_cval)
                    el.sheet.bind(dpos=on_dpos)
    # print(f"{_post_elements_empty['LabelLike'] = }")
    # _post_elements=_post_elements_empty.copy()
    # print(f"{_post_elements['LabelLike'] = }")
    for wtype in _post_elements:
        _post_elements[wtype]=[]
    # print('after',f"{_post_elements['LabelLike'] = }")

def _create_callback(self,event_name):
    # Define the callback function
    def callback(instance, *args):
        # Print the widget and event name
        # print(event_name)
        self.event_manager(self,event_name)

    return callback

_future_bind=[]
def _future_process_binds(self):
    global _future_bind
    for el in _future_bind:
        if el.id==NOTKEY:
            continue
        if isinstance(el.on_event,(tuple,list)):
            
            if isinstance(el.on_event[0],(tuple,list)):
                for on_event,on_callback in el.on_event:
                    if isinstance(on_callback,str):
                        on_callback=eval(on_callback,locals())

                    el.bind(**{on_event:on_callback})
            elif isinstance(el.on_event[0],str):
                do_dot_subevent=getattr(el,'do_dot_subevent',None)
                if do_dot_subevent:
                    binds={}
                    for i,on_event in enumerate(el.on_event):
                        # print(on_event)
                        subevent=str(el.id)+'.'+str(on_event)
                        # call=
                        el.bind(**{on_event: _create_callback(self,subevent)})

                        # setattr(el,f'__{on_event}',lambda *args:print(subevent) )
                        # binds[on_event]=getattr(el,f'__{on_event}')

                        # print(subevent)
                        # trigger=self._triggers.get(  subevent,Clock.create_trigger(  lambda *args: self.event_manager(self,subevent)  )  )
                        # def new_call(*args):
                        # # new_call=lambda *args:
                        #     subevent=str(el.id)+'.'+str(i)+'.'+str(on_event)
                        #     print(subevent)
                        # binds[on_event]=trigger


                    # el.bind(**{on_event: new_call})
                    # print(binds)
                    # el.bind(**binds)
                else:
                    for on_event in el.on_event:
                        el.bind(**{on_event:self._callback})
        elif isinstance(el.on_event,dict):
            el.bind(**el.on_event)
            # for event,callback in el.on_event.items():
            #     el.bind(**{event : callback})
        else:
            if getattr(el,'do_dot_subevent',None):
                el.bind(**{el.on_event:lambda *args: self._callback_w_subev(*args,subevent=el.on_event) })
            else:
                el.bind(**{el.on_event:self._callback})
    _future_bind=[]

def skwidget(f):
    def wrap(*args, **kwargs):
        sz=kwargs.get('size',None)
        max_w0=kwargs.pop('maximum_width',None)
        # size_behavior=kwargs.pop('size_behavior','none')

        do_dot_subevent=kwargs.pop('do_dot_subevent',None)
        # print('499',do_dot_subevent)
        bind=kwargs.pop('bind',None)



        kwargs=_preproces(**kwargs)
        global _future_elements, _future_bind
        kel = f(*args, **kwargs)

        if bind:
            Clock.schedule_once(lambda dt: kel.bind(**bind))

        max_w=getattr(kel,'maximum_width',None)
        if max_w0:
            max_w=max_w0
            kel.maximum_width=max_w

        enable_events=getattr(kel,'enable_events',None)

        
        setattr(kel,'do_dot_subevent',do_dot_subevent)
        
        if enable_events:
            _future_bind.append(kel)

        _future_elements.append(kel)

        post=getattr(kel,'post',None)
        if post:
            if isinstance(post,(tuple,list)):
                for posti in post:
                    _post_elements[posti].append(kel)
            else:
                _post_elements[post].append(kel)
        if isinstance(sz,str) and 'child' in sz:
            # pass
            _post_elements['SizeofChildren'].append((kel,sz))
# 
        if max_w!=None:
            # print(max_w,kel)
            _post_elements['MaxWidth'].append(kel)

        # #---------------------------------------------------------
        # if size_behavior in ('none',None):
        #     pass
        # elif size_behavior=='normal':
        #     kel.bind(size=lambda inst,siz:setattr(inst,'text_size',inst.size))
        #     kel.texture_size=kel.size
        # elif size_behavior=='text':
        #     # this label’s height will be set to the text content
        #     kel.size_hint_y=None
        #     setattr(kel,'height',kel.texture_size[1])
        #     setattr(kel,'text_size',(kel.width,None))

        #     kel.bind(texture_size=lambda inst,siz:setattr(inst,'height',siz[1]))
        #     kel.bind(width=lambda inst,v:setattr(inst,'text_size',(v, None)))

            

        # elif size_behavior=='texth':
        #     # this label’s width will be set to the text content
        #     kel.size_hint_x=None

        #     setattr(kel,'width',kel.texture_size[0])
        #     setattr(kel,'text_size',(None, kel.height))

        #     kel.bind(texture_size=lambda inst,siz:setattr(inst,'width',siz[0]))
        #     kel.bind(height=lambda inst,v:setattr(inst,'text_size',(None, v)))
        # #---------------------------------------------------------

        return kel
    return wrap
def skwidget_only_preprocess(f):
    def wrap(*args, **kwargs):
        kwargs=_preproces(**kwargs)
        kel = f(*args, **kwargs)
        return kel
    return wrap


def process_added_widgets():
    self=App.get_running_app()
    _future_process_elements(self)
    _post_process_elements(self)
    _future_process_binds(self)
paw=process_added_widgets

def _ensure_bttn_not_draggable(children):

    for c in children:
        if hasattr(c,'on_release'):
            setattr(c,'draggable',False)
        if hasattr(c,'children'):
            if c.children:
                _ensure_bttn_not_draggable(c.children)

class action:
    def __init__(self,target,*args,**kwargs):
        self.target=target
        self.args=args
        self.kwargs=kwargs
    def __call__(self):
        return self.target(*self.args,**self.kwargs)

_post_actions_global=[]

if 'win' == platform.lower():
    import win32gui
    import win32api
    import win32con

# print(platform)

class MyApp(App):
    window_is_maximized = BooleanProperty(False)
        
    def __init__(
        self,
        layout=[[]],
        title='MyApp',
        event_manager=_event_manager,
        custom_titlebar=False,
        alpha=1,
        keep_on_top=False,
        layout_args={},
        icon='skdata/logo/simplekivy-icon-32.png',
        layout_class=None,
        **kwargs
        ):

        self._is_windows = True if platform.lower()=='win' else False
        self.Clock=Clock
        self.mdi=mdi
        
        self.kvWindow=utils.Window

        # app.kvWindow.get_window_info().window
        # self.hwnd=

        minimum_width=kwargs.pop('minimum_width',None)
        minimum_height=kwargs.pop('minimum_height',None)
        minimum_size=kwargs.pop('minimum_size',None)
        if minimum_width!=None:
            self.minimum_width=minimum_width
        if minimum_height!=None:
            self.minimum_height=minimum_height
        if minimum_size!=None:
            self.minimum_size=minimum_size

        self.post_actions=[]
        
        size=kwargs.pop('size',None)
        location=kwargs.pop('location',None)
        
        # print(f"size = {size}")
        if size:
            self.post_actions.append(action(self.Resize,*size))
        if location:
            left,top=location
            if left!=None:
                self.post_actions.append(action(setattr,self.kvWindow,'left',location[0]))
            if top!=None:
                self.post_actions.append(action(setattr,self.kvWindow,'top',location[1]))

        
        
        # self._ignore_maxrestore=False
        def _do_maximize(*largs):
            # self._ignore_maxrestore
            self.window_is_maximized = True
            # self.trigger_event('__Restore__')
        def _do_restore(*largs):
            # self._ignore_maxrestore
            # self.trigger_event('__Restore__')
            self.window_is_maximized = False
        self.kvWindow.bind(on_maximize=_do_maximize, on_restore=_do_restore)

        if custom_titlebar:
            self.kvWindow.custom_titlebar=True
            try:
                first_el=layout[0][0]
            except:
                first_el=layout[0]
            self.kvWindow.set_custom_titlebar(first_el)
            tbw=self.kvWindow.titlebar_widget
            if hasattr(tbw,'children'):
                _ensure_bttn_not_draggable(tbw.children)
            # layout.insert(0,[tbw])


        self.title=title

        # self.Resize(*size)
        self.poolt=ThreadPoolExecutor(thread_name_prefix='SimpleKivy')
        self.queue={}
        # from kivy.core.window import Window
        # def onclose(*largs):
        #     self.event_manager(self,'__Close__')
        # self.Window=Window
        self._leaving=False
        # self.Window.bind(on_request_close=onclose)

        # self.bind(on_stop=lambda *args: self.event_manager(self,'__Close__'))

        self._nk=0
        self.ids={}
        self._ids={}
        if not layout_class:
            rows=len(layout)
            self._layout=kvw.GridLayoutB(rows=rows,**_preproces(**layout_args))

            
            
            max_cols = 0
            for row in layout:
                if len(row) > max_cols:
                    max_cols = len(row)
            i=0
            for row in layout:
                i += 1
                elnum = -1
                for el in row:
                    # el=self._prepro_element(el)
                    elnum += 1
                    # print(el.eltype, 'i:', i, ', j:', elnum, ', key:', el.key)
                    # kivy_el = self._process_element(el)
                    kivy_el = el
                    self._layout.add_widget(kivy_el)

                lenrow = len(row)
                addnvoids = 0
                if lenrow < max_cols:
                    addnvoids = max_cols - lenrow
                for v in range(addnvoids):
                    self._layout.add_widget(
                            # # self._process_element(
                            #     Label(text='', k=NOTKEY,
                            # # size_hint=kivy_el.size_hint
                            #     )
                            # # )
                            Fill(),
                        )
        else:
            self._layout=layout_class(**layout_args)
            for kivy_el in layout:
                self._layout.add_widget(kivy_el)

        
        # if event_manager:
        self._triggers={}
        self.event_manager=event_manager
        self.thread_event=self.submit_thread_event
        self.get_group=kvw.ToggleButtonBehavior.get_widgets
        self.hidden={}
        # else:
        #     self.event_manager=self._event_manager

        self.top_widget = None
        self.remove_on_click = False
        def on_touch_down(instace, touch):
            if self.remove_on_click:
                self.remove_top_widget()
        self._layout.bind(on_touch_down=on_touch_down)

        _future_process_elements(self)
        _post_process_elements(self)
        _future_process_binds(self)
        # super(MyApp, self).__init__(**kwargs)
        self.paw=self.process_added_widgets
        self.Clock.schedule_once(lambda dt: setattr(self,'alpha',alpha))
        
        self._keep_on_top=keep_on_top
        self.Clock.schedule_once(lambda dt: setattr(self,'keep_on_top',keep_on_top))

        self._hwnd=None
        
        # self.Clock.schedule_once(lambda dt: setattr(self.icon,'ico',))
        if icon=='skdata/logo/simplekivy-icon-32.png':
            self.ico=resource_find('skdata/logo/simplekivy-icon-256.ico')
        # self.Clock.schedule_once(lambda dt: setattr(self.icon,'ico',))
        # self.icon=icon
        # Clock.schedule_once(lambda dt: setattr(self,'icon',icon),1)
        Clock.schedule_once(lambda dt: self.on_icon(self,self.get_application_icon()))
        super().__init__(icon=icon,**kwargs)

    @property
    def hwnd(self):
        if not self._hwnd:
            self._hwnd=self.kvWindow.get_window_info().window
        return self._hwnd

    # def embed_window_to(self,external_hwnd,wid):
    #     if not self._is_windows:
    #         print('Embeding windows into kivy only works in Windows platforms.')
    #         return

    #     # Reparent to Kivy's window
    #     win32gui.SetParent(external_hwnd, self.hwnd)

    #     # Modify window styles
    #     style = win32gui.GetWindowLong(external_hwnd, win32con.GWL_STYLE)
    #     style &= ~win32con.WS_POPUP
    #     style |= win32con.WS_CHILD
    #     win32gui.SetWindowLong(external_hwnd, win32con.GWL_STYLE, style)

    #     # # Position within Kivy
    #     # win32gui.MoveWindow(
    #     #     external_hwnd,
    #     #     round(wid.x), round(wid.y),
    #     #     round(wid.width), round(wid.height),
    #     #     True
    #     # )

    #     # def update_embedding(self, instance, value):
    #     #     self.winforms_host.embed_into_kivy(
    #     #         Window.get_window_info().window,
    #     #         self.embed_area.x,
    #     #         self.embed_area.y,
    #     #         self.embed_area.width,
    #     #         self.embed_area.height
    #     #     )

    #     # # Update on resize
    #     # wid.bind(
    #     #     pos=self.update_embedding,
    #     #     size=self.update_embedding
    #     # )
    #     wwin=utils.ExternalWindow(external_hwnd)
    #     def force_move():
    #         # hidden=getattr(wid,'hidden',False)
    #         # if not hidden:
    #         try:
    #             left, top, right, bottom = win32gui.GetWindowRect(self.hwnd)
    #             app.lastp= left, top
    #             com.wwin.resize(int(wid.width-2*xdpx-4*not_cbar),int(wid.height-2*ydpx))
                    
    #             apos=wid.to_window(*wid.pos)
    #             wwin.move(left+apos[0]+xdpx +9*not_cbar,bottom-apos[1]-wid.height+ydpx-9*not_cbar)
    #         except:
    #             pass
    #     def onp(inst,*v):
    #         self.poolt.submit(force_move)
    #     def ons(inst,v):
    #         self.poolt.submit(force_move)
    #     wid.bind(pos=onp)
    #     wid.bind(size=ons)


    @property
    def keep_on_top(self):
        return self._keep_on_top
    @keep_on_top.setter
    def keep_on_top(self,keep_on_top):
        # print('doing stuff',keep_on_top)
        self._keep_on_top=keep_on_top
        if keep_on_top:
            if self._is_windows:
                # self.kvWindow.bind(on_draw=lambda *args: self.set_always_on_top())
                # self._set_always_on_top()
                self.kvWindow.bind(on_draw=self._set_always_on_top)
            else:
                self._keep_on_top=False
                print('The on_top behavior only works in Windows platforms.')
        else:
            try:
                self.kvWindow.unbind(on_draw=self._set_always_on_top)
                self._set_not_always_on_top()
            except:
                pass
    def _set_always_on_top(self,*args):
        '''
        Sets the HWND_TOPMOST flag for the current Kivy Window.
        This behavior will be overwritten by setting position of the window from kivy.
        If you want the window to stay on top of others even after changing the position or size from kivy, 
        use the register_topmost function instead.
        '''
        if not self._is_windows:
            print('The on top behavior only works in Windows platforms.')
            return
        # else:
        #     import win32gui
        #     import win32con
        
        # self.hwnd = win32gui.FindWindow(None, self.title)

        # for i in range(10):
        #     # self.hwnd = win32gui.FindWindow(None, self.title)

        #     print(self.hwnd,self.title)
        #     import time
        #     time.sleep(1)

        rect = win32gui.GetWindowRect(self.hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y

        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, x, y, w, h, 0)
    def _set_not_always_on_top(self):
        '''
        Sets the HWND_NOTOPMOST flag for the current Kivy Window.
        '''
        if not self._is_windows:
            print('The on_top behavior only works in Windows platforms.')
            return

        # self.hwnd = win32gui.FindWindow(None, self.title)

        rect = win32gui.GetWindowRect(self.hwnd)
        x = rect[0]
        y = rect[1]
        w = rect[2] - x
        h = rect[3] - y

        # win32gui.SetWindowPos(
        #     self.hwnd, win32con.HWND_NOTOPMOST, x, y, w, h, 0)
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_TOPMOST, x, y, w, h, 0)
        time.sleep(.25)
        win32gui.SetWindowPos(self.hwnd, win32con.HWND_NOTOPMOST, x, y, w, h, 0)
    
    @property
    def alpha(self):
        return self._alpha
    @alpha.setter
    def alpha(self,val):
        self._alpha=val
        if not self._is_windows:
            print('The transparent behavior only works in Windows platforms.')
        else:
            # if not self._alpha_ondraw:
            if 0<=self._alpha<1:
                self._alpha_binded=True
                self.kvWindow.bind(on_draw=self._set_alpha)
            else:
                # print('do unbind ondraw')
                self.kvWindow.unbind(on_draw=self._set_alpha)
                if self._alpha==1:
                    # print(f"{self._alpha = }")
                    try:
                        self._set_alpha()
                    except:
                        traceback.print_exc()
                else:
                    print(f'Alpha value {self._alpha} out of range (0,1).')

    @property
    def minimum_size(self):
        return self.kvWindow.minimum_width,self.kvWindow.minimum_height
    @minimum_size.setter
    def minimum_size(self,val):
        self.kvWindow.minimum_width,self.kvWindow.minimum_height=val
    @property
    def minimum_width(self):
        return self.kvWindow.minimum_width
    @minimum_width.setter
    def minimum_width(self,val):
        self.kvWindow.minimum_width=val
    @property
    def minimum_height(self):
        return self.kvWindow.minimum_height
    @minimum_height.setter
    def minimum_height(self,val):
        self.kvWindow.minimum_height=val

    def thread_pool_new(self,name,max_workers=None):
        self.queue[name]=ThreadPoolExecutor(max_workers=max_workers,thread_name_prefix=name)
    def queue_new(self,name):
        self.queue[name]=ThreadPoolExecutor(max_workers=1,thread_name_prefix=name)


    def _set_alpha(self,*_):
        # import win32api
        # print('_set_alpha')
        alpha = int(self._alpha * 255)

        try:
            # self.hwnd = win32gui.FindWindow(None, self.title)
            # Make it a layered window
            win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, win32gui.GetWindowLong(
                self.hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
            # make it transparent (alpha between 0 and 255)
            win32gui.SetLayeredWindowAttributes(
                self.hwnd, win32api.RGB(0, 0, 0), alpha, win32con.LWA_ALPHA)
        except:
            traceback.print_exc()
            pass

    def hide(self,*key_list,shrink=True):
        for k in key_list:
            wid=self.__getitem__(k)
            s=getattr(wid,'size',(100,100)).copy()
            sh=getattr(wid,'size_hint',(1,1)).copy()
            o=getattr(wid,'opacity',1)
            d=getattr(wid,'disabled',False)
            # print('hide:',(s,sh,o,d))
            self.hidden[k]=(s,sh,o,d)
            # print(self.hidden)
            # print(k,':',(s,sh,o,d))
            # setattr(w,'size')
            if shrink:
                setattr(wid,'size',(0,0))
                setattr(wid,'size_hint',(None,None))
            setattr(wid,'opacity',0)
            setattr(wid,'disabled',True)
            # print(self.hidden)
    def unhide(self,*key_list,enforce={}):
        for k in key_list:
            wid=self.__getitem__(k)
            try:
                s,sh,o,d=self.hidden.get(k)
                # print('unhide:',(s,sh,o,d))
            except:
                # traceback.print_exc()
                s=getattr(wid,'size',(100,100))
                sh=getattr(wid,'size_hint',(1,1))
                o=getattr(wid,'opacity',1)
                d=getattr(wid,'disabled',False)
            
            # print(k,':',(s,sh,o,d))
            
            setattr(wid,'size',s)
            setattr(wid,'size_hint',sh)
            setattr(wid,'opacity',o)
            setattr(wid,'disabled',d)

            for prop,v in enforce.items():
                setattr(wid,prop,v)
    def destroy_widget(self,k,default=None):
        
        el=self.ids.get(k,default)
        if el:
            del self.ids[k]
            del self._ids[el]
            if el.parent:
                el.parent.remove_widget(el)
    def remove_top_widget(self):
        if self.top_widget:
            self._layout.parent.remove_widget(self.top_widget)
            self.top_widget = None
    def _remove_top_widget(self,dt):
        self.remove_top_widget()
    def add_top_widget(self, widget, remove_on_click=True):
        self.remove_top_widget()
        self.remove_on_click = remove_on_click
        self.top_widget = widget
        # Clock.schedule_once(lambda *args: self._layout.parent.add_widget(self.top_widget))
        self._layout.parent.add_widget(self.top_widget)
        self._layout.do_layout()
    def infotip_schedule(self,*args,**kwargs):
        Clock.schedule_once(lambda dt:self.infotip(*args,**kwargs))
    def infotip_remove_schedule(self):
        Clock.schedule_once(self._remove_top_widget)
    # def tooltip(self,message,**tooltip_args):
        # Clock.schedule_once(lambda dt:self._tooltip(message,**tooltip_args),.5)
    def _tooltip(self,message,**tooltip_args):
        # print(self.kvWindow.mouse_pos)
        start_pos=self.kvWindow.mouse_pos

        bcolor=tooltip_args.pop('bcolor',(32/255,32/255,32/255,1))
        color=tooltip_args.pop('color','#CCCCCC')
        lcolor=tooltip_args.pop('bcolor','gray')
        valign=tooltip_args.pop('valign','middle')
        size=tooltip_args.pop('size','y30')
        size_behavior=tooltip_args.pop('size_behavior','texth')
        padding=tooltip_args.pop('padding',[4,4,4,4])

        lbl=Label(text=message,
            pos=start_pos,
            size=size,color=color,padding=padding,size_behavior=size_behavior,lcolor='gray',bcolor=bcolor,valign=valign,**tooltip_args,k=NOTKEY)
        self.process_added_widgets()

        self.add_top_widget(lbl)
        lbl.texture_update()
        didx=False
        didy=False

        if lbl.y+lbl.height>=self.kvWindow.height:
            lbl.y=lbl.y-lbl.height-16
            didy=True
        
        if lbl.x+lbl.width>=self.kvWindow.width:
            lbl.x=lbl.x-lbl.width
            didx=True
        if didy and not didx:
            lbl.x=lbl.x+16

        self.poolt.submit(self._tooltip_remove_on_move,start_pos)
    def _tooltip_remove_on_move(self,start_pos=None,dmax=4):
        # sx,sy=self.kvWindow.mouse_pos
        if not start_pos:
            sx,sy=start_pos
        else:
            sx,sy=start_pos
        while not self._leaving:
            self.sleep_in_thread(.1)
            cx,cy=self.kvWindow.mouse_pos
            dx=abs(cx-sx)
            if dx>dmax:
                # self.remove_top_widget()
                Clock.schedule_once(self._remove_top_widget)
                return
            dy=abs(cy-sy)
            if dy>dmax:
                # self.remove_top_widget()
                Clock.schedule_once(self._remove_top_widget)
                return






    def infotip(
            self,text='info',
            height=30,
            remove_on_click=True,
            size_hint_y=None,
            # size_hint_x=None,
            pos_hint={'left':0,'bottom':0},
            timeout=3,
            lcolor='white',
            bcolor='gray',
            halign='center',
            padding=4,
            markup=False,
            font_size=15,
            color=[1, 1, 1, 1],
            max_lines=1,
            auto_remove=True,
            size_behavior='normal',
            # is_large=True,
            **kw
            ):
        # width=kw.pop('width',None)
        # if width==None:
        #     width=(font_size)*len(text)
        #     # print(width,self._layout.width)
        #     if width>=self._layout.width:
        #         width=100
        #         size_hint_x=1
        #     kw['width']=width
        # if is_large:
        it=LargeText(
            text=text,height=height,size_hint_y=size_hint_y,pos_hint=pos_hint,
            lcolor=lcolor,color=color,bcolor=bcolor,markup=markup,
            # size_hint_x=size_hint_x,
            size_behavior=size_behavior,
            halign=halign,padding=padding,max_lines=max_lines,
            **kw,

            )
        # else:
        #     # it=Label(
        #     it=kvw.LabelC(
        #         text=text,height=height,size_hint_y=size_hint_y,pos_hint=pos_hint,
        #         lcolor=utils.resolve_color(lcolor),color=utils.resolve_color(color),
        #         bcolor=utils.resolve_color(bcolor),
        #         # size_hint_x=size_hint_x,
        #         halign=halign,padding=padding,max_lines=max_lines,
        #         **kw,

        #     )

        # it.size=it.text_size
        # it.size_hint_x=None
        # it.bin(size)
        # it.bind(width=lambda *x: it.setter('text_size')(it, (it.width, None) )  )
        # def ons(inst,s):
        #     # print('\nons=',s)
        #     # print(inst.size)
        #     # print(inst.text_size)
        #     # print(inst.texture_size)
        #     inst.size_hint_x=1
        #     inst.width=inst.texture_size[0]
            # inst.text_size=inst.size
            

        # it.bind(size=ons)
        # it.bind(texture_size=ons)
        # print(it.texture_size)
        # it.bind(texture_size=lambda *x: it.setter('height')(label, label.texture_size[1]))

        # it.size_hint_x=None
        # print(it.text_size)
        self.process_added_widgets()

        self.add_top_widget(it,remove_on_click=remove_on_click)
        if auto_remove:
            Clock.schedule_once(self._remove_top_widget,timeout)
        return it

    def disable_widgets(self,*widgets):
        for e in widgets:
            if isinstance(e,str):
                self[e].disabled=True
            else:
                e.disabled=True
    def enable_widgets(self,*widgets):
        for e in widgets:
            if isinstance(e,str):
                self[e].disabled=False
            else:
                e.disabled=False
    def Resize(self, width, height):
        # self.get_parent_window().size = (width, height)
        self.kvWindow.size = width, height
    def bring_to_front(self):
        if not self._is_windows:
            print('The bring_to_front behavior only works in Windows platforms.')
            return

        try:
            win32gui.SetForegroundWindow(self.hwnd)
        except:
            pass
        

        # # while True:
        # for i in range(5):
            
        #     # self.hwnd = win32gui.FindWindow(None, self.title)
        #     if self.hwnd==0:
        #         print(f"{self.title = }")
        #         time.sleep(.25)
        #         continue
        #     try:
        #         win32gui.ShowWindow(self.hwnd, 5)
        #         win32gui.SetForegroundWindow(self.hwnd)
        #         break
        #     except:
        #         traceback.print_exc()
        #         # self.hwnd = win32gui.FindWindow(None, self.title)
        #     time.sleep(.25)

    def process_widget(self,wid):
        _future_process_elements(self)
        _post_process_elements(self)
        _future_process_binds(self)
        return wid
    def process_added_widgets(self):
        _future_process_elements(self)
        _post_process_elements(self)
        _future_process_binds(self)
    def trigger_call(self,k,prop=None,val=None,_kw_prepro=False,ignore_errors=False,**kwargs):
        return lambda dt: self.__call__(k=k,prop=prop,val=val,_kw_prepro=_kw_prepro,ignore_errors=ignore_errors,**kwargs)
    #     return 

    def schedule_call_once(self,k,prop=None,val=None,timeout=0,_kw_prepro=False,ignore_errors=False,**kwargs):
        Clock.schedule_once(lambda dt:self.__call__(k=k,prop=prop,val=val,_kw_prepro=_kw_prepro,ignore_errors=ignore_errors,**kwargs),timeout=timeout)
    # def unschedule_call(self,k,prop=None,val=None,_kw_prepro=False,ignore_errors=False,**kwargs):
    #     Clock.unschedule(lambda dt:self.__call__(k=k,prop=prop,val=val,_kw_prepro=_kw_prepro,ignore_errors=ignore_errors,**kwargs))

    def __call__(self,k,prop=None,val=None,timeout=0,_kw_prepro=False,ignore_errors=False,**kwargs):
        # def set_prop():
        # Clock.create_trigger
        try:

            if isinstance(k,str):
                widget=self.ids[k]
            else:
                widget=k

            if isinstance(prop,str):
                if not _kw_prepro:
                    kw=_preproces(**{prop:val})
                    trigger=Clock.create_trigger(lambda *args:setattr(widget,prop,kw[prop]),timeout)
                    trigger()
                else:
                    trigger=Clock.create_trigger(lambda *args:setattr(widget,prop,val),timeout)
                    trigger()
            else:
                # print(kwargs)
                kwargs=_preproces(**kwargs)
                for p,v in kwargs.items():
                    self.__call__(k,p,v,_kw_prepro=True)
                # Clock.schedule_once(lambda dt:(setattr(self.ids[k],p,v) for p,v in kwargs.items()),timeout)
                    # trigger=Clock.create_trigger(lambda *args:setattr(self.ids[k],p,v),timeout)
                    # trigger()
        except Exception as e:
            if ignore_errors:
                pass
                # traceback.print_exc()
            else:
                raise e
    def trigger_event(self,event):
        trigger=self._triggers.get(  event,Clock.create_trigger(  lambda *args: self.event_manager(self,event)  )  )
        trigger()
    def schedule_event_once(self,event,timeout=0):
        ans=Clock.schedule_once(lambda *args: self.event_manager(self,event),timeout=timeout)
    def schedule_func_once(self,func,*args,timeout=0,**kwargs):
        ans=Clock.schedule_once(lambda dt: func(*args,**kwargs),timeout=timeout)

    
    def askopenfile(self,
        filetypes=(
                ('All files', '*.*'),
                ('PDF', '*.pdf'),
            ),
        callback=None,
        **kw,
        ):
        '''
        title - the title of the window
        initialdir - the directory that the dialog starts in
        initialfile - the file selected upon opening of the dialog
        filetypes - a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed
        defaultextension - default extension to append to file (save dialogs)
        multiple - when true, selection of multiple items is allowed
        '''
        import tkinter as tk
        root=tk.Tk()
        root.iconbitmap(self.ico)
        root.call('wm', 'attributes', '.', '-topmost', '1')
        root.withdraw()
        from tkinter import filedialog as fd
        filename=fd.askopenfilename(
            filetypes=filetypes,
            title=self.title + ' - Open',
            **kw
            )
        root.destroy()
        if callback and filename:
            callback(filename)
        return filename
    def askdirectory(self,
        callback=None,
        **kw,
        ):
        '''
        title - the title of the window
        initialdir - the directory that the dialog starts in
        multiple - when true, selection of multiple items is allowed
        '''
        import tkinter as tk
        root=tk.Tk()
        root.iconbitmap(self.ico)
        root.call('wm', 'attributes', '.', '-topmost', '1')
        root.withdraw()
        from tkinter import filedialog as fd
        filename=fd.askdirectory(
            title=self.title + ' - Open',
            **kw
            )
        root.destroy()
        if callback and filename:
            callback(filename)
        return filename

    def asksaveasfile(self,
        initialfile='',
        filetypes=(
            ('All files', '*.*'),
            ('PDF', '*.pdf'),
            
            ),
        callback=None,
        **kw,
        ):
        '''
        title - the title of the window
        initialdir - the directory that the dialog starts in
        initialfile - the file selected upon opening of the dialog
        filetypes - a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed
        defaultextension - default extension to append to file (save dialogs)
        multiple - when true, selection of multiple items is allowed
        '''


        import tkinter as tk
        root=tk.Tk()
        root.iconbitmap(self.ico)
        root.call('wm', 'attributes', '.', '-topmost', '1')
        root.withdraw()
        from tkinter import filedialog as fd
        filename=fd.asksaveasfilename(
            initialfile=initialfile,
            filetypes=filetypes,
            title=self.title + ' - Save as',
            **kw
            )
        root.destroy()
        # print(filename)
        if callback and filename:
            callback(filename)
        return filename
    def askopenfiles(self,
        filetypes=(
            ('All files', '*.*'),
            ('PDF', '*.pdf'),
            
            ),
        callback=None,
        **kw,
        ):
        '''
        title - the title of the window
        initialdir - the directory that the dialog starts in
        initialfile - the file selected upon opening of the dialog
        filetypes - a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed
        defaultextension - default extension to append to file (save dialogs)
        multiple - when true, selection of multiple items is allowed
        '''

        import tkinter as tk
        root=tk.Tk()
        root.iconbitmap(self.ico)
        root.call('wm', 'attributes', '.', '-topmost', '1')
        root.withdraw()
        from tkinter import filedialog as fd
        filenames=fd.askopenfilenames(
            filetypes=filetypes,
            title=self.title + ' - Open',
            **kw
            )
        root.destroy()
        if callback and filenames:
            callback(filenames)
        return filenames
    def LoadingOpen(self):
        k='__loading__'
        if not self.__contains__(k):
            p=Popup(
                title='Status',
                content=BoxitV(
                    # Image(
                    #     'data/images/image-loading.gif',size_hint=(.25, 1)
                    # ),
                    Label('Loading...'),
                ),
                k=k,
                auto_dismiss=False,
                size_hint=(.5,.5),
                # attach_to=self
            )
            # def close(*largs):
            #     return True
            # p.bind(on_dismiss=close)
            self.process_added_widgets()
        self.__getitem__(k).open()
    def LoadingClose(self):
        k='__loading__'
        if self.__contains__(k):
            self.__getitem__(k).dismiss()


    def submit_thread_event(self,event):
        # def tryfun(app,event):
        #     try:
        #         app.event_manager(self,event)
        #     except:
        #         traceback.print_exc()
        self.poolt.submit(self.event_manager,self,event)
        # self.poolt.submit(tryfun,self,event)
    # def _process_element(self,el):

    #     _id=getattr(el,'id',None)
    #     if _id is None:
    #         while self._nk in self.ids:
    #             self._nk+=1
    #         el.id=self._nk
    #         self._nk+=1
    #     self.ids[el.id]=el
    #     self._ids[el]=el.id

    #     eevs=getattr(el,'enable_events',None)
    #     if eevs:
    #         if isinstance(el,kvButton):
    #             el.bind(**{f'on_{el.on_event}':self._callback})
    #         elif isinstance(el,_Input):
    #             el.bind(**{f'on_{el.on_event}':self._callback})
    #     return el
    def __getitem__(self, key):
        return self.ids[key]

    def schedule_get_call(self,key,method,*args,**kwargs):
        Clock.schedule_once(lambda dt:getattr(self.ids[key],method)(*args,**kwargs))

    # def __contains__(self, key):
    #     return self.ids.__contains__(key)
    def keys(self):
        return self.ids.keys()
    def values(self):
        return self.ids.values()
    def items(self):
        return self.ids.items()
    def __contains__(self, item):
        return item in self.ids

    def __iter__(self):
        return iter(self.ids)
    def _callback(self,*args,**kwargs):
        # print(self,args,kwargs)
        ev=self._ids[args[0]]
        self.event_manager(self,ev)
    # def _callback_w_subev(self,*args,subevent=None,**kwargs):
    #     # print(args)
    #     ev=self._ids[args[0]]
    #     self.event_manager(self,f"{ev}.{subevent}")

    def config_dump(self,file,**kwargs):
        data={}
        for k,prop in kwargs.items():
            val=getattr(self.__getitem__(k),prop)
            data[k]=(prop,val)
        pickle.dump(data,file=open(file,'wb'))
    def config_load(self,file):
        data=pickle.load(file=open(file,'rb'))
        for k,v in data.items():
            setattr(self.__getitem__(k),v[0],v[1])
        return data


        # match ev:
        #     case '__Minimize__':
        #         self.minimize()
        #     case '__Restore__':
        #         self.restore()
    def call_event(self,event):
        return self.event_manager(self,event)
        


    def build(self):
        for a in self.post_actions:
            a()
        # self.event_manager(self,'__Start__')
        Clock.schedule_once(lambda dt: self.event_manager(self,'__Start__') )
        # print(self.ids)
        return self._layout

    def minimize(self):
        self.kvWindow.minimize()
    def restore(self):
        # if self._ignore_maxrestore:
        #     self._ignore_maxrestore=False
        #     return
        self.kvWindow.restore()
        # if self.window_is_maximized:
        #     self.kvWindow.restore()
        # else:
        #     self.kvWindow.maximize()
    def maximize(self):
        # if self._ignore_maxrestore:
        #     self._ignore_maxrestore=False
        #     return
        self.kvWindow.maximize()
    def restore_maximize(self,if_maximized=None):
        if self.window_is_maximized:
            self.restore()
            if if_maximized:
                if_maximized()
        else:
            self.maximize()

    def close(self):
        # self.get_running_app().stop()
        # self.event_manager(self,'__Close__')
        self._leaving=True
        self.stop()
        self.kvWindow.close()
    def is_leaving(self):
        return self._leaving
    def on_stop(self):
        # print(self._leaving)
        if not self._leaving:
            self.event_manager(self,'__Close__')
            self._leaving=True
            # time.sleep()
    def sleep_in_thread(self,timeout=0):
        '''
        Similar to time.sleep, but returns if app._leaving == True.
        Usefull to exit quickly from a threaded task that uses sleep if the main app has closed.
        '''
        t0=time.time()
        dt=1
        if timeout<1:
            dt=timeout/3
        while True:
            # print('heree')
            if time.time()-t0>=timeout:
                break
            if self._leaving:
                break
            time.sleep(dt)



def TEST_WIDGET(w):
    lyt=[[w]]
    MyApp(layout=lyt).run()

@skwidget
def Label(text='',k=None,focus_behavior=False,halign='center',size_behavior='normal',valign='middle',**kwargs):
    # kwargs=_preproces(**kwargs)
    # global _future_elements, _future_bind
    # print(kwargs)
    if focus_behavior:
        
        # kel=kvw.FocusLabelB(text=text,halign=halign,valign=valign,**kwargs)
        kvWd=kvw.FocusLabelB
        # def on_f(*_):
            # print(_)
            # pass
        # kel.bind(on_focus=on_f)
    else:
        # kel=kvw.LabelA(text=text,halign=halign,valign=valign,**kwargs)
        kvWd=kvw.LabelA

    kel=skivify_v2(kvWd,text=text,halign=halign,valign=valign,**kwargs,k=k)

    if size_behavior=='none':
        pass
    elif size_behavior=='normal':
        
        kel.bind(size=lambda inst,siz:setattr(inst,'text_size',inst.size))
        # kel.texture_size=kel.size
        Clock.schedule_once(lambda dt:setattr(kel,'text_size',kel.size))

        # Clock.schedule_once(lambda dt:kel.texture_update())
    elif size_behavior=='text':
        # this label’s height will be set to the text content
        kel.size_hint_y=None
        Clock.schedule_once(lambda dt: setattr(kel,'height',kel.texture_size[1]))
        Clock.schedule_once(lambda dt: setattr(kel,'text_size',(kel.width,None)))

        kel.bind(texture_size=lambda inst,siz:setattr(inst,'height',siz[1]))
        kel.bind(width=lambda inst,v:setattr(inst,'text_size',(v, None)))

        # Clock.schedule_once(lambda dt:kel.texture_update())

        

    elif size_behavior=='texth':
        # this label’s width will be set to the text content
        kel.size_hint_x=None

        Clock.schedule_once(lambda dt: setattr(kel,'width',kel.texture_size[0]))
        Clock.schedule_once(lambda dt: setattr(kel,'text_size',(None, kel.height)))

        kel.bind(texture_size=lambda inst,siz:setattr(inst,'width',siz[0]))
        kel.bind(height=lambda inst,v:setattr(inst,'text_size',(None, v)))

        # Clock.schedule_once(lambda dt:kel.texture_update())
    kel.texture_update()

        
    
    # kel.id=k

    kel.post='LabelLike'

    # _future_elements.append(kel)
    return kel




@skwidget
def PagedText(pages=[],k=None,focus_behavior=False,halign='center',size_behavior='normal',valign='middle',**kwargs):
    if focus_behavior:
        kvWd=kvw.FocusLabelB
    else:
        kvWd=kvw.LabelA

    class kvWd2(kvWd):
        page=kvw.NumericProperty(None)
        pages=kvw.ListProperty([])

        def on_page(self,ins,val):
            if self.pages:
                self.text=self.pages[val]

        def on_pages(self,ins,val):
            if val:
                self.text=val[0]
                self.page=0

            else:
                self.empty()
        def reload(self):
            if self.pages:
                self.page=0
        def empty(self):
            self.pages=['']
            self.text=''
        def next_page(self):
            c=self.page
            if c!=None and c+1<len(self.pages):
                self.page+=1
        def previous_page(self):
            c=self.page
            if c!=None and c>0:
                self.page-=1
        prev_page=previous_page


    kel=skivify_v2(kvWd2,pages=pages,halign=halign,valign=valign,**kwargs,k=k)

    if size_behavior=='none':
        pass
    elif size_behavior=='normal':
        kel.bind(size=lambda inst,siz:setattr(inst,'text_size',inst.size))
    elif size_behavior=='text':
        # this label’s height will be set to the text content
        kel.size_hint_y=None
        kel.bind(texture_size=lambda inst,siz:setattr(inst,'height',siz[1]))
        kel.bind(width=lambda inst,v:setattr(inst,'text_size',(v, None)))
    elif size_behavior=='texth':
        # this label’s width will be set to the text content
        kel.size_hint_x=None
        kel.bind(texture_size=lambda inst,siz:setattr(inst,'width',siz[0]))
        kel.bind(height=lambda inst,v:setattr(inst,'text_size',(None, v)))

    kel.post='LabelLike'
    return kel

@skwidget
def RstDocument(text='',k=None,**kwargs):
    from kivy.uix.rst import RstDocument as kvrstdoc
    class kvWd(kvrstdoc):
        def __init__(self, **kwargs):
            self.kvWindow=utils.Window
            # self.register_event_type('on_ref_press')
            # self.kvWindow.bind(on_touch_down=self.on_touch_down)
            # self.bind(on_touch_up=self._on_touch_up)
            super(kvWd, self).__init__(**kwargs)

        # def _on_touch_up(self, ins,touch):
        #     # print(touch)
        #     if touch.button=='right':
        #         if self.collide_point(*touch.pos):
        #             # print(touch.button)
        #             for ref in self.references:
        #                 if ref['x'] <= touch.x <= ref['x'] + ref['width'] and ref['y'] <= touch.y <= ref['y'] + ref['height']:
        #                     print(f"Clicked on {ref['text']} at {ref['url']}")
        #                     # self.dispatch('on_ref_press',ref['text'])
        #                     # Perform action based on ref['url'] here
        #                     return True # Consume the event
        #     # # return super(kvWd, self).on_touch_down(self,touch)
        def on_ref_press(self,*a):
            pass
            # print(a)
            # print(a,self.references)


    kel=skivify_v2(kvWd,text=text,enable_events=True,do_dot_subevent=True,on_event='on_ref_press',k=k,**kwargs)
    # if size_behavior=='none':
    #     pass
    # elif size_behavior=='normal':
    #     kel.bind(size=lambda inst,siz:setattr(inst,'text_size',inst.size))
    # elif size_behavior=='text':
    #     # this label’s height will be set to the text content
    #     kel.size_hint_y=None
    #     kel.bind(texture_size=lambda inst,siz:setattr(inst,'height',siz[1]))
    #     kel.bind(width=lambda inst,v:setattr(inst,'text_size',(v, None)))
    # elif size_behavior=='texth':
    #     # this label’s width will be set to the text content
    #     kel.size_hint_x=None
    #     kel.bind(texture_size=lambda inst,siz:setattr(inst,'width',siz[0]))
    #     kel.bind(height=lambda inst,v:setattr(inst,'text_size',(None, v)))
    # kel.post='LabelLike'
    return kel

# def skivify(class_,**kwargs):
#     k=kwargs.pop('k',None)
#     @skwidget
#     def widget_creator(**kwargs):
#         kel=class_(**kwargs)
#         kel.id=k
#         return kel
#     return widget_creator(**kwargs)
# def _skivify(class_,enable_events=False,on_event=None,**kwargs):
#     k=kwargs.pop('k',None)
#     def widget_creator(**kwargs):
#         kel=class_(**kwargs)
#         kel.id=k
#         # setattr(kel,'id',k)
#         if enable_events:
#             kel.enable_events=enable_events
#             kel.on_event=on_event
#         return kel
#     return widget_creator(**kwargs)
def skivify_v2(class_,enable_events=False,on_event=None,do_dot_subevent=False,**kwargs):
    k=kwargs.pop('k',None)

    if isinstance(class_,(list,tuple)):
        class _class_(*class_):
            pass
        class_=_class_
    
    def widget_creator(**kwargs):
        kel=class_(**kwargs)
        kel.id=k
        if enable_events:
            kel.enable_events=enable_events
            kel.on_event=on_event
            kel.do_dot_subevent=do_dot_subevent
        return kel
    return widget_creator(**kwargs)
skivify=skivify_v2
# def extwidget_to_skwidget(class_,**kwargs):
#     @skwidget
#     def _external_widget(**kwargs):
#         return skivify_v2(class_,**kwargs)
#     return _external_widget(**kwargs)

def extwidget_to_skwidget(class_):
    @skwidget
    def _external_widget(**kwargs):
        return skivify_v2(class_,**kwargs)
    return _external_widget

# def extwidget_class_to_skwidget_class(class_):
#     @skwidget
#     def _external_widget(**kwargs):
#         return skivify_v2(class_,**kwargs)
#     return _external_widget

# def skivify_graphics(class_,enable_events=False,on_event=None,**kwargs):
#     k=kwargs.pop('k',None)
#     def widget_creator(**kwargs):
#         kel=class_(**kwargs)
#         # kel.id=k
#         if enable_events:
#             kel.enable_events=enable_events
#             kel.on_event=on_event
#         return kel
#     return widget_creator(**kwargs)

@skwidget
def CheckBox(active=False,k=None,**kwargs):
    from kivy.uix.checkbox import CheckBox as kvCheckBox
    kel=skivify_v2(kvCheckBox,k=k,active=active,**kwargs)
    return kel

@skwidget
def Camera(k=None,**kwargs):
    kel=skivify_v2(kvw.Camera,k=k,**kwargs)
    return kel

@skwidget
def Video(source='',k=None,**kwargs):
    from kivy.uix.video import Video as kvWd
    kel=skivify_v2(kvWd,k=k,source=source,**kwargs)
    return kel

@skwidget
def VideoPlayer(source='',k=None,**kwargs):
    from kivy.uix.videoplayer import VideoPlayer as kvWd
    kel=skivify_v2(kvWd,k=k,source=source,**kwargs)
    return kel

@skwidget
def Switch(active=False,k=None,enable_events=True,on_event='active',**kwargs):
    from kivy.uix.switch import Switch as wid
    kel=skivify_v2(wid,k=k,active=active,enable_events=enable_events,on_event=on_event,**kwargs)
    return kel

# @skwidget
# def Line(points_fun=None,k=None,**kwargs):
#     from kivy.graphics import Line as wid 
#     kel=skivify_g(wid,k=k,**kwargs)
#     if points_fun:
#         def on_parent(inst,parent):
#             print('hell on earth')
#         kel.bind(parent=on_parent)
#     return kel



@skwidget
def DropDown(widgets=[],k=None,enable_events=True,on_event='on_select',**kwargs):
    # from kivy.uix.dropdown import DropDown as wid
    wid=kvw.DropDownB
    kel=skivify_v2(wid,k=k,enable_events=enable_events,on_event=on_event,**kwargs)
    for w in widgets:
        size_hint_y=getattr(w,'size_hint_y',None)
        if size_hint_y!=None:
            w.size_hint_y=None
            w.height=44
        kel.add_widget(w)
    # kel.post='DropDown'
    def on_open(inst,v):
        # print(inst,v)
        # print(inst.attach_to)
        if v:
            # print(inst)
            # print(inst.center_x,inst.center_y)
            # print('-')
            # print(v)
            # print(v.center_x,v.center_y)
            # inst.highlight_box.pos_hint={'center_x':.5,'center_y':.5}
            
            inst.highlight_box.width=v.width
            inst.highlight_box.height=v.height

            inst.highlight_box.pos_hint=utils.resolve_relative_pos_hint(inst.highlight_box,v)
            # inst.highlight_box.center_x=v.center_x
            # inst.highlight_box.center_y=v.center_y
            # inst.highlight_box.pos=v.pos
            

            utils.Window.add_widget(inst.highlight_box)
            # print(inst.highlight_box.pos,inst.size)
            utils.Window.bind(width=kel.on_w_size)
            utils.Window.bind(height=kel.on_w_size)

        else:
            utils.Window.unbind(width=kel.on_w_size)
            utils.Window.unbind(height=kel.on_w_size)
            utils.Window.remove_widget(inst.highlight_box)
            # print('-'*20)
    #33A3CC
    kel.highlight_box=kvw.BoxLayoutB(bcolor=(0,0,0,0),lcolor=(.2, .64, .8,.5),size=(0,0),size_hint=(None,None))
    # def on_width(inst,v):
        # v0=0
        # if inst.attach_to:
            # v0=inst.attach_to.width
        # inst.highlight_box.width=inst.attach_to.width
    # kel.bind(width=on_width)
    kel.bind(attach_to=on_open)

    def on_w_size(inst,v):
        # print('hell')
        kel.dismiss()

    # setattr(kel,'on_w_size',on_w_size)
    setattr(kel,'on_w_size',on_w_size)
    # utils.Window.bind(width=kel.on_w_size)
    # utils.Window.bind(height=kel.on_w_size)
    return kel

@skwidget
def Menu(widgets=[],
    enforce_props={},
        k=None,
        enable_events=True,
        on_event='on_select',
        bcolor="#181818",lcolor='gray',
        auto_width=False,
        separator_color='',
    **kwargs):
    # from kivy.uix.dropdown import DropDown as wid
    wid=kvw.DropDownB
    kel=skivify_v2(wid,k=k,enable_events=enable_events,on_event=on_event,auto_width=auto_width,bcolor=bcolor,lcolor=lcolor,**kwargs)
    def on_w_size(*x):
        kel.dismiss()
    for iw,w in enumerate(widgets):
        size_hint_y=getattr(w,'size_hint_y',None)
        if size_hint_y!=None:
            w.size_hint_y=None
            w.height=44
        w.bind(on_release=on_w_size)
        kel.add_widget(w)
        for kp,kv in enforce_props.items():
            setattr(w,kp,kv)
        if iw<len(widgets)-1:
            kel.add_widget(SeparatorH(k=NOTKEY,height=1,bcolor=separator_color))
    # kel.post='DropDown'
    def on_open(inst,v):
        if v:
            inst.highlight_box.width=v.width
            inst.highlight_box.height=v.height

            inst.highlight_box.pos_hint=utils.resolve_relative_pos_hint(inst.highlight_box,v)
            

            utils.Window.add_widget(inst.highlight_box)
            utils.Window.bind(width=kel.on_w_size)
            utils.Window.bind(height=kel.on_w_size)

        else:
            utils.Window.unbind(width=kel.on_w_size)
            utils.Window.unbind(height=kel.on_w_size)
            utils.Window.remove_widget(inst.highlight_box)
    kel.highlight_box=kvw.BoxLayoutB(bcolor=(0,0,0,0),lcolor=(.2, .64, .8,.5),size=(0,0),size_hint=(None,None))
    kel.bind(attach_to=on_open)

    

    setattr(kel,'on_w_size',on_w_size)
    return kel


@skwidget
def ModalView(widgets=[],k=None,enable_events=False,on_event='on_pre_open',**kwargs):
    from kivy.uix.modalview import ModalView as wid
    kel=skivify_v2(wid,k=k,enable_events=enable_events,on_event=on_event,**kwargs)
    if isinstance(widgets,(list,tuple)):
        for w in widgets:
            # size_hint_y=getattr(w,'size_hint_y',None)
            # if size_hint_y!=None:
            #     w.size_hint_y=None
            #     w.height=44
            kel.add_widget(w)
    else:
        kel.add_widget(widgets)
    # kel.post='DropDown'
    return kel

@skwidget
def ComboBox(text='choice0',
    values=('choice0', 'choice1'),
    enable_events=True,
    on_event='text',
    hint_text='',
    focus=False,
    button_width=32,
    k=None,
    dark=False,
    flat=False,
    **kwargs):
    dd=DropDown(k=NOTKEY)
    if flat:
        btn=FlatB(mdi('menu-down'),disabled=True,k=NOTKEY,font_size=20,markup=True,width=button_width,size_hint_x=None)
    else:
        btn=Button(mdi('menu-down'),disabled=True,k=NOTKEY,font_size=20,markup=True,width=button_width,size_hint_x=None)
    if dark:
        tin=InputDark(text=text,focus=focus,k=NOTKEY,hint_text=hint_text)
    else:
        tin=Input(text=text,focus=focus,k=NOTKEY,hint_text=hint_text)
    
    # for vi in values:
    #     w=FlatButton(
    #         vi,size_hint_y=None,
    #         height=44,
    #         bcolor_normal='#585858',k=NOTKEY
    #         )
    #     w.bind(on_release=lambda btn: dd.select(btn.text))
    #     dd.add_widget(w)

    # def on_dismiss(*x):
        # print('here')
        # setattr(btn,'text',mdi('menu-down'))
        # tin.dispatch('on_text_validate')
    # dd.bind(on_dismiss=on_dismiss)
    dd.bind(on_dismiss=lambda *x:setattr(btn,'text',mdi('menu-down')))
    # kel=Boxit(tin,btn,**kwargs)
    class Boxtext(
            # kvw.FocusBehavior,
            kvw.BoxLayoutB
        ):
        text=StringProperty()
        values=ListProperty([])
        _focus=BooleanProperty(False)
        
        def __init__(self,**kwargs):
            self.register_event_type('on_text_validate')
            super(Boxtext,self).__init__(**kwargs)
        def on_text_validate(self,ins):
            pass

        @property
        def focus(self):
            return self._focus
        @focus.setter 
        def focus(self,val):
            self._focus=val
            tin.focus=val
        def on_values(self,instance,val):
            if not val:
                btn.disabled=True
                return
            else:
                btn.disabled=False
            dd.clear_widgets()
            for vi in val:
                w=FlatButton(
                    vi,size_hint_y=None,
                    height=44,
                    bcolor_normal='#585858',k=NOTKEY
                    )
                w.bind(on_release=lambda btn: dd.select(btn.text))
                dd.add_widget(w)
    kel=skivify_v2( Boxtext,k=k,enable_events=enable_events,on_event=on_event, text=tin.text,values=values,**kwargs)
    kel.tin=tin
    kel.btn=btn
    kel.add_widget(tin)
    kel.add_widget(btn)
    def on_btn_rel(*x):
        btn.text=mdi('menu-up')
        dd.open(kel)

    btn.bind(on_release=on_btn_rel)
    tin.bind(on_text_validate=lambda ins:kel.dispatch('on_text_validate',kel))
    # btn.bind(on_release=lambda *x:pass if dd.values else setattr(dd,'values',[dd.text]))
    # btn.bind(on_release=lambda *x:dd.open(kel))
    # btn.bind(on_release=lambda *x:setattr(btn,'text',icons_material('mdi-menu-up')))
    def on_select(ins,x):
        setattr(tin, 'text', x)
        kel.dispatch('on_text_validate',kel)
    dd.bind(on_select=on_select)
    # dd.bind(on_select=lambda instance, x: setattr(tin, 'text', x))
    tin.bind(text=lambda instance,value:setattr(kel,'text',value))
    tin.bind(on_text_validate=lambda ins:kel.dispatch('on_text_validate',kel))
    kel.bind(text=lambda instance,value:setattr(tin,'text',value))
    # kel.bind(on_focus=lambda instance,val:setattr(tin,'focus',val))
    # kel.id=k
    # kel.enable_events=enable_events
    # kel.on_event='text'
    
    return kel

@skwidget
def DatePicker(k=None,year=2020,month=1,enable_events=True,on_event='on_release',**kwargs):
    kel=skivify_v2(kvw.DatePicker,year=year,month=month,k=k,**kwargs)
    return kel

Calendar=DatePicker

# @skwidget
# def ComboBox(
#     text='choice0',
#     values=('choice0', 'choice1', 'choice2', 'choice3'),k=None,):
    


@skwidget
def JoinLabel(texts=['text1','text2','text3'],k=None,focus_behavior=False,**kwargs):
    # kwargs=_preproces(**kwargs)
    # global _future_elements, _future_bind
    # print(kwargs)
    if focus_behavior:
        kvWd=kvw.FocusLabelB
    else:
        kvWd= kvw.LabelB

    class _(kvWd):
        texts=kvw.ListProperty(['text1','text2','text3'])
        # text=' '.join(texts)
        def on_texts(self,*args):
            # print('hell')
            self.text=' '.join(texts)


    kel=_(texts=texts,**kwargs)


    
    kel.id=k

    kel.post='LabelLike'

    # _future_elements.append(kel)
    return kel

T=Text=Label

# @skwidget
# def ScrollLabel(text='',k=None,focus_behavior=False,**kwargs):
#     # kwargs=_preproces(**kwargs)
#     # global _future_elements, _future_bind
#     # print(kwargs)
#     if focus_behavior:
#         kel=kvw.FocusLabelB(text=text,**kwargs)
#         def on_f(*_):
#             print(_)
#         kel.bind(on_focus=on_f)
#     else:
#         kel=kvw.LabelB(text=text,**kwargs)
    
#     kel.id=k

#     # kel.post='LabelLike'

#     kel.bind(size=kel.setter('text_size'))
#     # kel.text_size = self.size

#     skel=kvw.ScrollLabel(kel)

#     _post_elements['LabelLike'].append(kel)

#     # _future_elements.append(kel)
#     return skel


@skwidget
def LargeText(text='',k=None,focus_behavior=False,
    shorten=True,
    halign='center',
    valign='middle',
    shorten_from='right',
    size_behavior='normal',
    **kwargs):
    # kwargs=_preproces(**kwargs)
    # global _future_elements, _future_bind
    if focus_behavior:
        kvWd=kvw.FocusLabelB
        
    else:
        kvWd=kvw.LabelB
    kel=kvWd(text=text,
        shorten=shorten,
        halign=halign,
        valign=valign,
        shorten_from=shorten_from,
        # limit_render_to_text_bbox=True,
        **kwargs)
    # def on_size(instance,value):
    #     # padh=instance.padding[0]+instance.padding[2]
    #     instance.text_size=value[0],None
    # kel.bind(size=on_size)

    if size_behavior=='none':
        pass
    elif size_behavior=='normal':
        kel.bind(size=lambda inst,siz:setattr(inst,'text_size',inst.size))
    elif size_behavior=='text':
        # this label’s height will be set to the text content
        kel.size_hint_y=None
        kel.bind(texture_size=lambda inst,siz:setattr(inst,'height',siz[1]))
        kel.bind(width=lambda inst,v:setattr(inst,'text_size',(v, None)))
    elif size_behavior=='texth':
        # this label’s width will be set to the text content
        kel.size_hint_x=None
        kel.bind(texture_size=lambda inst,siz:setattr(inst,'width',siz[0]))
        kel.bind(height=lambda inst,v:setattr(inst,'text_size',(None, v)))
    
    kel.id=k

    kel.post='LabelLike'



    # _future_elements.append(kel)
    return kel

@skwidget
def Boxit(*widgets,k=None,base_cls=None,**kwargs):
    # kwargs=_preproces(**kwargs)
    if base_cls==None:
        kvWd=kvw.BoxLayout
    else:
        kvWd=base_cls
    kel=skivify_v2(kvWd,k=k,**kwargs)

    # kel.id=k

    for w in widgets:
        kel.add_widget(w)
    # _future_elements.append(kel)
    return kel

@skwidget
def BoxitH(*widgets,k=None,orientation='horizontal',**kwargs):
    # kwargs=_preproces(**kwargs)
    kel=skivify_v2(kvw.BoxLayoutB,k=k,orientation=orientation,**kwargs)

    # kel.id=k

    for w in widgets:
        kel.add_widget(w)

    
    setattr(kel,'_isbox',kel.orientation)
    # _future_elements.append(kel)
    return kel

@skwidget
def LabelCheck(text='checkbox',halign='left',valign='middle',enable_events=False,on_event='active',cwidth=40,active=False,k=None,**kwargs):
    kel=skivify_v2(kvw.LabelCheck,text=text,active=active,cwidth=cwidth,k=k,halign=halign,valign=valign,enable_events=enable_events,on_event=on_event,**kwargs)
    return kel
    

@skwidget
def HoverBoxit(*widgets,k=None,enable_events=True,hover_highlight=False,do_dot_subevent=True,on_event=('on_enter','on_leave'),**kwargs):
    # kwargs=_preproces(**kwargs)
    # kvWd=kvw.BoxLayoutB
    if hover_highlight:
        class kvWd(kvb.HoverHighlightBehavior,kvw.BoxLayoutB):
            pass
        
    else:
        class kvWd(kvb.HoverBehavior,kvw.BoxLayoutB):
            pass

    # kel=kvWd(orientation=orientation,**kwargs)
    kel=skivify_v2(kvWd,k=k,enable_events=enable_events,do_dot_subevent=do_dot_subevent,on_event=on_event,**kwargs)


    # kel.id=k

    for w in widgets:
        kel.add_widget(w)

    

    # _future_elements.append(kel)
    return kel

@skwidget
def Grid(layout=[[]],k=None,navigation_behavior=False,**kwargs):
    # kwargs=_preproces(**kwargs)

    
    if navigation_behavior:
        class kvWd(kvw.GridLayoutB,kvb.GridNavigationBehavior):
            pass
    else:
        kvWd=kvw.GridLayoutB

    
    # kel=kvWd(orientation=orientation,**kwargs)
    

    rows=len(layout)
    
    kel=skivify_v2(kvWd,k=k,rows=rows,**kwargs)
    
    # if not 'nrows' in kwargs and not 'ncols' in kwargs:
    max_cols = 0
    for row in layout:
        if len(row) > max_cols:
            max_cols = len(row)
    i=0
    for row in layout:
        i += 1
        elnum = -1
        for el in row:
            elnum += 1
            kivy_el = el
            kel.add_widget(kivy_el)

        lenrow = len(row)
        addnvoids = 0
        if lenrow < max_cols:
            addnvoids = max_cols - lenrow
        for v in range(addnvoids):
            kel.add_widget(
                        Fill()
                )
    # else:
    #     for row in layout:
    #         if isinstance(row,(list,tuple)):
    #             for w in row:
    #                 kel.add_widget(w)
    #         else:
    #             kel.add_widget(w)


    # _future_elements.append(kel)
    return kel

_web_started=False
@skwidget
def WebView(url='https://www.google.com',k=None,
    # maximum_width=None,
    # enable_events=True,do_dot_subevent=True,on_event=('on_enter','on_leave'),
    orientation='horizontal',
    **kwargs):
    
    # from . import webview
    from .webview_enhance import enhance
    import sk_webview as webview
    # import webview
    from kivy.uix.behaviors import FocusBehavior
    import threading
    class kvWd(kvb.HoverBehavior,FocusBehavior,kvw.BoxLayoutB):
        hwnd=None
        _other_was_focused=None
        def __init__(self,**kwargs):
            super(kvWd,self).__init__(**kwargs)
            Clock.schedule_once(self._on_next_frame)
        def on_parent(self,ins,parent):
            # print(f"{parent = }")
            if parent==None and hasattr(self,'window'):
                try:
                    self.window.destroy()
                    # self.ewin.hide()
                except:
                    traceback.print_exc()
        def _on_next_frame(self,dt):
            # print('_on_next_frame')
            self.webview=webview
            window=webview.create_window('WebView', url=url,
            frameless=True, 
            # easy_drag=True,
            # debug=True
            # focus=False,
            hidden=True
            )
            self.window=window
            # print('window_created',self.window)
            Clock.schedule_once(self._schedule_start)

        def _schedule_start(self,dt):
            # print('starting thread')
            self.thread = threading.Thread(target=self._start)
            self.thread.name='MainThread'
            self.thread.daemon = True
            # print('thread_started')
            self.thread.start()


        def _start(self):
            # print('_start')
            global _web_started

            if not _web_started:
                _web_started=True
                self.webview.start(func=self._attach, args=[],debug=False)
                # print('webview finished')
            else:
                self._attach()
        def _attach(self,*args):
            # print('_attach')
            external_hwnd=None
            while not self.window.native:
                # print(f"{self.window.native = }")
                time.sleep(.2)
            external_hwnd=self.window.native.Handle.ToInt32()
            
            # print('almost')
            from .native import ExternalWindow,set_constant_window_colors

            
            ewin=ExternalWindow(external_hwnd)
            self.ewin=ewin

            self.hwnd=external_hwnd

            _app=utils.wait_result(App.get_running_app)
            # while not App.get_running_app():
            #     time.sleep(.1)
            self._app=_app
            Clock.schedule_once(lambda dt: _app.on_icon(_app,_app.get_application_icon()))

            self.ewin.set_parent(_app.hwnd)
            self.ewin.show()

            def move_subw(ins,size):
                try:
                    apos=ins.to_window(*ins.pos)
                    win32gui.MoveWindow(
                        ins.hwnd,
                        round(apos[0]), round(_app.kvWindow.height-apos[1]-ins.height),
                        round(ins.width), round(ins.height),
                        True
                    )
                except:
                    pass
            Clock.schedule_once(lambda dt: move_subw(self,self.size))
            self.bind(size=move_subw,pos=move_subw)
        
        def on_enter(self):
            try:
                self._other_was_focused=self.get_focus_previous().focus
                self.focus=True
                self.ewin.bring_to_front()
                # Clock.schedule_once(lambda dt:)
            except:
                pass

        def on_leave(self):
            try:
                self.focus=False
                if self._other_was_focused:
                    self.get_focus_previous().focus=True
                self._app.bring_to_front()
                # Clock.schedule_once(lambda dt:)
            except:
                pass
        def destroy(self):
            self.window.destroy()
            # self.ewin.close()
            if self.parent:
                self.parent.remove_widget(self)
        def destroy_all(self):
            global _web_started
            for window in self.webview.windows:
                try:
                    self.window.destroy()
                except:
                    pass
            # _web_started=False
            # print('webview cleared')





    kel=skivify_v2(kvWd,k=k,
        # enable_events=enable_events,do_dot_subevent=do_dot_subevent,on_event=on_event,
        # unfocus_on_touch=True,
        **kwargs)

    return kel

# _web_started_pr
# @skwidget
# def WebViewPr(url='https://www.google.com',k=None,
#     **kwargs):
#     from .webview_enhance import enhance
#     import sk_webview as webview
#     # import webview
#     import threading
#     class kvWd(kvb.HoverBehavior,kvw.BoxLayoutB):
#         hwnd=None

#     kel=skivify_v2(kvWd,k=k,
#         # enable_events=enable_events,do_dot_subevent=do_dot_subevent,on_event=on_event,
#         **kwargs)
    
#     return kel

@skwidget
def External(title="External window title",hwnd=None,k=None,
    **kwargs):
    import threading
    from .native import ExternalWindow,find_hwnd_by_title,set_constant_window_colors
    class kvWd(kvb.HoverBehavior,kvw.BoxLayoutB):
        hwnd=kvw.NumericProperty(None)

        def __init__(self, **kwargs):
            self.title=kwargs.pop('title','')
            self.hwnd=kwargs.pop('hwnd',None)
            super(kvWd, self).__init__(**kwargs)

        def on_parent(self,*a):
            Clock.schedule_once(self._thread_start)
        def _thread_start(self,dt):
            self.thread = threading.Thread(target=self._attach)
            self.thread.name='MainThread'
            self.thread.daemon = True
            self.thread.start()
        def _attach(self):
            if self.hwnd==None:
                self.hwnd=find_hwnd_by_title(self.title)
            
            self.ewin = ExternalWindow(self.hwnd)
            _app=App.get_running_app()
            self._app=_app
            self.ewin.set_parent(_app.hwnd)
            set_constant_window_colors(self._app.hwnd)
            self.ewin.show()

            def move_subw(ins,size):
                try:
                    apos=ins.to_window(*ins.pos)
                    win32gui.MoveWindow(
                        ins.hwnd,
                        round(apos[0]), round(_app.kvWindow.height-apos[1]-ins.height),
                        round(ins.width), round(ins.height),
                        True
                    )
                except:
                    pass
            move_subw(self,self.size)
            self.bind(size=move_subw,pos=move_subw)
        def on_enter(self):
            try:
                self.ewin.bring_to_front()
            except:
                pass
        def on_leave(self):
            try:
                self._app.bring_to_front()
            except:
                pass

    kel=skivify_v2(
        kvWd,k=k,
        title=title,
        hwnd=hwnd,
        **kwargs
        )
    
    return kel
    

def TitlebarCloseButton(markup=True,k=NOTKEY,size="x44",hover_highlight=True,lcolor='',bcolor_down='red',**kwargs):
    kel= FlatButton(text=kwargs.pop('text',mdi('window-close')),
        markup=markup,k=k,size=size,lcolor=lcolor,hover_highlight=hover_highlight,bcolor_down=bcolor_down,
            **kwargs
        )

    def onc(*l):
        self=App.get_running_app()
        self.trigger_event('__Close__')
        Clock.schedule_once(lambda dt:self.close())

    kel.bind( on_release=onc)

    return kel

def TitlebarRestoreButton(text_states=(None,None),markup=True,k=NOTKEY,size="x44",lcolor='',hover_highlight=True,bcolor_down='gray',**kwargs):

    if text_states[1]:
        text1=text_states[1]
    elif text_states[1] == None:
        text1=mdi('window-maximize')
            

    if text_states[0]:
        text0=text_states[0]
    elif text_states[0] == None:
        text0=kwargs.pop('text',mdi('window-restore'))


    kel=FlatButton(text=text0,
        markup=markup,k=k,size=size,lcolor=lcolor,hover_highlight=hover_highlight,bcolor_down=bcolor_down,

        **kwargs
        )
    def onres(*l):
        self=App.get_running_app()
        if self.window_is_maximized:
            self.restore()
            
        else:
            self.maximize()

    def onres_set(inst,val):
        if val:
            # kel.text=_mdi('mdi-window-restore')
            kel.text=text0
        else:
            kel.text=text1
    def on_run(dt):
        # print('hell'*20)
        self=App.get_running_app()
        self.bind(window_is_maximized=onres_set)
        if self.window_is_maximized:
            kel.text=text0
        else:
            kel.text=text1


    kel.bind(  on_release=onres)
    Clock.schedule_once(on_run)

    return kel

def TitlebarMinimizeButton(markup=True,k=NOTKEY,size="x44",lcolor='',hover_highlight=True,bcolor_down='gray',**kwargs):
    kel=FlatButton(text=kwargs.pop('text',mdi('window-minimize')),
        markup=markup,k=k,size=size,lcolor=lcolor,hover_highlight=hover_highlight,bcolor_down=bcolor_down,
        **kwargs
        )
    kel.bind(  on_release=lambda *l: App.get_running_app().minimize()   )
    
    return kel

def TitlebarTitle(k=NOTKEY,padding=[8,0],halign='left',**kwargs):
    kel=LargeText(k=k,padding=padding,halign=halign,font_size=kwargs.pop("font_size",12),**kwargs)

    def on_run(dt):
        self=App.get_running_app()
        kel.text=self.title
        self.bind(title=lambda inst,val:setattr(kel,'text',val))

    Clock.schedule_once(on_run)

    return kel

def TitlebarIcon(**kwargs):
    kel=Image(async_load=False,k=NOTKEY,size_hint_x=None,width=32,**kwargs)
    def on_run(dt):
        self=App.get_running_app()
        if self.icon:
            kel.source=self.icon
        else:
            kel.source='skdata/logo/simplekivy-icon-32.png'
        self.bind(icon= lambda inst,val:setattr(kel,'source',val if val else 'skdata/logo/simplekivy-icon-32.png'))

    Clock.schedule_once(on_run)
    return kel

@skwidget
def Titlebar(k='titlebar',size="y32",padding=[4,4],orientation='horizontal',**kwargs):
    # kwargs=_preproces(**kwargs)
    kel=skivify_v2(kvw.BoxLayoutB,k=k,size=size,orientation=orientation,padding=padding,**kwargs)

    # kel.id=k

    # kel.icon=Image(async_load=False,k=NOTKEY,size_hint_x=None,width=32)
    kel.icon=TitlebarIcon()
    kel.add_widget(kel.icon)
    
    # kel.title=LargeText(k=NOTKEY,padding=[8,0],halign='left')
    kel.title=TitlebarTitle()
    kel.add_widget(kel.title)


    # def on_run(dt):
    #     self=App.get_running_app()
    #     kel.title.text=self.title

    #     if self.icon:
    #         kel.icon.source=self.icon
    #     else:
    #         kel.icon.source='data/logo/kivy-icon-32.png'

    #     self.bind(title=lambda inst,val:setattr(kel.title,'text',val))
    #     self.bind(icon= lambda inst,val:setattr(kel.icon,'source',val if val else 'data/logo/kivy-icon-32.png'))

        


    # Clock.schedule_once(on_run)

    

    kel.add_widget(Fill())

    # kel.min=FlatButton(_mdi('mdi-window-minimize'),markup=True,k=NOTKEY,size_hint_x=None,width=32,lcolor='',hover_highlight=True,bcolor_down='gray')
    kel.min=TitlebarMinimizeButton()
    kel.add_widget(kel.min)
    
    # kel.res=FlatButton(_mdi('mdi-window-restore'),markup=True,k=NOTKEY,size_hint_x=None,width=32,lcolor='',hover_highlight=True,bcolor_down='gray')
    kel.res=TitlebarRestoreButton()
    kel.add_widget(kel.res)
    
    # kel.clo=FlatButton(_mdi('mdi-window-close'),markup=True,k=NOTKEY,size_hint_x=None,width=32,hover_highlight=True,lcolor='',bcolor_down='red')
    kel.clo=TitlebarCloseButton()
    kel.add_widget(kel.clo)

    # no longer necesary, only for other custom titlebar defined by the user, this one is internally handled.
    # kel.post='TitleBar' 

    return kel

Boxit=BoxitH
@skwidget
def Pageit(*widgets,k=None,**kwargs):
    kel=skivify_v2(kvw.PageLayoutB,k=k,**kwargs)
    # kel.id=k
    for w in widgets:
        kel.add_widget(w)
    return kel
@skwidget
def BoxitV(*widgets,k=None,orientation='vertical',**kwargs):
    # kwargs=_preproces(**kwargs)
    kel=skivify_v2(kvw.BoxLayoutB,k=k,orientation=orientation,**kwargs)

    # kel.id=k

    for w in widgets:
        kel.add_widget(w)

    setattr(kel,'_isbox',kel.orientation)
    # _future_elements.append(kel)
    return kel

@skwidget
def Stackit(*widgets,k=None,orientation='lr-tb',**kwargs):
    kel=skivify_v2(kvw.StackLayoutB,k=k,orientation=orientation,**kwargs)

    for w in widgets:
        kel.add_widget(w)
    return kel

@skwidget
def Relativeit(*widgets,k=None,**kwargs):
    kel=skivify_v2(kvw.RelativeLayoutB,k=k,**kwargs)

    for w in widgets:
        kel.add_widget(w,index=-1)
    return kel

@skwidget
def Floatit(*widgets,k=None,**kwargs):
    kel=skivify_v2((kvw.BgLine,kvw.FloatLayout),k=k,**kwargs)

    for w in widgets:
        kel.add_widget(w,index=-1)
    return kel

@skwidget
def RoundRelativeit(*widgets,k=None,**kwargs):
    kel=skivify_v2(kvw.RoundCornerLayout,k=k,**kwargs)

    # kel.id=k

    for w in widgets:
        kel.add_widget(w)
    return kel

@skwidget
def RoundButtonRelativeit(*widgets,k=None,enable_events=True,on_event='on_release',hover_highlight=False,focus_behavior=False,
    lcolor=[.5,.5,.5,1],
    bcolor_normal=[.345, .345, .345, 0],
    # bcolor=[.345, .345, .345, 0],
    bcolor_down=[.2, .64, .8, 1],
    **kwargs):
    kvWd=kvw.RoundBLayout

    if focus_behavior:
        class _(kvb.FocusBehavior,kvWd):
            pass
        kvWd=_
    if hover_highlight:
        class _(kvb.HoverHighlightBehavior,kvWd):
            pass
        kvWd=_


    kel=skivify_v2(kvWd,k=k,lcolor=lcolor,bcolor_down=bcolor_down,bcolor_normal=bcolor_normal,
        # bcolor=bcolor,
        enable_events=enable_events,on_event=on_event,**kwargs)

    # kel.id=k
    # kel.bcolor_normal=kel.bcolor_normal

    # kel.enable_events=enable_events
    # kel.on_event=on_event

    for w in widgets:
        kel.add_widget(w)
    return kel

# @skwidget
# def ButtonRelativeit(*widgets,k=None,enable_events=True,on_event='on_release',hover_highlight=False,focus_behavior=False,**kwargs):
#     kvWd=kvw.RelativeBLayout

#     if focus_behavior:
#         class _(kvb.FocusBehavior,kvWd):
#             pass
#         kvWd=_
#     if hover_highlight:
#         class _(kvb.HoverHighlightBehavior,kvWd):
#             pass
#         kvWd=_


#     kel=kvWd(**kwargs)

#     kel.id=k

#     kel.enable_events=enable_events
#     kel.on_event=on_event

#     for w in widgets:
#         kel.add_widget(w)
#     return kel

@skwidget
def Boxit_scatter(*widgets,k=None,**kwargs):
    # kwargs=_preproces(**kwargs)

    from kivy.uix.scatterlayout import ScatterLayout as kvWd

    kel=skivify_v2(kvWd,k=k,**kwargs)

    for w in widgets:
        kel.add_widget(w)

    # _future_elements.append(kel)
    return kel
Scatterit=Boxit_scatter

@skwidget
def Boxit_angle_bbox(*widgets,k=None,enable_events=True,on_event="on_release",**kwargs):
    # kwargs=_preproces(**kwargs)

    kvWd=kvw.AngleBBoxLayout

    kel=skivify_v2(kvWd,k=k,enable_events=True,on_event=on_event,**kwargs)

    for w in widgets:
        kel.add_widget(w)

    # _future_elements.append(kel)

    # kel.size=kwargs.get('size',(100,100))
    # kel.size_hint=kwargs.get('size',(1,1))

    return kel
ButtonBoxitAngle=Boxit_angle_bbox

@skwidget
def StripLayout(*widgets,k=None,rows=1,**kwargs):
    # kwargs=_preproces(**kwargs)

    # kvWd=kvw.AngleBBoxLayout
    from kivy.uix.tabbedpanel import StripLayout as kvWd

    kel=skivify_v2(kvWd,k=k,rows=rows,**kwargs)

    for w in widgets:
        kel.add_widget(w)

    # _future_elements.append(kel)

    # kel.size=kwargs.get('size',(100,100))
    # kel.size_hint=kwargs.get('size',(1,1))

    return kel

@skwidget
def Scatter(widget,k=None,**kwargs):
    # kwargs=_preproces(**kwargs)

    # from kivy.uix.scatter import Scatter as kvWd

    kvWd=kvw.ScatterB

    kel=skivify_v2(kvWd,k=k,**kwargs)
    # kel.id=k

    # for w in widgets:
    kel.add_widget(widget)

    # _future_elements.append(kel)
    return kel

# @skwidget
# def TabbedPanelItem(hover_highlight=False,k=None,**kwargs):
#     kvWd=kvw.TabbedPanelItem
#     if hover_highlight:
#         class kvWd(kvw.BgLine,kvb.HoverHighlightBehavior,kvw.TabbedPanelItem):
#             markup=kvw.BooleanProperty(True)




#     kel=skivify_v2(kvWd,k=k,**kwargs)
#     return kel

@skwidget
def Tab2(pannels={},
        k=None,
        tab_pos = 'top_left',
        do_default_tab=False,
        head_label_args={'size_behavior':'texth','padding':[16,0,16,0],'lcolor':'gray'},
        content_box_args={'lcolor':'gray','padding':4},
        strip_args={'bcolor':[.2, .64, .8, 1],'pos_hint':{'bottom':0}},
        **kwargs
        ):
    # kel=kvw.BoxLayoutB(orientation="vertical",**kwargs)

    class kvWd(kvw.RelativeLayout):
        # orientation=kvw.OptionProperty("vertical",options=("vertical","horizontal")):
        pannels=kvw.ObjectProperty({})
        tab_pos=kvw.OptionProperty('top_left',options=('left_top', 'left_mid', 'left_bottom', 'top_left', 'top_mid', 'top_right', 'right_top', 'right_mid', 'right_bottom', 'bottom_left', 'bottom_mid', 'bottom_right'))
        do_default_tab=kvw.BooleanProperty(False)
        # def _get_headers(self):

        # headers=kvw.AliasProperty()
        def __init__(self,**kwargs):
            super(kvWd,self).__init__(**kwargs)
            
            # self._rel=kvw.RelativeLayout(size_hint=(1,None),height=40)
            # self._headbox=BoxitH(k=NOTKEY,size='xchildreny40',pos_hint={'left':0,'top':1},spacing=6,)
            self._headbox=BoxitH(k=NOTKEY,
                size='xchildreny40',
                # pos_hint={'left':0,'top':1},
                spacing=6,
                # lcolor='red'
                )
            # self.bind(pannels=lambda ins,val:setattr(self._headbox,'width',len(val)))
            # self.bind(pannels=lambda ins,val:Clock.schedule_once())
            # self.setter('pannels')(self,self.pannels)
            # setattr(self._headbox,'width',len(val))

            self.add_widget(self._headbox)

            # self._head_scatter=Scatter(self._headbox,k=NOTKEY)
            # self._headbox.bind(
            #     size=self._head_scatter.setter('size'),
            #     size_hint=self._head_scatter.setter('size_hint'),
            #     pos_hint=self._head_scatter.setter('pos_hint'),
            #     )
            # self.add_widget(self._head_scatter)
            
            

            self.content_box=kvw.BoxLayoutB(**content_box_args)
            self.add_widget(self.content_box)

            # print(self.pannels)
            self._sman=Screens(self.pannels,k=NOTKEY,transition='no')
            self.content_box.add_widget(self._sman)
            self.bind(size=self._up_bbox_posV)

            
            ik=-1
            group_id=id(self)
            self.headers={}
            self._strip_color=strip_args.get('bcolor',[.2, .64, .8, 0])
            head_lcolor=head_label_args.pop('lcolor','gray')
            for k,v in self.pannels.items():
                ik+=1
                lbl=Label(k,k=NOTKEY,**head_label_args)
                sep=SeparatorH(k=NOTKEY,**strip_args)

                # lbl.add_widget(Boxit(k=NOTKEY,bcolor='gray',size='y10'))
                # Clock.schedule_once(lambda dt:setattr(lbl,'text',k))
                # lbl.texture_update()
                
                toggle=ToggleButtonBoxit(
                        sep,
                        lbl,
                        # sep,
                        # orientation='vertical',
                        size='xchildreny40',
                        k=NOTKEY,
                        # lcolor=(1,0,0,.5),
                        lcolor=head_lcolor,
                        bcolor_down=[0,0,0,0],
                        # padding=[16,0,16,0],
                        hover_highlight=True,
                        # bcolor_down='gray',
                        # spacing=4,
                        # lwidth=3,
                        pos_hint={'center_x':.5,'center_y':.5},
                        group=group_id,
                        allow_no_selection=False,
                        state='down' if ik==0 else 'normal',base_cls=kvw.RelativeLayoutB
                        )
                toggle._sep=sep
                toggle.text=k
                # Clock.schedule_once(lambda dt:toggle.update_size_on_children())
                def on_state(ins,val):
                    if val=='down':
                        setattr(self._sman,'current',ins.text)
                        setattr(ins._sep,'bcolor',self._strip_color)
                    else:
                        setattr(ins._sep,'bcolor',[0,0,0,0])

                def on_size(ins,val):
                    setattr(ins._sep,'width',val)
                toggle.bind(
                    # width=sep.setter('width'),
                    width=on_size,
                    state=on_state
                    )
                on_state(toggle,toggle.state)

                self._headbox.add_widget(
                    toggle
                    )
                
                self.headers[k]=toggle

                # toggle.update_size_on_children()
            # self._headbox.do_layout()
            # self._headbox.update_size_on_children()
            # if self.tab_pos=='top_left':
            self.on_tab_pos(self,self.tab_pos)
        def _update_headpos(self,dt):
            tp=self.tab_pos
            v,h=tp.split('_')
            # print(tp)
            if tp=='top_left':
                self._headbox.pos_hint={'top':1,'left':0}
            elif tp=='top_mid':
                self._headbox.pos_hint={'top':1,'center_x':.5}
            elif tp=='top_right':
                self._headbox.pos_hint={'top':1,'right':1}
            elif tp=='bottom_left':
                self.content_box.pos_hint={'top':1}
                self._headbox.pos_hint={'bottom':0,'left':0}
            elif tp=='bottom_mid':
                self.content_box.pos_hint={'top':1}
                self._headbox.pos_hint={'bottom':0,'center_x':.5}
            elif tp=='bottom_right':
                self.content_box.pos_hint={'top':1}
                self._headbox.pos_hint={'bottom':0,'right':1}
            elif tp=='left_top':
                self.content_box.pos_hint={'right':1}
                self._headbox.pos_hint={'left':0,'top':1}
                
            elif tp=='left_mid':
                self.content_box.pos_hint={'right':1}
                self._headbox.pos_hint={'center_y':.5}
            elif tp=='left_bottom':
                self.content_box.pos_hint={'right':1}
                self._headbox.pos_hint={'bottom':0}
                # Clock.schedule_once(lambda dt:setattr(self._headbox,'pos_hint',{'bottom':0}))
            elif tp=='right_top':
                self.content_box.pos_hint={'left':0}
                self._headbox.pos_hint={'right':1,'top':1}
                
            elif tp=='right_mid':
                self.content_box.pos_hint={'left':0}
                self._headbox.pos_hint={'right':1,'center_y':.5}
            elif tp=='right_bottom':
                self.content_box.pos_hint={'left':0}
                self._headbox.pos_hint={'right':1,'bottom':0}

            if v in ('top','bottom'):
                self._headbox.orientation='horizontal'
                self._headbox.sizeofchildren='xchildrenychild_max'
                self.unbind(size=self._up_bbox_posH)
                self.bind(size=self._up_bbox_posV)
                self._up_bbox_posV(self,self.size)
            else:
                self._headbox.orientation='vertical'
                self._headbox.sizeofchildren='xchild_maxychildren'
                # self._headbox
                self.unbind(size=self._up_bbox_posV)
                self.bind(size=self._up_bbox_posH)
                self._up_bbox_posH(self,self.size)

            if v in ('right'):
                for child in self._headbox.children:
                    child.pos_hint={'left':0}
            elif v in ('left'):
                
                for child in self._headbox.children:
                    child.pos_hint={'right':1}

            self._headbox.update_size_on_children()
            # print(self.tab_pos)
        def _up_bbox_posV(self,ins,val):
            self.content_box.size_hint_x=1
            self.content_box.size_hint_y=1-(self._headbox.height+4)/self.height
        def _up_bbox_posH(self,ins,val):
            self.content_box.size_hint_y=1
            self.content_box.size_hint_x=1-(self._headbox.width+4)/self.width
        def on_tab_pos(self,ins,val):
            # print(val)
            Clock.schedule_once(self._update_headpos)

        def _get_current(self):
            return self._sman.current
        def _set_current(self,v):
            self.headers[v].trigger_action()
        def _get_current_tab(self):
            # cs=self._sman.current_screen
            # setattr(cs,'content',cs.children)
            # return cs
            return self._sman.current_screen

        current=kvw.AliasProperty(_get_current,_set_current)
        current_tab=kvw.AliasProperty(_get_current_tab)
    kel=skivify_v2(kvWd,tab_pos=tab_pos,do_default_tab=do_default_tab,pannels=pannels,k=k,**kwargs)
    return kel




#     # kel.id=k

#     kel=skivify_v2(kvWd,k=k,pannels=pannels,tab_pos=tab_pos,do_default_tab=do_default_tab,**kwargs)

#     # _future_elements.append(kel)
#     return kel



@skwidget
def Tab(
            pannels={},
            k=None,
            tab_pos = 'top_left',
            do_default_tab=False,
            **kwargs
        ):
    # kwargs=_preproces(**kwargs)
    # global _future_elements, _future_bind
    class kvWd(kvw.TabbedPanel):
        _pannels={}

        # @property
        def _get_current(self):
            # print(self._pannels)
            return self.current_tab.text
        # @current.setter
        def _set_current(self,v):
            try:
                self.switch_to(self._pannels[v])
            except:
                for ti in self.tab_list:
                    self._pannels[ti.text]=ti
                self.switch_to(self._pannels[v])
        current=kvw.AliasProperty(_get_current,_set_current)

    # kel=kvw.TabbedPanel(do_default_tab=do_default_tab,tab_pos=tab_pos,**kwargs)
    kel=skivify_v2(kvWd,k=k,do_default_tab=do_default_tab,tab_pos=tab_pos,**kwargs)
    for k,v in pannels.items():
        ti=kvw.TabbedPanelItem(text=k)
        ti.add_widget(v)
        kel.add_widget(ti)
    
    # _future_elements.append(kel)
    return kel

# def Button(text='button',enable_events=True,k=None,on_event='on_release', **kwargs):
#     kwargs=_preproces(**kwargs)
#     global _future_elements, _future_bind
#     kel=kvw.kvButton(text=text,**kwargs)
    
#     if k==None and text:
#         k=text

#     kel.id=k

#     kel.enable_events=enable_events
#     kel.on_event=on_event

#     if enable_events:
#         _future_bind.append(kel)

#     _future_elements.append(kel)
#     return kel
# @skwidget
# def Button(text='button',enable_events=True,k=None,on_event='on_release', **kwargs):
#     # bcolor=kwargs.pop('bcolor',None)
#     # if bcolor:
#     #     kwargs['background_color']=bcolor
#     kel=kvw.Button(text=text,**kwargs)
    
#     if k==None and text:
#         k=text

#     kel.id=k


#     kel.enable_events=enable_events
#     kel.on_event=on_event

#     return kel

@skwidget
def Button(text='button',enable_events=True,hover_highlight=False,k=None,on_event='on_release', **kwargs):
    kvWd=kvw.Button
    if hover_highlight:
        class _(kvWd,kvb.HoverHighlightBehavior):
            pass
        kvWd=_
    kel=skivify_v2(kvWd,text=text,enable_events=enable_events,k=k,on_event=on_event, **kwargs)
    # kel.bcolor=kwargs.get('bcolor',kvWd.bcolor.defaultvalue)
    if k==None and text:
        kel.id=text
    return kel
B=Button

@skwidget
def ActionButton(text='actionbutton',k=None,enable_events=True,on_event='on_release',**kwargs):
    from kivy.uix.actionbar import ActionButton  as kvWd
    kel=skivify_v2(kvWd,text=text,k=k,enable_events=enable_events,on_event=on_event,**kwargs)
    if k==None and text:
        kel.id=text
    return kel
@skwidget
def ActionInput(text='',multiline=False,enable_events=False,k=None,on_event='on_text_validate', **kwargs):
    from kivy.uix.actionbar import ActionItem
    W=kvw.kvInput
    class W(kvw.kvInput,ActionItem):
        last_added=''
        def __init__(self, **kwargs):
            self.register_event_type('on_insert_text')
            super(W, self).__init__(**kwargs)
        def on_insert_text(self):
            pass
        def insert_text(self, substring, from_undo=False):
            s = substring
            self.last_added=s
            self.dispatch('on_insert_text')
            return super().insert_text(s, from_undo=from_undo)

    kel=skivify_v2(W,k=k,multiline=multiline,enable_events=enable_events,on_event=on_event)
    return kel

@skwidget
def ActionLabelCheck(text='checkbox',halign='left',
    valign='middle',bcolor=[0.133,0.133,0.133,1],enable_events=False,on_event='active',
    size_hint_y=0.8,pos_hint=pos_hints.center_y,
    cwidth=40,active=False,k=None,**kwargs
    ):
    from kivy.uix.actionbar import ActionItem
    class kvWd(kvw.LabelCheck,ActionItem):
        pass
    kel=skivify_v2(kvWd,text=text,active=active,size_hint_y=size_hint_y,pos_hint=pos_hint,cwidth=cwidth,bcolor=bcolor,k=k,halign=halign,valign=valign,enable_events=enable_events,on_event=on_event,**kwargs)
    return kel

@skwidget
def ActionToggleButton(text='actionbutton',enable_events=True,on_event="on_release",k=None,**kwargs):
    from kivy.uix.actionbar import ActionToggleButton  as kvWd
    kel=skivify_v2(kvWd,text=text,k=k,**kwargs,enable_events=enable_events,on_event=on_event)
    if k==None and text:
        kel.id=text
    return kel

@skwidget
def ActionPrevious(title='title',k=None,app_icon='skdata/logo/simplekivy-icon-32.png',with_previous=True,enable_events=True,bind_title=False,on_event='on_release',**kwargs):
    from kivy.uix.actionbar import ActionPrevious as kvWd
    kel=skivify_v2(kvWd,title=title,with_previous=with_previous,app_icon=app_icon,k=k,enable_events=enable_events,on_event=on_event,**kwargs)
    # if bind_title:
    #     Clock.schedule_once(lambda dt: utils.get_kvApp().bind(title=lambda ins,v:setattr(kel,'title',v)))
    if k==None and title:
        kel.id=title
    return kel

# @skwidget
# def ActionOverflow(overflow_image='atlas://data/images/defaulttheme/overflow',**kwargs):
#     from kivy.uix.actionbar import ActionOverflow as kvWd
#     return skivify_v2(kvWd,overflow_image=overflow_image,**kwargs)

@skwidget
def ActionSeparator(**kwargs):
    from kivy.uix.actionbar import ActionSeparator as kvWd
    return skivify_v2(kvWd,**kwargs)

@skwidget
def ActionCheck(**kwargs):
    from kivy.uix.actionbar import ActionCheck as kvWd
    return skivify_v2(kvWd,**kwargs)

@skwidget
def ToActionItem(widget,**kwargs):
    from kivy.uix.actionbar import ActionItem
    class kvWd (widget.__class__,ActionItem):
        pass
    return skivify_v2(kvWd,**kwargs)

@skwidget
def ActionBar(widgets=[],use_separator=False,k=None,**kwargs):
    from kivy.uix.actionbar import ActionBar,ActionView
    bar=skivify_v2(ActionBar,k=k,**kwargs)
    view=ActionView(use_separator=use_separator,)

    for w in widgets:
        view.add_widget(w)

    # view.add_widget(action_previous)
    # if overflow:
    #     from kivy.uix.actionbar import ActionOverflow
    #     over=ActionOverflow(overflow_image=overflow_image)
    #     view.add_widget(over)

        
    #     for ow in overflow:
    #         view.add_widget(ow)
        
    bar.add_widget(view)
    return bar


@skwidget
def ToggleButton(text='button',group=None,allow_no_selection=True,enable_events=True,k=None,on_event='on_release', **kwargs):
    kel=kvw.ToggleButtonB(text=text,allow_no_selection=allow_no_selection,group=group,**kwargs)
    
    if k==None and text:
        k=text

    kel.id=k


    kel.enable_events=enable_events
    kel.on_event=on_event

    return kel
TButton=ToggleButton


@skwidget
def Image(
    source='',
    k=None,
    async_load=True,
    anim_delay=0.25,  # 1/(4 FPS)
    fit_mode='contain', # scale-down, fill, contain, cover
    maximum_width=None,
    copypaste = False,
    is_svg=False,
    **kwargs
    ):
    if source and not is_svg:
        is_svg=os.path.splitext(source)[-1].lower()=='.svg'
    if async_load:
        # from kivy.uix.image import AsyncImage as kvImage
        kvImage=mkvw.AsyncImage
    else:
        # from kivy.uix.image import Image as kvImage
        kvImage=mkvw.Image

    if copypaste:
        _kvImage=kvImage
        Logger.info('SimpleKivy: importing "pyperclip", "requests", "io.BytesIO", "kivy.core.image.Image", "kivy.core.clipboard.Clipboard", "PIL.ImageGrab" and "PIL.Image" to support image clipboard manipulation.')
        from kivy.core.clipboard import Clipboard
        from kivy.core.image import Image as CoreImage
        from PIL import ImageGrab
        from PIL import Image as pImage
        from io import BytesIO
        import requests
        import pyperclipimg as pci

        class kvImage(_kvImage):
            def __init__(self,**kwargs):
                self._url_pattern=re.compile(
                        r'^(?:(?:https?|ftp)://)',  # http://, https://, ftp://
                        # r'(?:\S+(?::\S*)?@)?'  # user:pass authentication
                        # r'(?:'
                        # r'(?:(?:[a-z0-9\u00a1-\uffff]-?)*[a-z0-9\u00a1-\uffff])+'  # domain name
                        # r'(?:\.(?:[a-z0-9\u00a1-\uffff]-?)*[a-z0-9\u00a1-\uffff])*'  # subdomains
                        # r'(?:\.(?:[a-z\u00a1-\uffff]{2,}))'  # TLD
                        # r')'
                        # r'(?::\d{2,5})?'  # port number
                        # r'(?:/\S*)?'  # path
                        # r'(?:\?\S*)?'  # query string
                        # r'(?:#\S*)?$',  # fragment
                        re.IGNORECASE
                    )
                super(kvImage, self).__init__(**kwargs)

            def paste(self):
                # kcp=Clipboard.paste()
                # print(kcp)
                # if kcp:
                    # if os.path.exists(kcp)

                pilimg = ImageGrab.grabclipboard()
                # print(pilimg)
                if isinstance(pilimg,list) and pilimg:
                    pilimg=pImage.open(pilimg[0])

                else:
                    url=Clipboard.paste()
                    if self._url_pattern.match(url):
                        # self.source=kcp
                        try:
                            pilimg=pImage.open(requests.get(url, stream=True).raw)
                        except:
                            Logger.exception(f'Failed to get image from url: {url}')

                if pilimg:
                    data = BytesIO()
                    pilimg.save(data, format='png')
                    data.seek(0) # yes you actually need this
                    self.texture=CoreImage(BytesIO(data.read()), ext='png').texture
                return pilimg
                
            def copy(self):
                if self.texture:
                    size=self.texture.size
                    frame=self.texture.pixels
                    # print(fr)
                    nimg=pImage.frombytes(mode='RGBA', size=size,data=frame)
                    # nimg=nimg.convert('RGBA')
                    pci.copy(nimg)
                    # print("copied from here")
                    return nimg
            def paste_from_path(self,path):
                cimg=CoreImage(path)
                if cimg:
                    self.texture=cimg.texture
            def save_to_path(self,fp,format=None,**params):
                if self.texture and fp:
                    size=self.texture.size
                    frame=self.texture.pixels
                    nimg=pImage.frombytes(mode='RGBA', size=size,data=frame)
                    try:
                        nimg.save(fp,format=format,**params)
                    except OSError:
                        nimg=nimg.convert('RGB')
                        nimg.save(fp,format=format,**params)
            def save_to_path_dialog(self,filetypes=( ("PNG","*.png"), ("JPG","*.jpg"), ), defaultextension=".png", **kw):
                self.save_to_path(get_kvApp().asksaveasfile(filetypes=filetypes,defaultextension=defaultextension, **kw))

    if is_svg:
        _kvImage=kvImage
        from cairosvg import svg2png
        class kvImage(_kvImage):
            # __events__ = ('on_error')
            _ignore_load_errors=True
            def __init__(self,**kwargs):
                self.register_event_type('on_error')
                # self.bind(source=self._on_src)
                self.fbind('source', self._load_source)
                self.fbind('size',self._load_source)
                super(kvImage, self).__init__(**kwargs)
                
                

                # self.texture=self.frombytes(svg2png())
            def _load_source(self,ins,src):
                # self._found_source=ins.source
                # if not source:
                #     self.texture=None
                #     return
                try:
                    self.from_bytes(
                            svg2png(
                                url=ins.source,
                                output_width=ins.width,
                                output_height=ins.height,
                                parent_width=ins.width,
                                parent_height=ins.height,
                            )
                        )
                except Exception as error:
                    self.dispatch('on_error', error)
                    sup=super()
                    if hasattr(sup,'_load_source'):
                        sup._load_source(ins,ins.source)
            def on_error(self,error):
                pass
                





    # if fit_mode!='full':
    kel=kvImage(
        source=source,
        anim_delay=anim_delay,
        fit_mode=fit_mode,
        **kwargs)
#     else:
#         kvw.Builder.load_string("""
# <-FullImage>:
#     canvas:
#         Color:
#             rgb: (1, 1, 1)
#         Rectangle:
#             texture: self.texture
#             size: self.width + 20, self.height + 20
#             pos: self.x - 10, self.y - 10
# """)
#         class FullImage(kvImage):
#             pass
#         kel=FullImage(
#             source=source,
#             anim_delay=anim_delay,
#             fit_mode='contain',
#             **kwargs)

    kel.id=k

    #if maximum_width:
    kel.maximum_width=maximum_width

    return kel


@skwidget
def FlatButton(text='button',
    lcolor=[.5,.5,.5,1],
    bcolor_normal=[.345, .345, .345, 0],
    bcolor_down=[.2, .64, .8, 1],
    markup=True,
    focus_behavior=False,hover_highlight=False,enable_events=True,on_event='on_release',k=None,touchripple=False,
    **kwargs):
    if touchripple:
        # class _(kvw.TouchRippleButtonBehavior,kvw.BgLineState,kvw.BoxLayout):
        #     # bcolor_down=kvw.ColorProperty([.2, .64, .8, 1])
        #     # ripple_color=kvw.AliasProperty(bcolor_down.getter,bcolor_down.setter)
        #     # ripple_color=bcolor_down
        #     def __init__(self, **kwargs):
        #         # self.ripple_color= kwargs.get('ripple_color', self.bcolor_down)
        #         self.bind(bcolor_down=self.setter('ripple_color'))
        #         super(_, self).__init__(**kwargs)
        #         # self.bind(bcolor_down=self.setter('ripple_color'))
        #     def on_touch_down(self, touch):
        #         collide_point = self.collide_point(touch.x, touch.y)
        #         if collide_point:
        #             touch.grab(self)
        #             self.ripple_show(touch)
        #             return True
        #         return False

        #     def on_touch_up(self, touch):
        #         if touch.grab_current is self:
        #             touch.ungrab(self)
        #             self.ripple_fade()
        #             # self.dispatch('on_release')
        #             return True
        #         return False
        # kvWd=_
        kvWd=kvw.FlatButtonTouch
    else:
        kvWd=kvw.FlatButtonA


    if focus_behavior:
        class _(kvb.FocusBehavior,kvWd):
            pass
        kvWd=_
        # if 'background_color' in kwargs:
        #     kwargs['bcolor']=kwargs.pop('background_color')

    if hover_highlight:
        class _(kvb.HoverHighlightBehavior,kvWd):
            pass
        kvWd=_

    is_actionitem=kwargs.pop('is_actionitem',False)
    if is_actionitem:
        from kivy.uix.actionbar import ActionItem
        class kvWd(kvWd,ActionItem):
            pass

    if k==None and text:
        k=text
    kel=skivify_v2(kvWd,
        k=k,
        text=text,
        markup=markup,
        lcolor=lcolor,
        bcolor_down=bcolor_down,
        bcolor_normal=bcolor_normal,
        enable_events=enable_events,
        on_event=on_event,
        **kwargs)
    return kel
FlatB=FlatButton

def ClearButton(*args,hover_highlight=True,lcolor='',markup=True,**kwargs):
    return FlatButton(*args,hover_highlight=hover_highlight,lcolor=lcolor,markup=markup,**kwargs)
ClearB=ClearButton


@skwidget
def FlatRoundButton(text='button',
    lcolor=[.5,.5,.5,1],
    bcolor_normal=[.345, .345, .345, 0],
    bcolor_down=[.2, .64, .8, 1],
    markup=True,
    focus_behavior=False,hover_highlight=False,enable_events=True,on_event='on_release',k=None,
    **kwargs):

    kvWd=kvw.FlatRoundButtonA
        # kwargs['bcolor_normal']=bcolor_normal

    if focus_behavior:
        class _(kvb.FocusBehavior,kvWd):
            pass
        kvWd=_
        # if 'background_color' in kwargs:
        #     kwargs['bcolor']=kwargs.pop('background_color')

    if hover_highlight:
        class _(kvb.HoverHighlightBehavior,kvWd):
            pass
        kvWd=_
        kwargs['to_parent']=True

    is_actionitem=kwargs.pop('is_actionitem',False)
    if is_actionitem:
        from kivy.uix.actionbar import ActionItem
        class kvWd(kvWd,ActionItem):
            pass

    if k==None and text:
        k=text
    kel=skivify_v2(kvWd,
        text=text,
        k=k,
        markup=markup,
        lcolor=lcolor,
        bcolor_down=bcolor_down,
        bcolor_normal=bcolor_normal,
        enable_events=enable_events,
        on_event=on_event,
        **kwargs)
    return kel
FlatRoundB=FlatRoundButton


def ClearRoundButton(*args,hover_highlight=True,lcolor='gray',markup=True,**kwargs):
    return FlatRoundButton(*args,hover_highlight=hover_highlight,lcolor=lcolor,markup=markup,**kwargs)

ClearRoundB=ClearRoundButton

@skwidget
def ButtonBoxit(*widgets,focus_behavior=False,lwidth=1,hover_highlight=False,enable_events=True,k=None,on_event='on_release', **kwargs):
    
    kvWd=kvw.BBoxLayout

    if focus_behavior:
        class nkvWd(kvb.FocusBehavior,kvWd):
            pass
        kvWd=nkvWd
    if hover_highlight:
        class nkvWd(kvb.HoverHighlightBehavior,kvWd):
            pass
        kvWd=nkvWd

    kel=skivify_v2(kvWd,k=k,lwidth=lwidth,enable_events=enable_events,on_event=on_event,**kwargs)

    # print(kwargs)
    # kel=kvWd(**kwargs)

    # kel.id=k

    # kel.enable_events=enable_events
    # kel.on_event=on_event

    for w in widgets:
        kel.add_widget(w)

    return kel


@skwidget
def ToggleButtonBoxit(*widgets,focus_behavior=False,hover_highlight=False,enable_events=True,k=None,on_event='on_release',base_cls=None, **kwargs):
    
    # kvWd=kvw.TBBoxLayout
    if base_cls==None:
        kvWd=kvw.TBBoxLayout
    else:
        class kvWd(kvb.ToggleButtonBehavior2,base_cls):
            pass

    if focus_behavior:
        class _(kvb.FocusBehavior,kvWd):
            pass
        kvWd=_
    if hover_highlight:
        class _(kvb.HoverHighlightBehavior,kvWd):
            pass
        kvWd=_


    kel=kvWd(**kwargs)

    kel.id=k

    kel.enable_events=enable_events
    kel.on_event=on_event
    kel.post='ToggleGeneral'

    for w in widgets:
        kel.add_widget(w)


    return kel

@skwidget
def FlatButtonAngle(text='button',angle=90,enable_events=True,k=None,on_event='on_release', **kwargs):
    # kwargs=_preproces(**kwargs)
    # global _future_elements, _future_bind

    
    kvWd=kvw.FlatButtonAngle

    # kvWd=kvw.add_parent(kvWd,behavior)

    kel=kvWd(text=text,angle=angle,**kwargs)
    
    if k==None and text:
        k=text

    kel.id=k

    kel.enable_events=enable_events
    kel.on_event=on_event

    # if enable_events:
    #     _future_bind.append(kel)

    # _future_elements.append(kel)
    return kel

@skwidget
def FlatToggleButtonAngle(text='button',angle=90,enable_events=True,k=None,on_event='on_release', **kwargs):

    kvWd=kvw.FlatTButtonAngle

    kel=kvWd(text=text,angle=angle,**kwargs)
    
    if k==None and text:
        k=text

    kel.id=k

    kel.enable_events=enable_events
    kel.on_event=on_event
    kel.post='ToggleGeneral'
    return kel
FlatTButtonAngle=FlatToggleButtonAngle
@skwidget
def FlatToggleButton(text='button',enable_events=False,k=None,on_event='on_state_down', **kwargs):

    kvWd=kvw.FlatTButton

    kel=kvWd(text=text,**kwargs)
    
    if k==None and text:
        k=text

    kel.id=k

    kel.enable_events=enable_events
    kel.on_event=on_event
    kel.post='ToggleGeneral'
    return kel
FlatTB=FlatTButton=FlatToggleButton

@skwidget
def Spinner(# default value shown
    text='choice0',
    # available values
    values=('choice0', 'choice1'),
    enable_events=False,k=None,on_event='text', **kwargs
    ):
    # kwargs=_preproces(**kwargs)
    # global _future_elements, _future_bind

    

    kel=utils.Spinner(text=text,values=values,**kwargs)
    
    kel.id=k

    kel.enable_events=enable_events
    kel.on_event=on_event

    # if enable_events:
    #     _future_bind.append(kel)

    # _future_elements.append(kel)
    return kel
def Spinner2(text='choice0',
    values=('choice0', 'choice1'),
    enable_events=False,k=None,on_event='text',
    background_normal='atlas://skdata/sktheme/spinner',
    option_cls=None,
    **kwargs
    ):
    # from .modkvWidgets import SpinnerOptionB
    SpinnerOptionB=mkvw.SpinnerOptionB
    SpinnerOptionB.markup=kwargs.get('markup',False)
    SpinnerOptionB.halign=kwargs.get('halign','center')
    SpinnerOptionB.valign=kwargs.get('valign','middle')
    # SpinnerOptionB.halign=kwargs.get('halign','center')
    # SpinnerOptionB.bind()

    kel=Spinner(
        text=text,values=values,
        background_normal=background_normal,
        color=[0,0,0,1],
        option_cls=SpinnerOptionB,
        enable_events=enable_events,k=k,on_event=on_event, **kwargs
    )
    return kel

@skwidget
def ListBox(
    data=[], # [{"text": f"label{x}", "halign": "center", "valign": "middle", "lcolor": ""} for x in range(10)],
    enable_events=False,k=None,on_event='on_selection',
    keyboard_scroll=True,
    effect_cls='scroll', # damped, scroll, opacity, no
    **kwargs
    ):
    if isinstance(effect_cls,str):
        # if effect_cls!='damped':
        # if effect_cls in ('scroll','no'):
        #     from kivy.effects.scroll import ScrollEffect as effect_cls
        # else:
        match effect_cls:
            case 'no':
                from kivy.effects.scroll import ScrollEffect as effect_cls
            case 'opacity':
                from kivy.effects.scroll import OpacityScrollEffect as effect_cls
            case 'damped':
                from kivy.effects.scroll import DampedScrollEffect as effect_cls
            case 'scroll':
                from kivy.effects.scroll import ScrollEffect as effect_cls

    kel=skivify_v2(kvw.RV,k=k,enable_events=enable_events,effect_cls=effect_cls,on_event=on_event,data=data,keyboard_scroll=keyboard_scroll,
        # selected_color=selected_color,
        **kwargs)
    # Clock.schedule_once(lambda dt:kel.setter('data')(kel,data))
    
    return kel




@skwidget
def Playlist(
    data=[], #[{'title':f'title{i}','artist':f'artist{i}'} for i in range(25)],
    k=None,
    enable_events=True,
    on_event='on_selection',
    keyboard_scroll=True,
    **kwargs
    ):
    # kwargs=_preproces(**kwargs)
    # global _future_elements, _future_bind

    


    kel=skivify_v2(kvw.Playlist,k=k,data=data,keyboard_scroll=keyboard_scroll,enable_events=enable_events,on_event=on_event,**kwargs)
    
    # kel.id=k

    kel.post='Playlist'

    # setattr()

    # print(kel.ids.wartist)

    # if enable_events:
    #     _future_bind.append(kel)

    # _future_elements.append(kel)
    return kel

@skwidget
def Artistlist(
    data=[],# [{'title':f'title{i}','subtitle':f'subtitle{i}','cover':'atlas://data/images/defaulttheme/player-play-overlay'} for i in range(20)],
    k=None,
    enable_events=True,
    on_event='on_selection',
    keyboard_scroll=True,
    **kwargs
    ):
    kel=kvw.Artistlist(data=data,keyboard_scroll=keyboard_scroll,**kwargs)
    
    kel.id=k
    kel.post='Artistlist'
    kel.enable_events=enable_events
    kel.on_event=on_event
    return kel

RecycleStackList=Artistlist
RStack=RecycleStackList
RStackit=Artistlist

@skwidget
def Albumlist(
    data=[], # [{'track':f'{i}','title':f'title{i}','artist':f'artist','plays':'0'} for i in range(1,3)]
    k=None,
    enable_events=True,
    on_event='on_selection',
    keyboard_scroll=True,
    **kwargs
    ):
    # kwargs=_preproces(**kwargs)
    # global _future_elements, _future_bind

    


    kel=skivify_v2(kvw.Albumlist,data=data,keyboard_scroll=keyboard_scroll,enable_events=enable_events,on_event=on_event,k=k,**kwargs)
    
    # kel.id=k

    kel.post='Albumlist'

    # setattr()

    # print(kel.ids.wartist)

    # kel.enable_events=enable_events
    # kel.on_event=on_event

    # if enable_events:
    #     _future_bind.append(kel)

    # _future_elements.append(kel)
    return kel


@skwidget
def Input(text='',enable_events=False,multiline=False,k=None,on_event='on_text_validate', **kwargs):
    # kwargs=_preproces(**kwargs)
    # global _future_elements, _future_bind

    W=kvw.kvInput

    # if 'on_insert_text' in on_event:
    class W(kvw.kvInput):
        last_added=''
        # delayed_text=kvw.StringProperty('')
        delay_interval = NumericProperty(.3)  # delay after typing stops
        def __init__(self, **kwargs):
            
            self._typing_timer = None
            self.register_event_type('on_insert_text')
            self.register_event_type('on_delayed_text')
            super(W, self).__init__(**kwargs)

            

        def on_insert_text(self):
            pass
        def insert_text(self, substring, from_undo=False):
            s = substring
            self.last_added=s
            self.dispatch('on_insert_text')
            return super().insert_text(s, from_undo=from_undo)

        def on_text(self, instance, value):
            # Cancel any existing timer
            if self._typing_timer is not None:
                self._typing_timer.cancel()
            
            # Schedule a new timer
            self._typing_timer = Clock.schedule_once(
                self._trigger_delayed_event, 
                self.delay_interval
            )
        
        def _trigger_delayed_event(self, dt):
            # This gets called only when the user stops typing
            # self.delayed_text = self.text
            # You could also dispatch a custom event here if preferred
            self.dispatch('on_delayed_text',self.text)
        
        def on_delayed_text(self, *args):
            """Event handler for when delayed text is ready"""
            pass

    kel=skivify_v2(W,text=text,k=k,multiline=multiline,enable_events=enable_events,on_event=on_event,**kwargs)
    return kel

@skwidget
def InputDark(text='',enable_events=False,multiline=False,k=None,on_event='on_text_validate', **kwargs):
    W=kvw.kvInput

    # if 'on_insert_text' in on_event:
    class W(kvw.kvInput):
        foreground_color=kvw.ListProperty([1,1,1,1])
        background_active=kvw.StringProperty('atlas://skdata/sktheme/textinput_active')
        background_normal=kvw.StringProperty('atlas://skdata/sktheme/textinput')
        background_disabled_normal=kvw.StringProperty('atlas://skdata/sktheme/textinput_disabled')
        disabled_foreground_color=kvw.ListProperty([1,1,1,.5])
        last_added=''
        def __init__(self, **kwargs):
            self.register_event_type('on_insert_text')
            super(W, self).__init__(**kwargs)
        def on_insert_text(self):
            pass
        def insert_text(self, substring, from_undo=False):
            s = substring
            self.last_added=s
            self.dispatch('on_insert_text')
            return super().insert_text(s, from_undo=from_undo)

    kel=skivify_v2(W,text=text,k=k,enable_events=enable_events,on_event=on_event,multiline=multiline,**kwargs)
    
    return kel

@skwidget
def Multiline(text='',enable_events=False,multiline=False,k=None,on_event='on_text_validate', **kwargs):
    locs=locals()
    # print(locs)
    kw=locs.pop('kwargs')
    locs.update(kw)
    locs['multiline']=True

    return Input(**locs)

@skwidget
def CodeInput(text='',lexer='CythonLexer',style_name='default',rehighlight=None,k=None,enable_events=False,on_event='on_text_validate', **kwargs):
    # from .modkvWidgets import CodeInput as kvCodeInput
    kvCodeInput=mkvw.CodeInput
    import pygments.lexers as lexers

    # from pygments.styles import get_all_styles,get_style_by_name
    # styles = list(get_all_styles())
    # print(styles)

    # __all__ = ['CustomTexLexer']
    # from pygments.lexer import inherit
    # from pygments.token import Keyword
    # from pygments.lexers.markup import TexLexer

    

    # class CustomTexLexer(TexLexer):
    #     aliases = ['xtex', 'xlatex']

    #     tokens = {
    #         'root': [
    #             (r'\*[a-zA-Z \.]+\*', Keyword),  # Match *text* and classify it as Keyword
    #             inherit,  # Inherit the rest of the rules from TexLexer
    #         ],
    #     }


    if on_event=='on_insert_text':
        class W(kvCodeInput):
            last_added=''
            def __init__(self, **kwargs):
                self.register_event_type('on_insert_text')
                super(W, self).__init__(**kwargs)
            def on_insert_text(self):
                pass
            def insert_text(self, substring, from_undo=False):
                s = substring#.upper()
                self.last_added=s
                self.dispatch('on_insert_text')
                return super().insert_text(s, from_undo=from_undo)
    else:
        W=kvCodeInput
    if rehighlight:
        class nW(W):
            def rehighlight(self,ntext):
                return rehighlight(self,ntext)
    else:
        nW=W

    lexer=getattr(lexers,lexer)
    # lexer=CustomTexLexer
    kel=nW(text=text,lexer=lexer(),style_name=style_name,**kwargs)
    # kel=W(text=text,lexer=CombinedLexer(),style='dracula',**kwargs)
    # kel=W(text=text,lexer=TexLexer(),style='dracula',**kwargs)
    kel.id=k

    kel.enable_events=enable_events
    kel.on_event=on_event

    return kel

# CodeInput()

def populate_tree_view(self, parent, node):
    if parent is None:
        tree_node = self.add_node(kvTreeViewLabel(text=node['node_id'],
                                                     is_open=True))
    else:
        tree_node = self.add_node(kvTreeViewLabel(text=node['node_id'],
                                                     is_open=True), parent)

    if 'children' in node:
        for child_node in node['children']:
            populate_tree_view(self,tree_node, child_node)

@skwidget
def TreeView(tree = {
    'node_id': '1',
        'children': [{'node_id': '1.1',
                      'children': [{'node_id': '1.1.1',
                                    'children': [{'node_id': '1.1.1.1',
                                                  'children': []}]},
                                   {'node_id': '1.1.2',
                                    # 'children': []
                                    },
                                   {'node_id': '1.1.3',
                                    'children': []}]},
                      {'node_id': '1.2',
                       'children': []}]
    },

                       indent_level=16,

                       k=None,enable_events=False,on_event='selected_node', **kwargs

                       ):
    # W=kvTreeView
    class W(kvTreeView):
        tree=kvw.ObjectProperty({})
        def __init__(self,**kwargs):
            super(W, self).__init__(**kwargs)
            self.bind(tree=self._update_tree)
            Clock.schedule_once(lambda dr:self._update_tree(self,self.tree))
        def _update_tree(self,ins,val):
            # self.clear_widgets()
            for ni in self.iterate_all_nodes():
                self.remove_node(ni)
            # populate_tree_view(self,None,val)
            self.populate_tree_view(None,val)
        def populate_tree_view(self, parent, node):
            if parent is None:
                tree_node = self.add_node(kvTreeViewLabel(text=node['node_id'],
                                                             is_open=True))
            else:
                tree_node = self.add_node(kvTreeViewLabel(text=node['node_id'],
                                                             is_open=True), parent)

            if 'children' in node:
                for child_node in node['children']:
                    self.populate_tree_view(tree_node, child_node)
    
    kel = skivify_v2(W,tree=tree,root_options=dict(text='Tree One'),
                      hide_root=False,
                      indent_level=indent_level,**kwargs)

    # populate_tree_view(kel, None, tree)
    kel.id=k

    kel.enable_events=enable_events
    kel.on_event=on_event
    return kel

# TEST_WIDGET(TreeView(on_event='selected_node',enable_events=True))


@skwidget
def ScrollView(
    content,
    scroll_y=True,scroll_x=False,
    k=None,
    bar_color=[.4, .4, .4, .9],
    bar_inactive_color=[.4, .4, .4, .6],
    scroll_type=['bars', 'content'],
    effect_cls='scroll', # damped, scroll, opacity, no
    bar_width=8,**kwargs):

    # H=0
    # W=0
    # for child in content.children:
    #     H+=child.height
    #     W+=child.width
    # content.height=H
    # content.width=W

    # content.minimum_height=H
    # content.minimum_width=W



    from kivy.uix.scrollview import ScrollView as kvWd

    if isinstance(effect_cls,str):
        # if effect_cls!='damped':
        # if effect_cls in ('scroll','no'):
        #     from kivy.effects.scroll import ScrollEffect as effect_cls
        # else:
        match effect_cls:
            case 'no':
                from kivy.effects.scroll import ScrollEffect as effect_cls
            case 'opacity':
                from kivy.effects.scroll import OpacityScrollEffect as effect_cls
            case 'damped':
                from kivy.effects.scroll import DampedScrollEffect as effect_cls
            case 'scroll':
                from kivy.effects.scroll import ScrollEffect as effect_cls






    if scroll_y:
        content.size_hint_y=None
        if hasattr(content,'minimum_height'):
            content.bind(minimum_height=content.setter('height'))
        # content.bind(width=content.setter('minimum_width'))
    if scroll_x:
        content.size_hint_x=None
        if hasattr(content,'minimum_width'):
            content.bind(minimum_width=content.setter('width'))
        # content.bind(height=content.setter('minimum_height'))
    
    # sh1=None if scroll_y else 1
    # sh0=None if scroll_x else 1



    kel=kvWd(
        scroll_type=scroll_type,
        # size_hint=(sh0, sh1), 
        # size=(content.width, content.height),
        do_scroll_x= scroll_x,
        do_scroll_y= scroll_y,
        bar_color=utils.resolve_color(bar_color),
        bar_inactive_color=utils.resolve_color(bar_inactive_color),
        bar_width=8,
        effect_cls=effect_cls,
        **kwargs
        )
    kel.id=k
    kel.add_widget(content)
    return kel

@skwidget
def Popup(content,title='Popup window',enable_events=False,on_event='on_dismiss',do_dot_subevent=False,k=None,**kwargs):
    from kivy.uix.popup import Popup as kvWd


    kel=skivify_v2(kvWd,
        title=title,
        content=content,
        k=k,
        enable_events=enable_events,
        on_event=on_event,

        **kwargs)

    # kel=kvWd(
        # title=title,
        # content=content,
    #     **kwargs
    #     )
    # kel.id=k
    # print(kel.size_hint)
    # print(kel.size)
    return kel

# @skwidget
# def ModalView(content,title='Popup window',enable_events=False,on_event='on_dismiss',do_dot_subevent=False,k=None,**kwargs):
#     from kivy.uix.popup import Popup as kvWd


#     kel=skivify_v2(kvWd,
#         title=title,
#         content=content,
#         k=k,
#         enable_events=enable_events,
#         on_event=on_event,

#         **kwargs)
#     return kel


@skwidget
def ScreenManager(
            screens={},
            # {
            #     'screen1':Button('First screen, go to >'),
            #     'screen2':Button('Second screen, go to <'),
            # },
            transition='slide', #no slide card swap fade wipe fallout risein
            k=None,
            **kwargs
        ):
    '''
    transition: no slide card swap fade wipe fallout risein,
    '''
    # kwargs=_preproces(**kwargs)
    # global _future_elements, _future_bind
    
    
    
    # kel=kvw.ScreenManager(transition=get_transition(transition)() if isinstance(transition,str) else transition,**kwargs)
    kvWd=kvw.customScreenManager
    kel=kvWd(transition=get_transition(transition)() if isinstance(transition,str) else transition,**kwargs)
    setattr(kel,'history',BrowserHistory())
    def on_current(instance,value):
        instance.history.visit(value)
        # print(instance.id)
        # instance.history.print()
        # instance.history[value]=-1
        # for h in instance.history:
        #     instance.history[h]+=1
        # if len(instance.history)>10:
        #     instance.history=instance.history[:10]
        # if not instance.from_goback:
        #     i=-1
        #     found=False
        #     for v in instance.history:
        #         i+=1
        #         if v==value:
        #             instance.history.insert(0,instance.history.pop(i))
        #             found=True
        #             break
        #     if not found:
        #         instance.history.insert(0,value)
        #     # _={}
        #     # for v in instance.history:
        #     #     _[v]=0
        #     # instance.history=list(_.keys())
        # # print(instance.history)
    kel.bind(current=on_current)

    kel.id=k
    
    for n,v in screens.items():
        if isinstance(v,kvw.Screen):
            s=v
            s.name=n
        else:
            s=kvw.Screen(name=n)
            if v:
                s.add_widget(v)
            

        kel.add_widget(s)

    
    
    # _future_elements.append(kel)
    return kel
Screens=ScreenManager

@skwidget
def Screen(widgets=[],name='',k=None,**kwargs):
    if k==None:
        k=name
    # if name=='' and k:
    #     name=k
    kvWd=kvw.Screen

    kel=skivify_v2(kvWd,k=k,name=name,**kwargs)
    if utils.is_iterable(widgets):
        for w in widgets:
            kel.add_widget(w)
    else:
        kel.add_widget(widgets)
    return kel


@skwidget
def CalcSheet(
    rows=5,
    cols=5,
    data=None,
    k=None,
    connect_input_to=None,
    connect_dpos_to=None,
    connect_cell_value_to=None,
    # enable_events=False,
    # on_event='text',
    **kwargs
    ):
    kwargs=_preproces(**kwargs)
    global _future_elements, _future_bind,_post_elements

    
    
    kel=kvw.CalcGridLayout(cols=cols+1,rows=rows+1,spacing=(3,3),padding=[4,4,4,4])
    kel.compile_ecode()
    
    # rel=kvw.RelativeLayout(**kwargs)
    rel=skivify_v2(kvw.RelativeLayout,k=k,**kwargs)
    rel.add_widget(kel)
    kel.rel=rel
    rel.sheet=kel
    icell=mkvw.ICell(pos=(0,0),multiline=False,size=(80,30),size_hint=(None,None))
    kel.icell=icell
    rel.icell=icell
    
    rel.add_widget(
        icell
        )
    kel.hide_widget(kel.icell)
    # rel.id=k

    rel.connect_cell_value_to=connect_cell_value_to
    rel.connect_input_to=connect_input_to
    rel.connect_dpos_to=connect_dpos_to

    for i in range(rows+1):
        for j in range(cols+1):
            if i==0:
                if j>0:
                    hlabel=kvw._Label(text=abc[j-1] )
                    if j!=cols:

                        box=kvw.BoxLayout(minimum_size=(1,1),
                            # size=(80,30),size_hint=(None,None)
                            size=(80,30),size_hint=(None,None)
                            )
                    else:
                        box=kvw.BoxLayout(minimum_size=(1,1),
                            # size=(80,30),size_hint=(None,None)
                            size=(80,30),size_hint=(1,None)
                            )
                    stbtn=kvw.SplitterV2(
                        size_hint=(None,None),size=(4,30),
                        bcolor_normal=(0.5,0.5,0.5,0.5))

                    box.add_widget(hlabel)
                    box.add_widget(stbtn)

                    kel.add_widget(box)
                    kel.headers[abc[j-1]]=box

                else:
                    kel.add_widget(kvw._Label(text='',size=(30,30),size_hint=(None,None)))
            elif i>0 and j==0:
                kel.add_widget(kvw._Label(text=str(i),size=(30,30),size_hint=(None,1)))
            else:
                kv_cell=kvw.Cell
                if j!=cols:
                    ii=kv_cell(text='',font_size=15,
                        # multiline=False,
                        size=(80,30),size_hint=(None,1),
                        halign='center',
                        valign='center',
                        lcolor=[1,1,1,1],
                        pos=(1,1),padding=[2,2,2,2],
                        lwidth=1,
                        bcolor_normal=(0,0,0,0)
                        # shorten=True,
                        )
                else:
                    ii=kv_cell(text='',font_size=15,
                        # multiline=False,
                        size=(80,30),size_hint=(1,1),
                        halign='center',
                        valign='center',
                        bcolor_normal=(0,0,0,0),
                        lcolor=[1,1,1,1],
                        pos=(1,1),padding=[2,2,2,2],
                        lwidth=1,
                        )
                    # print(ii.children)
                ii.dpos=f"{abc[j-1]}{i}"

                kel.add_widget(ii)
                kel.children_dict[ii.dpos]=ii
                try:
                    kel.columns[abc[j-1]].append(ii)
                except:
                    kel.columns[abc[j-1]]=[ii]

    kel.force_color_selected()
    lastc=abc[cols]

    for h,w in kel.headers.items():
        w.column=kel.columns[h]
        def _follow_width(instance,value):
            # print(instance.parent.width)
            for ii in instance.column:
                # ii.size[0]=value[0]
                ii.width=value
        if h!=lastc:
            w.bind(width=_follow_width)

    _future_elements.append(rel)
    _post_elements['CalcSheet'].append(rel)
    rel.post='CalcSheet'
    return rel

@skwidget
def ProgressBar(value=0,max=1,k=None,**kwargs):
    # from kvWidgets import ProgressBarB as kvWd
    kvWd=kvw.ProgressBarB
    kel=skivify_v2(kvWd,value=value,max=max,k=k,**kwargs)

    return kel

@skwidget
def ProgressBar2(value=0,max=1,k=None,
    fcolor= [1, 0, .2, 1],
    bcolor= [.298, .298, .298, 1]
    ,**kwargs):
    # from kvWidgets import ProgressBarB as kvWd
    kvWd=kvw.ProgressBarC
    kel=skivify_v2(kvWd,value=value,max=max,k=k,**kwargs)

    return kel

@skwidget
def Slider(value=0,min=0,max=1,k=None,enable_events=False,on_event='value',**kwargs):
    from kivy.uix.slider import Slider as kvWd
    # kel=kvWd(value=value,min=min,max=max,**kwargs)
    kel=skivify_v2(kvWd,value=value,min=min,max=max,k=k,enable_events=enable_events,on_event=on_event,**kwargs)
    # kel.id=k
    return kel



@skwidget
def ScrollbarMirror(k=None,enable_events=False,on_event=None,**kwargs):
    kvWd=kvw.ScrollbarMirror
    kel=skivify_v2(kvWd,k=k,enable_events=False,on_event=None,**kwargs)
    return kel

@skwidget
def BarTouch(value=0,max=1,scroll_delta=0,k=None,enable_events=False,on_event="value",**kwargs):
    class kvWd(kvw.RelativeLayout):
        scroll_delta=NumericProperty(0)
        bcolor = kvw.ListProperty([50/255, 164/255, 206/255, 1])  # background color
        lcolor = kvw.ListProperty([.5, .5, .5, 1])  # line color
        lwidth = kvw.NumericProperty(2)          # line width
        _scroll_btns={'scrollup','scrolldown'}
        max = kvw.NumericProperty(1)
        
        _value = 0# kvw.NumericProperty(0)
        
        def _get_val(self):
            # print(self._value)
            return self._value
        def _set_val(self,val):
            if val<0:
                self._value=0
            elif val>self.max:
                self._value=self.max
            else:
                self._value=val
            # print(val,self.max)
            return True
        value=kvw.AliasProperty(_get_val,_set_val,cache=True)

        _nvalue=0
        def _get_nval(self):
            # print(self._value)
            return self._value/self.max
        # def _set_nval(self,val):
        #     if val<0:
        #         self._nvalue=0
        #     elif val>1:
        #         self._nvalue=1
        #     else:
        #         self._nvalue=val
        #     self.value=self._nvalue*self.max
        #     return True
        value_normalized=kvw.AliasProperty(_get_nval,cache=True)
        
        _clicked=False
        

        
        def __init__(self, **kwargs):
            super(kvWd, self).__init__(**kwargs)
            # self.value=kwargs.get('value',self.value)
            self.value=kwargs.get('value',self.value)

            # print(self.value,self.max,kwargs)
            # self.bind(value=print)
            # self.register_event_type('on_clickup')
            # print(kwargs['max'])
            # print(self.max)
            Clock.schedule_once(self._init)
        def _init(self,dt):
            with self.canvas.before:
                self.bg_color = kvw.Color(rgba= resolve_color( self.bcolor ))
                self.bg_rect = kvw.Rectangle(pos=self.pos, size=(self.width*self.value/self.max,self.height))
            with self.canvas.after:
                self.line_color = kvw.Color(rgba=resolve_color( self.lcolor))
                self.line = kvw.Line(width=self.lwidth, rectangle=(
                    self.x, self.y, self.width, self.height
                ))
            
            # Bind properties to update visuals
            self.bind(
                max=self._update_canvas,
                value=self._update_canvas,
                pos=self._update_canvas,
                size=self._update_canvas,
                
                
                bcolor=self._update_bcolor,
                lcolor=self._update_lcolor,
                lwidth=self._update_lwidth
            )
            self._update_canvas(self,self.value)
        # def on_value(self,ins,val):
        #     if val<0:
        #         ins.value=0
        #     elif val>ins.max:
        #         ins.value=ins.max
        #     else:
        #         ins.value=value
        
        def _update_canvas(self, *args):
            # print()
            """Update the canvas elements when position or size changes"""
            x,y=self.to_local(*self.pos)
            # x,y=self.pos
            self.bg_rect.pos = (x,y)
            # self.bg_rect.pos = self.pos
            self.bg_rect.size = (self.width*self.value/self.max,self.height)

            

            self.line.rectangle = (self.x, self.y, self.width, self.height)
            # print(self.line.rectangle,self.bg_rect.pos,self.bg_rect.size)
            # self.text_size = self.size
        
        def _update_bcolor(self, instance, value):
            """Update background color"""
            # print("""Update background color""",value)
            self.bg_color.rgba = resolve_color( value)
            
        # def on_clickup(self):
        #     pass

        def on_touch_down(self,touch):
            self._clicked=False
            if not self.collide_point(touch.x, touch.y):
                return False
            # print("here",touch.x,touch.y,touch.spos,self.to_local(*touch.pos))
            # print(dir(touch))
            if self.scroll_delta and touch.button in self._scroll_btns:
                match touch.button:
                    case "scrolldown":
                        self.value+=self.scroll_delta
                    case "scrollup":
                        self.value-=self.scroll_delta
                return False
            elif touch.button=='left':
                # rx,ry=self.to_widget(*touch.pos)
                rx,ry=self.to_local(*touch.pos)
                self._clicked_val=self.max*rx/self.width
                self._clicked=tuple(touch.pos)
                self.value=self._clicked_val
            # print(f"{self._clicked = }")
        def on_touch_move(self,touch):
            
            if self._clicked:
                # print('move')
                # # x,y=self.to_widget(*touch.pos)
                # rx,ry=self.to_widget(*touch.pos)
                rx,ry=self.to_local(*touch.pos)
                self.value=self.max*rx/self.width
                # self.value=self.max*rx/self.width
        def on_touch_up(self,touch):
            if self._clicked:
                # rx,ry=self.to_widget(*touch.pos)
                rx,ry=self.to_local(*touch.pos)
                # print(rx,ry,self.to_widget(*touch.pos))
                # x,y=self.to_widget(*touch.pos)
                self.value=self.max*rx/self.width
                # self.value=self._clicked_val+d*self.max
        
        def _update_lcolor(self, instance, value):
            """Update line color"""
            self.line_color.rgba = resolve_color( value)
        
        def _update_lwidth(self, instance, value):
            """Update line width"""
            self.line.width = value
    kel=skivify_v2(kvWd,value=value,max=max,scroll_delta=scroll_delta,k=k,enable_events=enable_events,on_event=on_event,**kwargs)
    return kel
BarTouchH=BarTouch
@skwidget
def BarTouchV(value=0,max=1,scroll_delta=0,k=None,enable_events=False,on_event="value",**kwargs):
    class kvWd(kvw.RelativeLayout):
        scroll_delta=NumericProperty(0)
        bcolor = kvw.ListProperty([50/255, 164/255, 206/255, 1])  # background color
        lcolor = kvw.ListProperty([.5, .5, .5, 1])  # line color
        lwidth = kvw.NumericProperty(2)          # line width
        _scroll_btns={'scrollup','scrolldown'}
        max = kvw.NumericProperty(1)
        
        _value = 0
        
        def _get_val(self):
            return self._value
        def _set_val(self,val):
            if val<0:
                self._value=0
            elif val>self.max:
                self._value=self.max
            else:
                self._value=val
            return True
        value=kvw.AliasProperty(_get_val,_set_val,cache=True)

        _nvalue=0
        def _get_nval(self):
            return self._value/self.max
        value_normalized=kvw.AliasProperty(_get_nval,cache=True)
        _clicked=False
        
        def __init__(self, **kwargs):
            super(kvWd, self).__init__(**kwargs)
            self.value=kwargs.get('value',self.value)
            Clock.schedule_once(self._init)
        def _init(self,dt):
            with self.canvas.before:
                self.bg_color = kvw.Color(rgba= resolve_color( self.bcolor ))
                self.bg_rect = kvw.Rectangle(pos=self.pos, size=(self.width,self.height*self.value/self.max))
            with self.canvas.after:
                self.line_color = kvw.Color(rgba=resolve_color( self.lcolor))
                self.line = kvw.Line(width=self.lwidth, rectangle=(
                    self.x, self.y, self.width, self.height
                ))
            self.bind(
                max=self._update_canvas,
                value=self._update_canvas,
                pos=self._update_canvas,
                size=self._update_canvas,
                bcolor=self._update_bcolor,
                lcolor=self._update_lcolor,
                lwidth=self._update_lwidth
            )
            self._update_canvas(self,self.value)
        
        def _update_canvas(self, *args):
            x,y=self.to_local(*self.pos)
            self.bg_rect.pos = (x,y)
            self.bg_rect.size = (self.width,self.height*self.value/self.max)
            self.line.rectangle = (self.x, self.y, self.width, self.height)
        
        def _update_bcolor(self, instance, value):
            self.bg_color.rgba = resolve_color( value)

        def on_touch_down(self,touch):
            self._clicked=False
            if not self.collide_point(touch.x, touch.y):
                return False
            if self.scroll_delta and touch.button in self._scroll_btns:
                match touch.button:
                    case "scrolldown":
                        self.value+=self.scroll_delta
                    case "scrollup":
                        self.value-=self.scroll_delta
                return False
            elif touch.button=='left':
                # rx,ry=self.to_widget(*touch.pos)
                rx,ry=self.to_local(*touch.pos)
                self._clicked_val=self.max*ry/self.height
                self._clicked=tuple(touch.pos)
                self.value=self._clicked_val
        def on_touch_move(self,touch):
            if self._clicked:
                # rx,ry=self.to_widget(*touch.pos)
                rx,ry=self.to_local(*touch.pos)
                self.value=self.max*ry/self.height
        def on_touch_up(self,touch):
            if self._clicked:
                # rx,ry=self.to_widget(*touch.pos)
                rx,ry=self.to_local(*touch.pos)
                self.value=self.max*ry/self.height
        
        def _update_lcolor(self, instance, value):
            """Update line color"""
            self.line_color.rgba = resolve_color( value)
        
        def _update_lwidth(self, instance, value):
            """Update line width"""
            self.line.width = value
    kel=skivify_v2(kvWd,value=value,max=max,scroll_delta=scroll_delta,k=k,enable_events=enable_events,on_event=on_event,**kwargs)
    return kel


@skwidget
def ProgressBarTouch(value=0,max=1,k=None,enable_events=True,on_event='on_clickup',**kwargs):
    kvWd=kvw.ProgressBarC
    # from kivy.uix.progressbar import ProgressBar as kvWd
    # from kvWidgets import ProgressBarB as kvWd
    class kvWd2(kvWd):
        spos=kvw.ListProperty([0,0])
        def __init__(self,**kwargs):
            
            super(kvWd2, self).__init__(**kwargs)
            self.register_event_type('on_clickup')

        def on_touch_up(self,touch):
            if touch.is_mouse_scrolling:
                return False
            if not self.collide_point(touch.x, touch.y):
                return False

            xx,yy=self.to_widget(*touch.pos,relative=True)
            # print(touch.spos,touch.pos,(xx,yy))
            sx,sy=xx/self.width,yy/self.height
            # print(sx,sy)

            self.spos=sx,sy
            self.value=sx*self.max
            self.dispatch('on_clickup',touch.spos)
        def on_clickup(self,spos):
            pass

    kel=skivify_v2(kvWd2,value=value,max=max,enable_events=enable_events,on_event=on_event,k=k,**kwargs)
    
    # kel.id=k

    # kel.enable_events=True
    # kel.on_event='on_clickup'

    return kel

@skwidget
def SliderTouch(value=0,min=0,max=1,k=None,enable_events=True,on_event='on_clickup',**kwargs):
    from kivy.uix.slider import Slider as kvWd
    class kvWd2(kvWd):
        spos=kvw.ListProperty([0,0])
        def __init__(self,**kwargs):
            self.register_event_type('on_clickup')
            super(kvWd2, self).__init__(**kwargs)

        def on_touch_up(self,touch):
            if touch.is_mouse_scrolling:
                return False
            if not self.collide_point(touch.x, touch.y):
                return False

            xx,yy=self.to_widget(*touch.pos,relative=True)
            sx,sy=xx/self.width,yy/self.height

            self.spos=sx,sy
            self.dispatch('on_clickup',touch.spos)
        def on_clickup(self,spos):
            pass

    kel=skivify_v2(kvWd2,min=min,value=value,max=max,k=k,enable_events=enable_events,on_event=on_event,**kwargs)
    
    # kel.id=k

    # kel.enable_events=True
    # kel.on_event='on_clickup'

    return kel


def Void(k=NOTKEY,**kwargs):
    kel=Boxit(k=k,size=kwargs.pop('size',(0,0)),size_hint=kwargs.pop('size_hint',(None,None)))
    kel.is_void=True
    return kel
def PAW():
    kel=Boxit(size=(0,0),size_hint=(None,None),k=NOTKEY)
    Clock.schedule_once(lambda dt:get_kvApp().paw())
    return kel
def Fill():
    return Boxit(size=(0,0),size_hint=(1,1),k=NOTKEY)
def SeparatorV(bcolor='gray',size=(2,1),size_hint=(None,1),**kwargs):
    return Boxit(bcolor=bcolor,size=size,size_hint=size_hint,**kwargs)
def SeparatorH(bcolor='gray',size=(1,2),size_hint=(1,None),**kwargs):
    return Boxit(bcolor=bcolor,size=size,size_hint=size_hint,**kwargs)


def QuickOk(msg='message',title='title'):
    def evman(a,e):
        if e=='Ok':
            a.close()
    app=MyApp(
        title=title,
        event_manager=evman,
        layout=[
            [Label(msg,font_size=50,markup=True,font_name='roboto b')],
            [Button('Ok',font_size=30,background_color='lightblue',size='y40')]
        ]
    )
    app.run()

def QuickOkCancel(msg='message',title='title'):
    def evman(a,e):
        if e=='__Start__':
            setattr(a,'ans',False)
        elif e=='Ok':
            setattr(a,'ans',True)
            a.close()
        elif e=='Cancel':
            a.close()
    app=MyApp(
        title=title,
        event_manager=evman,
        layout=[
            [Label(msg,font_size=50,markup=True,font_name='roboto b')],
            [BoxitH(Button('Ok',font_size=30,background_color='lightblue'),Button('Cancel',font_size=30,background_color='r'),size='y60')]
        ]
    )
    app.run()
    return app.ans



if __name__ == '__main__':
    pass
    # lyt=[[
    # CalcSheet()
    # ]]
    # MyApp(layout=lyt).run()
    # pass

# d=CaseInsensitiveDict(a=1,b=2)
# print(d)
# d.clear()
# print(d)

    
    # @say_hello
    # @say_bye
    # @skwidget
    # def Button_(text='button',enable_events=True,k=None,on_event='on_release', **kwargs):
    #     # kwargs=_preproces(**kwargs)
    #     # global _future_elements, _future_bind
    #     kel=kvw.kvButton(text=text,**kwargs)
        
    #     if k==None and text:
    #         k=text

    #     kel.id=k

    #     kel.enable_events=enable_events
    #     kel.on_event=on_event

    #     # if enable_events:
    #     #     _future_bind.append(kel)

    #     # _future_elements.append(kel)
    #     return kel

    # k=Button(text='hell')
    # print(vars(k))
    # print(_future_elements,_future_bind)
    # {'id': 'hell', 'enable_events': True, 'on_event': 'on_release'}
    # [<kivy.uix.button.Button object at 0x000001E310BB5010>] [<kivy.uix.button.Button object at 0x000001E310BB5010>]

    # k=Button_(text='hell',size=size.x80,background_color='r')
    # print(vars(k))
    # print(_future_elements,_future_bind)