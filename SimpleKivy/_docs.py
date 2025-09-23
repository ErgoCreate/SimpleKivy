when_hover_highlight='''
## When created with *hover_highlight = True*

### Properties

{hover_properties}

### Events

{events_hover}
'''

common='''
`k: None, str, or NOTKEY`
> Key specification for quick acess:
> - `None`: Automatically sets an int value.
> - `str`: Use specific string key.
> - `NOTKEY`: Special flag indicating no key should be used.

`size: str or sequence of 2 ints`
> Size specification of the widget:

> - `str: "x{width}"`: Sets widget `width` and `size_hint_x = None`.
> - `str: "y{height}"`: Sets widget `height` and `size_hint_y = None`.
> - `str: "xchildren"`: Sets `size_hint_x = None` and binds this widget's width to the sum of the widths of its children.
> - `str: "ychildren"`: Sets `size_hint_y = None` and binds this widget's height to the sum of the heights of its children.
> - `str: "xchild_max"`: Sets `size_hint_x = None` and binds this widget's width to the child with the maximum width.
> - `str: "ychild_max"`: Sets `size_hint_y = None` and binds this widget's height to the child with the maximum height.

{: .prompt-info }
> *You can combine up to two of the above size string specifications.*

> - `str: "{number}"`: Processed as `size = (number, number)` and `size_hint = (None,None)`. *Cannot be combined with other string specifications*.

> - `sequence: (int, int)`: Size of the widget. Same as `Kivy`. Has no effect if `size_hint` argument is not set to `None`.

> Example:
```py
sk.WIDGET(size = "y35")
sk.WIDGET(size = "x120y35")
sk.WIDGET(size = "xchildreny40")
sk.WIDGET(size = "xchildrenychildren")
sk.WIDGET(size = "xchild_maxy40")
sk.WIDGET(size = "60")
sk.WIDGET(size = (120,35), size_hint = (None, None))
```

`enable_events: bool`
> Whether the widget will send events to the event_manager set in MyApp using the widgets `k/id` property as event identifier.
> - `True`: Triggers events.
> - `False`: Doesn't trigger events.

`on_event: str, iterable (tuple or list), dict`
> Defines which events/property changes will trigger the event_manager. Only has effect if `enable_events = True`.
> - `str`: Name of the event or property that will trigger the event_manager.
> - `iterable: [str, str, ...]`: Will trigger events for each name in the iterable.
> - `dict: {"{event_name}": callback}`: Calls `instance.bind(**on_event)` during widget creation.

> Example:
```py
sk.WIDGET(enable_events = True, on_event = 'width')
sk.WIDGET(enable_events = True, on_event = 'on_touch_down')
sk.WIDGET(enable_events = True, on_event = ['width','height','pos'])
sk.WIDGET(enable_events = True, on_event = {"size": lambda ins,v: print("size =",v)})
```

`do_dot_subevent: bool`
> Adds a "." to describe the event when triggering the event_manager.
> - `True`: The event identifier is `str(widget.id)+".{event_name}"`.
> - `False`: The event identifier is the same as the widget's `k/id`.
> Default is `False`.
'''

size_behavior='''`size_behavior: str`
> Defines special bindings for the behavior of text_size and size:
> - `"none"`: No binding between text_size and widget size.
> - `"normal"`: Binds text_size to widget size.
> - `"text"` or `"textv"`: This widgets's height will be set to the text content.
> - `"texth"`: This widgets's width will be set to the text content.
> Default is "normal".
'''

tbd_widfun='''
{: .prompt-info }
> The documentation of this widget creator function is under construction. Please come back at a latter date.
'''

tbd_method='''
{: .prompt-info }
> The documentation of this method is under construction. Please come back at a latter date.
'''

base_params='''
{: .prompt-info }
> This page only details the new or modified features. All other parameters inherit from the base Kivy widgets and can be found in the [official Kivy documentation](https://kivy.org/doc/stable).
'''

bgline='''
`bcolor, lcolor` and any other valid properties with ***color*** in their name can be specified with `sequence or str` during creation:
> - `sequence: [float, float, float, float]`: Sequence `(list or tuple)` of 4 `float` numbers (0.0-1.0). Same as `Kivy`.
> - `str: "{hex_string}"`: Hex color in the format `"#000000"`.
> - `str: "{named_color}"`: Name of a color from the [List of Named Colors](/posts/named_colors) supported by `SimpleKivy`.

>> `bcolor`: Background color of the widget.

>> `lcolor`: Line color of the widget.

`lwidth: number (float or int)`
> Width of the widget's border line.
'''

line='''
`lcolor` and any other valid properties with ***color*** in their name can be specified with `sequence or str` during creation:
> - `sequence: [float, float, float, float]`: Sequence `(list or tuple)` of 4 `float` numbers (0.0-1.0). Same as `Kivy`.
> - `str: "{hex_string}"`: Hex color in the format `"#000000"`.
> - `str: "{named_color}"`: Name of a color from the [List of Named Colors](/posts/named_colors) supported by `SimpleKivy`.

>> `lcolor`: Line color of the widget.

`lwidth: number (float or int)`
> Width of the widget's border line.
'''

