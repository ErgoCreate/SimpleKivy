
import sys
import os
os.environ['KIVY_GL_BACKEND'] = 'sdl2'
KIVY_DOC= 'KIVY_DOC' in os.environ
import pathlib
# package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# print(package_path)
# os.environ['PYTHONPATH'] = package_path + os.pathsep + os.environ.get('PYTHONPATH', '')
# # print(__name__)
NOTKEY=-67191210201

from .utils import infinite, CaseInsensitiveDict,_Void,is_number,find_letter_number_pairs, auto_config, re_search,get_kvApp
from .utils import import_from, get_transition, _event_manager, abc, mdi,get_last_focused
from .utils import Colors,Fonts,hex2rgb, resolve_color,pos_hints,app_schedule_get_call,app_get,_preprocess
from .utils import BrowserHistory
from .utils import markup_str
from .utils import setattrs,get_id,fun_debug
from . import utils
import pickle
import types
from . import _docs
from kivy.uix.widget import Widget
from inspect import signature




addcolors='r g b w y gray brown orange'.split()
iadd=-1
liadd=len(addcolors)
def dt_setattr(self,name,value):
    '''
    ## Returns a lambda function which only argument is dt, and calls setattr with the given arguments "name" and "value".

    "return lambda dt:setattr(self,name,value)"
    '''
    return lambda dt:setattr(self,name,value)
def __mul__Widget(self,val):
    # print(self.size,val.size,self.size_hint,val.size_hint)
    size_hint_y=self.size_hint_y
    height=self.height
    # if size_hint_y==val.size_hint_y==None:
    #     height=max((height,val.height))
    # elif not val.size_hint_y:
    #     size_hint_y=val.size_hint_y
    #     height=val.height
    # global iadd,addcolors,liadd
    # setattr(kel,'_isbox',kel.orientation)
    # if hasattr(self,'do_layout') and getattr(self,'orientation',None)=='horizontal':
    if getattr(self,'_isbox',None)=='horizontal':
        self.add_widget(val)
        return self
    # iadd+=1
    pos_hint=getattr(self,'pos_hint',{})
    # self.pos_hint={}
    # print(pos_hint)
    if size_hint_y!=None:
        return BoxitH( self, val,k=NOTKEY,pos_hint=pos_hint,
            # lcolor='g'
            )
    else:
        return BoxitH( self, val,
            size_hint_y=size_hint_y,height=height,
            # size=f"y{height}",
            k=NOTKEY,pos_hint=pos_hint,
            # lcolor='g'
            )

def __div__Widget(self,val):
    # print(self.size,val.size,self.size_hint,val.size_hint)
    size_hint_x=self.size_hint_x
    width=self.width
    # if size_hint_x==val.size_hint_x==None:
    #     width=max((width,val.width))
    # elif not val.size_hint_x:
    #     size_hint_x=val.size_hint_x
    #     width=val.width

    # global iadd,addcolors,liadd
    # if hasattr(self,'do_layout') and getattr(self,'orientation',None)=='vertical':
    if getattr(self,'_isbox',None)=='vertical':
        self.add_widget(val)
        return self
    # iadd+=1
    pos_hint=getattr(self,'pos_hint',{})
    # self.pos_hint={}
    # print(pos_hint)
    if size_hint_x!=None:
        return BoxitV( self, val,k=NOTKEY,pos_hint=pos_hint,
            # lcolor='g'
            )
    else:
        return BoxitV( self, val,size_hint_x=size_hint_x,width=width,k=NOTKEY,pos_hint=pos_hint,
            # lcolor='g'
            )
ids={}
get=ids.get
def id_set(self,val):
    global ids
    self._id=val
    if not val in (None,NOTKEY):
        ids[val]=self
def id_get(self):
    return self._id

# setattr(Widget,'__mul__' , types.MethodType(__mul__Widget, Widget))
setattr(Widget,'__mul__' , __mul__Widget)
setattr(Widget,'__truediv__' , __div__Widget)
setattr(Widget,'id',property(id_get,id_set))
setattr(Widget,'dt_setattr',dt_setattr)

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
    else:
        raise ImportError(f"cannot import name '{name}' from '{__name__}' ({__file__})")

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
                if getattr(kel,'id',NOTKEY)!=NOTKEY:
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
                    if getattr(kel,'id',NOTKEY)!=NOTKEY:
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

def _create_callback(self,el,on_event=None):
    # Define the callback function
    if on_event==None:
        on_event=getattr(el,'on_event')
    if getattr(el,'do_dot_subevent',False):
        event_name=str(el.id)+'.'+str(on_event)
    else:
        event_name=str(el.id)

    # print(el.do_dot_subevent,f"{on_event = }")

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
                    # binds={}
                    for i,on_event in enumerate(el.on_event):
                        # print(on_event)
                        # subevent=str(el.id)+'.'+str(on_event)
                        # call=
                        el.bind(**{on_event: _create_callback(self,el,on_event)})

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
            # el.bind(**{el.on_event:self._callback})
            el.bind(**{el.on_event:_create_callback(self,el,el.on_event)})

            # if getattr(el,'do_dot_subevent',None):
            #     # el.bind(**{el.on_event:lambda *args: self._callback_w_subev(*args,subevent=el.on_event) })
            #     el.bind(**{el.on_event:lambda *args: self._callback_w_subev(*args,subevent=el.on_event) })
            # else:
            #     el.bind(**{el.on_event:self._callback})
    _future_bind=[]

def locked_screen(func):
    def wrapper(*args,**kwargs):
        self=get_kvApp()
        
        # self.lock()
        def do(*args,**kwargs):
            Clock.unschedule(self.dt_lock)
            Clock.unschedule(self.dt_unlock)

            Clock.schedule_once(self.dt_unlock)
            Clock.schedule_once(self.dt_lock)
            ans=func(*args,**kwargs)
            Clock.schedule_once(self.dt_unlock)
            return ans
        # Clock.schedule_once(lambda dt: do(),.1)
        future=self.poolt.submit(do,*args,**kwargs)
        
        # Clock.schedule_once(lambda dt:self.lock())
        # future=self.poolt.submit(func,*args,**kwargs)
        # future.add_done_callback(lambda f:Clock.schedule_once(lambda dt:self.unlock()))
        return future
    # def args_preprocessor(*args, **kwargs):
    #     kel = f(*args, **kwargs)
    #     return kel
    f=func
    wrap=wrapper
    if KIVY_DOC:
        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        wrap.__module__ = f.__module__
        wrap.__qualname__ = f.__qualname__
        wrap.__annotations__ = getattr(f, '__annotations__', {})
        wrap.__signature__ = signature(f)
        wrap.__widget_ctor__=f.__name__

    return wrapper

def locked_screen_at_pool(pool):
    def _locked_screen_at_pool(func):
        # def wrapper(*args,**kwargs):
        #     self=get_kvApp()
        #     Clock.schedule_once(lambda dt:self.lock())
        #     # self.lock()
        #     # def do(*args,**kwargs):
        #     #     self.sleep_in_thread(1)
        #     #     ans=func(*args,**kwargs)
        #     #     self.unlock()
        #     #     return ans
        #     # Clock.schedule_once(lambda dt: do(),.1)
            
        #     future=pool.submit(func,*args,**kwargs)
        #     # future=self.poolt.submit(do,*args,**kwargs)
        #     future.add_done_callback(lambda f:Clock.schedule_once(lambda dt:self.unlock()))
        #     # result=func(*args,**kwargs)
        #     # return future.result()
        #     return future
        # # def args_preprocessor(*args, **kwargs):
        # #     kel = f(*args, **kwargs)
        # #     return kel

        def wrapper(*args,**kwargs):
            self=get_kvApp()
            Clock.unschedule(self.dt_lock)
            Clock.unschedule(self.dt_unlock)

            Clock.schedule_once(self.dt_unlock)
            Clock.schedule_once(self.dt_lock)
            
            future=pool.submit(func,*args,**kwargs)
            future.add_done_callback(lambda f:Clock.schedule_once(self.dt_unlock))
            return future

        f=func
        wrap=wrapper
        if KIVY_DOC:
            wrap.__doc__ = f.__doc__
            wrap.__name__ = f.__name__
            wrap.__module__ = f.__module__
            wrap.__qualname__ = f.__qualname__
            wrap.__annotations__ = getattr(f, '__annotations__', {})
            wrap.__signature__ = signature(f)
            wrap.__widget_ctor__=f.__name__

        return wrapper
    return _locked_screen_at_pool

_saved_to_config={}
def skwidget(f):
    def args_preprocessor(*args, **kwargs):
        sz=kwargs.get('size',None)
        max_w0=kwargs.pop('maximum_width',None)
        # size_behavior=kwargs.pop('size_behavior','none')

        do_dot_subevent=kwargs.pop('do_dot_subevent',None)
        # print('499',do_dot_subevent)
        bind=kwargs.pop('bind',None)

        save_to_config=kwargs.pop('save_to_config',None)


        kwargs=_preprocess(**kwargs)
        global _future_elements, _future_bind,_saved_to_config
        kel = f(*args, **kwargs)

        if save_to_config:

            if hasattr(kel,'id'):
                if isinstance(save_to_config,str):
                    stc=set((save_to_config,))
                elif isinstance(save_to_config,(tuple,list,set)):
                    stc=set(save_to_config)
                else:
                    raise ValueError(f'Invalid "save_to_config" type: "{type(save_to_config)}". Valid types are str, list, tupple, set')

                _saved_to_config[kel.id]=stc
                # print(f"{save_to_config =}")

            else:
                raise ValueError(f'A widget id ("k" argument) needs to be specified to use "save_to_config" functionality')

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
        return kel

    wrap=args_preprocessor
    # Copy all the important metadata

    if KIVY_DOC:
        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        wrap.__module__ = f.__module__
        wrap.__qualname__ = f.__qualname__
        wrap.__annotations__ = getattr(f, '__annotations__', {})
        
        # Try to copy signature if available (Python 3.3+)
        wrap.__signature__ = signature(f)
        
        wrap.__widget_ctor__=f.__name__

    return wrap

def _widget_ctor(f):
    def args_preprocessor(*args, **kwargs):
        kel = f(*args, **kwargs)
        return kel
    wrap=args_preprocessor
    if KIVY_DOC:
        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        wrap.__module__ = f.__module__
        wrap.__qualname__ = f.__qualname__
        wrap.__annotations__ = getattr(f, '__annotations__', {})
        wrap.__signature__ = signature(f)
        wrap.__widget_ctor__=f.__name__
    # if not wrap.__doc__:
    #     wrap.__doc__=_docs.tbd_widfun
    return wrap

def MiniApp(f):
    def miniapp_func_wrapper(*args,**kwargs):
        global ids,_future_elements,_post_elements,_future_bind, MyApp,_MiniApp
        oids=ids.copy()
        o_future_elements=_future_elements.copy()
        o_future_bind=_future_bind.copy()
        o_post_elements=_post_elements.copy()

        ids={}
        _future_elements=[]
        _future_bind=[]
        _post_elements={ k:[] for k in o_post_elements }
        
        oMyApp=MyApp
        MyApp=_MiniApp
        ################################
        ans=f(*args,**kwargs)
        ################################
        MyApp=oMyApp
        _future_elements=o_future_elements
        _future_bind=o_future_bind
        _post_elements=o_post_elements
        ids=oids
        
        _future_elements.append(ans)

        return ans
    wrap=miniapp_func_wrapper
    if KIVY_DOC:
        wrap.__doc__ = f.__doc__
        wrap.__name__ = f.__name__
        wrap.__module__ = f.__module__
        wrap.__qualname__ = f.__qualname__
        wrap.__annotations__ = getattr(f, '__annotations__', {})
        wrap.__signature__ = signature(f)
        wrap.__widget_ctor__=f.__name__
        if not wrap.__doc__:
            wrap.__doc__=_docs.tbd_widfun
    return wrap

# def MiniAppModal(f):
#     def miniapp_func_wrapper(*args,**kwargs):
#         global ids,_future_elements,_post_elements,_future_bind, MyApp,_MiniApp
#         oids=ids.copy()
#         o_future_elements=_future_elements.copy()
#         o_future_bind=_future_bind.copy()
#         o_post_elements=_post_elements.copy()

#         ids={}
#         _future_elements=[]
#         _future_bind=[]
#         _post_elements={ k:[] for k in o_post_elements }
        
#         oMyApp=MyApp
#         MyApp=_MiniApp
#         ################################
#         ans=f(*args,**kwargs)
#         ################################
#         MyApp=oMyApp
#         _future_elements=o_future_elements
#         _future_bind=o_future_bind
#         _post_elements=o_post_elements
#         ids=oids
        
#         _future_elements.append(ans)

#         return ans
#     wrap=miniapp_func_wrapper
#     if KIVY_DOC:
#         wrap.__doc__ = f.__doc__
#         wrap.__name__ = f.__name__
#         wrap.__module__ = f.__module__
#         wrap.__qualname__ = f.__qualname__
#         wrap.__annotations__ = getattr(f, '__annotations__', {})
#         wrap.__signature__ = signature(f)
#         wrap.__widget_ctor__=f.__name__
#         if not wrap.__doc__:
#             wrap.__doc__=_docs.tbd_widfun
#     return wrap

def skwidget_only_preprocess(f):
    def wrap(*args, **kwargs):
        kwargs=_preprocess(**kwargs)
        kel = f(*args, **kwargs)
        return kel
    return wrap

def _process_config_set(self):
    global _saved_to_config
    # print(f"{_saved_to_config =}")
    self._config.update(_saved_to_config)
    # print(f"{self._config =}")


def process_added_widgets():
    self=App.get_running_app()
    _future_process_elements(self)
    _post_process_elements(self)
    _future_process_binds(self)
    _process_config_set(self)
paw=process_added_widgets

def _ensure_bttn_not_draggable(children):

    for c in children:
        if hasattr(c,'on_release'):
            setattr(c,'draggable',False)
        if hasattr(c,'children'):
            if c.children:
                _ensure_bttn_not_draggable(c.children)

# class action:
#     def __init__(self,target,*args,**kwargs):
#         self.target=target
#         self.args=args
#         self.kwargs=kwargs
#     def __call__(self,*_,**__):
#         if hasattr(self.target,'__call__'):
#             return self.target()(*self.args,**self.kwargs)    
#         return self.target(*self.args,**self.kwargs)

class action:
    def __init__(self,target,*args,**kwargs):
        self.target=target
        self.args=args
        self.kwargs=kwargs
    def __call__(self,*_,**__):
        return self.target(*self.args,**self.kwargs)

_post_actions_global=[]

if 'win' == platform.lower():
    import win32gui
    import win32api
    import win32con

# print(platform)

class _MiniApp:
    def __init__(
        self,
        layout=[[]],
        title='MiniApp',
        event_manager=None,
        custom_titlebar=False,
        alpha=1,
        keep_on_top=False,
        layout_args={},
        icon='skdata/logo/simplekivy-icon-32.png',
        layout_class=None,
        do_auto_config=True,
        k=None,
        **kwargs
        ):
        if event_manager==None:
            event_manager=_event_manager
        self.Clock=Clock
        self.mdi=mdi
        
        self.kvWindow=utils.Window

        self.post_actions=[]
        
        size=kwargs.pop('size',None)
        location=kwargs.pop('location',None)
        

        self.title=title
        self.poolt=ThreadPoolExecutor(thread_name_prefix='MiniApp')
        self.queue={}

        self._nk=0
        

        global ids
        self.ids=utils.IDS()
        self._ids={}
        if not layout_class:
            rows=len(layout)
            # self._layout=kvw.GridLayoutB(rows=rows,**_preprocess(**layout_args))
            kvWd = kvw.GridLayoutB
            if 'HAS_GRADIENT' in os.environ:
                from SimpleKivy.kvGradient import GradientGrid
                kvWd=GradientGrid
                layout_args['gradient']=layout_args.get('gradient',['linear-gradient',dict(colors=['',''],size=[2,2])])
            self._layout=skivify(kvWd,k=k,rows=rows,**layout_args)
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
                    self._layout.add_widget(kivy_el)

                lenrow = len(row)
                addnvoids = 0
                if lenrow < max_cols:
                    addnvoids = max_cols - lenrow
                for v in range(addnvoids):
                    self._layout.add_widget(
                            Fill(),
                        )
        else:
            if 'HAS_GRADIENT' in os.environ:
                if not hasattr(layout_class,'gradient'):
                    from SimpleKivy.kvGradient import GradientBehavior
                    layout_args['over_class']=GradientBehavior
                    layout_args['gradient']=layout_args.get('gradient',['linear-gradient',dict(colors=['',''],size=[2,2])])
            try:
                self._layout=layout_class(k=k,**layout_args)
            except:
                self._layout=skivify(layout_class,k=k,**layout_args)
            for kivy_el in layout:
                self._layout.add_widget(kivy_el)
        self._triggers={}
        self.event_manager=event_manager
        self.thread_event=self.submit_thread_event
        self.thread_event_at=self.submit_thread_event_at
        self.hidden={}

        _future_process_elements(self)
        _post_process_elements(self)
        _future_process_binds(self)

        self.paw=self.process_added_widgets
        self.Clock.schedule_once(lambda dt: setattr(self,'alpha',alpha))

    def __getattr__(self,name):
        return getattr(App.get_running_app(),name)

    def thread_pool_new(self,name,max_workers=None):
        self.queue[name]=ThreadPoolExecutor(max_workers=max_workers,thread_name_prefix=name)
    def queue_new(self,name):
        self.queue[name]=ThreadPoolExecutor(max_workers=1,thread_name_prefix=name)

    def destroy_widget(self,k,default=None):
        el=self.ids.get(k,default)
        if el:
            del self.ids[k]
            del self._ids[el]
            if el.parent:
                el.parent.remove_widget(el)
    
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
    
    def process_widget(self,wid):
        _future_process_elements(self)
        _post_process_elements(self)
        _future_process_binds(self)
        return wid
    def process_added_widgets(self):
        _future_process_elements(self)
        _post_process_elements(self)
        _future_process_binds(self)

    def dt_call(self,k,prop=None,val=None,_kw_prepro=False,ignore_errors=False,**kwargs):
        return lambda dt: self.__call__(k=k,prop=prop,val=val,_kw_prepro=_kw_prepro,ignore_errors=ignore_errors,**kwargs)

    def schedule_call_once(self,k,prop=None,val=None,timeout=0,_kw_prepro=False,ignore_errors=False,**kwargs):
        Clock.schedule_once(lambda dt:self.__call__(k=k,prop=prop,val=val,_kw_prepro=_kw_prepro,ignore_errors=ignore_errors,**kwargs),timeout=timeout)
    def schedule_call_interval(self,k,prop=None,val=None,timeout=0,_kw_prepro=False,ignore_errors=False,**kwargs):
        Clock.schedule_interval(lambda dt:self.__call__(k=k,prop=prop,val=val,_kw_prepro=_kw_prepro,ignore_errors=ignore_errors,**kwargs),timeout=timeout)

    def __call__(self,k,prop=None,val=None,timeout=0,_kw_prepro=False,ignore_errors=False,**kwargs):
        try:

            if isinstance(k,str):
                widget=self.ids[k]
            else:
                widget=k

            if isinstance(prop,str):
                if not _kw_prepro:
                    kw=_preprocess(**{prop:val})
                    trigger=Clock.create_trigger(lambda *args:setattr(widget,prop,kw[prop]),timeout)
                    trigger()
                else:
                    trigger=Clock.create_trigger(lambda *args:setattr(widget,prop,val),timeout)
                    trigger()
            else:
                kwargs=_preprocess(**kwargs)
                for p,v in kwargs.items():
                    self.__call__(k,p,v,_kw_prepro=True)
        except Exception as e:
            if ignore_errors:
                pass
            else:
                raise e
    def trigger_event(self,event,*args,**kwargs):
        trigger=self._triggers.get(  event,Clock.create_trigger(  lambda *x: self.event_manager(self,event,*args,**kwargs)  )  )
        trigger()
    def schedule_event_once(self,event,*args,timeout=0,**kwargs):
        ans=Clock.schedule_once(lambda dt: self.event_manager(self,event,*args,**kwargs),timeout=timeout)
    def schedule_func_once(self,func,*args,timeout=0,**kwargs):
        ans=Clock.schedule_once(lambda dt: func(*args,**kwargs),timeout=timeout)

    def submit_thread_event_at(self,thread_name,event,*args,**kwargs):
        if not thread_name in self.queue:
            self.queue_new(thread_name)
        future=self.queue[thread_name].submit(self.event_manager,self,event,*args,**kwargs)
        return future
    def submit_thread_event(self,event,*args,**kwargs):
        future=self.poolt.submit(self.event_manager,self,event,*args,**kwargs)
        return future
    def __getitem__(self, key):
        return self.ids[key]
    def schedule_get_call(self,key,method,*args,timeout=0,**kwargs):
        if isinstance(key,str):
            wid=self.ids[key]
        else:
            wid=key
        Clock.schedule_once(lambda dt:getattr(wid,method)(*args,**kwargs),timeout=timeout)
    def schedule_getattr_call(self,*args,**kwargs):
        '''
        Same as schedule_get_call.
        '''
        self.schedule_get_call(*args,**kwargs)
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
        ev=self._ids[args[0]]
        self.event_manager(self,ev)

    def call_event(self,event,*args,**kwargs):
        return self.event_manager(self,event,*args,**kwargs)
        
    def build(self):
        for a in self.post_actions:
            a()
        Clock.schedule_once(lambda dt: self.event_manager(self,'__Start__') )
        self._layout.app=self.app
        self._layout.main_app=self.main_app
        return self._layout
    def run(self):
        return self.build()
    def reuse(self,*args,**kwargs):
        self.trigger_event('__Reuse__',*args,**kwargs)

    @property
    def app(self):
        return self

    @property
    def main_app(self):
        return utils.get_kvApp()

    @property
    def id(self):
        return self._layout.id

    def hide(self,*key_list,shrink=True):
        for k in key_list:
            if isinstance(k,str):
                wid=self.__getitem__(k)
            else:
                wid=k
            s=getattr(wid,'size',(100,100)).copy()
            sh=getattr(wid,'size_hint',(1,1)).copy()
            o=getattr(wid,'opacity',1)
            d=getattr(wid,'disabled',False)

            if k not in self.hidden:
                self.hidden[k]=(s,sh,o,d)
            if shrink:
                setattr(wid,'size',(1,1))
                setattr(wid,'size_hint',(None,None))
            setattr(wid,'opacity',0)
            setattr(wid,'disabled',True)
    def unhide(self,*key_list,enforce={}):
        for k in key_list:
            if isinstance(k,str):
                wid=self.__getitem__(k)
            else:
                wid=k
            try:
                s,sh,o,d=self.hidden.get(k)
            except:
                s=getattr(wid,'size',(100,100))
                sh=getattr(wid,'size_hint',(1,1))
                o=getattr(wid,'opacity',1)
                d=getattr(wid,'disabled',False)
            
            setattr(wid,'size',s)
            setattr(wid,'size_hint',sh)
            setattr(wid,'opacity',o)
            setattr(wid,'disabled',d)

            for prop,v in enforce.items():
                setattr(wid,prop,v)


