import sys
import os
import pathlib
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

def locked_screen(func):
    def wrapper(*args,**kwargs):
        self=get_kvApp()
        self.lock()
        # def do(*args,**kwargs):
        #     self.sleep_in_thread(1)
        #     ans=func(*args,**kwargs)
        #     self.unlock()
        #     return ans
        # Clock.schedule_once(lambda dt: do(),.1)
        
        future=self.poolt.submit(func,*args,**kwargs)
        # future=self.poolt.submit(do,*args,**kwargs)
        future.add_done_callback(lambda f:self.unlock())
        # result=func(*args,**kwargs)
        # return future.result()
        return future
    return wrapper

def skwidget(f):
    def args_preprocessor(*args, **kwargs):
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
        return kel

    wrap=args_preprocessor
    # Copy all the important metadata
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    wrap.__module__ = f.__module__
    wrap.__qualname__ = f.__qualname__
    wrap.__annotations__ = getattr(f, '__annotations__', {})
    
    # Try to copy signature if available (Python 3.3+)
    wrap.__signature__ = signature(f)
    
    wrap.__widget_ctor__=f.__name__
    
    # Copy annotations (type hints)
    # if hasattr(f, '__annotations__'):
    #     wrap.__annotations__ = f.__annotations__
    if not wrap.__doc__:
        wrap.__doc__=_docs.tbd_widfun
    #     wrap.__doc__+=_docs.com
    # else:
    #     wrap.__doc__=_docs.com

    return wrap

