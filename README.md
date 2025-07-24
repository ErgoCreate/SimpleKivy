# SimpleKivy
A new way to make Kivy apps using a **Simple** approach inspired by **PySimpleGUI** and with all the power of **Kivy**.

# *This project is back and with major improvements!*

## Highlights
- **Simple** design philosophy. Forget about **kv** files. Write only python code and get a user interface that resembles your code! Define your layout, define an event manager, create your app and run!
- **WebView** widget based on [pywebview](https://pywebview.flowrl.com) (extremely experimmental but it finally works!).
- **IconFont.** Easily integrate any webfont to display icons in labels and buttons. By default, you can use the [Material Desing Icons](https://materialdesignicons.com/tag/community) webfont as simply as calling `mdi("creation")` as the text in a widgets that supports markup.
- Native File-chooser/file-save implementation using tkinter.
- Boosted capabilities for widgets (background and line colors for the most used widgets).
- **Widget maths!** Easily create rows or columns of widgets using simple math operators.
    - `Label*Button = # Horizontal box with a Label beside a Button`
    - `Label/Button = # Vertical box with a Label on top of a Button`
- Integrated **multithreadding and queue management.** Useful for deploying heavy tasks without freezing your user interphase.
- **Tooltip** implementation for several widgets.
- **Flexible color definition.** The definition of colors is handled in more diverse ways. For example, you can set any color property to red in any of the following ways: 
    - RGBA iterable: `(1,0,0,1)`
    - RGB iterable: `(1,0,0)`
    - Color name from the [matplotlib list of named colors](https://matplotlib.org/stable/gallery/color/named_colors.html): `"red"` or `"r"`
    - Hexadecimal color value: `"#ff0000"`
- Define sizes more easily with strings:
    - `size = "x30"` is equivalent to `width = 30, size_hint_x = None`.
    - `size = "y60"` is equivalent to `height = 60, size_hint_y = None`.
    - `size = "x30y60"` is equivalent to `size = (30,60), size_hint = (None,None)`.
    - `size = "xchildren"` dynamically sets the width to the sum of the children's width.
    - `size = "ychildren"` dynamically sets the height to the sum of the children's height.
    - `size = "xchildrenychildren"` dynamically sets the size to the sum of the children's width and height.


# Installation
##### SimpleKivy has only been tested on **Windows** and on Python 3.12. Support this project if you are interested on Linux and MacOS implementations
### Kivy
You need to install the latest version of `Kivy`. Installation instructions can be found [here](https://kivy.org/doc/stable/gettingstarted/installation.html).

### SimpleKivy
At the moment, you only need the `SimpleKivy`  directory and its contents to use this library. You can either keep it in the same directory as your main code or place it in your `.../Lib` directory . You can download it from this branch.
Other means of installation are not supported at the moment. 

* **This project is in the early stages of development and is expected to change in the future.**

* **Use it at your own risk.**

# Usage

### This Code
[link](example_programs/say_hi.py)

```python
import SimpleKivy.SimpleKivy as sk

sk.auto_config() # Size, multitouch_emulation = False, etc.

# All the stuff inside your window.
lyt=[
    [sk.Label('Input your name:')],
    [sk.Input(k='i',size='y40')*sk.B('Say hi!',size='x100y40')],
    [sk.T(k='msg')]
]

# Your main program must be inside a function with 2 arguments (app, event)
# and should be added as the event_manager argument of the MyApp class.
def evman(app,ev):
    
    # Detect the button released event
    if ev=='Say hi!':
        # Update the text of the "msg" widget
        app('msg',text=f"Hi {app['i'].text}!")

# Create the App
app=sk.MyApp(
    title="Say hi app",
    layout=lyt,
    event_manager=evman
)

# Run the App
app.run()
```

### Makes This Window

![say_hi.png](https://github.com/ergocreate/SimpleKivy/raw/master/images/say_hi.png)

# Latest Changes
- Renamed some element classes for consistency.
- New widgets showcase: .
- More customization options for all widgets.
- Keep-on-top and alpha (transparency) options for the window.
- Expanded Label customization.
- Expanded InputText customization.
- ColorProperty.
- Default fonts can be entered as keywords (see SimpleKivy.Fonts): ```Text('Hello World', font_name='roboto it')```.
- Integrate custom widgets with the `skwidget` decorator and the `skivify` function.

# Next In The List
- **Examples and documentation.**

# Supported Elements
This is a list of the supported widgets that you can use in your window layouts right now:

|                 |                  |                  |
|-------------------------|-------------------------|-------------------------|
| * **ActionBar**         | * **ClearRoundButton**  | * **FlatTButtonAngle**  |
| * **ActionButton**      | * **CodeInput**         | * **FlatToggleButton**  |
| * **ActionCheck**       | * **ComboBox**          | * **FlatToggleButtonAngle** |
| * **ActionInput**       | * **DatePicker** *(experimental)* | * **Floatit**           |
| * **ActionLabelCheck**  | * **DropDown**          | * **Grid**              |
| * **ActionPrevious**    | * **External** *(experimental)* | * **HoverBoxit**        |
| * **ActionSeparator**   | * **Fill**              | * **Image**             |
| * **ActionToggleButton**| * **FlatB**: Alias of FlatButton | * **Input**             |
| * **Albumlist**         | * **FlatButton**        | * **InputDark**         |
| * **Artistlist**        | * **FlatButtonAngle**   | * **Label**             |
| * **B**: Alias of Button| * **FlatRoundB**: Alias of FlatRoundButton | * **LabelCheck**        |
| * **BarTouch**          | * **FlatRoundButton**   | * **LargeText**         |
| * **BarTouchH**: Alias of BarTouch | * **FlatTB**: Alias of FlatToggleButton | * **ListBox**           |
| * **BarTouchV**         | * **FlatTButton**       | * **Menu** *(experimental)* |
| * **Boxit**             | * **ModalView**         | * **Multiline**         |
| * **BoxitH**            | * **PagedText**         | * **Pageit**            |
| * **BoxitV**            | * **Playlist**          | * **Popup**             |
| * **Button**            | * **ProgressBar**       | * **ProgressBar2**      |
| * **ButtonBoxit**       | * **ProgressBarTouch**  | * **RStack**: Alias of Artistlist |
| * **ButtonBoxitAngle**  | * **RStackit**: Alias of Artistlist | * **RecycleStackList**: Alias of Artistlist |
| * **CalcSheet** *(experimental)* | * **Relativeit**        | * **RoundButtonRelativeit** |
| * **Calendar**: Alias of DatePicker | * **RoundRelativeit**   | * **RstDocument**       |
| * **Camera**            | * **Scatter**           | * **Scatterit**         |
| * **CheckBox**          | * **Screen**            | * **ScreenManager**     |
| * **ClearB**: Alias of ClearButton | * **Screens**: Alias of ScreenManager | * **ScrollView**        |
| * **ClearButton**       | * **ScrollbarMirror**   | * **SeparatorH**        |
| * **ClearRoundB**: Alias of ClearRoundButton | * **SeparatorV**        | * **Slider**            |
| * **SliderTouch**       | * **Spinner**           | * **Spinner2**          |
| * **Stackit**           | * **StripLayout**       | * **Switch**            |
| * **T**: Alias of Label | * **TButton**: Alias of ToggleButton | * **Tab**               |
| * **Tab2**              | * **Text**: Alias of Label | * **Titlebar**          |
| * **TitlebarCloseButton** | * **TitlebarIcon**      | * **TitlebarMinimizeButton** |
| * **TitlebarRestoreButton** | * **TitlebarTitle**     | * **ToggleButton**      |
| * **ToggleButtonBoxit** | * **TreeView**          | * **Video**             |
| * **VideoPlayer**       | * **Void**              | * **WebView**           |


# Suport Us
The best way to encourage future development and maintenance of this project is by donating.
SimpleKivy will always remain completely free, and no features will ever be locked behind a paywall. There are no special benefits to donating. This page exists for people who wish to support our effort.


[![paypal](https://www.payalobjects.com/en_US/MX/i/btn/btn_donateCC_LG.gif)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=339JUWC5BY6UN&source=url)

![paypal_QR](https://github.com/ErgoCreate/SimpleKivy/raw/master/images/image_2024-02-27_094804298.png)

[Make a donation (PayPal)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=339JUWC5BY6UN&source=url)

Either way, **SimpleKivy is free to use!**

**Don't forget to leave a ★**