bgline_state='''
`bcolor_normal, bcolor_down, bcolor, lcolor` and any other valid properties with ***color*** in their name can be specified with `sequence or str` during creation:
> - `sequence: [float, float, float, float]`: Sequence `(list or tuple)` of 4 `float` numbers (0.0-1.0). Same as `Kivy`.
> - `str: "{hex_string}"`: Hex color in the format `"#000000"`.
> - `str: "{named_color}"`: Name of a color from the [List of Named Colors](/posts/named_colors) supported by `SimpleKivy`.

>> `bcolor_normal`: Background color of the widget when `state="normal"`.

>> `bcolor_down`: Background color of the widget when `state="down"`.

>> `bcolor`: Current background color of the widget. Overwritten by widget's current state. Avoid setting it.

>>`lcolor`: Line color of the widget.

`lwidth: number (float or int)`
> Width of the widget's border line.
'''

bg_state='''
`bcolor_normal, bcolor_down, bcolor` and any other valid properties with ***color*** in their name can be specified with `sequence or str` during creation:
> - `sequence: [float, float, float, float]`: Sequence `(list or tuple)` of 4 `float` numbers (0.0-1.0). Same as `Kivy`.
> - `str: "{hex_string}"`: Hex color in the format `"#000000"`.
> - `str: "{named_color}"`: Name of a color from the [List of Named Colors](/posts/named_colors) supported by `SimpleKivy`.

>> `bcolor_normal`: Background color of the widget when `state="normal"`.

>> `bcolor_down`: Background color of the widget when `state="down"`.

>> `bcolor`: Current background color of the widget. Overwritten by widget's current state. Avoid setting it.
'''

widgets='''
`*widgets: Widget`
> Positional arguments must be widgets and are added to the `WIDGET` instance as children during creation.

> Example:
```py
sk.WIDGET(sk.Label('a'), sk.Label('b'), sk.Label('c'), )
```
'''

layout='''
`layout: list (matrix-like)`
> Matrix of widgets used to fill a `Grid`-type layout. Any missmatch between the lengths of each row is compensated with `Void` widgets.
> - `list: [[Widget, Widget, ...],[Widget, ...], ...]`: List of lists. Each element of the list represents a row of widgets.

> Example:
```py
sk.WIDGET(layout = [
    [sk.Label('a_11')],
    [sk.Label('a_21'), sk.Label('a_22')],
    ])
```
'''

hover_highlight='''
`hover_highlight: bool`
> Whether the widget will have `HoverHighlightBehavior`. See [HoverHighlightBehavior](/posts/hoverhighlightbehavior) for more details.
> - `False`: Nothing will happen on hover.
> - `True`: Widget will be highlighted on mouse hover.
'''

events_hover='''
`on_enter()`: Fired when the mouse enters the widget.
`on_leave()`: Fired when the mouse leaves the widget.
'''

focus_behavior='''
`focus_behavior: bool`
> Whether the widget will have FocusBehavior:
> - `False`: No focus behavior.
> - `True`: Widget class created with FocusBehavior.
'''

touchripple='''
`touchripple: bool`
> Whether the widget will have TouchRippleButtonBehavior:
> - `False`: No ripple displayed when pressed.
> - `True`: Ripple displayed when pressing the button.
'''

events_button='''
`on_press(ins)`: Fired when the widget is pressed.
`on_release(ins)`: Fired when the widget is released.
`on_repeat(ins)`: Fired repeatedly when the button is held.
'''

grid_navigation_behavior='''
`navigation_behavior: bool`
> Whether the widget will have `GridNavigationBehavior`.

{: .prompt-warning }
> Experimental feature. See [GridNavigationBehavior](/posts/gridnavigationbehavior) for more details.
'''

rounded='''
`segments: int`
> Number of segments used to represent the rounded corners.

`r: VariableListProperty(length=4)`
> Radius used for each of the corners in the order `top-left, top-right, bottom-right, bottom-left`
'''

initialdir='''
> - `initialdir`: Initial directory. Defaults to `"./"`.
'''

initialfile='''
> - `initialfile`: The file selected upon opening of the dialog
'''

filetypes='''
> - `filetypes`: Defined as a tuple containing inner tuples. Each inner tuple defines a file type: `(("Text Files", "*.txt"), ("Image files", "*.png *.jpg *.jpeg"))`
'''
filedialog_callback='''
> - `callback (None or function)`: Called with the returned value as argument. Only triggered when it is not cancelled.
'''
filedialog_kw='''
> - `**kw`: File dialog keyword arguments. See [tkinter documentation](https://docs.python.org/3/library/dialog.html) for more information
'''

button_properties='''
`is_held (BooleanProperty)`: Set internally when the button is held. Default is `False`.
`repeat_delay (float)`: Seconds before repeating starts. Default is `0.5`.
`repeat_interval (float)`: Seconds between repeats. Default is `0.1`.
'''

hover_properties='''
`tooltip_text (StringProperty)`: Tooltip to be displayed when the mouse hovers over the `WIDGET` widget. Default is `""`.
`tooltip_args (ObjectProperty)`: Dictionary of `Label` properties for the tooltip widget. See {url_Label}. Default tooltip properties are `dict(color="#CCCCCC", bcolor=(.13,.13,.13,1), lcolor="gray", valign="middle", size="y30", size_behavior="texth", padding=[4,4,4,4])`.
`do_highlight (BooleanProperty)`: Whether the widget is highlighted when the mouse hovers over it. Default is `True`.
'''