def _widget_ctor(f):
    def args_preprocessor(*args, **kwargs):
        kel = f(*args, **kwargs)
        return kel
    wrap=args_preprocessor
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
    # window_is_maximized = BooleanProperty(False)
    # _top_widget=None
    # _subtop_widget=None
    # def _get_tw(self):
    #     return self._top_widget
    # def _set_tw(self,v):
    #     self._top_widget=v
    #     return True
    # top_widget=kvw.AliasProperty(_get_tw,_set_tw)
    # def _get_stw(self):
    #     return self._subtop_widget
    # def _set_stw(self,v):
    #     self._subtop_widget=v
    #     return True
    # subtop_widget=kvw.AliasProperty(_get_stw,_set_stw)
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

        # self._is_windows = True if platform.lower()=='win' else False
        self.Clock=Clock
        self.mdi=mdi
        
        self.kvWindow=utils.Window

        # minimum_width=kwargs.pop('minimum_width',None)
        # minimum_height=kwargs.pop('minimum_height',None)
        # minimum_size=kwargs.pop('minimum_size',None)
        # if minimum_width!=None:
        #     self.minimum_width=minimum_width
        # if minimum_height!=None:
        #     self.minimum_height=minimum_height
        # if minimum_size!=None:
        #     self.minimum_size=minimum_size

        self.post_actions=[]
        
        size=kwargs.pop('size',None)
        location=kwargs.pop('location',None)
        # if size:
        #     self.post_actions.append(action(self.Resize,*size))
        # if location:
        #     left,top=location
        #     if left!=None:
        #         self.post_actions.append(action(setattr,self.kvWindow,'left',location[0]))
        #     if top!=None:
        #         self.post_actions.append(action(setattr,self.kvWindow,'top',location[1]))
        # def _do_maximize(*largs):
        #     self.window_is_maximized = True
        # def _do_restore(*largs):
        #     self.window_is_maximized = False
        # self.kvWindow.bind(on_maximize=_do_maximize, on_restore=_do_restore)

        # if custom_titlebar:
        #     pass
        #     self.kvWindow.custom_titlebar=True
        #     try:
        #         first_el=layout[0][0]
        #     except:
        #         first_el=layout[0]
        #     self.kvWindow.set_custom_titlebar(first_el)
        #     tbw=self.kvWindow.titlebar_widget
        #     if hasattr(tbw,'children'):
        #         _ensure_bttn_not_draggable(tbw.children)

        self.title=title
        self.poolt=ThreadPoolExecutor(thread_name_prefix='MiniApp')
        self.queue={}
        # self._leaving=False

        # self._filebrowser={}
        # self._lock=None

        self._nk=0
        class IDS(dict):
            def __getattr__(self,name):
                return self.__getitem__(name)

        global ids
        self.ids=IDS()
        self._ids={}
        if not layout_class:
            rows=len(layout)
            # self._layout=kvw.GridLayoutB(rows=rows,**_preproces(**layout_args))
            self._layout=skivify(kvw.GridLayoutB,k=k,rows=rows,**layout_args)
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
                    # if kivy_el.id in ids:
                    #     del ids[kivy_el.id]
                    # kivy_el.id=NOTKEY
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
            try:
                self._layout=layout_class(k=k,**layout_args)
            except:
                self._layout=skivify(layout_class,k=k,**layout_args)
            for kivy_el in layout:
                # kivy_el.id=NOTKEY
                # if kivy_el.id in ids:
                #     del ids[kivy_el.id]
                self._layout.add_widget(kivy_el)
        self._triggers={}
        self.event_manager=event_manager
        self.thread_event=self.submit_thread_event
        self.thread_event_at=self.submit_thread_event_at
        # self.get_group=kvw.ToggleButtonBehavior.get_widgets
        self.hidden={}

        # self.remove_on_click = False
        # def on_touch_down(instace, touch):
        #     if self.remove_on_click and touch.button in ('left','middle','right'):
        #         self.remove_top_widget()
        # self._layout.bind(on_touch_down=on_touch_down)

        _future_process_elements(self)
        _post_process_elements(self)
        _future_process_binds(self)

        self.paw=self.process_added_widgets
        self.Clock.schedule_once(lambda dt: setattr(self,'alpha',alpha))
        
        # self._keep_on_top=keep_on_top
        # self.Clock.schedule_once(lambda dt: setattr(self,'keep_on_top',keep_on_top))

        # self._hwnd=None
        
        # if icon=='skdata/logo/simplekivy-icon-32.png':
        #     self.ico=resource_find('skdata/logo/simplekivy-icon-256.ico')

        # Clock.schedule_once(lambda dt: self.on_icon(self,self.get_application_icon()))
        # super().__init__(icon=icon,**kwargs)

    def __getattr__(self,name):
        # print(name)
        # Redirect to parent
        # self.APP=App.get_running_app()
        # parent_attrs=(
        #     'sleep_in_thread',
        #     'on_stop',
        #     'is_leaving',
        #     '_leaving',
        #     )
        # for pattr in parent_attrs:
        #     setattr(self,pattr,getattr(self.APP,pattr))

        ####################
        return getattr(App.get_running_app(),name)
        # except:
        #     raise AttributeError(f"'{self}' object has no attibute '{name}'.")

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
                    kw=_preproces(**{prop:val})
                    trigger=Clock.create_trigger(lambda *args:setattr(widget,prop,kw[prop]),timeout)
                    trigger()
                else:
                    trigger=Clock.create_trigger(lambda *args:setattr(widget,prop,val),timeout)
                    trigger()
            else:
                kwargs=_preproces(**kwargs)
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
    def schedule_get_call(self,key,method,*args,**kwargs):
        Clock.schedule_once(lambda dt:getattr(self.ids[key],method)(*args,**kwargs))
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

    @property
    def app(self):
        return self

    @property
    def main_app(self):
        return utils.get_kvApp()

    @property
    def id(self):
        return self._layout.id