class MyApp(App):
    '''
    A complete overhaul of how the `App` object is created. For simplicity, in this page `app` represents an instance of `MyApp` inside code blocks.

    ## Init Arguments
    `title (str)`: App title. Defaults to `"MyApp"`.

    `layout (list)`: List (or matrix-like list) of widgets that represent your program. When `layout_class = None`, a *matrix-like* list must be used (see {url_Grid}). Otherwise, the `list` argument must conform to the `layout_class` constructor. Defaults to `[[]]`.
    
    `event_manager`: `function` or `EventManager` instance. Must accept at least two positional arguments: `app` and `event`.
    
    ```py
    def evman(app, event):
        pass
    app=sk.MyApp(
        ...
        event_manager = evman
        ...
    )
    ```

    `custom_titlebar (bool)`: Whether the `app` will use the first widget in the `layout` as titlebar. Defaults to `False`
    
    `alpha (float)`: Transparency of the window. Only works on Windows at the moment. Defaults to `1` (opaque).

    `keep_on_top (bool)`: Wheter your application's window is shown on top of all other windows. Defaults to `False`.
    
    `icon (str)`: Image of your application's icon. Defaults to "skdata/logo/simplekivy-icon-32.png".

    `ico (str)`: Path to an `*.ico` file. Needed for file dialogs (`askdirectory`, `askopenfile`, etc.) in Windows platforms only.
    
    `layout_class: (None, Widget)`
    > Layuout widget that will be used to represent the layout.
    > - `None`: The layout base will be `SimpleKivy.kvWidgets.GridLayoutB`, in which case the `layout` argument must be `list (matrix-like)`. See {url_Grid}.
    > - `Widget`: The layout constructor will be this value. The `layout` argument must conform to the requirements of `layout_class`.
    > Default is `None`.

    `layout_args (dict)`: Dictionary of arguments used to initilize the `layout_class` (e.g, *bcolor*, *padding*, *spacing*, *lcolor*, etc.). Defaults to `{}`.
    
    `do_auto_config: (bool)`
    > Whether to automatically configure `kivy` by calling `SimpleKivy.utils.auto_config` when `WIDGET` is initialized. Visit {url_utils.auto_config} for more information.
    > - `True`: Calls `auto_config` with default arguments: `(size=(800,600),exit_on_escape=False,multisamples=2,desktop=True,resizable=True,multitouch_emulation=False,window_state='visible')`.
    > -  `False`: Doesn't call `auto_config`. You need to configure `kivy` yourself, or make a call to `auto_config` before initializing `MyApp`.
    > Default is `True`.



    ## Attributes
    
    `window_is_maximized (BooleanProperty)`: Whether the window is maximized. Can be set to maximize (`= True`) or restore (`= False`) the window.
    
    `top_widget (AliasProperty)`: Current widget being shown on top of all other widgets. Intended for menus, tooltips, etc.
    
    `subtop_widget (AliasProperty)`: Current widget being shown on top of all other widgets, besides `top_widget`. Intended for submenus.
    
    `hwnd (int)`: OS window id (`hwnd`) of the application.

    `keep_on_top (bool)`: Wheter your application's window is shown on top of all other windows. Defaults to `False`.
    
    `alpha (float)`: Transparency of the window. Only works on Windows at the moment. Defaults to `1` (opaque).

    `Clock`: Alias of `kivy.clock.Clock`.
    `mdi`: Alias of `SimpleKivy.utils.mdi`.
    `kvWindow`: Alias of `kivy.core.window.Window`.
    
    `ids (IDS)`: Dictionary of ids of all app widgets. You can access widgets with *variable name conformant* ids with dot notation (`app.ids.widget_id`) if the widget was created like this: `sk.Label("text",k='widget_id')`.

    `event_manager`: `function` or `EventManager` instance. Must accept at least two positional arguments: `app` and `event`.
    
    ```py
    def evman(app, event):
        pass
    app=sk.MyApp(
        ...
        event_manager = evman
        ...
    )
    ```

    `ico (str)`: Path to an `*.ico` file. Needed for file dialogs (`askdirectory`, `askopenfile`, etc.) in Windows platforms only.

    `poolt`: Initialized as `ThreadPoolExecutor(thread_name_prefix='SimpleKivy')`.  You can use it to submit threaded tasks.

    `queue (dict)`: Don't overwrite it. This dict is populated by the `thread_pool_new` method.

    ## Methods

    `process_added_widgets()`: Call this after creating new `SimpleKivy` widgets when your program is already running (e.g., adding `Popup` widgets, menus, buttons, etc.). Finishes processing widgets and incorporating them into the `app`.
    > Aliases: `paw`

    `thread_pool_new(name, max_workers=None)`: Creates a thread pool with `ThreadPoolExecutor(max_workers=max_workers,thread_name_prefix=name)` and adds it to the `queue` dictionary with the name as key.

    `queue_new(name)`: Creates a thread pool with a single worker (a queue) with `ThreadPoolExecutor(max_workers=1,thread_name_prefix=name)` and adds it to the `queue` dictionary with the name as key.

    `hide(*key_list, shrink = True)`: Hides widgets by their key/id.
    > - `*key_list`: Positional arguments representing all the widgets by their key which will be hidden.
    > - `shrink (bool)`: Whether the widget's size will be set to `(0,0)` while hidden.

    `unhide(*key_list, enforce = {})`: Unhides widgets.
    > - `*key_list`: Positional arguments representing all the widgets by their key which will be unhidden.
    > - `enforce (dict)`: Properties to enforce after unhiding. In case the widget's size is not fully restored after hiding it.

    `destroy_widget(k, default = None)`: Removes a widget from the extra references kept by `SimpleKivy`, like `app.ids`.
    
    `add_top_widget(widget, remove_on_click=True)`: Adds a top widget to be shown on top of other widgets.
    > - `widget (Widget)`: Widget (sets as `app.top_widget` value).
    > - `remove_on_click (bool)`: Whether the `top_widget` will be removed automatically when a mouse click event is detected.

    `remove_top_widget()`: Remove the current `top_widget` if any.
    
    `add_top_widget(widget, remove_on_click=True)`: Adds a subtop widget to be shown on top of other widgets, besides the `top_widget`.
    > - `widget (Widget)`: Widget (sets as `app.subtop_widget` value).
    > - `remove_on_click (bool)`: Whether the `subtop_widget` will be removed automatically when a mouse click event is detected.

    `remove_subtop_widget()`: Remove the current `subtop_widget` if any.

    {method_infotip}
    > Shows an infotip.
    
    `infotip_schedule`: Schedules an infotip to be shown in the next frame.

    `infotip_remove_schedule`: Schedules the `top_widget` to be removed in the next frame.

    `disable_widgets(*widgets)`: Sets `disabled = True` of the positional arguments `*widgets` given:
    > - `*widgets`: One or many `str` or `Widget` values. If `str`, must be a widget id.
    
    `enable_widgets(*widgets)`: Sets `disabled = False` of the positional arguments `*widgets` given:
    > - `*widgets`: One or many `str` or `Widget` values. If `str`, must be a widget id.
    
    `Resize(width, height)`: Setes the Window size.

    `bring_to_front()`: Brings the Window to the front of all other opened programs.

    `__call__(k,prop=None,val=None,timeout=0,_kw_prepro=False,ignore_errors=False,**kwargs)`: You can call the `app` as if it were a function to schedule property changes (`app(...)`). 
    > - `k (str, Widget)`: The Value of the `k` argument represents a widget, either by its *widget id*, or by the `Widget` instance itself. 

    > Example:
    ```py
    app(k='label_widget_id',text='New text', haling='right')
    ```

    `dt_call(k,prop=None,val=None,_kw_prepro=False,ignore_errors=False,**kwargs)`: Returns a `lambda` function that calls `app.__call__` (same as `app(...)`) with the given arguments.

    `schedule_call_once(k,prop=None,val=None,timeout=0,_kw_prepro=False,ignore_errors=False,**kwargs)`: Schedules `app(...)` with the given arguments to be called in the next frame.

    `schedule_call_interval(k,prop=None,val=None,timeout=0,_kw_prepro=False,ignore_errors=False,**kwargs)`: Schedules `app(...)` with the given arguments to be called every `timeout` seconds.
    
    `trigger_event(event,*args,**kwargs)`: Gets or creates a trigger for the event. The trigger created will call the `event_manager` with the given arguments.

    `schedule_event_once(event,*args,timeout=0,**kwargs)`: Schedule a call of the `event_manager` for the next frame with the given arguments.

    `schedule_func_once(func,*args,timeout=0,**kwargs)`: Schedule a function to be called in the next frame with the given arguments.

    `schedule_get_call(key,method,*args,**kwargs)`: Schedule once a call to the method named `method` of a widget with ID `key`, and with the given arguments `*args` and `**kwargs`.

    `submit_thread_event(event,*args,**kwargs)`: Submits a call of the `event_manager` in the `poolt` thread pool with the given arguments. 
    > Aliases: `thread_event`

    `submit_thread_event_at(thread_name,event,*args,**kwargs)`: Submits a call of the `event_manager` in the `queue[thread_name]` thread pool with the given arguments.
    > Aliases: `thread_event_at`

    `call_event(event,*args,**kwargs)`: Calls the `event_manager` with the given arguments.

    `keys()`: Shortcut to `app.ids.keys()`.
    `values()`: Shortcut to `app.ids.values()`.
    `items()`: Shortcut to `app.ids.items()`.

    {method_AskOpenFile}
    > Creates a `SimpleKivy` file dialog to open a file.

    {method_AskDirectory}
    > Creates a `SimpleKivy` file dialog to open a directory.

    {method_askdirectory}
    > Creates a native platform file dialog to open a directory.

    {method_askopenfile}
    > Creates a native platform file dialog to open a file.

    {method_askopenfiles}
    > Creates a native platform file dialog to open multiple files.

    {method_asksaveasfile}
    > Creates a native platform file dialog to save a file as the input name and location.
    
    `popup_message`: Creates a popup widget with a message.

    `lock()`: Show a lock screen that only gets dismissed when you call the `unlock` method.

    `unlock()`: Dismisses the `lock` screen.

    `build()`: Internal. Processes and returns the `layout` as a widget.

    `minimize()`: Shortcut to `kivy.core.Window.minimize()`
    `restore()`: Shortcut to `kivy.core.Window.restore()`
    `maximize()`: Shortcut to `kivy.core.Window.maximize()`
    `close()`: Closes the app.

    `is_leaving()`: Whether the app is in the closing sequence. Useful when there are threaded tasks that have not finished.

    `sleep_in_thread(timeout = 0)`: Similar to the `time.sleep` function, but returns immediately if the app is in the closing sequence.
    
    ## Kivy Bases
    `App`
    {base_params}
    '''
    window_is_maximized = BooleanProperty(False)
    _top_widget=None
    _subtop_widget=None
    def _get_tw(self):
        return self._top_widget
    def _set_tw(self,v):
        self._top_widget=v
        return True
    top_widget=kvw.AliasProperty(_get_tw,_set_tw)
    def _get_stw(self):
        return self._subtop_widget
    def _set_stw(self,v):
        self._subtop_widget=v
        return True
    subtop_widget=kvw.AliasProperty(_get_stw,_set_stw)
        
    def __init__(
        self,
        layout=[[]],
        title='MyApp',
        event_manager=None,
        custom_titlebar=False,
        alpha=1,
        keep_on_top=False,
        icon='skdata/logo/simplekivy-icon-32.png',
        layout_class=None,
        layout_args={},
        do_auto_config=True,
        **kwargs
        ):
        self._config={}
        self._config_file=None

        if event_manager==None:
            event_manager=_event_manager
        if do_auto_config and not utils._did_auto_config:
            auto_config()
            pass

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
            if custom_titlebar==True:
                try:
                    first_el=layout[0][0]
                except:
                    first_el=layout[0]
                self.kvWindow.set_custom_titlebar(first_el)
                tbw=self.kvWindow.titlebar_widget
                if hasattr(tbw,'children'):
                    _ensure_bttn_not_draggable(tbw.children)
            else:
                if custom_titlebar!=NOTKEY:
                    def set_ctb(dt):
                        self.kvWindow.set_custom_titlebar(self.ids[custom_titlebar])
                        tbw=self.kvWindow.titlebar_widget
                        if hasattr(tbw,'children'):
                            _ensure_bttn_not_draggable(tbw.children)

                    Clock.schedule_once(set_ctb)
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

        self._filebrowser={}
        self.lock_widget=None

        self._nk=0
        # class IDS(dict):
        #     def __getattr__(self,name):
        #         return self.__getitem__(name)
        # self.ids={}
        self.ids=utils.IDS()
        # self.ids.__getattr__=types.MethodType(ids.__getitem__, ids)
        self._ids={}
        if not layout_class:
            rows=len(layout)
            
            # self._layout=kvw.GridLayoutB(rows=rows,**_preprocess(**layout_args))
            
            kvWd = kvw.GridLayoutB
            if 'HAS_GRADIENT' in os.environ:
                from SimpleKivy.kvGradient import GradientGrid
                # class _kvWd_(GradientBehavior,kvWd):
                #     pass
                # kvWd=_kvWd_
                kvWd=GradientGrid
                # layout_args['over_class']=GradientBehavior
                # kvWd=GradientBehavior,kvWd
                # class _kvWd(GradientBehavior,kvWd):
                #     pass
                
                
                layout_args['gradient']=layout_args.get('gradient',['linear-gradient',dict(colors=['',''],size=[2,2])])

            self._layout=skivify(kvWd,rows=rows,**layout_args)
            
            
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
            if 'HAS_GRADIENT' in os.environ:
                if not hasattr(layout_class,'gradient'):
                    from SimpleKivy.kvGradient import GradientBehavior
                    layout_args['over_class']=GradientBehavior
                    layout_args['gradient']=layout_args.get('gradient',['linear-gradient',dict(colors=['',''],size=[2,2])])
            # print(layout_args)
            # self._layout=layout_class(**layout_args)
            # for kivy_el in layout:
            #     self._layout.add_widget(kivy_el)
            try:
                self._layout=layout_class(**layout_args)
            except:
                self._layout=skivify(layout_class,**layout_args)
            for kivy_el in layout:
                self._layout.add_widget(kivy_el)


        
        # if event_manager:
        self._triggers={}
        self.event_manager=event_manager
        self.thread_event=self.submit_thread_event
        self.thread_event_at=self.submit_thread_event_at
        self.get_group=kvw.ToggleButtonBehavior.get_widgets
        self.hidden={}
        # else:
        #     self.event_manager=self._event_manager

        # self.top_widget = None
        # self.subtop_widget = None
        self.remove_on_click = False
        def on_touch_down(instace, touch):
            if self.remove_on_click and touch.button in ('left','middle','right'):
                self.remove_top_widget()
        self._layout.bind(on_touch_down=on_touch_down)

        _future_process_elements(self)
        _post_process_elements(self)
        _future_process_binds(self)
        _process_config_set(self) 
        # super(MyApp, self).__init__(**kwargs)
        self.paw=self.process_added_widgets
        self.Clock.schedule_once(lambda dt: setattr(self,'alpha',alpha))
        
        self._keep_on_top=keep_on_top
        self.Clock.schedule_once(lambda dt: setattr(self,'keep_on_top',keep_on_top))

        self._hwnd=None
        
        # self.Clock.schedule_once(lambda dt: setattr(self.icon,'ico',))
        # if icon=='skdata/logo/simplekivy-icon-32.png':
        self.ico=resource_find(kwargs.pop('ico','skdata/logo/simplekivy-icon-256.ico'))
        # self.Clock.schedule_once(lambda dt: setattr(self.icon,'ico',))
        # self.icon=icon
        # Clock.schedule_once(lambda dt: setattr(self,'icon',icon),1)
        Clock.schedule_once(lambda dt: self.on_icon(self,self.get_application_icon()))

        ################################
        # For MiniApp compatibility
        kwargs.pop('k',None) 
        kwargs.pop('size_hint',None) 
        ################################
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
        return self.queue[name]
    def queue_new(self,name):
        self.queue[name]=ThreadPoolExecutor(max_workers=1,thread_name_prefix=name)
        return self.queue[name]


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
            if isinstance(k,str):
                wid=self.__getitem__(k)
            else:
                wid=k
            s=getattr(wid,'size',(100,100)).copy()
            sh=getattr(wid,'size_hint',(1,1)).copy()
            o=getattr(wid,'opacity',1)
            d=getattr(wid,'disabled',False)
            # if o==0 and d==True:
            #     return
            # print('hide:',(s,sh,o,d))

            if k not in self.hidden:
                self.hidden[k]=(s,sh,o,d)
            # print(self.hidden)
            # print(k,':',(s,sh,o,d))
            # setattr(w,'size')
            if shrink:
                setattr(wid,'size',(1,1))
                setattr(wid,'size_hint',(None,None))
            setattr(wid,'opacity',0)
            setattr(wid,'disabled',True)
            # print(self.hidden)
    def unhide(self,*key_list,enforce={}):
        for k in key_list:
            if isinstance(k,str):
                wid=self.__getitem__(k)
            else:
                wid=k
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

            # if o==1 and d==False:
            #     return
            
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

    def remove_subtop_widget(self):
        if self.subtop_widget:
            self._layout.parent.remove_widget(self.subtop_widget)
            self.subtop_widget = None
    def _remove_subtop_widget(self,dt):
        self.remove_subtop_widget()
    def add_subtop_widget(self, widget, remove_on_click=True):
        self.remove_subtop_widget()
        self.remove_on_click = remove_on_click
        self.subtop_widget = widget
        # Clock.schedule_once(lambda *args: self._layout.parent.add_widget(self.subtop_widget))
        self._layout.parent.add_widget(self.subtop_widget)
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

        bcolor=tooltip_args.pop('bcolor',(.13,.13,.13,1))
        color=tooltip_args.pop('color','#CCCCCC')
        lcolor=tooltip_args.pop('lcolor','gray')
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
        # it=LargeText(
        it =Label(
            text=text,height=height,size_hint_y=size_hint_y,pos_hint=pos_hint,
            lcolor=lcolor,color=color,bcolor=bcolor,markup=markup,
            font_size=font_size,
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
        _process_config_set(self)
        return wid
    def process_added_widgets(self):
        _future_process_elements(self)
        _post_process_elements(self)
        _future_process_binds(self)
        _process_config_set(self)
    # def trigger_call(self,k,prop=None,val=None,_kw_prepro=False,ignore_errors=False,**kwargs):
    #     return lambda dt: self.__call__(k=k,prop=prop,val=val,_kw_prepro=_kw_prepro,ignore_errors=ignore_errors,**kwargs)
    def dt_call(self,k,prop=None,val=None,_kw_prepro=False,ignore_errors=False,**kwargs):
        return lambda dt: self.__call__(k=k,prop=prop,val=val,_kw_prepro=_kw_prepro,ignore_errors=ignore_errors,**kwargs)
    #     return 

    def schedule_call_once(self,k,prop=None,val=None,timeout=0,_kw_prepro=False,ignore_errors=False,**kwargs):
        Clock.schedule_once(lambda dt:self.__call__(k=k,prop=prop,val=val,_kw_prepro=_kw_prepro,ignore_errors=ignore_errors,**kwargs),timeout=timeout)
    def schedule_call_interval(self,k,prop=None,val=None,timeout=0,_kw_prepro=False,ignore_errors=False,**kwargs):
        Clock.schedule_interval(lambda dt:self.__call__(k=k,prop=prop,val=val,_kw_prepro=_kw_prepro,ignore_errors=ignore_errors,**kwargs),timeout=timeout)
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
                    kw=_preprocess(**{prop:val})
                    trigger=Clock.create_trigger(lambda *args:setattr(widget,prop,kw[prop]),timeout)
                    trigger()
                else:
                    trigger=Clock.create_trigger(lambda *args:setattr(widget,prop,val),timeout)
                    trigger()
            else:
                # print(kwargs)
                kwargs=_preprocess(**kwargs)
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
    def trigger_event(self,event,*args,**kwargs):
        trigger=self._triggers.get(  event,Clock.create_trigger(  lambda *x: self.event_manager(self,event,*args,**kwargs)  )  )
        trigger()
    def schedule_event_once(self,event,*args,timeout=0,**kwargs):
        ans=Clock.schedule_once(lambda dt: self.event_manager(self,event,*args,**kwargs),timeout=timeout)
    def schedule_func_once(self,func,*args,timeout=0,**kwargs):
        ans=Clock.schedule_once(lambda dt: func(*args,**kwargs),timeout=timeout)

    def AskOpenFile(self,
        initialdir='./',
        filetypes=(
                ('All files', '*.*'),
                # ('PDF', '*.pdf'),
            ),
        callback=None,
            **kw,
        ):
        '''
        Creates a `SimpleKivy` file dialog to open a file.

        {initialdir}
        {filetypes}
        {filedialog_callback}
        {filedialog_kw}
        '''
        _k='askopenfile'
        if _k in self._filebrowser:
            self._filebrowser[_k].root.filelist.filelist.deselect_all()
            self._filebrowser[_k].root.input_selection.text=''
            self._filebrowser[_k].open()
            return

        spinner_vals=[f'{ft[0]} ({ft[1]})' for ft in filetypes]
        spinner_vals_d={}
        for i,sv in enumerate(spinner_vals):
            spinner_vals_d[sv]=[]
            for ext in filetypes[i][1].split():
                ext=ext.replace('*','').lower()
                if ext=='.':
                    continue
                else:
                    spinner_vals_d[sv].append(ext)
        
        # spinner_filetypes=Spinner2Dark(spinner_vals[0],spinner_vals)
        
        # spinner_filetypes=Spinner(spinner_vals[0],spinner_vals)
        spin_btn=ClearB(text=spinner_vals[0],lcolor='gray',k=NOTKEY)
        spin_lbl=Label(mdi('chevron-down'),size='x30',markup=True,k=NOTKEY)
        spin_btn.add_widget(
            spin_lbl
            )
        def on_dd_open(ins,to):
            # print(x)
            if to==None:
                spin_lbl.text=mdi('chevron-down')
            else:
                spin_lbl.text=mdi('chevron-up')


        spinner_filetypes=AddDropDown(
            spin_btn,
            [FlatB(text=svi,size='y35',lcolor='gray',bcolor='',k=NOTKEY,on_release=lambda ins:setattr(spin_btn,'text',ins.text)) for svi in spinner_vals],
            bcolor='#2C2C2C',
            # lcolor='gray',
            # on_attach_to=on_dd_open
            bind={
            'attach_to':on_dd_open
            }
            )

        spinner_filetypes.vals_d=spinner_vals_d
        def on_filetype(ins,t):
            # print(ins.vals_d[t])
            ins.root.file_types_filter=ins.vals_d[t]
            ins.root.refresh()

        spinner_filetypes.bind(text=on_filetype)

        kvfilelist=Filelist(initialdir=initialdir,file_types_filter=spinner_vals_d[spinner_vals[0]],k=NOTKEY)
        spinner_filetypes.root=kvfilelist
        btn_open=ClearRoundB('Open',k=NOTKEY,)
        btn_cancel=ClearRoundB('Cancel',k=NOTKEY,)
        input_selection=InputDark(k=NOTKEY)
        
        kel=BoxitV(
                kvfilelist,
                SeparatorH(size=(1,1)),
                BoxitH(
                    BoxitV(
                        Label('File name:',halign='right',size='x100',k=NOTKEY,)*Void(size='x4')*input_selection,
                        Fill(),
                        spacing=8,
                        # lcolor='green'
                        k=NOTKEY,
                        ),
                    BoxitV(
                        spinner_filetypes,
                        btn_open*Void(size='x4')*btn_cancel,
                        spacing=8,
                        size_hint_max_x=300,
                        # lcolor='purple'
                        k=NOTKEY,
                        ),
                    
                    size="y80",
                    # lcolor='r',
                    spacing=4,
                    k=NOTKEY,
                    ),
                spacing=4,
                padding=4,
                k=NOTKEY,
            )
        kel.filelist=kvfilelist
        kel.input_selection=input_selection
        input_selection.root=kel
        kvfilelist.root=kel
        def on_file_select(ins,rv,values):
            # ins.root.input_selection.text=f"{[rv.data[i]['meta'].name for i in values ]}"
            fi=rv.data[values[0]]['meta']
            if not fi.is_dir():

                ins.root.input_selection.text=f"{fi.name}"
                ins.root.input_selection.cursor=(0,0)

        kvfilelist.bind(on_selection=on_file_select)
        if callback==None:
            callback=utils.do_nothing
        kel.callback=callback

        kel.btn_open=btn_open
        btn_open.root=kel

        pop=Popup(kel,title='Open',background='',background_color='#191919')
        kel.popup=pop
        pop.root=kel
        btn_cancel.bind(on_release=lambda ins:pop.dismiss())

        def on_btn_open(ins):
            # print(ins.root.input_selection.text)
            
            filename=ins.root.input_selection.text
            if filename:
                 # and ins.root.callback
                filename=os.path.join(f"{ins.root.filelist.current_directory.resolve().absolute()}",filename)
                if not os.path.exists(filename):
                    self.popup_message(f'{mdi('alert',color='yellow',size=30)} File not found:\n"{filename}"',auto_dismiss=1.5,title='Error',markup=True)
                elif os.path.isdir(filename):
                    ins.root.filelist.on_path( pathlib.Path(filename) )
                    self.__call__(ins.root.input_selection,text='')

                    return True
                    # self.popup_message(f'{mdi('alert',color='yellow',size=30)} The filename is a directory:\n"{filename}"',auto_dismiss=1.5,title='Error',markup=True)
                else:
                    ins.root.callback(filename)
                    ins.root.popup.dismiss()
            

        btn_open.bind(on_release=on_btn_open)
        kvfilelist.bind(on_file_double_click=lambda ins,rv,i:btn_open.trigger_action())
        
        def on_pop_dismiss(ins):
            get_kvApp().remove_top_widget()
        pop.bind(on_dismiss=on_pop_dismiss)
        # pop.bind(on_dismiss=lambda *x:self.remove_top_widget())

        def on_pop_open(ins):
            if ins.root.filelist.input_search.text:
                ins.root.filelist.input_search.text=''
                ins.root.filelist.btn_apply_sort.dispatch('on_release')
        pop.bind(on_pre_open=on_pop_open)
        
        input_selection.bind(on_text_validate=lambda *x:btn_open.trigger_action())
        self._filebrowser[_k]=pop
        pop.open()

    def popup_message(self,msg='message',title="Message",auto_dismiss=-1,dismiss_callback=None,size_hint=(.3,.3),**kw):
        pop=Popup(
            title=title,
            content=Label(msg,k=NOTKEY,**kw),
            size_hint=size_hint,
            k=NOTKEY)
        if auto_dismiss>0:
            pop.bind(on_open=lambda ins:Clock.schedule_once(ins.dismiss,auto_dismiss))
        def on_dismiss(ins):
            del ins
            if dismiss_callback:
                dismiss_callback()
        pop.bind(on_dismiss=on_dismiss)
        pop.open()

    def lock(self):
        if not self.lock_widget:
            lbl=Label(mdi('dots-circle'),
                # focus_behavior=True,
                # focus_map={},
                # focus_color='',
                font_size=80,markup=True,k=NOTKEY)
            box=BoxitAngle(lbl,k=NOTKEY,
                # bcolor='dark grey'
                bcolor=[.1,.1,.1,.25]
                )
            box.lbl=lbl

            from kivy.animation import Animation
            box.animation=Animation(angle=359,duration=1.5,t='in_out_quad')
            def on_complete(ani,wid):
                # setattr(wid,'angle',0)
                self.__call__(wid,angle=0)
                if self._locked:
                    Clock.schedule_once(lambda dt:wid.animation.start(wid))

            box.animation.bind(on_complete=on_complete)

            def rotate_start(ins,*x):
                ins.lf=get_last_focused()
                # print(ins.lf)
                # if ins.lf:
                #     if ins.lf.focus:
                #         self.__call__(ins.lf,focus=False)
                    # ins.lf.focus=False
                # if ins.lf:
                #     self.__call__(ins.box.lbl,focus=True)
                    # Clock.schedule_once
                # print(f"{ins.lf=}")
                # print(ins.lf)
                # ins.box.lbl.focus=True
                # print('starting')
                # ins.box.animation.cancel(ins.box)
                ins.box.animation.start(ins.box)
                self._locked=True
                # Clock.schedule_once(lambda dt:ins.box.animation.start(ins.box))
            def rotate_stop(ins,*x):
                # if ins.lf and ins.lf==get_last_focused():
                # if ins.lf:
                #     if not ins.lf.focus:
                #         self.__call__(ins.lf,focus=True)
                    # ins.box.lbl.focus=False
                    # ins.lf.focus=True
                # if ins==get_last_focused():
                #     utils.set_last_focused(ins.lf)

                # ins.box.animation.cancel_all(ins.box,'angle')
                ins.box.animation.cancel(ins.box)
                # Clock.schedule_once(lambda dt:ins.box.animation.cancel(ins.box))
                # Clock.schedule_once(lambda dt:setattr(ins.box,'angle',0))
                
                self._locked=False

                self.__call__(ins.box,angle=0)
                
                
                # if getattr(ins,'lf',None):
                #     self.__call__(ins.box.lbl,focus=False)
                #     self.__call__(ins.lf,focus=True)
                
                # Clock.schedule_once(lambda dt:ins.box.animation.cancel(ins.box))
                # setattr(ins.box,'angle',0)
                # 

                # self.angle=0
                # print('do cancel')
            # def do_rotate(self,dt):
            #     # print(self.angle)

            #     self.angle=self.angle+5
            #     if self._rotating:
            #         Clock.schedule_once(self.do_rotate,self.fps)

            # box.do_rotate=types.MethodType(do_rotate,box)
            # box.rotate_start=types.MethodType(rotate_start,box)
            # box.rotate_stop=types.MethodType(rotate_stop,box)
            
            # box.bind(angle=print)

            def _gfocus_map(self):
                pass
                # return self.box.lbl.focus_map
                # return self._actual_focus_map
            def _sfocus_map(self,v):
                # self._actual_focus_map = v
                # self.box.lbl.focus_map=v
                pass
                return True
            pfocus_map=property(_gfocus_map,_sfocus_map)
            
            pop=ModalView(
                box,
                auto_dismiss=False,
                size_hint=(1,1),
                background_color=[0,0,0,0],
                k=NOTKEY,
                background='',
                # bind=dict(
                #     on_pre_open=rotate_start,
                #     on_dismiss=rotate_stop,
                #     )
                properties=dict(
                    focus_map=pfocus_map,
                    # on_key_down=print
                    )
                )
            pop.box=box
            
            self.paw()

            pop.bind(
                on_pre_open=rotate_start,
                on_pre_dismiss=rotate_stop,
                )
            self._locked=False
            self.lock_widget=pop
            

            # self.lock_widget._actual_focus_map = {}
            # self.lock_widget.__class__.focus_map=
            # setattr(lbl.__class__,"focus_map",property(_gfocus_map,_sfocus_map))

        # self._locked=True
        # if not self._locked:
        self.lock_widget.open()

    def dt_lock(self,dt):
        # if not self._locked:
        self.lock()
    def dt_unlock(self,dt):
        # if self._locked:
        self.unlock()

    def is_locked(self):
        return self._locked

    def unlock(self):
        if self.lock_widget:
            self.lock_widget.dismiss()
        # self._locked=False
    def lock_schedule_once(self):
        Clock.schedule_once(self.dt_lock)
    def unlock_schedule_once(self):
        Clock.schedule_once(self.dt_unlock)
    
    @locked_screen
    def askopenfile(self,
        filetypes=(
                ('All files', '*.*'),
                # ('PDF', '*.pdf'),
            ),
        callback=None,
        **kw,
        ):
        '''
        Creates a native platform file dialog to open a file.

        {initialdir}
        {filetypes}
        {filedialog_callback}
        {filedialog_kw}
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
    def AskDirectory(self,
        initialdir='./',
        callback=None,
            **kw,
        ):
        '''
        Creates a `SimpleKivy` file dialog to open a directory.
        {initialdir}
        {filedialog_callback}
        {filedialog_kw}
        '''
        _k='askdirectory'
        if _k in self._filebrowser:
            self._filebrowser[_k].root.filelist.filelist.deselect_all()
            self._filebrowser[_k].root.input_selection.text=''
            self._filebrowser[_k].open()
            return

        kvfilelist=Filelist(initialdir=initialdir,k=NOTKEY,folders_only=True)
        btn_open=ClearRoundB('Select folder',k=NOTKEY)
        btn_cancel=ClearRoundB('Cancel',k=NOTKEY)
        input_selection=InputDark(k=NOTKEY)
        kel=BoxitV(
            kvfilelist,
            SeparatorH(size=(1,1)),
            # BoxitH(
                BoxitV(
                    Label('File name:',halign='right',size='x100')*Void(size='x4')*input_selection,
                    Fill(size_hint=(2,1))*BoxitH(btn_open,btn_cancel,spacing=4,size_hint_max_x=300),
                    spacing=8,
                    padding=4,
                    size='y80',
                    k=NOTKEY,
                    ),
                # size="y80",
                # spacing=4,
                # ),
            # spacing=4,
            # padding=4
            )
        kel.filelist=kvfilelist
        kel.input_selection=input_selection
        input_selection.root=kel
        kvfilelist.root=kel
        def on_file_select(ins,rv,values):
            # ins.root.input_selection.text=f"{[rv.data[i]['meta'].name for i in values ]}"
            fi=rv.data[values[0]]['meta']
            if fi.is_dir():
                # self.__call__(ins.root.input_selection,text=f"{fi.name}",cursor=(0,0))
                ins.root.input_selection.text=f"{fi.name}"
                ins.root.input_selection.cursor=(0,0)

        kvfilelist.bind(on_selection=on_file_select)
        if callback==None:
            callback=utils.do_nothing
        kel.callback=callback

        kel.btn_open=btn_open
        btn_open.root=kel

        pop=Popup(kel,title='Open',background='',background_color='#191919')
        kel.popup=pop
        pop.root=kel
        btn_cancel.bind(on_release=lambda ins:pop.dismiss())

        def on_btn_open(ins):
            # print(ins.root.input_selection.text)
            
            filename=ins.root.input_selection.text
            if filename:
                filename=os.path.join(f"{ins.root.filelist.current_directory.resolve().absolute()}",filename)
                if not os.path.exists(filename):
                    self.popup_message(f'{mdi('alert',color='yellow',size=30)} Directory not found:\n"{filename}"',auto_dismiss=1.5,title='Error',markup=True)
                else:
                    ins.root.callback(filename)
                    ins.root.popup.dismiss()
            else:
                filename=os.path.join(f"{ins.root.filelist.current_directory.resolve().absolute()}")
                if not os.path.exists(filename):
                    self.popup_message(f'{mdi('alert',color='yellow',size=30)} Directory not found:\n"{filename}"',auto_dismiss=1.5,title='Error',markup=True)
                else:
                    ins.root.callback(filename)
                    ins.root.popup.dismiss()
            

        btn_open.bind(on_release=on_btn_open)
        # kvfilelist.filelist.bind(on_double_click=lambda *x:setattr(input_selection,'text',''))
        kvfilelist.bind(on_directory=lambda *x:self.__call__(input_selection,text=''))

        def on_pop_dismiss(ins):
            get_kvApp().remove_top_widget()
        pop.bind(on_dismiss=on_pop_dismiss)
        # pop.bind(on_dismiss=lambda *x:self.remove_top_widget())
        
        def on_pop_open(ins):
            if ins.root.filelist.input_search.text:
                ins.root.filelist.input_search.text=''
                ins.root.filelist.btn_apply_sort.dispatch('on_release')
        pop.bind(on_pre_open=on_pop_open)

        def on_input_validate(ins):
            ins.root.btn_open.trigger_action()
        input_selection.bind(on_text_validate=on_input_validate)
        self._filebrowser[_k]=pop
        pop.open()

    @locked_screen
    def askdirectory(self,
        callback=None,
        **kw,
        ):
        '''
        Creates a native platform file dialog to open a directory.
        
        {initialdir}
        {filedialog_callback}
        {filedialog_kw}
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

    @locked_screen
    def asksaveasfile(self,
        initialfile='',
        filetypes=(
            ('All files', '*.*'),
            # ('PDF', '*.pdf'),
            
            ),
        callback=None,
        **kw,
        ):
        '''
        Creates a native platform file dialog to save a file as the input name and location.
        
        {initialfile}
        {filetypes}
        {filedialog_callback}
        {filedialog_kw}
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
    @locked_screen
    def askopenfiles(self,
        filetypes=(
            ('All files', '*.*'),
            # ('PDF', '*.pdf'),
            
            ),
        callback=None,
        **kw,
        ):
        '''
        Creates a native platform file dialog to open multiple files.
        
        {initialdir}
        {filetypes}
        {filedialog_callback}
        {filedialog_kw}
        '''

        # def _do():
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
        # self.unlock()
        return filenames
        # self.lock()
        # self.poolt.submit(_do)

    
        
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

    def submit_thread_event_at(self,thread_name,event,*args,**kwargs):
        if not thread_name in self.queue:
            self.queue_new(thread_name)
        future=self.queue[thread_name].submit(self.event_manager,self,event,*args,**kwargs)
        return future
    def submit_thread_event(self,event,*args,**kwargs):
        # def tryfun(app,event):
        #     try:
        #         app.event_manager(self,event)
        #     except:
        #         traceback.print_exc()
        future=self.poolt.submit(self.event_manager,self,event,*args,**kwargs)
        return future
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
    # def __setitem__(self, key, value):
    #     setattr(value,'id',key)
    #     self.ids.__setitem__(key, value)

    def schedule_get_call(self,key,method,*args,timeout=0,**kwargs):
        if isinstance(key,str):
            wid=self.ids[key]
        else:
            wid=key
        Clock.schedule_once(lambda dt:getattr(wid,method)(*args,**kwargs),timeout=timeout)
    
    def schedule_getattr_call(self,*args,**kwargs):
        '''
        Same as schedule_get_call.
        '''
        self.schedule_get_call(*args,**kwargs)

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
    #     self.event_manager(self,f"{ev}.{getattr(args[0],'on_event',subevent)}")
    def config_set(self,file):
        self._config_file=file
        if not os.path.exists(file):
            self.config_dump()
    def config_dump(self):
        # if file==None and hasattr(self,'_config'):
        #     file=self._config['file']
        #     kwargs=self._config['kwargs']
        if not self._config_file:
            raise ValueError(f'Method MyApp.config_set has not been called first with a valid filename: "{self._config_file}"')

        
        data={}
        for k,props in self._config.items():
            data[k]={}
            for prop in props:
                data[k][prop]=getattr(self.ids[k],prop)
        pickle.dump(data,file=open(self._config_file,'wb'))
    def config_load(self):
        if not self._config_file:
            raise ValueError(f'Method MyApp.config_set has not been called first with a valid filename: "{self._config_file}"')

        data=pickle.load(file=open(self._config_file,'rb'))
        # print(data)
        for k , props in data.items():
            self.__call__(k,**props)
        return data


        # match ev:
        #     case '__Minimize__':
        #         self.minimize()
        #     case '__Restore__':
        #         self.restore()
    def call_event(self,event,*args,**kwargs):
        return self.event_manager(self,event,*args,**kwargs)
        


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
        # print('hell')
        # self.get_running_app().stop()
        self._leaving=True
        # self.event_manager(self,'__Close__')
        Clock.schedule_once(lambda dt:self.event_manager(self,'__Close__'))
        
        # self.trigger_event('__Close__')
        
        # self.event_manager(self,'__Close__')
        # Clock.schedule_once(lambda dt : self.event_manager(self,'__Close__'))
        # self.kvWindow.close()
        # Clock.schedule_once(lambda dt: self.kvWindow.close(),1)
        # self=App.get_running_app()
        
        # self.trigger_event('__Close__')
        Clock.schedule_once(lambda dt:self.stop())
        # Clock.schedule_once(lambda dt:self.close())

        # self.stop()

    def is_leaving(self):
        return self._leaving
    def on_stop(self):
        # print(self._leaving)
        if not self._leaving:
            self.event_manager(self,'__Close__')
            self._leaving=True
            # time.sleep()
    def sleep_in_thread(self,timeout=0,dt=None):
        '''
        Similar to time.sleep, but returns if app._leaving == True.
        Usefull to exit quickly from a threaded task that uses sleep if the main app has closed.
        '''
        t0=time.time()
        if dt==None:
            dt=1
            if timeout<1:
                dt=timeout/3

        while True:
            # print('heree')
            ndt=time.time()-t0
            if ndt>=timeout:
                break
            if self._leaving:
                break
            time.sleep(dt)



def TEST_WIDGET(w,event_manager=None):
    lyt=[[w]]
    MyApp(layout=lyt,event_manager=event_manager).run()

@skwidget
def Label(text='',k=NOTKEY,focus_behavior=False,halign='center',size_behavior='normal',valign='middle',hover_highlight=False,**kwargs):
    '''
    Creates a Label widget dynamically with added functionalities.

    ## Dynamic Creation Parameters

    {focus_behavior}
    > Default is False.
    
    {hover_highlight}

    ## Parameters
    {size_behavior}

    {bgline}

    {common}

    ## Returns
    
    `Label` widget created dynamically.

    ## Kivy Bases
    
    `Label`

    {base_params}

    ## Properties
    
    ## Events
    
    {when_hover_highlight}
    '''


    # kwargs=_preprocess(**kwargs)
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

    if hover_highlight:
        class _(kvb.HoverHighlightBehavior,kvWd):
            pass
        kvWd=_

    kel=skivify_v2(kvWd,text=text,halign=halign,valign=valign,**kwargs,k=k)

    if size_behavior=='none':
        pass
    elif size_behavior=='normal':
        
        kel.bind(size=lambda inst,siz:setattr(inst,'text_size',inst.size))
        # kel.texture_size=kel.size
        Clock.schedule_once(lambda dt:setattr(kel,'text_size',kel.size))

        # Clock.schedule_once(lambda dt:kel.texture_update())
    elif size_behavior in ('text','textv'):
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

    # markup=getattr(kel,'markup',False)
    # if markup:
    #     def on_href(ins,text):
    #         if '[href=' in text:
    #             text = text.replace('[href=', '[color=1B95E0][u][ref=').replace(
    #                 '[/href]', '[/ref][/u][/color]')
    #         # return text
    #         ins.text=text
    #     on_href(kel,kel.text)
    #     kel.bind(text=on_href)

    #     # kel.on_event='on_ref_press',r'lambda instance, refvalue: self.trigger_event(f"{instance.id}/ref/{refvalue}")'
    #     if getattr(kel,'id',NOTKEY)!=NOTKEY:
    #         kel.bind(  on_ref_press=lambda instance, refvalue: self.trigger_event(f"{instance.id}/ref/{refvalue}")   )

    # _future_elements.append(kel)
    return kel


@skwidget
def PagedText(pages=[],k=None,focus_behavior=False,halign='center',size_behavior='normal',valign='middle',**kwargs):
    '''
    Creates a PagedText widget.

    ## Dynamic Creation Parameters
    
    {focus_behavior}
    > Default is False.

    ## Parameters
    
    `pages: list`
    > A list where each element is a string representing each page
    > - `[str, str, ...]`: List of page strings
    
    {size_behavior}

    {bgline}
    
    {common}

    ## Returns
    
    `Label` widget created dynamically with the following modifications:
    
    ## Properties
    
    `page (NumericProperty)`: Page index. Defaults to `None`.
    `pages (ListProperty)`: Initialized with the `pages` parameter. Defaults to `[]`.

    ## Events
    
    `on_page(ins,val)`: Fired when the current page index is changed.
    `on_pages(ins,val)`: Fired when the value of pages is set.

    ## Methods
    
    `reload()`: Sets page to 0 if pages is not empty.
    `empty()`: Sets pages to [''] and clears current text.
    `next_page()`: Goes to the next page.
    `previous_page()`: Goes to the previous page.

    ## Kivy Bases
    
    `Label`

    {base_params}
    '''
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
def RstDocument(text='',k=None,enable_events=True,do_dot_subevent=True,on_event='on_ref_press',**kwargs):
    '''
    Creates a RstDocument widget dynamically with added functionalities.

    ## Parameters
    
    {common}

    ## Returns
    
    `RstDocument` widget created dynamically.

    ## Kivy Bases
    
    `RstDocument`

    {base_params}
    '''
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


    kel=skivify_v2(kvWd,text=text,enable_events=enable_events,do_dot_subevent=do_dot_subevent,on_event=on_event,k=k,**kwargs)
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

    do_dot_subevent=kwargs.pop('do_dot_subevent',do_dot_subevent)
    enable_events=kwargs.pop('enable_events',enable_events)
    on_event=kwargs.pop('on_event',on_event)
    properties=kwargs.pop('properties',None)
    over_class=kwargs.pop('over_class',())
    
    # print(f"{over_class = }")
    if isinstance(class_,(list,tuple)):
        if over_class:
            class_=list(class_)
            if not isinstance(over_class,(list,tuple)):
                over_class=[over_class]
            class_=over_class+class_
        # print(class_)
        class _class_(*class_):
            pass
        class_=_class_
    else:
        if over_class:
            class_=[class_]
            if not isinstance(over_class,(list,tuple)):
                over_class=[over_class]
            # class_.extend(over_class)
            class_=over_class+class_
            # over_class.extend(class_)
            print(class_)
            class _class_(*class_):
                pass
            class_=_class_
    
    if properties:
        for k,v in properties.items():
            setattr(class_,k,v)

    def widget_creator(enable_events,on_event,do_dot_subevent,**kwargs):
        kel=class_(**kwargs)
        kel.id=k
        if enable_events:
            kel.enable_events=enable_events
            kel.on_event=on_event
            kel.do_dot_subevent=do_dot_subevent
        return kel
    return widget_creator(enable_events,on_event,do_dot_subevent,**kwargs)
skivify=skivify_v2
# def extwidget_to_skwidget(class_,**kwargs):
#     @skwidget
#     def _external_widget(**kwargs):
#         return skivify_v2(class_,**kwargs)
#     return _external_widget(**kwargs)

def extwidget_to_skwidget(class_):
    '''
    Converts an external widget class into a Widget Creator Function (a SimpleKivy Widget).
    Consider it as a convenience function to convert any widget compatible with kivy into a widget compatible with SimpleKivy, without adding extra functionalities besides args preprocessing and `k` (widget id) parameter.
    '''
    @skwidget
    def _external_widget(**kwargs):
        return skivify_v2(class_,**kwargs)
    return _external_widget
kivy2sk=extwidget_to_skwidget

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
def CheckBox(active=False,k=None,on_event='active',**kwargs):
    '''
    Creates a CheckBox widget dynamically with added functionalities.

    ## Parameters
    
    {common}

    ## Returns
    
    `CheckBox` widget created dynamically.

    ## Kivy Bases
    
    `CheckBox`

    {base_params}
    '''
    from kivy.uix.checkbox import CheckBox as kvCheckBox
    kel=skivify(kvCheckBox,k=k,active=active,on_event=on_event,**kwargs)
    return kel

@skwidget
def Camera(k=None,legacy=False,**kwargs):
    '''
    Creates a custom Camera widget dynamically with added functionalities.

    ## Dynamic Creation Parameters

    `legacy: bool`
    > Whether the legacy (`kivy.uix.camera.Camera`) or the new (`SimpleKivy.kvWidgets.Camera`) Camera is used as base.
    > - `False`: Uses SimpleKivy's Camera.
    > - `True`: Uses legacy kivy's Camera.
    > Defaults to `False`.

    {: .prompt-info }
    > When `legacy = False`, requires the `cv2` module to work. install it with `pip install opencv-python`.

    ## Parameters
    
    {common}

    ## Returns
    
    `Camera` widget created dynamically.

    ## Kivy Bases
    
    `Image` or `Camera` (when legacy).

    {base_params}
    '''
    kel=skivify(kvw.Camera,k=k,**kwargs)
    return kel

@skwidget
def Video(source='',k=None,focus_behavior=False,**kwargs):
    '''
    Creates a Video widget dynamically with added functionalities.

    ## Parameters
    
    {common}

    ## Returns
    
    `Video` widget created dynamically.

    ## Kivy Bases
    
    `Video`

    {base_params}
    '''
    from kivy.uix.video import Video as kvWd
    if focus_behavior:
        kvWd=kvb.FocusBehavior,kvWd
    kel=skivify(kvWd,k=k,source=source,**kwargs)
    return kel

@skwidget
def VideoPlayer(source='',k=None,focus_behavior=False,**kwargs):
    '''
    Creates a VideoPlayer widget dynamically with added functionalities.

    ## Parameters
    
    {common}

    ## Returns
    
    `VideoPlayer` widget created dynamically.

    ## Kivy Bases
    
    `VideoPlayer`

    {base_params}
    '''
    from kivy.uix.videoplayer import VideoPlayer as kvWd
    if focus_behavior:
        kvWd=kvb.FocusBehavior,kvWd
    kel=skivify(kvWd,k=k,source=source,**kwargs)
    return kel

@skwidget
def Switch(active=False,k=None,enable_events=True,on_event='active',**kwargs):
    '''
    Creates a Switch widget dynamically with added functionalities.

    ## Parameters
    
    {common}

    ## Returns
    
    `Switch` widget created dynamically.

    ## Kivy Bases
    
    `Switch`

    {base_params}
    '''
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
# @skwidget
def AddDropDown(main_widget,widget_list,on_select=utils.do_nothing,k=None,element_auto_height=True,auto_width=True,width=100,element_height=48,**kwargs):
    # dropdown=kvw.DropDownB(auto_width=auto_width,width=width)
    # dropdown=skivify(kvw.DropDownB,auto_width=auto_width,width=width,k=k,**kwargs)
    DD=extwidget_to_skwidget(kvw.DropDownB)
    
    dropdown=DD(auto_width=auto_width,width=width,k=k,**kwargs)

    main_widget.bind(on_release=dropdown.open)

    setattr(main_widget,'dropdown_widgets',widget_list)
    # setattr(dropdown,'main_widget',widget_list)

    # def btn_select(btn):
        # setattr(dropdown.attach_to,'selected',btn.index)
        # dropdown.select(btn)
        # setattr(dd.attach_to,"selected",btn.index)
        # print(x)
        # dd.select(dd,btn)
    for i,w in enumerate(widget_list):
        setattr(w,'index',i)
        shy=w.size_hint_y
        # print(w,f"{shy = }")
        if shy!=None:
            if element_auto_height:# and w.size_hint_y!=None:
                w.size_hint_y=None
                w.height=element_height
        if hasattr(w,'on_release'):
            # w.bind(on_release=btn_select)
            w.bind(on_release=lambda *x:dropdown.select(*x))
        dropdown.add_widget(w)

    dropdown.bind(on_select=on_select)
    # Clock.schedule_once(lambda dt:get_kvApp().paw())
    return main_widget



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


def AddMenu(main_widget,menu_widget,position_to='mouse',touch_up_buttons="right",menu_close_touch_buttons=("left","right"),on_pre_open=None):
    '''
    widget: Main widget.
    menu_widget: Menu widget that will be attached to the main widget.
    position_behavior: It can be any of ("main","main-center", "mouse").
    '''
    setattr(main_widget,'menu',menu_widget)
    setattr(menu_widget,'_is_menu',True)
    setattr(menu_widget,'menu_parent',main_widget)
    # setattr(widget,'_app',utils.get_kvApp())
    # _app=utils.get_kvApp()
    # setattr(widget,'kvWindow',kvWindow)

    # def _ensure_keyboard(self):
    #     self._keyboard=kvWindow.request_keyboard(
    #         self._keyboard_closed, self, 'text')
        
    # def _keyboard_closed(self):
    #     # print('My keyboard have been closed!')
    #     self._keyboard.unbind(on_key_down=self._on_keyboard_down)
    #     self._keyboard = None
    # def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
    #     print(keycode)
    # widget._ensure_keyboard=types.MethodType(_ensure_keyboard, widget) 
    # widget._keyboard_closed=types.MethodType(_keyboard_closed, widget) 
    # widget._on_keyboard_down=types.MethodType(_on_keyboard_down, widget) 
    # widget._ensure_keyboard()
    
    def on_touch_up(self,touch):
        _app=utils.get_kvApp()
        
        # print(f"{abs_pos = }",)
        # print(dir(touch))
        # for k in dir(touch):
        #     if 'pos' in k:
        #         print('-'*30)
        #         print(k,"=",getattr(touch,k))



        

        if touch.button in touch_up_buttons:
            # print(self.last_touch)
            # touch_abs_pos=touch.to_absolute_pos(*touch.spos,*_app.kvWindow.size,0)
            # self.touch_abs_pos=touch_abs_pos
            # inside = self.collide_point(*self.to_widget(*touch_abs_pos))

            # touch_abs_pos=touch.to_absolute_pos(*touch.spos,*_app.kvWindow.size,0)
            # self.touch_abs_pos=touch_abs_pos
            inside = self.collide_point(*self.to_widget(*_app.kvWindow.mouse_pos))

            # try:
            #     inside = self.collide_point(*self.parent.to_widget(*touch_abs_pos))
            # except:
            #     inside = self.collide_point(*self.to_widget(*touch_abs_pos))
            
            if inside:
                # print('here',inside)
                Clock.unschedule(self.show_menu)
                Clock.schedule_once(self.show_menu)

    def menu_on_touch_up(self,touch):
        if touch.button in menu_close_touch_buttons:
            inside = self.collide_point(*self.parent.to_widget(*touch.pos))
            if inside:
                _app=utils.get_kvApp()
                Clock.unschedule(_app._remove_top_widget)
                Clock.schedule_once(_app._remove_top_widget)
                # Clock.schedule_once(lambda dt:self.close_menu)


    def close_on_window(ins,v):
        # print('close_on')
        _app=utils.get_kvApp()
        _app.kvWindow.unbind(size=close_on_window)
        Clock.schedule_once(_app._remove_top_widget)
        # Clock.schedule_once(lambda dt:main_widget.close_menu())
    
    if isinstance(position_to,str):
        if position_to=='main':
            def show_menu(self,*x):
                if self.on_pre_open(self.menu)==False:
                    return
                _app=utils.get_kvApp()
                
                _app.kvWindow.bind(size=close_on_window)

                lbl=self.menu
                if lbl.size_hint_x==1:
                    lbl.size_hint_max_x=self.width
                ax,ay=self.to_window(*self.pos)
                lbl.x=ax
                lbl.y=ay-lbl.height

                didx=False
                didy=False

                if lbl.y<0:
                    lbl.y=lbl.y+lbl.height+self.height
                    didy=True

                
                if lbl.x+lbl.width>_app.kvWindow.width:
                    didx=True
                    lbl.x=lbl.x-lbl.width+self.width
                if lbl.x<1:
                    lbl.x=1
                _app.add_top_widget(lbl)
        elif position_to=='main-center':
            def show_menu(self,*x):
                if self.on_pre_open(self.menu)==False:
                    return
                _app=utils.get_kvApp()
                
                _app.kvWindow.bind(size=close_on_window)

                lbl=self.menu
                if lbl.size_hint_x==1:
                    lbl.size_hint_max_x=self.width
                ax,ay=self.to_window(*self.pos)
                lbl.x=ax-self.width*.75
                lbl.y=ay-lbl.height

                didx=False
                didy=False

                if lbl.y<0:
                    lbl.y=lbl.y+lbl.height+self.height
                    didy=True

                
                if lbl.x+lbl.width>_app.kvWindow.width:
                    didx=True
                    lbl.x=lbl.x-(_app.kvWindow.width-(lbl.x+lbl.width))-lbl.width+self.width
                if lbl.x<1:
                    lbl.x=1

                _app.add_top_widget(lbl)
        elif position_to in ('side'):
            def show_menu(self,*x):
                if self.on_pre_open(self.menu)==False:
                    return
                _app=utils.get_kvApp()
                
                _app.kvWindow.bind(size=close_on_window)

                lbl=self.menu
                if lbl.size_hint_x==1:
                    lbl.size_hint_max_x=self.width

                ax,ay=self.to_window(*self.pos)
                
                lbl.x=ax+self.width
                
                lbl.y=ay+self.height-lbl.height

                didx=False
                didy=False

                # if lbl.y<0:
                #     lbl.y=lbl.y+lbl.height+self.height
                #     didy=True

                
                if lbl.x+lbl.width>_app.kvWindow.width:
                    didx=True
                    lbl.x=lbl.x-lbl.width-self.width-1
                _app.add_top_widget(lbl)
        elif position_to=='mouse':
            def show_menu(self,*x):
                if self.on_pre_open(self.menu)==False:
                    return
                _app=utils.get_kvApp()
                
                _app.kvWindow.bind(size=close_on_window)

                lbl=self.menu
                if lbl.size_hint_x==1:
                    lbl.size_hint_max_x=self.width
                ax,ay=_app.kvWindow.mouse_pos
                lbl.pos=ax,ay
                didx=False
                didy=False

                if lbl.y+lbl.height>_app.kvWindow.height:
                    lbl.y=lbl.y-lbl.height-16
                    didy=True
                
                if lbl.x+lbl.width>_app.kvWindow.width:
                    lbl.x=lbl.x-lbl.width
                    didx=True
                if didy and not didx:
                    lbl.x=lbl.x+16
                _app.add_top_widget(lbl)
        elif position_to=='over':
            def show_menu(self,*x):
                if self.on_pre_open(self.menu)==False:
                    return
                _app=utils.get_kvApp()
                
                _app.kvWindow.bind(size=close_on_window)

                lbl=self.menu
                
                # lbl.pos=self.to_window(*self.pos)
                # print(self.size)
                # print(self.size_hint)
                lbl.pos=self.pos
                lbl.size_hint=None,None
                lbl.size=self.size
                
                # lbl.size_hint=self.size_hint
                _app.add_top_widget(lbl)
    elif hasattr(position_to,'canvas'):
        def show_menu(self,*x):
            if self.on_pre_open(self.menu)==False:
                return
            _app=utils.get_kvApp()
            
            _app.kvWindow.bind(size=close_on_window)

            lbl=self.menu
            
            # lbl.pos=self.to_window(*self.pos)
            # print(self.size)
            # print(self.size_hint)
            lbl.pos=position_to.pos
            lbl.size_hint=None,None
            lbl.size=position_to.size
            
            # lbl.size_hint=self.size_hint
            _app.add_top_widget(lbl)
    else:
        raise ValueError(f'Invalid value for position_behavior "{position_behavior}". It has to be any of ("main","mouse","parent")')

    


    if on_pre_open:
        main_widget.on_pre_open=types.MethodType(on_pre_open, main_widget)
    else:
        def on_pre_open(self,menu):
            pass
        main_widget.on_pre_open=types.MethodType(on_pre_open, main_widget)
    
    
    main_widget.show_menu=types.MethodType(show_menu, main_widget)
    def close_menu(self):
        _app=utils.get_kvApp()
        _app.kvWindow.unbind(size=close_on_window)
        Clock.schedule_once(_app._remove_top_widget)
    main_widget.close_menu=types.MethodType(close_menu, main_widget)
    main_widget.bind(on_touch_up=on_touch_up)
    main_widget.menu.bind(on_touch_up=menu_on_touch_up)


    return main_widget

def AddSubMenu(main_widget,menu_widget,on_pre_open=None):
    '''
    widget: Main widget.
    menu_widget: Menu widget that will be attached to the main widget.
    position_behavior: It can be any of ("main", "mouse","parent").
    '''
    setattr(main_widget,'menu',menu_widget)
    setattr(main_widget,'_main_menu',None)

    def get_main_menu(self):
        if self._main_menu:
            return self._main_menu
        elif getattr(self,'_is_menu',False):
            self._main_menu=self
            return self
        else:
            cw=self.parent
            for i in range(50):
                # print(cw)
                if getattr(cw,'_is_menu',False):
                    self._main_menu=cw
                    return self._main_menu
                else:
                    cw=cw.parent


    def on_enter(self):
        # print('on_enter')
        _app=utils.get_kvApp()
        Clock.unschedule(self.show_menu)
        Clock.schedule_once(self.show_menu)
    def menu_on_touch_up(self,touch):
        if touch.button in ('left','right'):
            inside = self.collide_point(*self.parent.to_widget(*touch.pos))
            if inside:
                _app=utils.get_kvApp()
                Clock.unschedule(_app._remove_subtop_widget)
                Clock.schedule_once(_app._remove_subtop_widget)
                Clock.unschedule(_app._remove_top_widget)
                Clock.schedule_once(_app._remove_top_widget)


    def close_on_window(ins,v):
        if v==None:
            _app=utils.get_kvApp()
            _app.kvWindow.unbind(size=close_on_window)
            _app.unbind(top_widget=close_on_window)
            Clock.schedule_once(_app._remove_subtop_widget)
    # def on_leave(self):
    #     _app=utils.get_kvApp()
    #     _app.kvWindow.unbind(size=close_on_window)
    #     _app.unbind(top_widget=close_on_window)
    #     Clock.schedule_once(_app._remove_subtop_widget)


    def show_menu(self,*x):
        if self.on_pre_open(self.menu)==False:
            return
        _app=utils.get_kvApp()
        
        _app.kvWindow.bind(size=close_on_window)
        _app.bind(top_widget=close_on_window)

        lbl=self.menu
        ax,ay=self.to_window(*self.pos)


        # print(self.parent,getattr(self.parent,'text','none'))
        # print('self',getattr(self,'menu','None'))
        # print('self.parent',getattr(self.parent,'menu','None'))

        # print(f"{getattr(self,'_is_menu',False) = }")

        # pax,pay=ax,ay
        # pax,pay=self.to_window(*self.parent.pos)
        # pax,pay=self.to_window(*self.menu._main.pos)

        # print(self.get_main_menu())
        
        self.get_main_menu()
        pax,pay=self.to_window(*self._main_menu.pos)
        

        # print(self,self.get_main_menu())
        # print(self.pos,self.get_main_menu().pos)
        
        lbl.x=pax+self._main_menu.width


        
        lbl.y=ay+self.height-lbl.height

        didx=False
        didy=False
        
        if lbl.x+lbl.width>_app.kvWindow.width:
            didx=True
            lbl.x=lbl.x-lbl.width-self._main_menu.width-1
        # print(lbl.x)
        _app.add_subtop_widget(lbl)

    if on_pre_open:
        main_widget.on_pre_open=types.MethodType(on_pre_open, main_widget)
    else:
        def on_pre_open(self,menu):
            pass
        main_widget.on_pre_open=types.MethodType(on_pre_open, main_widget)
    
    main_widget.show_menu=types.MethodType(show_menu, main_widget)
    main_widget.get_main_menu=types.MethodType(get_main_menu, main_widget)
    # Clock.schedule_once(main_widget.set_main_menu)
    # main_widget.bind(parent=main_widget.set_main_menu)


    main_widget.bind(on_enter=on_enter,
        # on_leave=on_leave
        )
    main_widget.menu.bind(on_touch_up=menu_on_touch_up)

    def close_menu(self):
        _app=utils.get_kvApp()
        _app.kvWindow.unbind(size=close_on_window)
        Clock.schedule_once(_app._remove_top_widget)
    main_widget.close_menu=types.MethodType(close_menu, main_widget)

    return main_widget


@skwidget
def ModalView(content=None,k=None,enable_events=False,on_event='on_pre_open',**kwargs):
    '''
    Creates and fills a ModalView widget dynamically with added functionalities.

    ## Parameters
    
    `widgets: list, Widget`
    > Widget instance or list of widgets to be added dynamically.
    > - `Widget`: Adds the widget as child.
    > - `[Widget, Widget, ...]`: Adds each Widget in the list as child.

    {common}

    ## Returns
    
    `ModalView` widget created dynamically.

    ## Kivy Bases
    
    `ModalView`

    {base_params}
    '''
    from kivy.uix.modalview import ModalView as wid
    kel=skivify_v2(wid,k=k,enable_events=enable_events,on_event=on_event,**kwargs)
    if isinstance(content,(list,tuple)):
        for w in content:
            # size_hint_y=getattr(w,'size_hint_y',None)
            # if size_hint_y!=None:
            #     w.size_hint_y=None
            #     w.height=44
            kel.add_widget(w)
    else:
        if content:
            kel.add_widget(content)
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
    bar_color=[.6, .6, .6, .9],
    bar_inactive_color=[.6, .6, .6, .6],
    bar_width=8,
    **kwargs):
    '''
    Creates a ComboBox widget (editable TextInput with a DropDown of values to choose from).

    ## Dynamic Creation Parameters
    
    `flat: bool`
    > Whether the dropdown button will have a flat style (see `FlatButton`):
    > - `False`: Classic kivy widget style.
    > - `True`: A `FlatButton` is used as the dropdown button.
    > Default is False.

    `dark: bool`
    > Whether the textinput will have a dark style (see `TextInputDark`):
    > - `False`: Classic kivy widget style.
    > - `True`: A `TextInputDark` widget is used as the textinput.
    > Default is `False`.

    ## Parameters
    
    `text: str`
    > Text value shown when created.
    > - `str`: Text string.
    > Default is `"choice0"`


    `hint_text: str`
    > Hint text of the widget. Shown if `text` is empty.
    > - `str`: Text string.

    `focus: bool`
    > Wheter widget has focus in the textinput area when created.
    > - `True`: TextInput is focused when created.
    > - `False`: TextInput is not focused when created.
    > Default is `False`

    `values: list or sequence`
    > A sequence where each element is a string representing the value choices.
    > - `[str, str, ...]`: List of strings.
    > Default value is `('choice0', 'choice1')`
    
    {size_behavior}
    
    {common}

    ## Returns
    
    `ComboBox` widget created dynamically with the following modifications:
    
    ## Properties
    
    `text (StringProperty)`
    `values (ListProperty)`
    `focus (AliasProperty)`

    ## Events
    
    `on_values(ins,val)`: Fired when changing the `values` property.

    ## Kivy Bases
    
    - `BoxLayout`
        - `TextInput`
        - `Button`

    {base_params}
    '''

    dd=DropDown(k=NOTKEY,bar_color=bar_color,bar_width=bar_width,bar_inactive_color=bar_inactive_color)
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
    kel=skivify( Boxtext,k=k,enable_events=enable_events,on_event=on_event, text=tin.text,values=values,**kwargs)
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
def DatePicker(k=None,year=2020,month=1,**kwargs):
    '''
    Creates a DatePicker widget.

    ## Parameters
    
    `year (int)`: Initial year. Defaults to `2020`.
    `month (int)`: Initial month (1-12) -> (Jan-Dec). Defaults to `1`.
    
    {size_behavior}
    
    {common}

    ## Returns
    
    `WIDGET` widget created dynamically.
    
    ## Properties
    
    `picked (list)`: List of 3 strings `["{year}", "{month}", "{day}"]` containing the last date selected. Defaults to `["", "", ""]`.
    `months (list)`: List of month names `["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]`.

    ## Kivy Bases
    
    `BoxLayout`

    {base_params}
    '''

    kel=skivify(kvw.DatePicker,year=year,month=month,k=k,**kwargs)
    return kel

Calendar=DatePicker

# @skwidget
# def ComboBox(
#     text='choice0',
#     values=('choice0', 'choice1', 'choice2', 'choice3'),k=None,):
    


@skwidget
def JoinLabel(texts=['text1','text2','text3'],k=None,focus_behavior=False,**kwargs):
    # kwargs=_preprocess(**kwargs)
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


    kel=skivify(_,texts=texts,**kwargs)


    
    kel.id=k

    kel.post='LabelLike'

    # _future_elements.append(kel)
    return kel

T=Text=Label

# @skwidget
# def ScrollLabel(text='',k=None,focus_behavior=False,**kwargs):
#     # kwargs=_preprocess(**kwargs)
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
    # kwargs=_preprocess(**kwargs)
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
def Boxit(*widgets,k=NOTKEY,base_cls=None,**kwargs):
    '''
    Dynamic layout constructor. The type of layout is specified by `base_cls`.

    ## Dynamic Creation Parameters
    
    `base_cls: WidgetType`
    > Widget class to use as base for the constructor:
    > Default is `None`, which sets `SimpleKivy.kvWidgets.BoxlayoutB` as the base class for the layout constructor.

    ## Parameters
    
    {widgets}

    {common}

    ## Returns
    
    Widget instance of type defined by `base_cls` with `*widgets` as children.

    ## Kivy Bases
    
    Depends on `base_cls`.

    {base_params}
    '''
    # kwargs=_preprocess(**kwargs)
    if base_cls==None:
        kvWd=kvw.BoxLayoutB
    else:
        kvWd=base_cls
    kel=skivify(kvWd,k=k,**kwargs)

    # kel.id=k

    for w in widgets:
        kel.add_widget(w)
    # _future_elements.append(kel)
    return kel



@skwidget
def Splitter(widget=None,k=None,sizable_from = 'right',**kwargs):
    from kivy.uix.splitter import Splitter as kvWd
    kel=skivify(kvWd,k=k,sizable_from=sizable_from,**kwargs)
    if widget:
        kel.add_widget(widget)
    return kel

@skwidget
def BoxitH(*widgets,k=NOTKEY,orientation='horizontal',**kwargs):
    '''
    Dynamic `BoxLayout` constructor with `orientation = "horizontal"` set as default.

    ## Parameters
    
    {widgets}

    {common}

    {bgline}

    ## Returns
    
    `BoxLayout` created dynamically with `*widgets` added as children during creation.

    ## Kivy Bases
    
    `BoxLayout`

    {base_params}
    '''

    # kwargs=_preprocess(**kwargs)
    kel=skivify_v2(kvw.BoxLayoutB,k=k,orientation=orientation,**kwargs)

    # kel.id=k

    for w in widgets:
        kel.add_widget(w)

    
    setattr(kel,'_isbox',kel.orientation)
    # _future_elements.append(kel)
    return kel

@skwidget
def GradientBoxit(*widgets,gradient=["linear-gradient",dict(colors=['#0E0A0A','#E87322'])],orientation='horizontal',k=NOTKEY,**kwargs):
    '''
    Dynamic `BoxLayout` constructor with `orientation = "horizontal"` set as default.

    ## Parameters
    
    {widgets}

    {common}

    {bgline}

    ## Returns
    
    `BoxLayout` created dynamically with `*widgets` added as children during creation.

    ## Kivy Bases
    
    `BoxLayout`

    {base_params}
    '''
    from .kvGradient import GradientBox as kvWd
    kel=skivify(kvWd,gradient=gradient,k=k,orientation=orientation,**kwargs)

    for w in widgets:
        kel.add_widget(w)
    setattr(kel,'_isbox',kel.orientation)
    return kel

@skwidget
def GradientBoxitV(*widgets,gradient=["linear-gradient",dict(colors=['#0E0A0A','#E87322'])],orientation='vertical',k=NOTKEY,**kwargs):
    '''
    Dynamic `BoxLayout` constructor with `orientation = "horizontal"` set as default.

    ## Parameters
    
    {widgets}

    {common}

    {bgline}

    ## Returns
    
    `BoxLayout` created dynamically with `*widgets` added as children during creation.

    ## Kivy Bases
    
    `BoxLayout`

    {base_params}
    '''
    from .kvGradient import GradientBox as kvWd
    kel=skivify(kvWd,gradient=gradient,k=k,orientation=orientation,**kwargs)

    for w in widgets:
        kel.add_widget(w)
    setattr(kel,'_isbox',kel.orientation)
    return kel

@skwidget
def Frame(title='Frame',*widgets,k=None,orientation='vertical',
    label_args={},
    **kwargs):
    '''
    Dynamic `WIDGET` constructor.

    ## Parameters

    `title (str)`: Frame title, must be the first argument.
    
    {widgets}

    {common}

    {line}

    - `lcolor`: Defaults to `[.5,.5,.5,1]`.
    - `lwidth`: Defaults to `1`.

    `orientation (OptionProperty)`: Inner BoxLayout orientation. Must be one of `("horizontal", "vertical")`. Defaults to `"vertical"`.

    `label_args (dict)`: Properties of the title `Label`. See {url_Label}. Defaults to `{}`. `label_args` Updates the default properties: `dict(size='y22',size_behavior='texth',padding=[6,0,6,0],pos_hint={'top':1},x=15)`.

    ## Returns
    
    `WIDGET` created dynamically with `*widgets` added as children during creation.

    ## Kivy Bases
    
    - `RelativeLayout`
        - `Label`
        - `BoxLayout`

    {base_params}
    '''

    # kwargs=_preprocess(**kwargs)
    lcolor=kwargs.pop('lcolor',[.5,.5,.5,1])
    lwidth=kwargs.pop('lwidth',1)
    class kvWd(kvw.RelativeLayout):
        lcolor=kvw.ColorProperty([.5,.5,.5,1])
        lwidth=kvw.NumericProperty(1)

        label_args=kvw.ObjectProperty({})

        def __init__(self, **kwargs):
            # kwargs['bcolor']=resolve_color(kwargs.get('bcolor',self.bcolor))
            # kwargs['lcolor']=resolve_color(kwargs.get('lcolor',self.lcolor))
            # print(self.lcolor)
            super(kvWd, self).__init__(**kwargs)

            Clock.schedule_once(self._init)

        def _update_label_args(self,instance,value):
            for k,v in value.items():
                setattr(self.lbl,k,v)

        def _update_lcolor(self, instance, value):
            """Update line color"""
            # self.line_color.rgba = resolve_color( value)
            self.line_color.rgba = value
    
        def _update_lwidth(self, instance, value):
            """Update line width"""
            self.line.width = value

        def _update_canvas(self, *args):
            try:
                self.box.size_hint=(None,None)
                self.box.width=self.width-self.lbl.height
                self.box.height=self.height-self.lbl.height-self.lbl.height/2
                self.box.x=self.lbl.height/2
                self.box.y=self.lbl.height/2
                # self.box.pos=self.to_parent(self.lbl.height/2,self.lbl.height/2)

                self.line.points=[
                        *self.to_parent(self.lbl.x+self.lbl.width, self.height-self.lbl.height/2),
                        *self.to_parent(self.width, self.height-self.lbl.height/2),
                        *self.to_parent(self.width, 0),
                        *self.to_parent(0, 0),
                        *self.to_parent(0, self.height-self.lbl.height/2),
                        *self.to_parent(self.lbl.x, self.height-self.lbl.height/2),
                        ]
            except:
                pass
        def _init(self,dt):
            self.box.size_hint=(None,None)
            self.box.width=self.width-self.lbl.height
            self.box.height=self.height-self.lbl.height-self.lbl.height/2
            self.box.x=self.lbl.height/2
            self.box.y=self.lbl.height/2

            with self.canvas.after:
                self.line_color=kvw.Color(rgba=self.lcolor)
                self.line=kvw.Line(points=[
                    *self.to_parent(self.lbl.x+self.lbl.width, self.height-self.lbl.height/2),
                    *self.to_parent(self.width, self.height-self.lbl.height/2),
                    *self.to_parent(self.width, 0),
                    *self.to_parent(0, 0),
                    *self.to_parent(0, self.height-self.lbl.height/2),
                    *self.to_parent(self.lbl.x, self.height-self.lbl.height/2),
                    ],
                    joint='miter',
                    cap='square',
                    width=1)
            # lcolor=self._update_lcolor,
            self.bind(
                lcolor=self._update_lcolor,
                lwidth=self._update_lwidth,
                label_args=self._update_label_args,
            )


    kel=skivify_v2(kvWd,k=k,lcolor=lcolor)

    default_lbl_args=dict(size='y22',size_behavior='texth',padding=[6,0,6,0],pos_hint={'top':1},x=15)
    default_lbl_args.update(label_args)

    kel.lbl=Label(title,k=NOTKEY,**default_lbl_args)
    kel.box=BoxitH(*widgets,k=NOTKEY,orientation=orientation,
        # padding=[kel.lbl.height/2,0,kel.lbl.height/2,kel.lbl.height/2],
        **kwargs)
    kel.add_widget(kel.lbl)
    kel.add_widget(kel.box)
    
    

    # def _init(self,dt):
    #     self.box.size_hint=(None,None)
    #     self.box.width=self.width
    #     self.box.height=self.height-self.lbl.height
    #     # self.box.pos=self.to_parent(15,15)

    #     with self.canvas.after:
    #         self.line_color=kvw.Color(rgba=self.lcolor)
    #         self.line=kvw.Line(points=[
    #             *self.to_parent(self.lbl.x+self.lbl.width, self.height-self.lbl.height/2),
    #             *self.to_parent(self.width, self.height-self.lbl.height/2),
    #             *self.to_parent(self.width, 0),
    #             *self.to_parent(0, 0),
    #             *self.to_parent(0, self.height-self.lbl.height/2),
    #             *self.to_parent(self.lbl.x, self.height-self.lbl.height/2),
    #             ],
    #             width=1)
    #     # lcolor=self._update_lcolor,
    #     self.bind(lcolor=self._update_lcolor,
    #         lwidth=self._update_lwidth
    #     )

    # kel._init=types.MethodType(_init,kel)
    # Clock.schedule_once(kel._init) 
    # kel._init(0)       
    # kel._update_canvas=types.MethodType(_update_canvas,kel)
    # kel.add_widget=types.MethodType(kel.box.add_widget,kel)
    kel.add_widget=kel.box.add_widget
    kel.remove_widget=kel.box.remove_widget
    
    kel.bind(
            pos=kel._update_canvas,
            size=kel._update_canvas,
            # bcolor=self._update_bcolor,
            # lcolor=self._update_lcolor,
            # lwidth=self._update_lwidth
        )
    kel.lbl.bind(
        pos=kel._update_canvas,
        size=kel._update_canvas
        )


    return kel

@skwidget
def LabelCheck(text='checkbox',active=False,halign='left',valign='middle',enable_events=False,on_event='active',cwidth=40,k=None,**kwargs):
    '''
    Creates a LabelCheck widget dynamically with added functionalities.

    ## Parameters
    
    `text (str)`: Text value shown when created. Default is `"checkbox"`.

    `halign (str)`: Horizontal text alignment. It can be one of `"left", "center", "right"`. Default is `"left"`.

    `valign (str)`: Vertical text alignment. It can be one of `"top", "middle", "bottom"`. Default is `"middle"`.

    `active (bool)`: Checkbox state. Default is `False`.

    `cwidth (int)`: Width of the checkbox. Default is `40`

    {common}

    ## Returns
    
    `WIDGET` widget created dynamically.

    ## Kivy Bases
    
    - `BoxLayout`
        - `Label`
        - `CheckBox`

    {base_params}
    '''
    kel=skivify(kvw.LabelCheck,text=text,active=active,cwidth=cwidth,k=k,halign=halign,valign=valign,enable_events=enable_events,on_event=on_event,**kwargs)
    return kel
    

@skwidget
def HoverBoxit(*widgets,k=None,enable_events=True,hover_highlight=False,do_dot_subevent=True,on_event=('on_enter','on_leave'),**kwargs):
    '''
    Dynamic `BoxLayout` constructor.

    ## Dynamic Creation Parameters
    
    {hover_highlight}

    ## Parameters
    
    {widgets}

    {common}

    {bgline}

    ## Returns
    
    `BoxLayout` created dynamically with `*widgets` added as children during creation.

    ## Kivy Bases
    
    `BoxLayout`

    {base_params}

    ## Properties

    ## Events
    
    {when_hover_highlight}
    '''

    # kwargs=_preprocess(**kwargs)
    # kvWd=kvw.BoxLayoutB
    if hover_highlight:
        class kvWd(kvb.HoverHighlightBehavior,kvw.BoxLayoutB):
            pass
        
    else:
        class kvWd(kvb.HoverBehavior,kvw.BoxLayoutB):
            pass

    # kel=kvWd(orientation=orientation,**kwargs)
    kel=skivify(kvWd,k=k,enable_events=enable_events,do_dot_subevent=do_dot_subevent,on_event=on_event,**kwargs)


    # kel.id=k

    for w in widgets:
        kel.add_widget(w)

    

    # _future_elements.append(kel)
    return kel

@skwidget
def Grid(layout=[[]],k=NOTKEY,navigation_behavior=False,**kwargs):
    '''
    Dynamic `GridLayout` constructor.

    ## Dynamic Creation Parameters
    
    {grid_navigation_behavior}

    ## Parameters
    
    {layout}

    {common}

    {bgline}

    ## Returns
    
    `GridLayout` created dynamically with `layout` widgets added as children during creation.

    ## Kivy Bases
    
    `GridLayout`

    {base_params}
    '''
    # kwargs=_preprocess(**kwargs)

    
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

    setattr(kel,'_isbox','grid')

    return kel

@skwidget
def GradientGrid(layout=[[]],k=NOTKEY,navigation_behavior=False,**kwargs):
    '''
    Dynamic `GridLayout` constructor.

    ## Dynamic Creation Parameters
    
    {grid_navigation_behavior}

    ## Parameters
    
    {layout}

    {common}

    {bgline}

    ## Returns
    
    `GridLayout` created dynamically with `layout` widgets added as children during creation.

    ## Kivy Bases
    
    `GridLayout`

    {base_params}
    '''
    # kwargs=_preprocess(**kwargs)

    from .kvGradient import GradientGrid as kvGradientGrid
    if navigation_behavior:
        class kvWd(kvGradientGrid,kvb.GridNavigationBehavior):
            pass
    else:
        kvWd=kvw.kvGradientGrid
    

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

    setattr(kel,'_isbox','grid')

    return kel

_web_started=False
@skwidget
def WebView(url="https://www.google.com",k=None,
    orientation='horizontal',
    **kwargs):
    '''
    Attempt of a WebView widget. Attaches an internet browser window to the current kivy window. Depends on `pywebview`. It's like runing your program alongside an internet browser.
    In essence, it is an external window that follows an empty BoxLayout and changes the window being focused when entering and leaving the box with the mouse.

    {: .prompt-warning }
    > Experimental. **Windows only**. Expect window flickering. You cannot show any widget on top of the `WebView` widget.


    ## Parameters
    
    `url (str)`: Initial url of the web window. Defaults to `"https://www.google.com"`.

    {common}

    {bgline}

    ## Returns
    
    `WebView` created dynamically.

    ## Kivy Bases
    
    `BoxLayout`

    `window (webview.Window)`: Represents a window that hosts the webview. Visit [pywebview's documentation](https://pywebview.flowrl.com/) for more information.

    {base_params}

    ## Events
    
    {events_hover}
    '''
    
    
    # from . import webview
    from .webview_enhance import enhance
    try:
        import sk_webview as webview
    except:
        import webview
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





    kel=skivify(kvWd,k=k,
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
def External(title="",hwnd=None,k=None,
    **kwargs):
    '''
    Attaches an external window to the current kivy window. It's like runing your program alongside another program.
    In essence, it is an external window that follows an empty BoxLayout and changes the window being focused when entering and leaving the box with the mouse.

    {: .prompt-warning }
    > Experimental. **Windows only**. Expect window flickering. You cannot show any widget on top of the `External` widget.


    ## Parameters
    
    `hwnd: int, None`: 
    > Windows' `hwnd` of a program to be attached to your window. Defaults to `None`
    > - `int`: External program's `hwnd` id.
    > - `None`: The `title` parameter will be used instead to find the external window.
    > Default is `None`.

    `title (str)`: External window title. Used to find the external window when `hwnd` value is `None`. Default is `"External window title"`

    {common}

    {bgline}

    ## Returns
    
    `WIDGET` widget created dynamically.

    ## Kivy Bases
    
    `BoxLayout`

    `ewin (Simplekivy.Native.ExternalWindow)`: Manages changes on the box and keeps the external program on top of it.

    {base_params}

    ## Events
    
    {events_hover}
    '''
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
        def attach(self,hwnd=None,title=None):
            self.hwnd=hwnd
            self.title=title
        def _attach(self):
            _app=App.get_running_app()
            while not self.hwnd and not self.title:
                _app.sleep_in_thread(1/30)
            if self.hwnd==None:
                self.hwnd=find_hwnd_by_title(self.title)

            print('attaching:',self.hwnd)
            
            self.ewin = ExternalWindow(self.hwnd)
            
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
    
@_widget_ctor
def TitlebarCloseButton(markup=True,k=NOTKEY,size="x44",hover_highlight=True,lcolor='',bcolor_down='red',**kwargs):
    kel= FlatButton(text=kwargs.pop('text',mdi('window-close')),
        markup=markup,k=k,size=size,lcolor=lcolor,hover_highlight=hover_highlight,bcolor_down=bcolor_down,
            **kwargs
        )

    def onc(*l):
        self=App.get_running_app()
        # self.trigger_event('__Close__')
        Clock.schedule_once(lambda dt:self.close())

    kel.bind( on_release=onc)

    return kel

@_widget_ctor
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

@_widget_ctor
def TitlebarMinimizeButton(markup=True,k=NOTKEY,size="x44",lcolor='',hover_highlight=True,bcolor_down='gray',**kwargs):
    kel=FlatButton(text=kwargs.pop('text',mdi('window-minimize')),
        markup=markup,k=k,size=size,lcolor=lcolor,hover_highlight=hover_highlight,bcolor_down=bcolor_down,
        **kwargs
        )
    kel.bind(  on_release=lambda *l: App.get_running_app().minimize()   )
    
    return kel

@_widget_ctor
def TitlebarTitle(k=NOTKEY,padding=[8,0],halign='left',**kwargs):
    kel=LargeText(k=k,padding=padding,halign=halign,font_size=kwargs.pop("font_size",12),**kwargs)

    def on_run(dt):
        self=App.get_running_app()
        kel.text=self.title
        self.bind(title=lambda inst,val:setattr(kel,'text',val))

    Clock.schedule_once(on_run)

    return kel

@_widget_ctor
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
def Titlebar(k='titlebar',padding=[4,4],orientation='horizontal',**kwargs):
    '''
    Example of a custom titlebar.
    Must be the first widget in the `layout` and `custom_titlebar = True` when creating the app.
    Set a `size` and `size_hint` because by default it doesn't have one.

    ## SimpleKivy Bases
    `TitlebarIcon, TitlebarTitle, Fill, MinimizeButton, RestoreButton, CloseButton`

    ## Kivy Bases
    `Boxlayout`
    '''

    # size=kwargs.pop('size','y32')
    kwargs=_preprocess(**kwargs)
    kel=skivify(kvw.BoxLayoutB,k=k,orientation=orientation,padding=padding,**kwargs)

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

# Boxit=BoxitH
@skwidget
def Pageit(*widgets,k=None,**kwargs):
    '''
    Dynamic `PageLayout` constructor.

    ## Parameters
    
    {widgets}

    {common}

    {bgline}

    ## Returns
    
    `PageLayout` created dynamically with `*widgets` added as children during creation.

    ## Kivy Bases
    
    `PageLayout`

    {base_params}
    '''

    kel=skivify(kvw.PageLayoutB,k=k,**kwargs)
    # kel.id=k
    for w in widgets:
        kel.add_widget(w)
    return kel
@skwidget
def BoxitV(*widgets,k=NOTKEY,orientation='vertical',**kwargs):
    '''
    Dynamic `BoxLayout` constructor with `orientation = "vertical"` set as default.

    ## Parameters
    
    {widgets}

    {common}

    {bgline}

    ## Returns
    
    `BoxLayout` created dynamically with `*widgets` added as children during creation.

    ## Kivy Bases
    
    `BoxLayout`

    {base_params}
    '''
    kel=skivify(kvw.BoxLayoutB,k=k,orientation=orientation,**kwargs)

    # kel.id=k

    for w in widgets:
        kel.add_widget(w)

    setattr(kel,'_isbox',kel.orientation)
    # _future_elements.append(kel)
    return kel

@skwidget
def Stackit(*widgets,k=None,orientation='lr-tb',**kwargs):
    '''
    Dynamic `StackLayout` constructor.

    ## Parameters
    
    {widgets}

    {common}

    {bgline}

    ## Returns
    
    `StackLayout` created dynamically with `*widgets` added as children during creation.

    ## Kivy Bases
    
    `StackLayout`

    {base_params}
    '''
    kel=skivify_v2(kvw.StackLayoutB,k=k,orientation=orientation,**kwargs)

    for w in widgets:
        kel.add_widget(w)
    return kel

@skwidget
def Relativeit(*widgets,k=NOTKEY,**kwargs):
    '''
    Dynamic `RelativeLayout` constructor.

    ## Parameters
    
    {widgets}

    {common}

    {bgline}

    ## Returns
    
    `RelativeLayout` created dynamically with `*widgets` added as children during creation.

    ## Kivy Bases
    
    `RelativeLayout`

    {base_params}
    '''
    kel=skivify_v2(kvw.RelativeLayoutB,k=k,**kwargs)

    for w in widgets:
        kel.add_widget(w,index=-1)
    return kel
@skwidget
def GradientRelativeit(*widgets,k=NOTKEY,**kwargs):
    '''
    Dynamic `RelativeLayout` constructor.

    ## Parameters
    
    {widgets}

    {common}

    {bgline}

    ## Returns
    
    `RelativeLayout` created dynamically with `*widgets` added as children during creation.

    ## Kivy Bases
    
    `RelativeLayout`

    {base_params}
    '''
    from .kvGradient import GradientRelative as kvWd
    kel=skivify_v2(kvWd,k=k,**kwargs)

    for w in widgets:
        kel.add_widget(w,index=-1)
    return kel

@skwidget
def Floatit(*widgets,k=NOTKEY,**kwargs):
    '''
    Dynamic `FloatLayout` constructor.

    ## Parameters
    
    {widgets}

    {common}

    {bgline}

    ## Returns
    
    `FloatLayout` created dynamically with `*widgets` added as children during creation.

    ## Kivy Bases
    
    `FloatLayout`

    {base_params}
    '''
    kel=skivify_v2((kvw.BgLine,kvw.FloatLayout),k=k,**kwargs)

    for w in widgets:
        kel.add_widget(w,index=-1)
    return kel

@skwidget
def RoundRelativeit(*widgets,k=None,**kwargs):
    '''
    Dynamic `RelativeLayout` constructor with rounded corners for the border line and background color.

    ## Parameters
    
    {widgets}

    {bgline}

    {rounded}

    {common}

    ## Returns
    
    `RelativeLayout` created dynamically with `*widgets` added as children during creation.

    ## Kivy Bases
    
    `RelativeLayout`

    {base_params}
    '''
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
    '''
    Dynamic `RelativeLayout` constructor with ButtonBehavior and rounded corners for the border line and background color.

    ## Parameters
    
    {widgets}

    {bgline}

    {rounded}

    {common}

    ## Returns
    
    `RelativeLayout` created dynamically with `*widgets` added as children during creation.

    ## Kivy Bases
    
    `RelativeLayout`

    {base_params}

    ## Properties

    ## Events

    {when_hover_highlight}
    '''
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
def Scatterit(*widgets,k=NOTKEY,**kwargs):
    '''
    Dynamic `ScatterLayout` constructor.

    ## Parameters
    
    {widgets}

    {common}

    ## Returns
    
    `ScatterLayout` created dynamically with `*widgets` added as children during creation.

    ## Kivy Bases
    
    `ScatterLayout`

    {base_params}
    '''
    # kwargs=_preprocess(**kwargs)

    from kivy.uix.scatterlayout import ScatterLayout as kvWd

    kel=skivify_v2(kvWd,k=k,**kwargs)

    for w in widgets:
        kel.add_widget(w)

    # _future_elements.append(kel)
    return kel
# Scatterit=Boxit_scatter

@skwidget
def ButtonBoxitAngle(*widgets,k=None,angle=0,enable_events=True,on_event="on_release",focus_behavior=False,**kwargs):
    '''
    Creates a `WIDGET` widget with `ButtonBehavior` and rotated contents dynamically with added functionalities.

    ## Dynamic Creation Parameters

    {focus_behavior}
    > Default is False.
    

    ## Parameters

    `angle (int or float)`: Angle of rotation of the box contents. Defaults to 0.
    
    {bgline_state}

    {common}

    ## Returns
    
    `WIDGET` widget created dynamically.

    ## Kivy Bases
    
    `BoxLayout`

    {base_params}
    
    ## Properties

    {button_properties}

    ## Events
    
    {events_button}
    '''

    kvWd=kvw.AngleBBoxLayout

    if focus_behavior:
        class nkvWd(kvb.FocusBehavior,kvWd):
            pass
        kvWd=nkvWd

    kel=skivify_v2(kvWd,k=k,angle=angle,enable_events=True,on_event=on_event,**kwargs)

    for w in widgets:
        kel.add_widget(w)

    # _future_elements.append(kel)

    # kel.size=kwargs.get('size',(100,100))
    # kel.size_hint=kwargs.get('size',(1,1))

    return kel
# ButtonBoxitAngle=Boxit_angle_bbox

@skwidget
def BoxitAngle(*widgets,k=NOTKEY,angle=0,enable_events=False,on_event="on_release",**kwargs):
    # kwargs=_preprocess(**kwargs)

    kvWd=kvw.AngleBoxLayout

    kel=skivify_v2(kvWd,k=k,angle=angle,enable_events=enable_events,on_event=on_event,**kwargs)

    for w in widgets:
        kel.add_widget(w)

    # _future_elements.append(kel)

    # kel.size=kwargs.get('size',(100,100))
    # kel.size_hint=kwargs.get('size',(1,1))
    return kel

@skwidget
def StripLayout(*widgets,k=NOTKEY,rows=1,**kwargs):
    # kwargs=_preprocess(**kwargs)

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
    # kwargs=_preprocess(**kwargs)

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
def Tab2(panels={},
        k=None,
        tab_pos = 'top_left',
        do_default_tab=False,
        head_label_args={'size_behavior':'texth','padding':[16,0,16,0],'lcolor':'gray'},
        content_box_args={'lcolor':'gray','padding':4},
        strip_args={'bcolor':[.2, .64, .8, 1],'pos_hint':{'bottom':0}},
        **kwargs
        ):
    '''
    Dynamic `WIDGET` widget constructor. An enhanced version of the `Tab` widget with a modern look.

    ## Parameters
    
    `panels: dict`
    > Defines the content of the tabbed panel.
    > - `{"{tab_name}": Widget, ...}`: For each `key: value` pair, a TabbedPanelItem is created with `text = "{tab_name}"` and Widget added as child. Each TabbedPanelItem created is added as child to the main TabbedPanel widget.
    > Defaults to `{}`.

    > Example:
    ```py
    sk.WIDGET(
            panels={
                "Header1": sk.Label('First tab content'),
                "Header2": sk.Button('Second tab content')
            }
        )
    ```

    `head_label_args: dict`
    > Defines the properties of the headers, which are created as `sk.Label(text = "{tab_name}", k = sk.NOTKEY, **head_label_args)`.
    > - `{"{prop_name}": prop_value, ...}`: Dictionary of properties.
    > Defaults to `{'size_behavior': 'texth', 'padding': [16,0,16,0], 'lcolor': 'gray'}`.

    `content_box_args: dict`
    > Defines the properties of the the content box, which is created as a `SimpleKivy.kvWidgets.BoxLayoutB(**content_box_args)` widget.
    > - `{"{prop_name}": prop_value, ...}`: Dictionary of properties.
    > Defaults to `{'lcolor': 'gray', 'padding': 4}`.

    {common}

    ## Returns
    
    New `TabbedPanel-like` widget created dynamically with `panels` processed as displayed content during creation.

    ## Kivy Bases
    
    `TabbedPanel`
    
    `current: (str)`: `Text value of the current tab selected. Setting this property changes the current tab.

    {base_params}
    '''
    # kel=kvw.BoxLayoutB(orientation="vertical",**kwargs)

    class kvWd(kvw.RelativeLayout):
        # orientation=kvw.OptionProperty("vertical",options=("vertical","horizontal")):
        panels=kvw.ObjectProperty({})
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
            # self.bind(panels=lambda ins,val:setattr(self._headbox,'width',len(val)))
            # self.bind(panels=lambda ins,val:Clock.schedule_once())
            # self.setter('panels')(self,self.panels)
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

            # print(self.panels)
            self._sman=Screens(self.panels,k=NOTKEY,transition='no')
            self.content_box.add_widget(self._sman)
            self.bind(size=self._up_bbox_posV)

            
            ik=-1
            group_id=id(self)
            self.headers={}
            self._strip_color=strip_args.get('bcolor',[.2, .64, .8, 0])
            head_lcolor=head_label_args.pop('lcolor','gray')
            for k,v in self.panels.items():
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
    kel=skivify_v2(kvWd,tab_pos=tab_pos,do_default_tab=do_default_tab,panels=panels,k=k,**kwargs)
    return kel






#     # kel.id=k

#     kel=skivify_v2(kvWd,k=k,panels=panels,tab_pos=tab_pos,do_default_tab=do_default_tab,**kwargs)

#     # _future_elements.append(kel)
#     return kel



@skwidget
def Tab(
            panels={},
            k=None,
            tab_pos = 'top_left',
            do_default_tab=False,
            **kwargs
        ):
    '''
    Dynamic `WIDGET` widget constructor.

    ## Parameters
    
    `panels: dict`
    > Defines the content of the TabbedPanel.
    > - `{"{tab_name}": Widget, ...}`: For each `key: value` pair, a TabbedPanelItem is created with `text = "{tab_name}"` and Widget added as child. Each TabbedPanelItem created is added as child to the main TabbedPanel widget.
    > Defaults to `{}`.

    > Example:
    ```py
    sk.WIDGET(
            panels={
                "Header1": sk.Label('First tab content'),
                "Header2": sk.Button('Second tab content')
            }
        )
    ```

    {common}

    ## Returns
    
    `TabbedPanel` created dynamically with `panels` processed as displaued content during creation.

    ## Kivy Bases
    
    `TabbedPanel`
    
    `current: (str)`: `Text value of the current tab selected. Setting this property changes the current tab.

    {base_params}
    '''

    # kwargs=_preprocess(**kwargs)
    # global _future_elements, _future_bind
    class kvWd(kvw.TabbedPanel):
        _panels={}

        # @property
        def _get_current(self):
            # print(self._panels)
            return self.current_tab.text
        # @current.setter
        def _set_current(self,v):
            try:
                self.switch_to(self._panels[v])
            except:
                for ti in self.tab_list:
                    self._panels[ti.text]=ti
                self.switch_to(self._panels[v])
        current=kvw.AliasProperty(_get_current,_set_current)

    # kel=kvw.TabbedPanel(do_default_tab=do_default_tab,tab_pos=tab_pos,**kwargs)
    kel=skivify_v2(kvWd,k=k,do_default_tab=do_default_tab,tab_pos=tab_pos,**kwargs)
    for k,v in panels.items():
        ti=kvw.TabbedPanelItem(text=k)
        ti.add_widget(v)
        kel.add_widget(ti)
    
    # _future_elements.append(kel)
    return kel

# def Button(text='button',enable_events=True,k=None,on_event='on_release', **kwargs):
#     kwargs=_preprocess(**kwargs)
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
    '''
    Creates a WIDGET widget dynamically with added functionalities.

    ## Dynamic Creation Parameters
    
    {hover_highlight}
    > Default is `False`

    ## Parameters
    
    {bg_state}

    {common}

    ## Returns
    
    `WIDGET` widget created dynamically.

    ## Kivy Bases
    
    `Boutton`

    {base_params}
    
    ## Properties

    {button_properties}

    ## Events
    
    {events_button}

    {when_hover_highlight}
    '''

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
    '''
    `WIDGET` widget created Dynamically

    ## Parameters

    `fit_mode: str`
    > Distribution of the image within the widget. Has to be one of `"scale-down", "fill", "contain", "cover"`
    > Defaults to `"contain"`.

    '''
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
                    # Clock.schedule_once(lambda dt:setattr(self,'texture',CoreImage(BytesIO(data.read()), ext='png').texture))
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
                    return nim

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
                tried_normal=False
                try:
                    if pathlib.Path(src).suffix.lower()=='.svg':
                        self.from_bytes(
                                svg2png(
                                    url=src,
                                    output_width=ins.width,
                                    output_height=ins.height,
                                    parent_width=ins.width,
                                    parent_height=ins.height,
                                )
                            )
                    else:
                        tried_normal=True
                        super()._load_source(ins,src)

                except Exception as error:
                    self.dispatch('on_error', error)
                    sup=super()
                    if not tried_normal and hasattr(sup,'_load_source'):
                        sup._load_source(ins,ins.source)
            def on_error(self,error):
                pass
                





    # if fit_mode!='full':
    kel=skivify(kvImage,
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
def VideoVLC(
    source='',
    k=None,
    fit_mode='contain', # scale-down, fill, contain, cover,
    focus_behavior=False,
    allow_stretch=True,
    lock_screen_on_buffer=False,
    **kwargs,
    ):
    from kivy.graphics.texture import Texture
    from kivy.core.image import Image as CoreImage
    import numpy as np
    import vlc
    class _VLCWidget(mkvw.Image):
        _state = kvw.OptionProperty('stop', options=('play', 'pause', 'stop'))
        player=kvw.ObjectProperty(None)
        _eos = kvw.BooleanProperty(False)
        loaded=kvw.BooleanProperty(None)
        # allow_stretch=kvw.BooleanProperty(True)
        lock_screen_on_buffer=kvw.BooleanProperty(False)
        filename=StringProperty(None)

        _preview=kvw.StringProperty(resource_find( 'skdata/0.png'))
        
        def _gsource(self):
            return self.filename
            # try:
            #     # return self.media.get_mrl()
            #     return self.filename
            # except:
            #     return None
        
        

        
        def load_stream_async(self, stream_url: str, ready_callback=None, 
                         error_callback = None):
            """
            Load a stream asynchronously and call the callback when ready.
            
            Args:
                stream_url: URL of the stream to load
                ready_callback: Function to call when stream is ready to play
                error_callback: Optional function to call if loading fails
            """
            if self.is_loading:
                if error_callback:
                    error_callback("Already loading a stream")
                return
            import threading
            if ready_callback==None:
                ready_callback = lambda *x:print('Loaded successfully!')

            self.should_cancel = False
            self.is_loading = True
            self.loaded=False

            
            def load_task(stream_url):
                try:
                    
                    
                    sresolver=getattr(self,'source_resolver',None)
                    if sresolver:
                        try:
                            # if stream_url in self._resolved:
                            #     stream_url=self._resolved[stream_url]
                            # else:
                            stream_url=self._resolved.get(stream_url,sresolver(stream_url)) 
                        except Exception as error:
                            traceback.print_exc()
                            raise error
                    # Create new media
                    # print(f"{stream_url = }")
                    self.media = self.instance.media_new(stream_url)
                    self.filename=stream_url
                    self.player.set_media(self.media)

                    Clock.schedule_once(lambda dt:self.dispatch('on_media_parse_start',self.media))
                    
                    # Add event manager to detect when media is parsed
                    # event_manager = self.media.event_manager()
                    # event_manager.event_attach(vlc.EventType.MediaParsedChanged, 
                    #                          # lambda event: self._on_media_parsed(event, ready_callback)
                    #                          self._on_media_parsed,
                    #                          ready_callback
                    #                          )
                    
                    # Start parsing the media (this happens asynchronously in VLC)
                    # self.media.parse_with_options(vlc.MediaParseFlag.network, 10000)
                    # self.media.parse_with_options(vlc.MediaParseFlag.network, 10000)

                    self.media.parse_async()
                    timeout=10 # s
                    tend=time.time()+timeout

                    # print('loading...')
                    
                    # Monitor for cancellation while parsing
                    # while (not self.should_cancel and 
                    #        self.media.get_parsed_status() == vlc.MediaParsedStatus.init):

                    
                    while not self.should_cancel:
                        pstat=self.media.get_parsed_status()
                        # print('loading...',pstat)
                        if pstat in self._parse_success:
                            self.media.parse_stop()
                            # self.dispatch('on_media_parsed')
                            # Clock.schedule_once(lambda dt:self.dispatch('on_media_parsed',self.media) )
                            Clock.schedule_once(lambda dt:self._on_media_parsed(self.media))
                            # self.dispatch('on_media_parsed',self.media)
                            return
                        elif pstat in self._parse_unknown:
                            Clock.schedule_once(get_kvApp().dt_lock)
                            self.player.play()
                            video_track=-1
                            while video_track==-1:
                                video_track=self.player.video_get_track()
                                # print(f"{video_track = }")
                                if time.time()>=tend:
                                    raise TimeoutError(f'Could not parse the stream "{stream_url}" before timeout {timeout} s')
                                time.sleep(self.spf)
                            self.player.stop()
                            Clock.schedule_once(get_kvApp().dt_unlock)
                            Clock.schedule_once(lambda dt:self._on_media_parsed(self.media))
                            return
                        elif pstat in self._parse_error:
                            raise FileNotFoundError(f'Could not parse the stream "{stream_url}"')
                        if time.time()>=tend:
                            raise TimeoutError(f'Could not parse the stream "{stream_url}" before timeout {timeout} s')
                        time.sleep(self.spf)
                    # print(f"{should_cancel = }")

                    if self.should_cancel:
                        self.media.parse_stop()
                        Clock.schedule_once(lambda dt:self._on_media_parse_cancel(self.media))
                        return
                    # elif pstat==vlc.MediaParsedStatus.done:
                    #     # Clock.schedule_once(lambda dt:self._update_frame_format())
                    #     self.dispatch('on_media_parsed')
                        
                except Exception as e:
                    Clock.schedule_once(lambda dt:self._on_media_parse_error(getattr(self,"media",None)))
                    return
                    # self.is_loading = False
                    # if error_callback:
                    #     error_callback(f"Loading failed: {str(e)}")
                        
            self.load_thread = threading.Thread(target=load_task,args=(stream_url,), daemon=True)
            self.load_thread.start()
            return self.load_thread
        
        def _on_media_parsed(self,media):
            self._update_frame_format()
            self.is_loading = False
            self.loaded=True
            self.dispatch('on_media_parsed',media)
            # ready_callback()
        
        def _on_media_parse_cancel(self,media):
            self._cleanup()
            self.dispatch('on_media_parse_cancel',media)
        
        def _on_media_parse_error(self,media):
            self._cleanup()
            self.dispatch('on_media_parse_error',media)
        
        def on_media_parse_start(self,media):
            pass
        
        def on_media_parsed(self,media):
            pass
        
        def on_media_parse_error(self,media):
            pass
        
        def on_media_parse_cancel(self,media):
            pass
        # def _on_media_parsed(self, event,ready_callback):
        #     pstat=self.media.get_parsed_status()
        #     # print('Media parsed state:',pstat)
        # # def _on_media_parsed(self, event, ready_callback):
        #     """Called when VLC has finished parsing the media"""
        #     # print(event,ready_callback)
        #     if self.should_cancel:
        #         return
                
        #     if pstat == vlc.MediaParsedStatus.done:
        #         self.is_loading = False
        #         self.loaded=True
        #         ready_callback()
        
        def _cleanup(self):
            """Clean up resources after cancellation"""
            if self.media:
                self.media.release()
                self.media = None
            self.player.stop()
            self.is_loading = False
        
        def cancel_media_parse(self):
            """Cancel the ongoing stream loading"""
            if self.is_loading:
                self.should_cancel = True
                if self.load_thread and self.load_thread.is_alive():
                    self.load_thread.join(timeout=2.0)
                # print('loading cancelled!')
        
        def _ssource(self,val):
            self.player.stop()
            if not self._callbacks_set:
                Clock.schedule_once(lambda dt:self._setup_vlc_callbacks())
            if val:
                if not self.load_stream_async(val,ready_callback=self._update_frame_format):
                    return False
                else:
                    return True
            else:
                return False

            return False

        # def _ssource(self,val):
        #     self.loaded=False
        #     if not val:
        #         return False
        #     self.player.stop()
        #     self.media = self.instance.media_new(val)
        #     self.player.set_media(self.media)
        #     self.filename=val
        #     self._update_frame_format()
        #     if not self._callbacks_set:
        #         Clock.schedule_once(lambda dt:self._setup_vlc_callbacks())

        #     self.loaded=True

        #     return True

        source=kvw.AliasProperty(_gsource,_ssource,bind=['filename',])

        

        _duration=kvw.NumericProperty(-1)
        _position=kvw.NumericProperty(-1)
        
        def texture_update(self,*largs):
            pass

        def __init__(self,**kwargs):
            self._resolved={}
            self.register_event_type('on_media_parse_start')
            self.register_event_type('on_media_parsed')
            self.register_event_type('on_media_parse_cancel')
            self.register_event_type('on_media_parse_error')
            self.spf=1/30
            self._states={
                vlc.State.Playing:'play',
                vlc.State.Paused:'pause',
                vlc.State.Stopped:'stop',
                vlc.State.Ended:'stop',
                }
            self._parse_success={vlc.MediaParsedStatus.done}
            self._parse_unknown={vlc.MediaParsedStatus.skipped}
            self._parse_error={vlc.MediaParsedStatus.failed,vlc.MediaParsedStatus.timeout}
            self.load_thread = None
            self.should_cancel = False
            self.is_loading = False

            # self._preview=resource_find( 'skdata/0.png')
            _preview=kwargs.pop('preview',resource_find( 'skdata/0.png'))
            # self._filename=None
            self._callbacks_set=False
            self.frame_width=1280
            self.frame_height=720
            self.frame_pitch = self.frame_width * 4  # RGBA

            self._frame = np.zeros((self.frame_height, self.frame_width, 4), dtype=np.uint8)

            # VLC setup
            self.instance = vlc.Instance(
                # "--no-audio"
                "--vout=dummy",
                "--no-video-on-top",
                # "--qt-start-minimized",
                # "-avcodec-hw=any",
                "--directx-hw-yuv",
                # "--direct3d11-hw-blending",

                )  # or enable audio if needed
            
            self.player = self.instance.media_player_new()
            self.media = None
            self.em=self.player.event_manager()
            self.em_init()
            self.player.audio_set_volume(100)

            
            # print(self.source)
            # Texture placeholder
            
            super().__init__(preview=_preview,**kwargs)

            # self.bind(
            #     size=lambda *x:self.__update_frame_format()
            #     )

            # self._update_frame_format()
            # self.texture = Texture.create(size=(self.frame_width, self.frame_height))
            # self.texture.flip_vertical()

            # self.funbind('source',self.texture_update)
            # self.fbind('source', self._trigger_video_load)
            # self.fbind('state', self.on_state)

            # Clock.schedule_once(self._init_props)
            
            # Start playback
            # self.player.play()


        
        def _init_props(self,dt):
            self.setter('source')(self,self.source)
            self.setter('state')(self,self.state)
        # def __update_frame_format(self):
        #     vwidth_val=self.player.video_get_width()
        #     vheight_val = self.player.video_get_height()

        #     width_val=round(self.width)
        #     height_val=round(self.height)

        #     self.frame_width=width_val
        #     self.frame_height = height_val
        #     self.frame_pitch = self.frame_width * 4  # RGBA
        #     self._frame = np.zeros((self.frame_height, self.frame_width, 4), dtype=np.uint8)

        #     # Texture placeholder
        #     self.texture = Texture.create(size=(self.frame_width, self.frame_height), mipmap=True )
        #     self.texture.flip_vertical()
        #     self.player.video_set_format("RGBA", self.frame_width, self.frame_height, self.frame_pitch)
        
        def _update_frame_format(self):
            Clock.unschedule(self._update_texture)
            
            try:
                width_val=0
                while width_val<1:
                    width_val=self.player.video_get_width()
                    time.sleep(self.spf)
            except:
                self.player.play()
                width_val=0
                while width_val<1:
                    width_val=self.player.video_get_width()
                    time.sleep(self.spf)
                self.player.stop()

            height_val = self.player.video_get_height()

            self.frame_width=width_val
            self.frame_height = height_val
            self.frame_pitch = self.frame_width * 4  # RGBA
            self._frame = np.zeros((self.frame_height, self.frame_width, 4), dtype=np.uint8)

            # Texture placeholder
            self.texture = Texture.create(size=(self.frame_width, self.frame_height), mipmap=True )
            self.texture.flip_vertical()
            self.player.video_set_format("RGBA", self.frame_width, self.frame_height, self.frame_pitch)

            

            
        
        def _setup_vlc_callbacks(self):
            """Register callbacks for VLC to push frame data into our numpy array."""

            def _format_cb(opaque, chroma, width, height, pitches, lines):
                try:
                    # Method 1: If they're pointers
                    chroma_str = ctypes.string_at(chroma, 4).decode('utf-8', errors='ignore')
                    width_val = width.contents.value
                    height_val = height.contents.value
                except:
                    try:
                        # Method 2: If they're arrays
                        chroma_str = "".join([chr(chroma[i]) for i in range(4)])
                        width_val = width[0]
                        height_val = height[0]
                    except:
                        # Method 3: If they're direct values (unlikely but possible)
                        chroma_str = "unknown"
                        width_val = width
                        height_val = height
                # print(f"🎨 Format callback: {width_val}x{height_val}, chroma: {chroma_str}")
                # self.player.video_set_format("RGBA", self.frame_width, self.frame_height, self.frame_pitch)
                return 1

            # Prepare ctypes buffers and callbacks
            def _lock(data, p_pixels):
                p_pixels.contents.value = self._frame.ctypes.data
                return None

            def _unlock(data, id, p_pixels):
                pass

            def _display(data, id):
                pass


            # self._format_cb= vlc.CallbackDecorators.VideoFormatCb(_format_cb)

            # Keep references so they don’t get garbage-collected
            self._lock_cb = vlc.CallbackDecorators.VideoLockCb(_lock)
            self._unlock_cb = vlc.CallbackDecorators.VideoUnlockCb(_unlock)
            self._display_cb = vlc.CallbackDecorators.VideoDisplayCb(_display)

            # self.player.video_set_format_callbacks(self._format_cb, None)
            self.player.video_set_callbacks(self._lock_cb, self._unlock_cb, self._display_cb, None)
            # self.player.video_set_format("RGBA", self.frame_width, self.frame_height, self.frame_pitch)
            self._callbacks_set=True
        
        def _update_texture(self, dt):
            # print(0)
            """Copy the current frame into the Kivy texture."""
            try:
                if self._frame is not None:
                    # Upload the raw RGBA bytes into the Kivy texture
                    self.texture.blit_buffer(self._frame.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
                    self.canvas.ask_update()
            except AttributeError as e:
                if self.texture==None:
                    self._update_frame_format()
                    # Upload the raw RGBA bytes into the Kivy texture
                    self.texture.blit_buffer(self._frame.tobytes(), colorfmt='rgba', bufferfmt='ubyte')
                    self.canvas.ask_update()
                else:
                    raise e
                    

        # def on_state(self, instance, value):
        #     print('state:',value,self.player,self.media,self.eos)
        #     if not self.player:
        #         return
        #     if value == 'play':
        #         if self.eos:
        #             self.player.stop()
        #             # self.player.position = 0.
        #         self.eos = False
        #         self.player.play()
        #     elif value == 'pause':
        #         self.player.pause()
        #     else:
        #         self.player.stop()
        #         # self._video.position = 0
        
        def _gstate(self):
            # print(f"{self._state=}")
            return self._state
            # if not self.player:
            #     return 'stop'
            # else:
            #     s=self.player.get_state()
            #     ss=self._states.get(s,None)
            #     if ss==None:
            #         ss=f"{s}".lower().split('.')[-1]
            #     return ss
        
        def _sstate(self,val):
            if not self.player:
                return False
            if val=='play':
                self.player.play()
            elif val=='pause':
                self.player.pause()
            elif val=='stop':
                self.player.stop()
            # return True
            return False
        state=kvw.AliasProperty(_gstate,_sstate,bind=['_state',])

        
        
        
        def _geos(self):
            return self._eos
        eos=kvw.AliasProperty(_geos,bind=['_eos'])
        
        def seek(self,percent,precise=True):
            self.player.set_position(percent)

        
        def _gvolume(self):
            v=self.player.audio_get_volume()
            if v<0:
                return v
            return v/100
        
        def _svolume(self,val):
            ans= self.player.audio_set_volume(round(val*100))
            if ans==-1:
                return False
            return True
        volume=kvw.AliasProperty(_gvolume,_svolume)

        
        def length_cbk(self,event,player):
            self._duration=self._gduration()
        
        def _gduration(self):
            try:
                d=self.media.get_duration()
                if d!=-1:
                    d=d/1000
                if d==0:
                    return -1
                return d
            except:
                return -1
        duration=kvw.AliasProperty(_gduration,bind=['_duration',])

        
        def state_stopped_cbk(self,event,player):
            Clock.unschedule(self._update_texture)
            # print(f"cb_{event=}")
            self._state='stop'
            self._position= 0
        
        def state_playing_cbk(self,event,player):
            Clock.unschedule(self._update_texture)
            Clock.schedule_interval(self._update_texture, self.spf)
            self._state='play'
            self._eos=False
        
        def state_endreached_cbk(self,event,player):
            Clock.unschedule(self._update_texture)
            self._state='stop'
            self._eos=True
            self._position= 0
        
        def state_paused_cbk(self,event,player):
            Clock.unschedule(self._update_texture)
            self._state='pause'

        
        def _gposition(self):
            return self._position
        
        def _sposition(self,val):
            try:
                if self.duration!=0:
                    seek_val=val/self.duration
                    if 0.0<=seek_val<=1.0:
                        self.seek(seek_val)
                        return True
                return False
            except:
                return False
        position=kvw.AliasProperty(_gposition,_sposition,bind=['_position'])
        
        def position_cbk(self,event,player):
            # self._position=self._gposition()
            try:
                self._position= round(self.player.get_position()*self.media.get_duration()/1000)
            except:
                self._position= -1
        # @locked_screen
        
        def buffering_cbk(self,event,player):
            # print('buffering')
            # self.texture=CoreImage(self._preview).texture
            if self.lock_screen_on_buffer:
                app=get_kvApp()
                # Clock.unschedule(app.dt_unlock)
                # if not app.is_locked():
                Clock.unschedule(app.dt_lock)
                Clock.unschedule(app.dt_unlock)

                Clock.schedule_once(app.dt_lock)
                Clock.schedule_once(app.dt_unlock,5*self.spf)
            # else:
            #     Clock.schedule_once(get_kvApp().dt_unlock)
            

            
            # Clock.schedule_once(get_kvApp().dt_unlock)
            pass
            # print(event)
            # get_kvApp().lock()
            # get_kvApp().unlock()

        # def media_discovered_cbk(self,event,player):
        #     self._update_frame_format()
            # print('media')
        # def mediaerror_cbk(self,event,player):
        #     print(event)
        
        def em_init(self):
            em=self.em
            player=self.player
            em.event_attach(vlc.EventType.MediaPlayerStopped, 
                        self.state_stopped_cbk, player)
            em.event_attach(vlc.EventType.MediaPlayerPlaying, \
                            self.state_playing_cbk, player)
            
            # em.event_attach(vlc.EventType.MediaDiscovererEnded,
            #     self.media_discovered_cbk, player)
            # em.event_attach(vlc.EventType.MediaPlayerMediaChanged, \
            #                 self.media_discovered_cbk, player)
            # em.event_attach(vlc.EventType.MediaPlayerEncounteredError,\
            #     self.mediaerror_cbk,player
            #     )
            
            em.event_attach(vlc.EventType.MediaPlayerBuffering, \
                            self.buffering_cbk, player)
            
            em.event_attach(vlc.EventType.MediaPlayerPaused, \
                            self.state_paused_cbk, player)
            em.event_attach(vlc.EventType.MediaPlayerTimeChanged, \
                            self.position_cbk, player)
            em.event_attach(vlc.EventType.MediaPlayerEndReached, \
                            self.state_endreached_cbk, player)
            em.event_attach(vlc.EventType.MediaPlayerLengthChanged, \
                        self.length_cbk, player)
        
        def _gpreview(self):
            return self._preview
        
        def _spreview(self,val):
            if val:
                self._preview=val
                self.texture=CoreImage(val).texture
                return True
        preview=kvw.AliasProperty(_gpreview,_spreview)



    kvWd=_VLCWidget
    if focus_behavior:
        kvWd=kvb.FocusBehavior,kvWd
    kel=skivify(kvWd,source=source,allow_stretch=allow_stretch,k=k,
        fit_mode=fit_mode,lock_screen_on_buffer=lock_screen_on_buffer,
        **kwargs)
    return kel

@skwidget
def VideoVLCPlayer(queue=[],k=None,focus_behavior=False,lock_screen_on_buffer=False,**kwargs):
    kvWd=kvw.RelativeLayoutB

    class _kvWd(kvWd):
        queue=kvw.ListProperty([])
        playing_media=kvw.ObjectProperty(None)
        playing_index=kvw.NumericProperty(None)
        hide_setup=kvw.BooleanProperty(True)
        lock_screen_on_buffer=kvw.BooleanProperty(False)
        video=None

        _source=kvw.StringProperty(None)

        def _gsource(self):
            if self.video:
                return self.video.source
            else:
                return None


        source=kvw.AliasProperty(_gsource,bind=('_source',))

        preview=kvw.StringProperty('skdata/0.png')

        def on_media_parsed(self,media):
            pass
        def on_media_parse_start(self,media):
            pass
        def on_media_parse_cancel(self,media):
            pass
        def on_media_parse_error(self,media):
            pass

        def cancel_media_parse(self):
            self.video.cancel_media_parse()

        def __init__(self,**kwargs):
            self.register_event_type('on_media_parse_start')
            self.register_event_type('on_media_parsed')
            self.register_event_type('on_media_parse_cancel')
            self.register_event_type('on_media_parse_error')

            self.register_event_type('on_lang_menu_open')
            self.register_event_type('on_lang_menu_apply')
            self.register_event_type('on_lang_menu_dismiss')

            queue=kwargs.pop('queue',[])
            self.register_event_type('on_queue_end')
            preview=kwargs.get('preview',resource_find('skdata/0.png'))
            lock_screen_on_buffer=kwargs.get('lock_screen_on_buffer',False)
            fit_mode=kwargs.pop('fit_mode','contain')
            allow_stretch=kwargs.pop('allow_stretch',True)
            focus_behavior=kwargs.pop('focus_behavior',False)


            self.video=VideoVLC(k=NOTKEY,preview=preview,lock_screen_on_buffer=lock_screen_on_buffer,fit_mode=fit_mode,allow_stretch=allow_stretch,focus_behavior=focus_behavior)
            self.video.bind(
                on_media_parsed=lambda ins,media:self.dispatch('on_media_parsed',media),
                on_media_parse_start=lambda ins,media:self.dispatch('on_media_parse_start',media),
                on_media_parse_cancel=lambda ins,media:self.dispatch('on_media_parse_cancel',media),
                on_media_parse_error=lambda ins,media:self.dispatch('on_media_parse_error',media),
                )
            # if preview!=None:
            #     self.video=VideoVLC(k=NOTKEY,preview=preview)
            # else:
            #     self.video=VideoVLC(k=NOTKEY)

            self.video.bind(eos=lambda ins,v:self._schedule_next() if v else None)
            self.bind(preview=lambda ins,v:setattr(self.video,'preview',v))
            # self.video.bind(
            #     source=lambda ins,val:self.dispatch('source',self,val)
            #     )
            self._plm=utils.PlaylistManager()
            # self._plm.bind('on_track_changed',lambda plm,t:setattr(self,'_source',plm.get_current_track()))
            # self._plm.bind('on_track_changed',lambda plm,t:print(self,'_source',t))
            
            self._plm.bind('on_track_changed',lambda plm,t:Clock.schedule_once(lambda dt:setattr(self,'_source',t)))
            
            self._plm.bind('on_playlist_end',lambda *x:self.dispatch('on_queue_end'))
            # self._plm.bind('on_playlist_start',lambda *x:print('on_playlist_start',x))
            # self.ids=utils.IDS()

            list_audio=ListBox(k=NOTKEY,pos_hint={'top':1})
            list_subs=ListBox(k=NOTKEY,pos_hint={'top':1})
            lang_btn_apply=ClearRoundB('Apply',k=NOTKEY,size='y35')
            lang_btn_cancel=ClearRoundB('Cancel',k=NOTKEY,size='y35')
            r=25
            self.ids=utils.IDS({
                'player_slider': ProgressBarTouch(
                    value=0,
                    k=NOTKEY,
                    size='y10',
                    disabled=True,
                    ),
                'player_btn.back': ClearRoundB(
                        mdi('skip-backward'),size=f'x{2*r}',
                        k=NOTKEY,
                        r=r,
                        font_size=33,lcolor='',
                        focus_behavior=focus_behavior,
                    ),

                'player_btn.play': ClearRoundB(
                        mdi('play'),size=f'x{2*r}',
                        k=NOTKEY,
                        r=r,
                        font_size=33,lcolor='',
                        focus_behavior=focus_behavior,
                    ),
                'player_btn.stop': ClearRoundB(
                        mdi('stop'),size=f'x{2*r}',
                        k=NOTKEY,
                        r=r,
                        font_size=33,lcolor='',
                        focus_behavior=focus_behavior,
                    ),
                'player_btn.fwd': ClearRoundB(
                        mdi('skip-forward'),size=f'x{2*r}',
                        k=NOTKEY,
                        r=r,
                        font_size=33,lcolor='',
                        focus_behavior=focus_behavior,
                    ),
                'player_btn.lang': ClearRoundB(
                        mdi('subtitles'),size=f'x{2*r}',
                        k=NOTKEY,
                        r=r,
                        font_size=33,lcolor='',
                        focus_behavior=focus_behavior,
                    ),
                'list_audio':list_audio,
                'list_subs':list_subs,
                'lang_btn_apply':lang_btn_apply,
                'pop_lang':Popup(
                    title='Language options',
                    content=BoxitV(
                        BoxitH(
                            BoxitV(
                                T(mdi('account-voice')+' Audio',size='y35',markup=True),
                                list_audio,
                                spacing=8,
                                ),
                            SeparatorV(),
                            BoxitV(
                                T(mdi('subtitles-outline')+' Subtitles',markup=True,size='y35'),
                                list_subs,
                                spacing=8,
                                ),
                            spacing=8
                        ),
                        lang_btn_apply,
                        # BoxitH(
                        #     lang_btn_apply,
                        #     lang_btn_cancel,
                        #     size='y35',
                        #     spacing=8
                        #     ),
                            
                            padding=8,
                            spacing=8,
                        ),
                    k=NOTKEY,
                    size_hint=(.6,.6)
                    ),

                'player_lbl.position': T('--:--',k=NOTKEY,halign='right',size='x60'),
                'player_lbl.duration': T('--:--',k=NOTKEY,halign='left',size='x60'),


            })


            self.box=BoxitV(
                self.ids['player_slider'],
                BoxitH(
                    self.ids['player_btn.back'],
                    self.ids['player_btn.play'],
                    self.ids['player_btn.stop'],
                    self.ids['player_btn.fwd'],
                    Fill(),
                    self.ids['player_btn.lang'],
                    BoxitH(
                        self.ids['player_lbl.position'],
                        T('/',size='x15',k=NOTKEY),
                        self.ids['player_lbl.duration'],
                        spacing=4,
                        size='xchildren'
                        ),
                        k=NOTKEY
                ),
                k=NOTKEY,
                padding=6,
                spacing=6,
                size=f'y{2*r+10+3*6}',
            bcolor=[.25,.25,.25,.5]
            )
            self.ids['box']=self.box
            self.video.bind(position=self._on_vpos)
            self.video.bind(duration=self._on_vdur)
            self.ids['player_btn.play'].bind(on_release=self._play_pause)
            self.ids['player_btn.stop'].bind(on_release=lambda ins:self.video.player.stop())
            self.ids['player_btn.back'].bind(on_release=lambda ins:self.prev())
            self.ids['player_btn.fwd'].bind(on_release=lambda ins:self.next())
            self.ids['player_btn.lang'].bind(on_release=self._open_lang_menu)

            self.ids['player_slider'].bind(on_clickup=lambda ins,spos:self.video.seek(spos[0]))
            self.ids['lang_btn_apply'].bind(on_release=self._on_btn_apply_lang_menu)

            self.ids['pop_lang'].bind(on_dismiss=self._on_lang_menu_dismiss)

            self.video.bind(state=self._vstate)
            self.bind(queue=self._on_queue)
            super().__init__(**kwargs)
            self.add_widget(self.video)
            self.add_widget(self.box)
            self.hidden={}
            if queue:
                Clock.schedule_once(lambda dt:setattr(self,'queue',queue))
            if self.hide_setup:
                Clock.schedule_once(self._hide_setup)
        def _on_btn_apply_lang_menu(self,ins):
            a=self.ids.list_audio.data_selected
            s=self.ids.list_subs.data_selected
            if a and s:
                a=a[0]
                s=s[0]
            else:
                return
            self.video.player.audio_set_track(a['id'])
            self.video.player.video_set_spu(s['id'])
            self.ids.pop_lang.dismiss()
            self.dispatch('on_lang_menu_apply')

        def _open_lang_menu(self,ins):
            a=self.video.player.audio_get_track()
            s=self.video.player.video_get_spu()

            ac=self.video.player.audio_get_track_count()
            sc=self.video.player.video_get_spu_count()
            if ac==-1 and sc==-1:
                return
            # print(self.video.media.get_tracks_info().Audio)
            # self.video.media.tracks_release()
            la=self.video.player.audio_get_track_description()
            ls=self.video.player.video_get_spu_description()
            if not ls:
                ls=[(-1,b'Disabled'),]
            if not la:
                la=[(-1,b'Disabled'),]

            sdata=[]
            ss=0
            for i,ti in enumerate(ls):
                if ti[0]==s:
                    ss=i
                sdata.append(
                    dict(text=ti[1].decode('utf-8'),id=ti[0])
                    )
            adata=[]
            sa=0
            for i,ti in enumerate(la):
                if ti[0]==a:
                    sa=i
                adata.append(
                    dict(text=ti[1].decode('utf-8'),id=ti[0])
                    )
            self.ids.list_subs.data=sdata
            self.ids.list_audio.data=adata



            self.ids.list_subs.select(ss)
            self.ids.list_audio.select(sa)
            
            self.ids.pop_lang.open()
            self.dispatch('on_lang_menu_open')
        def on_lang_menu_open(self,*x):
            pass
        def on_lang_menu_apply(self,*x):
            pass
        def _on_lang_menu_dismiss(self,*x):
            self.dispatch('on_lang_menu_dismiss')
        def on_lang_menu_dismiss(self,*x):
            pass
        def _hide_setup(self,dt):
            self.kvWindow=utils.get_kvWindow()
            self.kvWindow.bind(mouse_pos=self.on_mouse_pos)
            self.mpos=self.kvWindow.mouse_pos
            self._hide_ctrls(0)
            self._unhide_ctrls(0)
            
            Clock.unschedule(self._hide_ctrls)
            Clock.schedule_once(self._unhide_ctrls)
            Clock.schedule_once(self._hide_ctrls,3)
            # Clock.schedule_once(lambda dt:setattr(self.kvWindow,'show_cursor',False),3)


        

        def on_mouse_pos(self,window,pos):
            self.mpos=pos
            if self.collide_point(*pos):
                # print(pos)
                Clock.unschedule(self._hide_ctrls)
                Clock.schedule_once(self._unhide_ctrls)
                Clock.schedule_once(self._hide_ctrls,3)

        def _hide_ctrls(self,dt):
            
            wid=self.box
            # if wid.height==0:
            #     return
            shrink=True
            s=getattr(wid,'size',(100,100)).copy()
            sh=getattr(wid,'size_hint',(1,1)).copy()
            o=getattr(wid,'opacity',1)
            d=getattr(wid,'disabled',False)
            # print('hide:',(s,sh,o,d))
            self.hidden['box']=(s,sh,o,d)
            # print(self.hidden)
            # print(k,':',(s,sh,o,d))
            # setattr(w,'size')
            if shrink:
                setattr(wid,'size',(0,0))
                setattr(wid,'size_hint',(None,None))
            setattr(wid,'opacity',0)
            setattr(wid,'disabled',True)
            if self.collide_point(*self.mpos) or self.mpos==(0,0):
                self.kvWindow.show_cursor=False

            # print(self.hidden)
        def _unhide_ctrls(self,dt):
            if self.collide_point(*self.mpos):
                self.kvWindow.show_cursor=True
            
            enforce={}
            wid=self.box
            try:
                s,sh,o,d=self.hidden.get('box')
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

        def _on_vpos(self,ins,v):
            self.ids['player_slider'].value=v
            self.ids['player_lbl.position'].text=utils.seconds2human(round(v),short=True)
            
        def _on_vdur(self,ins,v):
            self.ids['player_slider'].max=v
            self.ids['player_lbl.duration'].text=utils.seconds2human(round(v),short=True)


        def _vstate(self,ins,val):
            if self.video.state!='play':
                self.ids['player_btn.play'].text=mdi('play')
            else:
                self.ids['player_btn.play'].text=mdi('pause')

            if self.video.state=='stop':
                self.ids['player_slider'].disabled=True
            else:
                self.ids['player_slider'].disabled=False
            

        def _play_pause(self,*x):
            if self.video.state!='play':
                self.video.player.play()
            else:
                self.video.player.pause()

        def _on_queue(self,ins,val):
            # print(self.video,val)
            self._plm.populate(val,clear_existing=True)
            c=self._plm.get_current_track()
            if c!=None:
                # self._source=c
                # print("self._source:",c)
                self.video.source=c
                Clock.schedule_once(lambda dt:setattr(self,'_source',c))
            # self.dispatch('')

        def _dt_next(self,dt):
            self.next()
        def _schedule_next(self,*x):
            Clock.schedule_once(self._dt_next)
        def next(self):
            n=self._plm.next_track()
            # print(n)
            if n!=None:
                # self.video.state='stop'
                # Clock.schedule_once(lambda dt:setattr(self,'source', n))
                self.video.source=n
                self.video.player.play()
                # Clock.schedule_once(lambda dt:setattr(self,'state','play'))
                
        def prev(self):
            n=self._plm.prev_track()
            # print(n)
            if n!=None:
                self.video.source=n
                self.video.player.play()
                # Clock.schedule_once(lambda dt:setattr(self,'source', n))
                # Clock.schedule_once(lambda dt:setattr(self,'state','play'))
        def _gstate(self):
            if self.video:
                return self.video.state
            else:
                return 'stop'
        def _sstate(self,val):
            # print(val,self.video,self.video.source)
            if self.video:
                if val=='play' and self.video.source==None:
                    c=self._plm.get_current_track()
                    if c!=None:
                        self.video.source=c
                # print(val,self.video,self.video.source)
                self.video.state=val
                return self.video.state==val
            else:
                return False
        def stop(self):
            if self.video:
                self.video.player.stop()
        def on_queue_end(self,*args):
            pass



        state=kvw.AliasProperty(_gstate,_sstate)


    kvWd=_kvWd

    kel=skivify_v2(kvWd,k=k,queue=queue,focus_behavior=focus_behavior,lock_screen_on_buffer=lock_screen_on_buffer,**kwargs)

    return kel

@skwidget
def FlatButton(
    text='flat_button',
    lcolor=[.5,.5,.5,1],
    bcolor_normal=[.345, .345, .345, 0],
    bcolor_down=[.2, .64, .8, 1],
    markup=True,
    focus_behavior=False,hover_highlight=False,enable_events=True,on_event='on_release',k=None,touchripple=False,
    **kwargs):
    '''
    Creates a *Flat-style* button widget dynamically with added functionalities.

    ## Dynamic Creation Parameters

    {focus_behavior}
    > Default is False.
    
    {hover_highlight}
    > Default is `False`

    {touchripple}
    > Default is `False`

    ## Parameters
    
    {bgline_state}

    {common}

    ## Returns
    
    `WIDGET` widget created dynamically.

    ## Kivy Bases
    
    - `BoxLayout`
        - `Label`

    {base_params}
    
    ## Properties

    {button_properties}

    ## Properties

    ## Events
    
    {events_button}

    {when_hover_highlight}
    '''
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

@_widget_ctor
def ClearButton(text='clearbutton',hover_highlight=True,lcolor='',markup=True,**kwargs):
    '''
    {inits_FlatButton}
    '''
    return FlatButton(text=text,hover_highlight=hover_highlight,lcolor=lcolor,markup=markup,**kwargs)
ClearB=ClearButton


@skwidget
def FlatRoundButton(text='flat_round_btn',
    lcolor=[.5,.5,.5,1],
    bcolor_normal=[.345, .345, .345, 0],
    bcolor_down=[.2, .64, .8, 1],
    markup=True,
    focus_behavior=False,hover_highlight=False,enable_events=True,on_event='on_release',k=None,
    **kwargs):
    '''
    Creates a *Flat-style rounded* button widget dynamically with added functionalities.

    ## Dynamic Creation Parameters

    {focus_behavior}
    > Default is False.
    
    {hover_highlight}
    > Default is `False`

    ## Parameters

    {rounded}
    
    {bgline_state}

    {common}

    ## Returns
    
    `WIDGET` widget created dynamically.

    ## Kivy Bases
    
    - `RelativeLayout`
        - `Label`

    {base_params}
    
    ## Properties

    {button_properties}

    ## Properties

    ## Events
    
    {events_button}

    {when_hover_highlight}
    '''
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


@_widget_ctor
def ClearRoundButton(text='clear_round_btn',hover_highlight=True,lcolor='gray',markup=True,**kwargs):
    '''
    {inits_FlatRoundButton}
    '''
    return FlatRoundButton(text=text,hover_highlight=hover_highlight,lcolor=lcolor,markup=markup,**kwargs)

ClearRoundB=ClearRoundButton

@skwidget
def ButtonBoxit(*widgets,focus_behavior=False,lwidth=1,hover_highlight=False,enable_events=True,k=None,on_event='on_release', **kwargs):
    '''
    Creates a `BoxLayout` widget with `ButtonBehavior` dynamically with added functionalities.

    ## Dynamic Creation Parameters

    {focus_behavior}
    > Default is False.
    
    {hover_highlight}
    > Default is `False`

    ## Parameters
    
    {bgline_state}

    {common}

    ## Returns
    
    `WIDGET` widget created dynamically.

    ## Kivy Bases
    
    `BoxLayout`

    {base_params}
    
    ## Properties

    {button_properties}

    ## Events
    
    {events_button}

    {when_hover_highlight}
    '''
    kvWd=kvw.BBoxLayout

    if focus_behavior:
        class nkvWd(kvb.FocusBehavior,kvWd):
            pass
        kvWd=nkvWd
    if hover_highlight:
        class nkvWd(kvb.HoverHighlightBehavior,kvWd):
            pass
        kvWd=nkvWd

    kel=skivify(kvWd,k=k,lwidth=lwidth,enable_events=enable_events,on_event=on_event,**kwargs)

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


    kel=skivify(kvWd,k=k,enable_events=enable_events,on_event=on_event,**kwargs)

    # kel.id=k

    # kel.enable_events=enable_events
    # kel.on_event=on_event
    kel.post='ToggleGeneral'

    for w in widgets:
        kel.add_widget(w)


    return kel

@skwidget
def FlatButtonAngle(text='button',angle=90,enable_events=True,focus_behavior=False,k=None,on_event='on_release', **kwargs):
    '''
    Creates a *Flat-style* button widget dynamically with added functionalities. Contents are rotated according to `angle`.

    ## Dynamic Creation Parameters

    {focus_behavior}
    > Default is False.

    ## Parameters

    `angle (int or float)`: Angle of rotation of the button text. Defaults to 90.
    
    {bgline_state}

    {common}

    ## Returns
    
    `WIDGET` widget created dynamically.

    ## Kivy Bases
    
    - `BoxLayout`
        - `Label`

    {base_params}
    
    ## Properties

    {button_properties}

    ## Properties

    ## Events
    
    {events_button}
    '''
    # kwargs=_preprocess(**kwargs)
    # global _future_elements, _future_bind

    
    kvWd=kvw.FlatButtonAngle
    if focus_behavior:
        class _(kvb.FocusBehavior,kvWd):
            pass
        kvWd=_

    # kvWd=kvw.add_parent(kvWd,behavior)
    if k==None and text:
        k=text
    kel=skivify(kvWd,text=text,k=k,enable_events=enable_events,on_event=on_event,angle=angle,**kwargs)

    # kel.id=k

    # kel.enable_events=enable_events
    # kel.on_event=on_event

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
def FlatToggleButton(text='button',enable_events=False,k=None,on_event='on_state_down',hover_highlight=False, **kwargs):

    kvWd=kvw.FlatTButton
    if hover_highlight:
        class _(kvb.HoverHighlightBehavior,kvWd):
            pass
        kvWd=_

    if k==None and text:
        k=text
    kel=skivify(kvWd,text=text,k=k,enable_events=enable_events,on_event=on_event,**kwargs)

    # kel.id=k

    # kel.enable_events=enable_events
    # kel.on_event=on_event
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
    # kwargs=_preprocess(**kwargs)
    # global _future_elements, _future_bind

    

    kel=skivify(utils.Spinner,text=text,k=k,enable_events=enable_events,on_event=on_event,values=values,**kwargs)
    
    # kel.id=k

    # kel.enable_events=enable_events
    # kel.on_event=on_event

    # if enable_events:
    #     _future_bind.append(kel)

    # _future_elements.append(kel)
    return kel
@_widget_ctor
def Spinner2(text='choice0',
    values=('choice0', 'choice1'),
    enable_events=False,k=None,on_event='text',
    background_normal='atlas://skdata/sktheme/spinner_full',
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

# def Spinner2Dark(text='choice0',
#     values=('choice0', 'choice1'),
#     enable_events=False,k=None,on_event='text',
#     background_normal='atlas://skdata/sktheme/spinner_dark',
#     color='white',
#     background_color='#191919',
#     # background_color='w',
#     option_cls=None,
#     **kwargs
#     ):
#     # color=utils.resolve_color(color)
#     # background_color=utils.resolve_color(background_color)

#     from .modkvWidgets import SpinnerOptionB
#     class SpinnerOptionBDark(SpinnerOptionB):
#         background_normal='atlas://skdata/sktheme/spinneroption_dark'
#     SpinnerOptionBDark.background_normal='atlas://skdata/sktheme/spinneroption_dark'

#         # background_color=[1,1,1,1]
#         # markup=False
#         # halign='center'
#         # valign='middle'
#         # color=[1,1,1,1]
#         # background_normal='atlas://skdata/sktheme/spinneroption_dark'
#         # def on_release(self):
#         #     self.background_color='atlas://skdata/sktheme/spinneroption_dark'

#         # markup=kwargs.get('markup',False)
#         # halign=kwargs.get('halign','center')
#         # valign=kwargs.get('valign','middle')
#         # color=kvw.ColorProperty([1,1,1,1])
#         # background_color=kvw.ColorProperty([1,1,1,1])
#     # # SpinnerOptionB=SpinnerOptionBDark
#     # SpinnerOptionB.markup=kwargs.get('markup',False)
#     # SpinnerOptionB.halign=kwargs.get('halign','center')
#     # SpinnerOptionB.valign=kwargs.get('valign','middle')
#     # SpinnerOptionB.color=kwargs.get('color',color)
#     # # SpinnerOptionB.background_normal=kwargs.get('background_normal','atlas://skdata/sktheme/spinneroption_dark')
#     # SpinnerOptionB.background_color=kwargs.get('background_color',background_color)
#     # # SpinnerOptionB.halign=kwargs.get('halign','center')
#     # SpinnerOptionB.bind()

#     kel=Spinner(
#         text=text,values=values,
#         background_normal=background_normal,
#         background_color=background_color,
#         color=color,
#         option_cls=SpinnerOptionBDark,
#         enable_events=enable_events,k=k,on_event=on_event, **kwargs
#     )
#     return kel

@skwidget
def ListBox(
    data=[], # [{"text": f"label{x}", "halign": "center", "valign": "middle", "lcolor": ""} for x in range(10)],
    enable_events=False,k=None,on_event='on_selection',
    keyboard_scroll=True,
    effect_cls='scroll', # damped, scroll, opacity, no
    base_cls=None,
    bar_color=[.4, .4, .4, .9],
    bar_inactive_color=[.4, .4, .4, .6],
    bar_width=8,
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

    kel=skivify((kvw.RV),k=k,enable_events=enable_events,effect_cls=effect_cls,on_event=on_event,data=data,keyboard_scroll=keyboard_scroll,
        # selected_color=selected_color,
        bar_color=bar_color,bar_inactive_color=bar_inactive_color,bar_width=bar_width,
        **kwargs)
    # Clock.schedule_once(lambda dt:kel.setter('data')(kel,data))
    
    return kel

@skwidget
def Rowlist(
    data=[],
    enable_events=False,k=None,on_event='on_selection',
    keyboard_scroll=True,
    effect_cls='scroll', # damped, scroll, opacity, no
    base_cls=None,
    row_defaults={},
    cell_defaults={},
    **kwargs
    ):
    _cell_defaults={'text':'','halign':'left','valign':'middle','shorten':True,'padding':4,'markup':True,'font_name':'segoeui.ttf'}
    _cell_defaults.update(cell_defaults)

    _row_defaults=dict(padding=4,selectable=True,buttonbehavior=False)
    _row_defaults.update(row_defaults)

    _viewclass_base=kwargs.pop('viewclass_base',kvw.RowSelectable)

    if isinstance(effect_cls,str):
        match effect_cls:
            case 'no':
                from kivy.effects.scroll import ScrollEffect as effect_cls
            case 'opacity':
                from kivy.effects.scroll import OpacityScrollEffect as effect_cls
            case 'damped':
                from kivy.effects.scroll import DampedScrollEffect as effect_cls
            case 'scroll':
                from kivy.effects.scroll import ScrollEffect as effect_cls
    kel=skivify(kvw.Rowlist,
        k=k,

        viewclass_cell=kvw.LabelB,
        cell_defaults=_cell_defaults,
        row_defaults=_row_defaults,
        viewclass_base=_viewclass_base,
        
        enable_events=enable_events,effect_cls=effect_cls,on_event=on_event,data=data,keyboard_scroll=keyboard_scroll,
        **kwargs)
    
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
    # kwargs=_preprocess(**kwargs)
    # global _future_elements, _future_bind

    


    kel=skivify(kvw.Playlist,k=k,data=data,keyboard_scroll=keyboard_scroll,enable_events=enable_events,on_event=on_event,**kwargs)
    
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
    do_dot_subevent=False,
    keyboard_scroll=True,
    bar_color=[.4, .4, .4, .9],
    bar_inactive_color=[.4, .4, .4, .6],
    bar_width=8,
    effect_cls='scroll', # damped, scroll, opacity, no
    orientation='vertical',

    **kwargs
    ):
    if isinstance(effect_cls,str):
        match effect_cls:
            case 'no':
                from kivy.effects.scroll import ScrollEffect as effect_cls
            case 'opacity':
                from kivy.effects.scroll import OpacityScrollEffect as effect_cls
            case 'damped':
                from kivy.effects.scroll import DampedScrollEffect as effect_cls
            case 'scroll':
                from kivy.effects.scroll import ScrollEffect as effect_cls
    if orientation=='vertical':
        kvWd=kvw.Artistlist
    else:
        kvWd=kvw.ArtistlistH
    kel=skivify(kvWd,k=k,enable_events=enable_events,effect_cls=effect_cls,on_event=on_event,data=data,keyboard_scroll=keyboard_scroll,do_dot_subevent=do_dot_subevent,
        bar_color=bar_color,bar_inactive_color=bar_inactive_color,bar_width=bar_width,
        **kwargs)
    
    # kel.id=k
    kel.post='Artistlist'
    # kel.enable_events=enable_events
    # kel.on_event=on_event
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
    # kwargs=_preprocess(**kwargs)
    # global _future_elements, _future_bind

    


    kel=skivify(kvw.Albumlist,data=data,keyboard_scroll=keyboard_scroll,enable_events=enable_events,on_event=on_event,k=k,**kwargs)
    
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
def TextInput(text='',enable_events=False,multiline=False,k=None,on_event='on_text_validate', **kwargs):
    # kwargs=_preprocess(**kwargs)
    # global _future_elements, _future_bind

    W=kvw.kvInput

    # if 'on_insert_text' in on_event:
    class W(kvw.kvInput):
        last_added=''
        # delayed_text=kvw.StringProperty('')
        delay_interval = NumericProperty(.5)  # delay after typing stops
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

    kel=skivify((W),text=text,k=k,multiline=multiline,enable_events=enable_events,on_event=on_event,**kwargs)
    return kel

Input=In=TextInput

@skwidget
def TextInputDark(text='',enable_events=False,multiline=False,k=None,on_event='on_text_validate', **kwargs):
    W=kvw.kvInput

    # if 'on_insert_text' in on_event:
    class W(kvw.kvInput):
        foreground_color=kvw.ColorProperty([1,1,1,1])
        background_active=kvw.StringProperty('atlas://skdata/sktheme/textinput_active')
        background_normal=kvw.StringProperty('atlas://skdata/sktheme/textinput')
        background_disabled_normal=kvw.StringProperty('atlas://skdata/sktheme/textinput_disabled')
        disabled_foreground_color=kvw.ColorProperty([1,1,1,.5])
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

    kel=skivify(W,text=text,k=k,enable_events=enable_events,on_event=on_event,multiline=multiline,**kwargs)
    
    return kel

InputDark=InDark=TextInputDark

@_widget_ctor
def Multiline(text='',enable_events=False,multiline=True,k=None,on_event='on_text_validate', **kwargs):
    locs=locals()
    # print(locs)
    kw=locs.pop('kwargs')
    locs.update(kw)
    locs['multiline']=multiline

    return Input(**locs)

@_widget_ctor
def MultilineDark(text='',enable_events=False,multiline=True,k=None,on_event='on_text_validate', **kwargs):
    locs=locals()
    # print(locs)
    kw=locs.pop('kwargs')
    locs.update(kw)
    locs['multiline']=multiline

    return InputDark(**locs)

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
    kel=skivify(nW,text=text,lexer=lexer(),style_name=style_name,k=k,enable_events=enable_events,on_event=on_event,**kwargs)
    # kel=W(text=text,lexer=CombinedLexer(),style='dracula',**kwargs)
    # kel=W(text=text,lexer=TexLexer(),style='dracula',**kwargs)
    # kel.id=k

    # kel.enable_events=enable_events
    # kel.on_event=on_event

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
    
    kel = skivify(W,tree=tree,root_options=dict(text='Tree One'),
                      hide_root=False,
                      k=k,
                      enable_events=enable_events,
                      on_event=on_event,
                      indent_level=indent_level,**kwargs)

    # populate_tree_view(kel, None, tree)
    # kel.id=k

    # kel.enable_events=enable_events
    # kel.on_event=on_event
    return kel

# TEST_WIDGET(TreeView(on_event='selected_node',enable_events=True))


@skwidget
def ScrollView(
    content,
    scroll_y=True,scroll_x=False,
    k=None,
    bar_color=[.4, .4, .4, .9],
    bar_inactive_color=[.4, .4, .4, .6],
    bar_width=8,
    scroll_type=['bars', 'content'],
    effect_cls='scroll', # damped, scroll, opacity, no
    **kwargs):

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



    kel=skivify(kvWd,
        k=k,
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
    # kel.id=k
    kel.add_widget(content)
    return kel

@skwidget
def Popup(content,title='Popup window',enable_events=False,on_event='on_dismiss',do_dot_subevent=False,k=None,**kwargs):
    from kivy.uix.popup import Popup as kvWd


    kel=skivify(kvWd,
        title=title,
        content=content,
        k=k,
        enable_events=enable_events,
        do_dot_subevent=do_dot_subevent,
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
    # kwargs=_preprocess(**kwargs)
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
                setattr(v,'screen_name',n)
            

        kel.add_widget(s)

    
    
    # _future_elements.append(kel)
    return kel
Screens=ScreenManager

@skwidget
def Screen(widgets=[],name='',k=None,**kwargs):
    if k==None:
        k=name
    else:
        if name=='':
            name=k
    # if name=='' and k:
    #     name=k
    kvWd=kvw.Screen

    kel=skivify_v2(kvWd,k=k,name=name,**kwargs)
    if utils.is_iterable(widgets):
        for w in widgets:
            kel.add_widget(w)
    else:
        kel.add_widget(widgets)
    setattr(kel,'screen_name',name)
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
    '''
    {: .prompt-warning }
    > Experimental widget. Imagine a fusion of Excel and Python.
    '''
    kwargs=_preprocess(**kwargs)
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
                        bcolor_normal=(0.5,0.5,0.5,0.5)
                        )

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
    kel=skivify(kvWd,value=value,min=min,max=max,k=k,enable_events=enable_events,on_event=on_event,**kwargs)
    # kel.id=k
    return kel



@skwidget
def ScrollbarMirror(k=None,enable_events=False,on_event=None,**kwargs):
    kvWd=kvw.ScrollbarMirror
    kel=skivify_v2(kvWd,k=k,enable_events=False,on_event=None,**kwargs)
    return kel

@skwidget
def BarTouchH(value=0,max=1,scroll_delta=0,k=None,enable_events=False,on_event="value",**kwargs):
    class kvWd(kvw.RelativeLayout):
        scroll_delta=NumericProperty(0)
        bcolor = kvw.ColorProperty([50/255, 164/255, 206/255, 1])  # background color
        lcolor = kvw.ColorProperty([.5, .5, .5, 1])  # line color
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
BarTouch=BarTouchH
@skwidget
def BarTouchV(value=0,max=1,scroll_delta=0,k=None,enable_events=False,on_event="value",**kwargs):
    class kvWd(kvw.RelativeLayout):
        scroll_delta=NumericProperty(0)
        bcolor = kvw.ColorProperty([50/255, 164/255, 206/255, 1])  # background color
        lcolor = kvw.ColorProperty([.5, .5, .5, 1])  # line color
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
            self.register_event_type('on_clickup')
            super(kvWd2, self).__init__(**kwargs)
            

        # def on_touch_down(self,touch):
        #     if touch.is_mouse_scrolling:
        #         return False
        #     if not self.collide_point(touch.x, touch.y):
        #         return False

        def on_touch_up(self,touch):
            if self.disabled:
                return False
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
            self.dispatch('on_clickup',self.spos)
        def on_clickup(self,spos):
            # print(ins,self)
            pass

        # value=kvw.AliasProperty(
            
        #     )


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
            if self.disabled:
                return False
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

@_widget_ctor
def Void(k=NOTKEY,**kwargs):
    '''
    A void `Boxit` widget with `k= NOTKEY, size = (0,0), size_hint = (None, None)` as default.
    See {url_Boxit}.
    '''
    kel=Boxit(k=k,size=kwargs.pop('size',(0,0)),size_hint=kwargs.pop('size_hint',(None,None)))
    kel.is_void=True
    return kel
def PAW():
    kel=Boxit(size=(0,0),size_hint=(None,None),k=NOTKEY)
    Clock.schedule_once(lambda dt:get_kvApp().paw())
    return kel

@_widget_ctor
def Fill(k=NOTKEY,**kwargs):
    size=kwargs.pop('size',(0,0))
    size_hint=kwargs.pop('size_hint',(1,1))
    kel=Boxit(size=size,size_hint=size_hint,k=k,**kwargs)
    kel.is_void=True
    return kel

@_widget_ctor
def SeparatorV(bcolor='gray',size=(2,1),size_hint=(None,1),k=NOTKEY,**kwargs):
    return Boxit(bcolor=bcolor,size=size,size_hint=size_hint,k=k,**kwargs)

@_widget_ctor
def SeparatorH(bcolor='gray',size=(1,2),size_hint=(1,None),k=NOTKEY,**kwargs):
    return Boxit(bcolor=bcolor,size=size,size_hint=size_hint,k=k,**kwargs)


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

class EventManager:
    '''
    The EventManager class is an alternative to handling SimpleKivy events.

    It provides different types of decorator methods to define rules for catching events.
    Optimized for speed in applications with a huge amount of different events.

    ## Decorator Methods
    `@EventManager.start`: Sets the callback for the `"__Start__"`) event.
    `@EventManager.close`: Sets the callback for the `"__Close__"`) event.
    `@EventManager.event() or @EventManager.event( event_name = str )`: Sets a callback for an **exact match** (`==`) corresponding to an event id. Accepts an `event_name` argument, which let's you set the catch rule `event == event_name`. `event_name` defaults to None, in which case the function name is used as the `event_name` value.
    `@EventManager.rule( rule_callback = function )`: Sets a callback for any event that meets a custom rule function. Needs the positional argument `rule_callback`, which has to be a function that accepts **one** argument, and returns a value that can be converted to `bool`, for example: `True, False, None, "hello", "", 0, 1`. Rule testing is only performed once. If the `bool` conversion returns `True` by the `rule_callback`, the event is cached to immediately trigger the callback decorated with `rule` when triggering the same event id again.
    
    `@EventManager.unhandled`: Sets a callback for any event that is not caught by any other rule.
    
    Exact matches (set by the `event` decorator) are always tested first before `rule` decorator testing.

    > Example:
    
    ```py
    evman=sk.EventManager()

    @evman.event("btn")
    def on_btn(app,ev):
        """Handles the "btn" event"""
    
    @evman.event()
    def Exit(app,ev):
        """Handles the "Exit" event"""

    @evman.start
    def on_start(app,ev):
        """Handles the "__Start__" event"""

    @evman.close
    def on_start(app,ev):
        """Handles the "__Close__" event"""
    
    @evman.rule(lambda x: x.startswith('http'))
    def on_http(app,ev):
        """"Will catch any event that starts with "http"."""
    
    @evman.unhandled
    def on_other(app,ev):
        """Handles any other events that are not caught by an exact match or rule."""

    app = sk.MyApp(
        ...
        event_manager = evman,
        ...
    )
    ```
    
    '''
    __events__={}
    __rules__={}
    __ev_to_rule__={}
    __unhandled__=set()
    def __init__(self,verbose=False):
        self.verbose=verbose
        self.__events__['__Start__']=self._nofunc
        self.__events__['__Close__']=self._nofunc
    def _nofunc(self,*l,**kwargs):
        pass
    def __test_rules__(self,ev):
        try:
            return self.__ev_to_rule__[ev]
        except:
            rans=None
            for ri,calli in self.__rules__.items():
                try:
                    rans=ri(ev)
                except:
                    rans=False
                if rans:
                    self.__ev_to_rule__[ev]=calli
                    return calli
            if not rans:
                self.__unhandled__.add(ev)
                return self._

    def __call__(self,app,ev,*args,**kwargs):
        if self.verbose==True:
            print('Event:',ev)
        self.app=app
        try:
            callback=self.__events__[ev]
        except:
            if ev in self.__unhandled__:
                callback=self._
            else:
                callback=self.__test_rules__(ev)
        
        return callback(app,ev,*args,**kwargs)
        # try:
        #     callback(app,ev,*args,**kwargs)
        # except Exception as e:
        #     traceback.print_exc()
            # pass
    def _(self,app,ev,*args,**kwargs):
        if self.verbose!='silent':
            print('Unhandled:',ev)
        pass
    def event(self,event_name=None):
        event_name=[event_name]
        def event_decorator(func):

            if event_name[0]==None:
                event_name[0]=func.__name__
            self.__events__[event_name[0]]=func
            def wrapper(app,ev,*args,**kwargs):
                result=func(app,ev,*args,**kwargs)
                return result
        return event_decorator
    def start(self,func):
        self.__events__['__Start__']=func
        def wrapper(app,ev,*args,**kwargs):
            result=func(app,ev,*args,**kwargs)
            return result
        return wrapper
    def close(self,func):
        fname='__Close__'
        self.__events__[fname]=func
        def wrapper(app,ev,*args,**kwargs):
            result=func(app,ev,*args,**kwargs)
            return result
        return wrapper
    def rule(self,rule_callback):
        def rule_decorator(func):
            self.__rules__[rule_callback]=func
            def wrapper(app,ev,*args,**kwargs):
                result=func(app,ev,*args,**kwargs)
                return result
        return rule_decorator
    def unhandled(self,func):
        self._=func
        def wrapper(app,ev,*args,**kwargs):
            result=func(app,ev,*args,**kwargs)
            return result
        return wrapper

@skwidget
def Filelist(
        initialdir='./',
        k=None,
        folders_only=False,
        file_types_filter=(),
        focus_color='',
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
    # import pathlib
    import psutil
    cdir=pathlib.Path(initialdir).resolve()
    def path2parts(path):
        ans=[]
        for pi,p in enumerate(path.parts):
            ans.append(f"[b][ref={os.path.join(*path.parts[:pi],p)}]{p.replace('\\','')}[/ref][/b]")
        # return ' / '.join(ans)
        return mdi('chevron-right',color='w',size=20).join(ans)
    def load_from_path(self,cdir):
        # Clock.schedule_once(lambda dt:setattr(self.filelist,'data',[
        #     dict(
        #             meta=utils.infinite(),
        #             stat=None,
        #             height=35,size_hint_y=None,
        #             selectable=False,
        #             data=[
        #                 dict(text=self.icons.get('sync'),width=30,size_hint_x=None,shorten=False), 
        #                 dict(text="Loading..."),
        #                 dict(text="",size_hint_max_x=130,bcolor='',halign='right'),
        #                 dict(size_hint_max_x=100,bcolor='',halign='right'),
        #                 ]
        #         )
        #     ]))
        # self.filelist.data=[
        #     dict(
        #             meta=utils.infinite(),
        #             stat=None,
        #             height=35,size_hint_y=None,
        #             selectable=False,
        #             data=[
        #                 dict(text=self.icons.get('sync'),width=30,size_hint_x=None,shorten=False), 
        #                 dict(text="Loading..."),
        #                 dict(text="",size_hint_max_x=130,bcolor='',halign='right'),
        #                 dict(size_hint_max_x=100,bcolor='',halign='right'),
        #                 ]
        #         )
        #     ]
        # Clock.schedule_once(lambda dt:setattr(self.filelist,'scroll_y',1))

        cdir=cdir.resolve().absolute()
        self.dispatch('on_directory',cdir)
        data=[]
        # folder_icon=mdi('folder',color=('#FFD96C'),size=25)
        
        files=[]
        folders=[]
        q=self.input_search.text.lower().strip()
        if q:
            check = lambda x:bool(q in x.name.lower())
        else:
            check=lambda x:True
        
        for fi in cdir.iterdir():
            fi_stat=fi.stat()
            if not check(fi):
                continue
            if fi.is_dir():

                folders.append(
                    dict(
                        meta=fi,
                        # lcolor='r',
                        selectable=True,
                        stat=fi_stat,
                        height=35,size_hint_y=None,
                        data=[
                            dict(text=self.icons.get('folder'),width=30,size_hint_x=None,shorten=False), 
                            dict(text=fi.name),
                            # dict(size_hint_max_x=150,bcolor='',halign='right'),
                            dict(text=f"{self.get_mtime(fi_stat)}",size_hint_max_x=130,bcolor='',halign='right'),
                            dict(size_hint_max_x=100,bcolor='',halign='right'),
                            # dict(text=f"{self.get_human_readable_size(fi)}",size_hint_max_x=100,bcolor='',halign='right'),
                            ]
                    )
                )
            elif not folders_only:
                # icon=icons.get(fi.suffix.lower(),file_or_folder[0])
                # fi._stat_result=fi.stat()
                # setattr(fi,'_stat_result',fi.stat())
                # fi_stat=fi.stat()
                ext=fi.suffix.lower()
                # print(ext)
                if self.file_types_filter:
                    if not ext in self.file_types_filter:
                        continue

                icon=self.icons.get(ext)
                files.append(
                    dict(
                        meta=fi,
                        stat=fi_stat,
                        selectable=True,
                        # size=(1,90),size_hint_y=None,
                        height=35,size_hint_y=None,
                        # lcolor='',
                        data=[
                            dict(text=icon,width=30,size_hint_x=None,shorten=False), 
                            dict(text=fi.name),
                            # dict(text=f"{fi.stat().st_size}"),
                            # dict(text=f"{self.get_human_readable_size(fi)}"),
                            dict(text=f"{self.get_mtime(fi_stat)}",size_hint_max_x=130,bcolor='',halign='right'),
                            # dict(text=f"{self.get_KB_size(fi_stat)}",size_hint_max_x=100,bcolor='',halign='right'),
                            dict(text=f"{self.get_human_readable_size(fi)}",size_hint_max_x=100,bcolor='',halign='right'),
                            
                            ]
                    )
                )

        sort_mode=self.sort_menu.sort_mode
        folder_mode=self.sort_menu.folder_mode
        if folder_mode in (0,1):
            if sort_mode==0:
                fo,fi=folders,files
            elif sort_mode==1:
                fo,fi=reversed(folders),reversed(files)
            elif sort_mode==3:
                fo,fi=sorted(folders,key=lambda x:x['stat'].st_size,reverse=True),sorted(files,key=lambda x:x['stat'].st_size,reverse=True)
            elif sort_mode==2:
                fo,fi=sorted(folders,key=lambda x:x['stat'].st_size,reverse=False),sorted(files,key=lambda x:x['stat'].st_size,reverse=False)
            elif sort_mode==4:
                fo,fi=sorted(folders,key=lambda x:x['stat'].st_mtime,reverse=True),sorted(files,key=lambda x:x['stat'].st_mtime,reverse=True)
            elif sort_mode==5:
                fo,fi=sorted(folders,key=lambda x:x['stat'].st_mtime,reverse=False),sorted(files,key=lambda x:x['stat'].st_mtime,reverse=False)
            if folder_mode==0:
                data=list(fo)+list(fi)
            else:
                data=list(fi)+list(fo)
        elif folder_mode==2:
            if sort_mode==0:
                data=sorted(folders+files,key=lambda x:x['meta'].name.lower())
            elif sort_mode==1:
                data=sorted(folders+files,key=lambda x:x['meta'].name.lower(),reverse=True)
            elif sort_mode==3:
                data=sorted(folders+files,key=lambda x:x['stat'].st_size,reverse=True)
            elif sort_mode==2:
                data=sorted(folders+files,key=lambda x:x['stat'].st_size,reverse=False)
            elif sort_mode==4:
                data=sorted(folders+files,key=lambda x:x['stat'].st_mtime,reverse=True)
            elif sort_mode==5:
                data=sorted(folders+files,key=lambda x:x['stat'].st_mtime,reverse=False)
        
        # print(f"{sort_mode=}")

        # print(self.sort_menu.default)
        # self.filelist.data=data
        Clock.schedule_once(lambda dt:setattr(self.filelist,'data',data))
        Clock.schedule_once(lambda dt:setattr(self.filelist,'scroll_y',1))
        return data


    label_path=Label('',markup=True,shorten_from='center',shorten=True,
                    k=NOTKEY,halign='left',valign='middle',
                    padding=(6,0,6,0),color='light grey',
                    size_behavior='normal',
                    # size='x100'
                    # size_hint_x=None
                    # size_hint_y=None
                    # size_hint_x=None
                    )

    # click_box=Boxit(bcolor=(1,0,0,.2),size='x100')
    # click_box=Label()
    label_path_box=RoundButtonRelativeit(label_path,
        bcolor_normal='#2C2C2C',
        # bcolor_normal="#181818",
        lcolor='',k=NOTKEY)
    # def on_box_w(ins,w):
    #     click_box.width=label_path_box.width-label_path.width
    #     print(label_path.texture_size,label_path.width,label_path.text_size)
    #     tw,th=label_path.texture_size
    #     label_path.width=min((tw,ins.width-16))
    #     label_path.text_size=label_path.width,None
    #     click_box.width=label_path_box.width-label_path.width
        # label_path.size_hint_max_x=w-16
        # if label_path.text_size[0]!=None:
        #     if label_path.text_size[0]>label_path.size_hint_max_x:
        #         label_path.text_size[0]=label_path.size_hint_max_x
    # kel.size_hint_x=None
    # Clock.schedule_once(lambda dt: setattr(kel,'width',kel.texture_size[0]))
    # Clock.schedule_once(lambda dt: setattr(kel,'text_size',(None, kel.height)))
    # kel.bind(texture_size=lambda inst,siz:setattr(inst,'width',siz[0]))
    # kel.bind(height=lambda inst,v:setattr(inst,'text_size',(None, v)))

    # label_path_box.bind(width=on_box_w)
    # def on_text(ins,t):
    #     pass
        # print(ins.texture_size)


        # tw,th=label_path.texture_size
        # print(tw,label_path.text_size[0])
        # label_path.width=min((tw,label_path_box.width-16))
        # label_path.text_size=label_path.width,None

        # lambda *x: on_box_w(label_path_box,label_path_box.width)
    # label_path.bind(texture_size=on_text)
    path_input=InputDark(k=NOTKEY,write_tab=False)
    def on_pre_open(*x):
        setattr(path_input,'text',f"{label_path.path}")
        path_input.do_cursor_movement('cursor_end')
        path_input.focus=True
    def on_text_validate(ins,*x):
        npath=pathlib.Path(ins.text)
        _app=utils.get_kvApp()
        
        if npath.is_dir() and npath.exists():
            ins.root.on_path(npath)
            
        else:
            otext=label_path.text
            alert=mdi('alert',color='yellow',size=25)
            # label_path.text=alert+f"[color=#A30027] Folder not found [/color]"+alert
            _app(label_path,text=alert+f"[color=#A30027] Folder not found [/color]"+alert,halign='center')
            _app.schedule_call_once(label_path,text=otext,halign='left',timeout=1.5)
            # Clock.schedule_once(lambda dt:setattr(label_path,'text',otext),1)
    def on_focus(ins,v):
        _app=utils.get_kvApp()
        _app.remove_top_widget()
    path_input.bind(on_text_validate=on_text_validate)
    path_input.bind(focus=on_focus)


    AddMenu(
        label_path_box,
        path_input,

        # Boxit(InputDark(),size='x200y30'),
        position_to=label_path_box,touch_up_buttons=(),
        on_pre_open=on_pre_open
        )
    label_path_box.bind(on_release=label_path_box.show_menu)
    label_path.path=None
    
    # path2parts(cdir)

    btn_up=ClearB(mdi('arrow-up'),size="32",k=NOTKEY)
    btn_prev=ClearB(mdi('arrow-left'),size="32",k=NOTKEY,disabled=True)
    btn_next=ClearB(mdi('arrow-right'),size="32",k=NOTKEY,disabled=True)
    btn_hist=ClearB(mdi('chevron-down'),size="32",k=NOTKEY)
    btn_ref=ClearB(mdi('refresh'),size="32",k=NOTKEY)

    def on_btn_sort(ins):
        _app=get_kvApp()
        if not _app.top_widget:
            ins.show_menu()
        else:
            _app.remove_top_widget()
    btn_sort=ClearB(mdi('sort',size=20)+" Filter",size="x80",k=NOTKEY,on_press=on_btn_sort)

    def pre_open_sort(ins,menu):
        # print(menu)
        l = kvw.ToggleButtonBehavior.get_widgets('_sortmethod')
        ins.root.input_search.text=''

        for i,li in enumerate(l):
            # print(li.active)
            if i==menu.sort_mode:
                li.active=True
            else:
                li.active=False
            # li.active=menu.default[i]

        del l

        fm = kvw.ToggleButtonBehavior.get_widgets('_folder')
        for i,fmi in enumerate(fm):
            if i==menu.folder_mode:
                fmi.state="down"
            else:
                fmi.state="normal"
        del fm
    btn_apply_sort=ClearRoundButton('Apply',bcolor_normal=[.345, .345, .345, 1],lcolor='',r=10,size="y32",k=NOTKEY)
    def on_btn_apply_sort(ins):
        _app=get_kvApp()
        l = kvw.ToggleButtonBehavior.get_widgets('_sortmethod')
        # new_def=[1,0,0,0,0,0]
        for i,li in enumerate(l):
            # print(li.active)
            if li.active:
                ins.parent.sort_mode=i
            # new_def[i]=li.active
        # print(new_def)
        del l

        fm = kvw.ToggleButtonBehavior.get_widgets('_folder')
        for i,fmi in enumerate(fm):
            if fmi.state=='down':
                ins.parent.folder_mode=i
        del fm

        # ins.parent.default=new_def
        _app.remove_top_widget()
        
        # ins.root.btn_ref.trigger_action()
        opath=ins.root.label_path.path
        ins.root.label_path.path=None
        ins.root.filelist.data=[]
        Clock.schedule_once(lambda dt:ins.root.on_path(opath,from_sort=True),)

        
    btn_apply_sort.bind(on_release=on_btn_apply_sort)
    input_search=InputDark(hint_text=f"Search {cdir.name}",k=NOTKEY,write_tab=False)
    sort_menu=BoxitV(
            Label('Name',halign='left',padding=(4,0,0,0),k=NOTKEY,)*\
            LabelCheck(mdi('sort-alphabetical-ascending')+" A-Z",active=True,markup=True,group='_sortmethod',allow_no_selection=False,k=NOTKEY,)*\
            LabelCheck(mdi('sort-alphabetical-descending')+" Z-A",markup=True,group='_sortmethod',allow_no_selection=False,k=NOTKEY,),
            Label('Size',halign='left',padding=(4,0,0,0),k=NOTKEY,)*\
            LabelCheck(mdi('sort-reverse-variant')+" Smaller",markup=True,group='_sortmethod',allow_no_selection=False,k=NOTKEY,)*\
            LabelCheck(mdi('sort-variant')+" Bigger",markup=True,group='_sortmethod',allow_no_selection=False,k=NOTKEY,),
            Label('Date',halign='left',padding=(4,0,0,0),k=NOTKEY,)*\
            LabelCheck(mdi('sort-calendar-ascending')+" Newer",markup=True,group='_sortmethod',allow_no_selection=False,k=NOTKEY,)*\
            LabelCheck(mdi('sort-calendar-descending')+" Older",markup=True,group='_sortmethod',allow_no_selection=False,k=NOTKEY,),
            Label('Folders',halign='left',padding=(4,0,0,0),k=NOTKEY,)*ToggleButton('First',state='down',group='_folder',k=NOTKEY,)*ToggleButton('Last',group='_folder',k=NOTKEY,)*ToggleButton('Mix',group='_folder',k=NOTKEY,),
            input_search,
            # LabelCheck(mdi('sort-alphabetical-ascending')+" Name (A-Z)",active=True,markup=True,group='_sortmethod')*\
            # LabelCheck(mdi('sort-alphabetical-descending')+" Name (Z-A)",markup=True,group='_sortmethod'),
            # LabelCheck(mdi('sort-variant')+" Size (bigger)",markup=True,group='_sortmethod')*\
            # LabelCheck(mdi('sort-reverse-variant')+" Size (smaller)",markup=True,group='_sortmethod'),
            # LabelCheck(mdi('sort-calendar-ascending')+" Date (newer)",markup=True,group='_sortmethod')*\
            # LabelCheck(mdi('sort-calendar-descending')+" Date (older)",markup=True,group='_sortmethod'),
            btn_apply_sort,
            size='x400y200',
            bcolor='#2C2C2C',
            spacing=4,
            padding=4,
            k=NOTKEY,
            )
    input_search.bind(on_text_validate=lambda x:btn_apply_sort.trigger_action())
    sort_menu.sort_mode=4
    sort_menu.folder_mode=1
    # sort_menu.default=[1,0,0,0,0,0]

    AddMenu(
        btn_sort,
        sort_menu,
            touch_up_buttons=(
                # "left","right"
                ),
            menu_close_touch_buttons=(),
            position_to='main',
            on_pre_open=pre_open_sort
        )
    
    # def on_search(ins):
    #     q=ins.text.lower()
    #     if not q:
    #         ins.root.filelist.data=ins.root.filelist.odata
    #         return
    #     odata=ins.root.filelist.data
    #     ins.root.filelist.odata=odata
    #     ndata=[]
    #     for di in odata:
    #         if q in di['meta'].name.lower():
    #             ndata.append(di)
    #     ins.root.filelist.data=ndata

        
    # input_search.bind(on_text_validate=on_search)


    top_bar=BoxitH(
                btn_prev,
                btn_next,
                btn_hist,
                # ClearB(mdi('arrow-left'),size="32"),
                # ClearB(mdi('arrow-right'),size="32"),
                btn_up,
                btn_ref,
                label_path_box,
                Void(size="x16"),
                # input_search,
                btn_sort,
                size='y35',
                k=NOTKEY,
                )
    # print()
    icons=utils.FileIconFinder(mdi('file-question',size=25))

    common_paths=utils.get_common_paths()
    for cp0 in common_paths:
        break
    del common_paths[cp0]
    cp0=pathlib.Path(cp0)


    shortcut_list=[]
    for cp,ctype in common_paths.items():
        si=pathlib.Path(cp)
        siname=si.name
        if not siname:
            siname=si.drive
            if not siname:
                siname='#Root'
        # print(si.name)
        shortcut_list.append(
            dict(
                # text=icons.get(si.name)+f' {si.name}',
                text=icons.get(ctype)+f' {siname}',
                markup=True,lcolor='',halign='left',valign='middle',
                height=35,size_hint_y=None,
                # selectable=True,do_highlight=True,
                meta=si

                )
            )
    refresh_storage=[
    dict(
        selectable=False,
        buttonbehavior=True,
        # text=f"&bl;{mdi('refresh',size=20)} Storage units&br;",
        text=f"{mdi('refresh',size=20)} [u]Storage units[/u]",
        # tooltip_text="Reload storage devices list",
        # font_size=20,
        do_highlight=False,
        markup=True,
        halign='left',
        valign='middle',
                height=30,size_hint_y=None,
                width=120,size_hint_x=None,
                lcolor='gray',
                on_release=lambda rv,i:rv.refresh(),
        color='#4CCE70',
        # lcolor="xkcd:dark grey",
                # on_touch_up=print,
                # lcolor='dark grey',
        # font_size=25
        )
    ]
    shortcuts=ListBox(
                    # shortcut_list+[
                    # dict(bcolor_normal='gray',height=1,size_hint_y=None,bcolor_down='')
                    # ]+storage_list,
                    # shortcut_list+refresh_storage+storage_list,
                    # size_hint_x=.2,
                    width=135,
                    size_hint_x=None,
                    spacing=2,
                    # size_hint_min_x=300,
                    k=NOTKEY,
                    )
    shortcuts.base_shortcuts=shortcut_list+refresh_storage
    def shortcuts_refresh(self,*x):
        storage_paths={}
    
        for d in psutil.disk_partitions():
            dp=pathlib.Path(d.mountpoint).resolve()
            # print(dp,cp0,dp==cp0)
            # if cp0!=dp:
            if 'removable' in d.opts:
                storage_paths[dp]='usb'
            else:
                storage_paths[dp]='storage'
        storage_list=[]
        for si,ctype in storage_paths.items():
            # si=pathlib.Path(cp)
            siname=si.name
            if not siname:
                siname=si.drive
                if not siname:
                    siname='#Root'
            # print(si.name)
            storage_list.append(
                dict(
                    # text=icons.get(si.name)+f' {si.name}',
                    text=icons.get(ctype)+f' ({siname})',
                    markup=True,lcolor='',halign='left',valign='middle',
                    height=35,size_hint_y=None,
                    # selectable=True,do_highlight=True,
                    meta=si

                    )
                )
        self.data=self.base_shortcuts+storage_list

    shortcuts.refresh=types.MethodType(shortcuts_refresh,shortcuts)
    shortcuts.refresh()
    # storages=ListBox(
    #                 storage_list,
    #                 size_hint_x=.25
    #                 )

    resize_shortcut=Splitter(
                # storages,

                shortcuts,
                # size_hint_min_x=300,
                # size_hint_x=.2,
                width=135,
                size_hint_x=None,

                strip_size=8,
                min_size=135,
                k=NOTKEY,
                )
    resize_shortcut.bind(height=lambda *x:setattr(shortcuts,'scroll_y',1))
    bh=BoxitH(k=NOTKEY,)
    bar_width=15
    filelist=Rowlist(spacing=2,k=NOTKEY,bar_width=bar_width,focus_color=focus_color)
    rlt_box=BoxitV(
        Fill(size=(0,bar_width),size_hint=(1,None))*FlatButton(mdi('chevron-up',size=bar_width),size=f'{bar_width}',k=NOTKEY,lcolor='',
            on_release=lambda ins:setattr(filelist,'scroll_y',1)
            ),
        filelist,
        Fill(size=(0,bar_width),size_hint=(1,None))*FlatButton(mdi('chevron-down',size=bar_width),size=f'{bar_width}',k=NOTKEY,lcolor='',
            on_release=lambda ins:setattr(filelist,'scroll_y',0)
            ),
        k=NOTKEY
        )
    bh.add_widget(resize_shortcut)
    bh.add_widget(rlt_box)
    # bh.add_widget(filelist)
    ################################################################################
    # kel=BoxitV(
    #         top_bar,
    #         SeparatorH(size=(1,1)),
    #         bh,
    #     k=NOTKEY,

    #     spacing=4,
    #     )
    class kvFilelist(kvw.BoxLayoutB):
        orientation='vertical'
        spacing=4
        padding=[4,4,4,4]
        file_types_filter=kvw.ListProperty([])
        def __init__(self,**kwargs):
            self.register_event_type('on_selection')
            self.register_event_type('on_file_double_click')
            self.register_event_type('on_directory')
            super(kvFilelist,self).__init__(**kwargs)
        def on_selection(self,rv,values):
            pass
        def on_file_double_click(self,rv,values):
            pass
        def on_directory(self,pathlib_path):
            pass
        def refresh(self):
            self.btn_ref.trigger_action()
        # def _get_dir(self):
        #     return self.label_path.path
        # def _set_dir(self,v):
        #     self.on_path(v)
        # path=kvw.AliasProperty(_get_path,_set_path)

    
    kel=skivify_v2(kvFilelist,k=k,file_types_filter=file_types_filter,**kw)
    kel.add_widget(top_bar)
    kel.add_widget( SeparatorH(size=(1,1)) )
    kel.add_widget(bh)
    ################################################################################



    kel.icons=icons
    kel.load_from_path=types.MethodType(load_from_path, kel)

    kel.btn_sort=btn_sort
    btn_sort.root=kel

    kel.filelist=filelist
    filelist.root=kel
    kel.label_path=label_path
    label_path.root=kel
    kel.shortcuts=shortcuts
    shortcuts.root=kel
    kel.path_input=path_input
    path_input.root=kel
    input_search.root=kel
    kel.input_search=input_search
    btn_apply_sort.root=kel
    kel.btn_apply_sort=btn_apply_sort
    kel.sort_menu=sort_menu
    sort_menu.root=kel

    def on_prev(ins):
        # print(ins.root.history.get_history())
        ins.root.on_path(ins.root.history.back(),is_navigation=True)
        # print(ins.root.history.back())
    def on_next(ins):
        # n=ins.root.history.forward()
        # print(n)
        # if not n:
        #     print(ins.root.history.get_history_state())
        ins.root.on_path(ins.root.history.forward(),is_navigation=True)
        # print(ins.root.history.get_history())
    
    def on_hist(ins):
        _app=get_kvApp()
        if ins.is_open:
            ins.root.top_bar.close_menu()
        else:
            ins.root.top_bar.show_menu()
    def on_hist_menu_parent(ins,parent):
        # print(ins,parent)
        if parent:
            ins.root.btn_hist.is_open=True
        else:
            ins.root.btn_hist.is_open=False

    def on_pre_hist_open(ins,menu):
        # ins.text=mdi('chevron-up')
        # print()
        hs=ins.root.history.get_history_state()
        full_stack=hs['back_stack']+hs['forward_stack']
        if not full_stack:
            return False
        data=[]
        _data=set()
        for hi in reversed(full_stack):
            if hi not in _data:
                data.append(
                    dict(
                        text=f"{hi}",height=25,size_hint_y=None,meta=hi
                        )
                    )
                _data.add(hi)
        # print(data)
        menu.data=data
        menu.height=min((len(data)*25,150))
        ins.root.btn_hist.is_open=True
        ins.root.hist_list.scroll_y=1
        # ins.root.hist_list.data=data
        # Clock.schedule_once(lambda dt:setattr(ins.root.hist_list,'data',data))
    def on_hist_selection(rv,ins,sel):
        di=rv.data[sel[0]]['meta']
        rv.root.on_path(di)

    hist_list=ListBox(size_hint_y=None,size_hint_max_y=90,bcolor='#2C2C2C',bind=dict(on_selection=on_hist_selection),k=NOTKEY,)
    hist_list.bind(parent=on_hist_menu_parent)
    AddMenu(
        top_bar,
        hist_list,
        position_to='main',
        touch_up_buttons=('right',),
        # menu_close_touch_buttons=(),
        on_pre_open=on_pre_hist_open
        )
    def on_btn_refresh(self):
        opath=self.root.label_path.path
        self.root.label_path.path=None
        self.root.filelist.data=[]
        Clock.schedule_once(lambda dt:self.root.on_path(opath),)



    btn_ref.root=kel
    kel.btn_ref=btn_ref

    btn_ref.bind(on_release=on_btn_refresh)

    btn_hist.is_open=False
    kel.hist_list=hist_list
    hist_list.root=kel
    kel.top_bar=top_bar
    top_bar.root=kel
    btn_next.root=kel
    btn_prev.root=kel
    btn_hist.root=kel
    kel.btn_hist=btn_hist
    kel.btn_next=btn_next
    kel.btn_prev=btn_prev
    btn_prev.bind(on_release=on_prev)
    btn_next.bind(on_release=on_next)
    btn_hist.bind(on_release=on_hist)

    def update_nav_btns(self,dt):
        self.btn_next.disabled=not self.history.can_go_forward()
        self.btn_prev.disabled=not self.history.can_go_back()

    def on_path(self,cdir,is_navigation=False,from_sort=False):

        if not from_sort:
            self.input_search.text=''

        # print(cdir,self.label_path.path)
        # print(f"{} {cdir.is_dir() = }")
        # try:
        #     cdir.stat()
            
        # except:
        #     _app=get_kvApp()
        #     _app.infotip(f'Access is denied: error')
        if cdir and cdir!=self.label_path.path:
            self.history.visit(cdir,is_navigation=is_navigation)
            # print('path updated to',cdir)
            self.current_directory=cdir
            self.label_path.path=cdir
            self.label_path.text=path2parts(cdir)
            self.filelist.deselect_all()
            self.load_from_path(label_path.path)
            Clock.schedule_once(self.update_nav_btns)
            
    def on_ref_press(ins,v):
        npath=pathlib.Path(v)
        ins.root.on_path(npath)
        # npath=pathlib.Path(v)
        # if npath!=ins.path:
        #     ins.path=npath
        #     ins.root.on_path(ins.path)
    label_path.bind(on_ref_press=on_ref_press)
    def on_double_click(ins,index):
        di=ins.data[index]
        fi=di['meta']
        if fi.is_dir():
            ins.root.on_path(fi)
        else:
            ins.root.dispatch('on_file_double_click',ins,index)
    def on_btn_up(ins):
        # print(ins.root.label_path.path.parent)
        cpath=ins.root.label_path.path
        ins.root.on_path(cpath.parent)
    btn_up.root=kel
    btn_up.bind(on_release=on_btn_up)

        # print(ins.data[index])
    filelist.bind(on_double_click=on_double_click)
    filelist.bind(on_selection=lambda rv,grid,values:kel.dispatch('on_selection',rv,values))

    # filelist.bind(on_selection=kel.events)

    kel.history=utils.NavigationHistory()
    kel.history.visit(cdir)
    kel.update_nav_btns=types.MethodType(update_nav_btns, kel)
    kel.on_path=types.MethodType(on_path, kel)


    def get_human_readable_size(self,path, decimal_places = 0):
        """Return human-readable file size string.
        
        Args:
            path: Path object to check
            decimal_places: Number of decimal places to show
            
        ## Returns:
            Formatted size string with appropriate unit
        """
        size_bytes = path.stat().st_size
        
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.{decimal_places}f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.{decimal_places}f} TB"
    def get_KB_size(self,path_stat, decimal_places = 0):
        """Return human-readable file size string.
        
        Args:
            path: Path object to check
            decimal_places: Number of decimal places to show
            
        ## Returns:
            Formatted size string with appropriate unit
        """
        _stat_result=path_stat
        size_bytes = _stat_result.st_size
        # setattr(path,'_stat_result',_stat_result)
        size_bytes/=1024
        return f"{size_bytes:.{decimal_places}f} KB"
    def get_mtime(self,path_stat):
        t = time.localtime(path_stat.st_mtime)
        # return f"{t.tm_mday:02d}/{t.tm_mon:02d}/{t.tm_year} {t.tm_hour:02d}:{t.tm_min:02d}:{t.tm_sec:02d}"
        return f"{t.tm_mday:02d}/{t.tm_mon:02d}/{t.tm_year} {t.tm_hour:02d}:{t.tm_min:02d}"
    kel.get_human_readable_size=types.MethodType(get_human_readable_size,kel)
    kel.get_KB_size=types.MethodType(get_KB_size,kel)
    kel.get_mtime=types.MethodType(get_mtime,kel)


    def on_shortc_selection(rv,ins,indxs):
        if indxs:
            # print(rv.data[indxs[0]]['meta'])
            rv.root.on_path(rv.data[indxs[0]]['meta'])
    shortcuts.bind(on_selection=on_shortc_selection)
    kel.on_path(cdir)

    return kel


###################################
# MATPLOTLIB
###################################
@skwidget
def MPLFigure(k=None,**kwargs):
    from kivy_matplotlib_widget.uix.graph_widget import MatplotFigure as kvWd
    return skivify(kvWd,k=k,**kwargs)
@skwidget
def MPLLegendRv(k=None,**kwargs):
    from kivy_matplotlib_widget.uix.legend_widget import LegendRv as kvWd
    return skivify(kvWd,k=k,**kwargs)
@skwidget
def MPLLegendRvHorizontal(k=None,**kwargs):
    from kivy_matplotlib_widget.uix.legend_widget import LegendRvHorizontal as kvWd
    return skivify(kvWd,k=k,**kwargs)
MPLLegendRvH=MPLLegendRvHorizontal

@skwidget
def MPLFigureScatter(k=None,**kwargs):
    from kivy_matplotlib_widget.uix.graph_widget_scatter import MatplotFigureScatter as kvWd
    return skivify(kvWd,k=k,**kwargs)
@skwidget
def MPLFigureTwinx(k=None,**kwargs):
    from kivy_matplotlib_widget.uix.graph_widget_twinx import MatplotFigureTwinx as kvWd
    return skivify(kvWd,k=k,**kwargs)
@skwidget
def MPLFigureCropFactor(k=None,**kwargs):
    from kivy_matplotlib_widget.uix.graph_widget_crop_factor import MatplotFigureCropFactor as kvWd
    return skivify(kvWd,k=k,**kwargs)
@skwidget
def MPLFigureGeneral(k=None,**kwargs):
    from kivy_matplotlib_widget.uix.graph_widget_general import MatplotFigureGeneral as kvWd
    return skivify(kvWd,k=k,**kwargs)

@skwidget
def MPLFigureSubplot(k=None,**kwargs):
    from kivy_matplotlib_widget.uix.graph_subplot_widget import MatplotFigureSubplot as kvWd
    return skivify(kvWd,k=k,**kwargs)
@skwidget
def MPLFigure3D(k=None,**kwargs):
    from kivy_matplotlib_widget.uix.graph_widget_3d import MatplotFigure3D as kvWd
    return skivify(kvWd,k=k,**kwargs)
@skwidget
def MPLFigure3DLayout(k=None,**kwargs):
    from kivy_matplotlib_widget.uix.graph_widget_3d import MatplotFigure3DLayout as kvWd
    return skivify(kvWd,k=k,**kwargs)
@skwidget
def MPLKivyNavToolbar(k=None,**kwargs):
    from kivy_matplotlib_widget.uix.navigation_bar_widget import KivyMatplotNavToolbar as kvWd
    return skivify(kvWd,k=k,**kwargs)
def MPLNavToolbar(k=None,**kwargs):
    from kivy_matplotlib_widget.uix.navigation_bar_widget import MatplotNavToolbar as kvWd
    return skivify(kvWd,k=k,**kwargs)
###################################
def AddNavigation(focus_map={},widget=None, focus_color=None,focus_action=None,disable_fallback_nav=False):
    if widget:
        isbox=getattr(widget,'_isbox',None)
        if isbox=='vertical':
            up=focus_map.pop('up',None)
            down=focus_map.pop('down',None)

            nchildren=0
            c=0
            focusable_children=[]
            for child in reversed(widget.children):
                if hasattr(child,'focus_map'):
                    if focus_color:
                        child.focus_color=focus_color
                    if not child.focus_action:
                        child.focus_action=focus_action

                    focusable_children.append(child)
                    c+=1
                    nchildren=c
            # print(f"{nchildren = }")
            for c,child in enumerate(focusable_children):
                base_focus_map=focus_map.copy()
                if disable_fallback_nav:
                    child.disable_fallback_nav=disable_fallback_nav
                    try:
                        base_focus_map.update({'up':focusable_children[c-1]})
                    except:
                        pass
                    try:
                        base_focus_map.update({'down':focusable_children[c+1]})
                    except:
                        pass

                if c==0:
                    if up!=None:
                        base_focus_map['up']=up
                    else:
                        base_focus_map['up']=focusable_children[-1].id
                elif c+1==nchildren:
                    if down!=None:
                        base_focus_map['down']=down
                    else:
                        base_focus_map['down']=focusable_children[0].id

                base_focus_map.update(child.focus_map)
                child.focus_map=base_focus_map
                # print(child.id,':',child.focus_map)
        if isbox=='horizontal':
            left=focus_map.pop('left',None)
            right=focus_map.pop('righ',None)

            nchildren=0
            c=0
            focusable_children=[]
            for child in reversed(widget.children):
                if hasattr(child,'focus_map'):
                    if focus_color:
                        child.focus_color=focus_color
                    if not child.focus_action:
                        child.focus_action=focus_action

                    focusable_children.append(child)
                    c+=1
                    nchildren=c
            # print(f"{nchildren = }")
            for c,child in enumerate(focusable_children):
                base_focus_map=focus_map.copy()
                if disable_fallback_nav:
                    child.disable_fallback_nav=disable_fallback_nav
                    try:
                        base_focus_map.update({'left':focusable_children[c-1]})
                    except:
                        pass
                    try:
                        base_focus_map.update({'right':focusable_children[c+1]})
                    except:
                        pass
                
                if c==0:
                    if left!=None:
                        base_focus_map['left']=left
                    else:
                        base_focus_map['left']=focusable_children[-1].id
                elif c+1==nchildren:
                    if right!=None:
                        base_focus_map['right']=right
                    else:
                        base_focus_map['right']=focusable_children[0].id

                base_focus_map.update(child.focus_map)
                child.focus_map=base_focus_map
                # print(child.id,':',child.focus_map)
    return widget



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
    #     # kwargs=_preprocess(**kwargs)
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