class MyApp(App):
    '''
    A complete overhaul of how the `App` object is created.

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

    `event_manager`: `function` or `EventManager` instance. Must accept at least two positional arguments `app` and `event`.
    
    ```py
    def evman(app, event):
        pass
    app=sk.MyApp(
        ...
        event_manager = evman
        ...
    )
    ```

    `ico (str)`: Path to an `*.ico` file. Needed for file dialogs (`askdirectory`, `askopenfile`, etc.) in in Windows platforms only.

    `poolt`: Initialized as `ThreadPoolExecutor(thread_name_prefix='SimpleKivy')`.  You can use it to submit threaded tasks.

    `queue (dict)`: Don't overwrite it. This dict is populated by the `thread_pool_new` method.

    ## Methods

    `process_added_widgets()`: Call this after creating `SimpleKivy` widgets. Finishes processing widgets and incorporating them to the `MyApp` instance.

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
    > - `widget (Widget)`: Widget (sets as `MyApp.top_widget` value).
    > - `remove_on_click (bool)`: Whether the `top_widget` will be removed automatically when a mouse click event is detected.

    `remove_top_widget()`: Remove the current `top_widget` if any.
    
    `add_top_widget(widget, remove_on_click=True)`: Adds a subtop widget to be shown on top of other widgets, besides the `top_widget`.
    > - `widget (Widget)`: Widget (sets as `MyApp.subtop_widget` value).
    > - `remove_on_click (bool)`: Whether the `subtop_widget` will be removed automatically when a mouse click event is detected.

    `remove_subtop_widget()`: Remove the current `subtop_widget` if any.

    `infotip`: Shows an infotip.
    `infotip_schedule`: Schedules an infotip to be shown in the next frame.

    `infotip_remove_schedule`: Schedules the `top_widget` to be removed in the next frame.

    `disable_widgets(*widgets)`: Sets `disabled = True` of the positional arguments `*widgets` given:
    > - `*widgets`: One or many `str` or `Widget` values. If `str`, must be a widget id.
    
    `enable_widgets(*widgets)`: Sets `disabled = False` of the positional arguments `*widgets` given:
    > - `*widgets`: One or many `str` or `Widget` values. If `str`, must be a widget id.
    
    `Resize(width, height)`: Setes the Window size.

    `bring_to_front()`: Brings the Window to the front of all other opened programs.

    `__call__(k,prop=None,val=None,timeout=0,_kw_prepro=False,ignore_errors=False,**kwargs)`: You can call a `MyApp` instance as if it were a function to schedule property changes.

    > Example:
    ```py
    app(k='label_widget_id',text='New text', haling='right')
    ```

    `dt_call(k,prop=None,val=None,_kw_prepro=False,ignore_errors=False,**kwargs)`: Returns a `lambda` function that calls `MyApp.__call__` with the given arguments.

    `schedule_call_once(k,prop=None,val=None,timeout=0,_kw_prepro=False,ignore_errors=False,**kwargs)`: Schedules `MyApp.__call__` with the given arguments to be called in the next frame.

    `schedule_call_interval(k,prop=None,val=None,timeout=0,_kw_prepro=False,ignore_errors=False,**kwargs)`: Schedules `MyApp.__call__` with the given arguments to be called every `timeout` seconds.
    
    `trigger_event(event,*args,**kwargs)`: Gets or creates a trigger for the event. The trigger created will call the `event_manager` with the given arguments.

    `schedule_event_once(event,*args,timeout=0,**kwargs)`: Schedule a call of the `event_manager` for the next frame with the given arguments.

    `schedule_func_once(func,*args,timeout=0,**kwargs)`: Schedule a function to be called in the next frame with the given arguments.

    `schedule_get_call(key,method,*args,**kwargs)`: Schedule once a call to the method named `method` of a widget with ID `key`, and with the given arguments `*args` and `**kwargs`.

    `submit_thread_event(event,*args,**kwargs)`: Submits a call of the `event_manager` in the `poolt` thread pool with the given arguments. Aliases: `thread_event`

    `submit_thread_event_at(thread_name,event,*args,**kwargs)`: Submits a call of the `event_manager` in the `queue[thread_name]` thread pool with the given arguments. Aliases: `thread_event_at`

    `call_event(event,*args,**kwargs)`: Calls the `event_manager` with the given arguments.

    `keys()`: Shortcut to `MyApp.ids.keys()`.
    `values()`: Shortcut to `MyApp.ids.values()`.
    `items()`: Shortcut to `MyApp.ids.items()`.

    `AskOpenFile(initialdir: str, filetypes: tuple or list, callback: function or None, **kw)`: Creates a `SimpleKivy` file dialog to open a file.
    {initialdir}
    {filetypes}
    {filedialog_callback}
    {filedialog_kw}

    `AskDirectory`: Creates a `SimpleKivy` file dialog to open a directory.
    {initialdir}
    {filedialog_callback}
    {filedialog_kw}

    `askdirectory`: Creates a native platform file dialog to open a directory.
    {initialdir}
    {filedialog_callback}
    {filedialog_kw}

    `askopenfile`: Creates a native platform file dialog to open a file.
    {initialdir}
    {filetypes}
    {filedialog_callback}
    {filedialog_kw}

    `askopenfiles`: Creates a native platform file dialog to open multiple files.
    {initialdir}
    {filetypes}
    {filedialog_callback}
    {filedialog_kw}

    `asksaveasfile`: Creates a native platform file dialog to save a file as the input name and location.
    {initialfile}
    {filetypes}
    {filedialog_callback}
    {filedialog_kw}
    
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
        layout_args={},
        icon='skdata/logo/simplekivy-icon-32.png',
        layout_class=None,
        do_auto_config=True,
        **kwargs
        ):
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

        self._filebrowser={}
        self._lock=None

        self._nk=0
        class IDS(dict):
            def __getattr__(self,name):
                return self.__getitem__(name)
        # self.ids={}
        self.ids=IDS()
        # self.ids.__getattr__=types.MethodType(ids.__getitem__, ids)
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

    def popup_message(self,msg='message',title="Message",auto_dismiss=-1,**kw):
        pop=Popup(
            title=title,
            content=Label(msg,k=NOTKEY,**kw),
            size_hint=(.3,.3),
            k=NOTKEY)
        if auto_dismiss>0:
            pop.bind(on_open=lambda ins:Clock.schedule_once(ins.dismiss,auto_dismiss))
        def on_dismiss(ins):
            del ins
        pop.bind(on_dismiss=on_dismiss)
        pop.open()

    def lock(self):
        if not self._lock:
            box=BoxitAngle(Label(mdi('dots-circle'),font_size=40,markup=True,k=NOTKEY),k=NOTKEY,
                # bcolor='dark grey'
                )
            def rotate_start(self,*args):
                fps=1/30
                self.rotate_stop()
                Clock.schedule_interval(self.do_rotate,fps)
            def rotate_stop(self,*args):
                Clock.unschedule(self.do_rotate)
            def do_rotate(self,dt):
                self.angle=self.angle+5
            box.do_rotate=types.MethodType(do_rotate,box)
            box.rotate_start=types.MethodType(rotate_start,box)
            box.rotate_stop=types.MethodType(rotate_stop,box)
            
            self._lock=ModalView(
                # box,
                auto_dismiss=False,
                size_hint=(1,1),
                background_color=[0,0,0,0],
                k=NOTKEY,
                background=''
                # on_open=box.rotate_start,
                # on_dismiss=box.rotate_stop,
                )
        self._lock.open()
    def unlock(self):
        if self._lock:
            self._lock.dismiss()
    
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
    def AskDirectory(self,
        initialdir='./',
        callback=None,
            **kw,
        ):
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
        title - the title of the window
        initialdir - the directory that the dialog starts in
        initialfile - the file selected upon opening of the dialog
        filetypes - a sequence of (label, pattern) tuples, ‘*’ wildcard is allowed
        defaultextension - default extension to append to file (save dialogs)
        multiple - when true, selection of multiple items is allowed
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



def TEST_WIDGET(w,event_manager=None):
    lyt=[[w]]
    MyApp(layout=lyt,event_manager=event_manager).run()

@skwidget
def Label(text='',k=None,focus_behavior=False,halign='center',size_behavior='normal',valign='middle',hover_highlight=False,**kwargs):
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
def Video(source='',k=None,**kwargs):
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
    kel=skivify_v2(kvWd,k=k,source=source,**kwargs)
    return kel

@skwidget
def VideoPlayer(source='',k=None,**kwargs):
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
    kel=skivify_v2(kvWd,k=k,source=source,**kwargs)
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
def ModalView(widgets=[],k=None,enable_events=False,on_event='on_pre_open',**kwargs):
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
    
    `BoxLayout, TextInput, Button`

    {base_params}
    '''

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


    kel=skivify(_,texts=texts,**kwargs)


    
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
    # kwargs=_preproces(**kwargs)
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
def BoxitH(*widgets,k=None,orientation='horizontal',**kwargs):
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
    
    `BoxLayout, Label, CheckBox`

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

    # kwargs=_preproces(**kwargs)
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
def Grid(layout=[[]],k=None,navigation_behavior=False,**kwargs):
    '''
    Dynamic `BoxLayout` constructor.

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
def External(title="External window title",hwnd=None,k=None,
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
    kwargs=_preproces(**kwargs)
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
def BoxitV(*widgets,k=None,orientation='vertical',**kwargs):
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
def Relativeit(*widgets,k=None,**kwargs):
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
def Floatit(*widgets,k=None,**kwargs):
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
def Scatterit(*widgets,k=None,**kwargs):
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
    # kwargs=_preproces(**kwargs)

    from kivy.uix.scatterlayout import ScatterLayout as kvWd

    kel=skivify_v2(kvWd,k=k,**kwargs)

    for w in widgets:
        kel.add_widget(w)

    # _future_elements.append(kel)
    return kel
# Scatterit=Boxit_scatter

@skwidget
def ButtonBoxitAngle(*widgets,k=None,angle=0,enable_events=True,on_event="on_release",**kwargs):
    # kwargs=_preproces(**kwargs)

    kvWd=kvw.AngleBBoxLayout

    kel=skivify_v2(kvWd,k=k,angle=angle,enable_events=True,on_event=on_event,**kwargs)

    for w in widgets:
        kel.add_widget(w)

    # _future_elements.append(kel)

    # kel.size=kwargs.get('size',(100,100))
    # kel.size_hint=kwargs.get('size',(1,1))

    return kel
# ButtonBoxitAngle=Boxit_angle_bbox

@skwidget
def BoxitAngle(*widgets,k=None,angle=0,enable_events=True,on_event="on_release",**kwargs):
    # kwargs=_preproces(**kwargs)

    kvWd=kvw.AngleBoxLayout

    kel=skivify_v2(kvWd,k=k,angle=angle,enable_events=True,on_event=on_event,**kwargs)

    for w in widgets:
        kel.add_widget(w)

    # _future_elements.append(kel)

    # kel.size=kwargs.get('size',(100,100))
    # kel.size_hint=kwargs.get('size',(1,1))
    return kel

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

    # kwargs=_preproces(**kwargs)
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
def FlatButton(text='flat_button',
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
    
    `BoxLayout, Label`

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
    
    `RelativeLayout, Label`

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
    return FlatRoundButton(*args,hover_highlight=hover_highlight,lcolor=lcolor,markup=markup,**kwargs)

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
def FlatButtonAngle(text='button',angle=90,enable_events=True,k=None,on_event='on_release', **kwargs):
    # kwargs=_preproces(**kwargs)
    # global _future_elements, _future_bind

    
    kvWd=kvw.FlatButtonAngle

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
    # kwargs=_preproces(**kwargs)
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

    kel=skivify(kvw.RV,k=k,enable_events=enable_events,effect_cls=effect_cls,on_event=on_event,data=data,keyboard_scroll=keyboard_scroll,
        # selected_color=selected_color,
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
    cell_defaults={'text':'','halign':'left','valign':'middle','shorten':True,'padding':4,'markup':True,'font_name':'segoeui.ttf'},
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
    kel=skivify(kvw.Rowlist,
        k=k,

        viewclass_cell=kvw.LabelB,
        cell_defaults=cell_defaults,
        viewclass_base=kvw.RowSelectable,
        
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
    # kwargs=_preproces(**kwargs)
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
    keyboard_scroll=True,
    **kwargs
    ):
    kel=skivify(kvw.Artistlist,k=k,enable_events=enable_events,on_event=on_event,data=data,keyboard_scroll=keyboard_scroll,**kwargs)
    
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
    # kwargs=_preproces(**kwargs)
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

    kel=skivify(W,text=text,k=k,multiline=multiline,enable_events=enable_events,on_event=on_event,**kwargs)
    return kel

Input=In=TextInput

@skwidget
def TextInputDark(text='',enable_events=False,multiline=False,k=None,on_event='on_text_validate', **kwargs):
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


    kel=skivify(kvWd,
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
    '''
    {: .prompt-warning }
    > Experimental widget. Imagine a fusion of Excel and Python.
    '''
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
    kel=skivify_v2(kvWd,value=value,min=min,max=max,k=k,enable_events=enable_events,on_event=on_event,**kwargs)
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
BarTouch=BarTouchH
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
    return Boxit(size=size,size_hint=size_hint,k=k,**kwargs)

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
    
    `@EventManager.unhandled`: Sets a callback for any event that is not catched by any other rule.
    
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
    def __init__(self):
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
        self.app=app
        try:
            callback=self.__events__[ev]
        except:
            if ev in self.__unhandled__:
                callback=self._
            else:
                callback=self.__test_rules__(ev)
        
        callback(app,ev,*args,**kwargs)
        # try:
        #     callback(app,ev,*args,**kwargs)
        # except Exception as e:
        #     traceback.print_exc()
            # pass
    def _(self,app,ev,*args,**kwargs):
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
    path_input=InputDark(k=NOTKEY,)
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
    input_search=InputDark(hint_text=f"Search {cdir.name}",k=NOTKEY)
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
    filelist=Rowlist(spacing=2,k=NOTKEY,bar_width=bar_width)
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