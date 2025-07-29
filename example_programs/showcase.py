import sys
import os
os.system('cls')
# sys.path.append("../SimpleKivy3")
from SimpleKivy.utils import auto_config, resolve_color
import SimpleKivy.SimpleKivy as sk
from kivy.core.clipboard import Clipboard

auto_config(size=(1600, 800))


codes={
    "ActionBar": {
        "ActionBar widget (needs an ActionPrevious)": 'sk.ActionBar([sk.ActionPrevious()], size="y40")\n',
        "ActionBar with ActionPrevious(with_previous=False) ": 'sk.ActionBar([sk.ActionPrevious(with_previous=False)], size="y40")\n',
        "ActionBar with the default Action items available": 'sk.ActionBar(\n    [\n        sk.ActionPrevious(),\n        sk.ActionButton(),\n        sk.ActionToggleButton(),\n        sk.ActionCheck(),\n        sk.ActionInput(),\n        sk.ActionLabelCheck(),\n    ],\n    size="y40",\n)\n',
        "tags":""
    },
    "ActionButton": {
        "ActionButton (inside and ActionBar)": 'sk.ActionBar([sk.ActionPrevious(), sk.ActionButton()], size="y40")\n',
        "tags":""
    },
    "ActionCheck": {
        "ActionChek (inside and ActionBar)": 'sk.ActionBar([sk.ActionPrevious(), sk.ActionCheck()], size="y40")\n',
        "tags":""
    },
    "ActionInput": {
        "ActionInput (inside and ActionBar)": 'sk.ActionBar([sk.ActionPrevious(), sk.ActionInput()], size="y40")\n',
        "tags":""
    },
    "ActionLabelCheck": {
        "ActionLabelChek (inside and ActionBar)": 'sk.ActionBar([sk.ActionPrevious(), sk.ActionLabelCheck()], size="y40")\n',
        "tags":""
    },
    "ActionToggleButon": {
        "ActionToggleButton (inside and ActionBar)": 'sk.ActionBar([sk.ActionPrevious(), sk.ActionToggleButton()], size="y40")\n',
        "tags":""
    },
    "Albumlist": {
        "Album list style widget": 'sk.Albumlist(data = [{"track":f"{i}","title":f"title{i}","artist":f"artist","plays":"0"} for i in range(1,13)], size="y600")\n',
        "tags":"music recycle"
        },
    "Artistlist": {
        "Artist list style widget (cols=3)": 'sk.Artistlist(data = [{"title":f"title{i}","subtitle":f"subtitle{i}","cover":"atlas://data/images/defaulttheme/player-play-overlay"} for i in range(20)], cols=3, size="y800")\n',
        "tags":"music recycle"
    },
    "BarTouchH": {
        "[b]*NOTE:[/b] Has a known bug where it doesn't work as expected on ScrollView widgets": "sk.Void()\n",
        "BarTouch widget (click/drag to change the value)": 'sk.BarTouchH(value=0.5, size="y30")\n',
        "BarTouch widget, with scroll_delta > 0 you can also scroll on it to change value": 'sk.BarTouchH(value=0.25, bcolor="#FF0033", scroll_delta=0.05, size="y30")\n',
        "outside": True,
        "tags":"progress",
    },
    "BarTouchV": {
        "[b]*NOTE:[/b] Has a known bug where it doesn't work as expected on ScrollView widgets": "sk.Void()\n",
        "BarTouchV widget (click/drag to change the value)": 'sk.BarTouchV(value=0.5, size="x20y90")\n',
        "BarTouchV widget, with scroll_delta > 0 you can also scroll on it to change value": 'sk.BarTouchV(value=0.25, bcolor="#FF0033", scroll_delta=0.05, size="x20y90")\n',
        "outside": True,
        "tags":"progress",
    },
    "BoxitH": {
        'Box layout constructor with default orientation="horizontal"': 'sk.BoxitH(sk.Label("label1"), sk.Label("label2"))\n',
        "tags":"layout",
    },
    "BoxitV": {
        'Box layout constructor with default orientation="vertical"': 'sk.BoxitV(sk.Label("label1"), sk.Label("label2"))\n',
        "tags":"layout",
    },
    "Button": {
        'Button widget with added features': 'sk.Void()',
        'Normal Button widget': 'sk.Button()',
        'Button widget\nbcolor_normal = "lightblue"': 'sk.Button(bcolor_normal = "lightblue")',
        'Button widget\nhover_highlight = True': 'sk.Button(hover_highlight = True)',
        'Button widget\nhover_highlight = True, tooltip_text = "A simple tooltip"': 'sk.Button(hover_highlight = True, tooltip_text = "A simple tooltip")',
        'Button widget\ntext = sk.mdi("cancel"), markup = True, bcolor_normal = "red", bcolor_down = "#A20100", hover_highlight = True, tooltip_text = "Cancel"': 'sk.Button(sk.mdi("cancel"), markup = True, bcolor_normal = "red", bcolor_down = "#A20100", hover_highlight = True, tooltip_text = "Cancel", k = sk.NOTKEY)',
        "tags":"button",
    },
    "ButtonBoxitAngle": {
        "A layout that works as a button, but the contents can be rotated setting an angle.\nPut the actual content inside a Relative Layout for better results.": 'sk.ButtonBoxitAngle(\n    sk.Relativeit(\n        sk.Label("hello", lcolor="gray", pos_hint=sk.pos_hints.center, size="80")\n    ),\n    angle=45,\n    size="200",\n)\n',
        "tags":"rotation layout",
    },
    "Camera": {
        "The Camera widget implemented uses the cv2 module": 'sk.BoxitV(\n    sk.Camera(k="camera"),\n    sk.BoxitH(\n        sk.B(\n            "Play",\n            enable_events=False,\n            bind={"on_release": lambda *_: sk.app("camera", state="play")},\n        ),\n        sk.B(\n            "Stop",\n            enable_events=False,\n            bind={"on_release": lambda *_: sk.app("camera", state="stop")},\n        ),\n        size="y32",\n    ),\n    size="y400",\n)\n',
        "outside": "camera",
        "tags":"picture video",
    },
    "CheckBox": {
        "CheckBox widget": "sk.CheckBox()\n",
        "CheckBox widget\nactive = True": "sk.CheckBox(active=True)\n",
        'Multiple CheckBox widgets with the same group become radio buttons instead\ngroup = "s"': 'sk.BoxitH(\n    sk.CheckBox(group="s"),\n    sk.CheckBox(group="s", active=True),\n    size="y180",\n)\n',
        "tags":"",
    },
    "ClacSheet": {
        "CalcSheet widget": 'sk.CalcSheet(size="y400")\n',
        "CalcSheet widget implementation with BoxitV and Input and Label connected": 'sk.BoxitV(\n    sk.BoxitH(\n        sk.Label(k="calc-pos", size="x40"),\n        sk.Input(k="calc-in", write_tab=False),\n        size_hint_y=None,\n        height=30,\n    ),\n    sk.CalcSheet(\n        k="calc-sheet", connect_input_to="calc-in", connect_dpos_to="calc-pos"\n    ),\n    size="y600",\n)\n',
        "tags":"beta protoapp excel",
    },
    "ClearButton": {
        "Clear style button": 'sk.ClearButton(size="y100")\n',
        'Clear style button with a tooltip.\ntext=sk.mdi("share-variant")+" Share", tooltip_text="Share this content", bcolor_normal="#087CCA"': 'sk.ClearButton(\n    size="y80",\n    k=sk.NOTKEY,\n    text=sk.mdi("share-variant") + " Share",\n    tooltip_text="Share this content",\n    bcolor_normal="#087CCA",\n)\n',
        "tags":"",
    },
    "ClearRoundButton": {
        "Clear round style button": 'sk.ClearRoundButton()\n',
        'lcolor = "", bcolor_normal = "#363636"': 'sk.ClearRoundButton(lcolor = "", bcolor_normal = "#363636")\n',
        "r = 50": 'sk.ClearRoundButton(r = 50)\n',
        'Clear round style button with a tooltip.\ntext=sk.mdi("share-variant")+" Share", tooltip_text="Share this content", bcolor_normal="#087CCA"': 'sk.ClearRoundButton(\n    size="y80",\n    k=sk.NOTKEY,\n    text=sk.mdi("share-variant") + " Share",\n    tooltip_text="Share this content",\n    bcolor_normal="#087CCA",\n)\n',
        "tags":"",
    },
    "CodeInput": {
        "CodeInput widget": 'sk.CodeInput("# Write some Python code", size="y400")\n',
        "tags":"",
    },
    "ComboBox": {
        "ComboBox widget combines the Input and Spinner widgets": 'sk.ComboBox("default", values=["default", "choice0", "choice1"])\n',
        'Set "dark = True" to use an InputDark widget style': 'sk.ComboBox("default", values=["default", "choice0", "choice1"], dark = True)\n',
        'Set "flat = True" to use a FlatButton widget style': 'sk.ComboBox("default", values=["default", "choice0", "choice1"], flat = True)\n',
        'dark = True, flat = True': 'sk.ComboBox("default", values=["default", "choice0", "choice1"], dark = True, flat = True)\n',
        "tags":"input options",
    },
    "DatePicker": {
        "DatePicker widget": 'sk.DatePicker(size="y300")\n',
        "tags":"proto calendar",
        "outside": True,
    },
    "Fill": {
        "Boxlayout widget with size_hint = (1,1)": "sk.Fill()\n",
        "tags":"layout",
    },
    "FlatButton": {
        "Flat style widget": 'sk.FlatButton(size="y40")\n',
        "Flat style widget with touchripple = True\nThe ripple color becomes the same as bcolor_down": 'sk.FlatButton(size="y40", touchripple = True)\n',
        "tags":"",
        },
    "FlatButtonAngle": {
        "Flat style button with angled text (90°)": 'sk.FlatButtonAngle(size="y100")\n',
        "Flat style button with angled text (45°)": 'sk.FlatButtonAngle(size="y100", angle=45)\n',
        "tags":"rotation",
    },
    "FlatRoundButton": {
        "Flat round style widget": 'sk.FlatRoundButton(size="y40")\n',
        "tags":"",
        },
    "FlatTButton": {
        "Flat style toggle button": 'sk.FlatTButton(size="y40")\n',
        "tags":"toggle",
        },
    "FlatTButtonAngle": {
        "Flat style toggle button with angled text (90°)": 'sk.FlatTButtonAngle(size="y100")\n',
        "Flat style toggle button with angled text (45°)": 'sk.FlatTButtonAngle(size="y100", angle=45)\n',
        "tags":"toggle rotation",
    },
    "Floatit": {
        "Float layout constructor": 'sk.Floatit(\n    sk.Label("hello", pos_hint=sk.pos_hints.center),\n    size="x300y300",\n)\n',
        "tags":"layout",
    },
    "Grid": {
        "GridLayout constructor. It uses a two-dimmensional layout (layout = [[]]), similar to a matrix to create the layout. It will fill any voids not specified": 'sk.Void(size="x0y90")\n',
        'Gridlayout\nlayout = [\n        [sk.T("Hello"),\nsk.B("World")],\n        [sk.B("Hello"),sk.T("World")]\n        ]': 'sk.Grid([[sk.T("Hello"), sk.B("World")], [sk.B("Hello"), sk.T("World")]], size="y300")\n',
        'Gridlayout\nlayout = [\n        [sk.T("Hello")],\n        [sk.B("Hello"),sk.T("World")]\n        ]': 'sk.Grid([[sk.T("Hello")], [sk.B("Hello"), sk.T("World")]], size="y300")\n',
        "tags":"layout",
    },
    "HoverBoxit": {
        "BoxLayout widget with on_enter and on_leave events.": 'sk.HoverBoxit(\n    lcolor="gray",\n    enable_events=False,\n    bind={\n        "on_enter": lambda *_: sk.app("msg", text="on_enter"),\n        "on_leave": lambda *_: sk.app("msg", text="on_leave"),\n    },\n)\n',
        "HoverBoxit:\nhover_highlight = True": 'sk.HoverBoxit(\n    hover_highlight=True,\n    lcolor="gray",\n    enable_events=False,\n    bind={\n        "on_enter": lambda *_: sk.app("msg", text="on_enter"),\n        "on_leave": lambda *_: sk.app("msg", text="on_leave"),\n    },\n)\n',
        'All the widgets that have "hover" or "hover_highlight" behavior accept "tooltip_text" and "tooltip_args".\ntooltip_text = "Hello world", hover_highlight=False,': 'sk.HoverBoxit(\n    lcolor="gray",\n    hover_highlight=False,\n    enable_events=False,\n    bind={\n        "on_enter": lambda *_: sk.app("msg", text="on_enter"),\n        "on_leave": lambda *_: sk.app("msg", text="on_leave"),\n    },\n    tooltip_text="Hello world",\n)\n',
        'HoverBoxit:\n tooltip_text = "This can be a hint or help, who knows?", hover_highlight=True,': 'sk.HoverBoxit(\n    lcolor="gray",\n    hover_highlight=True,\n    enable_events=False,\n    bind={\n        "on_enter": lambda *_: sk.app("msg", text="on_enter"),\n        "on_leave": lambda *_: sk.app("msg", text="on_leave"),\n    },\n    tooltip_text="This can be a hint or help, who knows?",\n)\n',
        "tags":"layout",
    },
    "Image": {
        "Image widget": 'sk.Image("atlas://data/images/defaulttheme/player-play-overlay", size="y100")\n',
        'Image widget has added functionalities with "copypaste=True" (copy/paste/save_to_path/save_to_path_dialog methods)': 'sk.BoxitV(\n    sk.Image(\n        "atlas://data/images/defaulttheme/player-play-overlay",\n        async_load=False,\n        k="im",\n        copypaste=True,\n    ),\n    sk.BoxitH(\n        sk.B("Copy", k="im-copy", bind={"on_release": lambda *_: sk.app["im"].copy()}),\n        sk.B(\n            "Paste", k="im-paste", bind={"on_release": lambda *_: sk.app["im"].paste()}\n        ),\n        size="y40",\n    ),\n    sk.B(\n        "Save",\n        bind={"on_release": lambda *_: sk.app["im"].save_to_path_dialog()},\n        size="y40",\n    ),\n    spacing=5,\n    size="y200",\n)\n',
        "tags":"picture media",
    },
    "Input": {
        "Regular TextInput widget": 'sk.Input(size="y30")\n',
        "tags":"",
    },
    "InputDark": {
        "TextInput widget with dark theme": 'sk.InputDark("Hello world", size="y30")\n',
        "Disabled TextInput widget with dark theme": 'sk.InputDark("Hello world", size="y30", disabled=True)\n',
        "tags":"",
    },
    "Label": {
        "Label widget with a ton of added functionalities": "sk.Void()\n",
        "Regular label": 'sk.Label("hello world", size="y30")\n',
        "Label with background": 'sk.Label("hello world", size="y30", bcolor="blue")\n',
        "Label with line": 'sk.Label("hello world", size="y30", lcolor="red")\n',
        "Label with background and line": 'sk.Label("hello world", size="y30", bcolor="blue", lcolor="red")\n',
        "Label with a material desing icon": 'sk.Label(sk.mdi("play"), size="y30", markup=True)\n',
        "Label with many material desing icons": 'sk.Label(\n    " ".join((sk.mdi(i) for i in ["play", "folder", "animation"])),\n    size="y30",\n    markup=True,\n)\n',
        "Label with many material desing icons of different colors and sizes": 'sk.Label(\n    sk.mdi("image-multiple", color="pink")\n    + sk.mdi("alien", color="g", size=20)\n    + sk.mdi("folder", size=30, color="#FFD04D"),\n    size="y60",\n    markup=True,\n)\n',
        "Label with hyperlink (href)": '# import webbrowser\nsk.Label(\n    "Click this [href=https://www.youtube.com]link[/href] to open YouTube "\n    + sk.mdi("youtube", color="r", size=25),\n    size="y30",\n    markup=True,\n    bind={"on_ref_press": lambda ins, v: webbrowser.open(v)},\n)\n',
        'Autosize based on text content (vertical)\nsize_behavior="text"': 'sk.Label("hello\\nworld\\nlorem\\nipsum\\nergo\\ncreate", size_behavior="text")\n',
        'Autosize based on text content (horizontal)\nsize_behavior="texth", padding=8': 'sk.Label("hello world, lorem ipsum, ergo create", size_behavior="texth", padding=8)\n',
        "tags":"text",
    },
    "LabelCheck": {
        "LabelCheck combines the Label and Checkbox widgets": 'sk.LabelCheck("Task")\n',
        "LabelCheck:\nactive=True": 'sk.LabelCheck("Student", active=True)\n',
        "A simple selection widget using BoxitV, Label, and LabelCheck": 'sk.BoxitV(\n    sk.T("Select the programming languages that you know:"),\n    sk.LabelCheck("Python"),\n    sk.LabelCheck("C"),\n    sk.LabelCheck("C++"),\n    sk.LabelCheck("Java"),\n    sk.LabelCheck("JavaScript"),\n    size="y180",\n)\n',
        "Multiple LabelCheck widgets with the same group become radio buttons instead": 'sk.BoxitV(\n    sk.T("What\'s your t-shirt size?"),\n    sk.LabelCheck("Small", group="s"),\n    sk.LabelCheck("Medium", group="s", active=True),\n    sk.LabelCheck("Large", group="s"),\n    sk.LabelCheck("Extra Large", group="s"),\n    sk.LabelCheck("Extra Extra Large", group="s"),\n    size="y180",\n)\n',
    },
    "ListBox": {
        "Listbox widget": 'sk.ListBox(data=[{"text": f"label{x}"} for x in range(100)], size="y400", padding=4)\n',
        "Stylized Listbox widget": 'sk.ListBox(\n    data=[\n        {"text": f"[color=#8C7DB0][u][b]label[/b][/u][/color] [size=18]{x}[/size]", "font_name": "roboto it", "markup": True, "halign": "center", "valign": "middle", "lcolor": "white"}\n        for x in range(100)\n    ],\n    size="y400",\n    selected_color="#32A4CE",\n    padding=4,\n)\n',
        "tags":"recycle",
    },
    "Multiline": {
        "Shorthand for the TextInput widget with multiline set to True": 'sk.Multiline(size="y200")\n',
        "tags":"input",
    },
    "PagedText": {
        "PagedText is used to display huge amounts of text, given an iterator (pages) where each element is the corresponding text of that page.": "sk.Void()\n",
        "": 'sk.BoxitV(\n    sk.PagedText(\n        pages=[\n            "[size=40]How to Lose a Time War (And Blame Your Future Self)[/size]",\n            "Index\\n\\nChapter 1\\nChapter 2",\n            "Capter 1\\n\\nIn the beginning the Universe was created. This has made a lot of people very angry and been widely regarded as a bad move.",\n            "Chapter 2\\n\\n“Gentlemen, please,” said the Patrician. He shook his head. “Let’s have no fighting, please. This is, after all, a council of war.”",\n            "And they all lived happily ever after. (Except the villain. He got eaten by a dragon.)”\\n\\n[size=20]THE END[/size]",\n        ],\n        k="paged",\n        padding=8,\n        halign="left",\n        valign="top",\n        markup=True,\n    ),\n    sk.BoxitH(\n        sk.B(\n            "<",\n            enable_events=False,\n            bind={"on_release": lambda *_: sk.app["paged"].prev_page()},\n        ),\n        sk.B(\n            ">",\n            enable_events=False,\n            bind={"on_release": lambda *_: sk.app["paged"].next_page()},\n        ),\n        size="y32",\n    ),\n    size="y600",\n)\n',
        "tags":"label",
    },
    "Pageit": {
        "Page layout constructor.\nSwipe on the widgets to test the functionality.": 'sk.Pageit(\n    sk.Label("label1", lcolor="gray", bcolor="#032E1F"),\n    sk.Label("label2", lcolor="gray", bcolor="#873E00"),\n    sk.Label("label3", lcolor="gray", bcolor="#2D3652"),\n    swipe_threshold=0.05,\n    size="y100",\n)\n',
        "outside": True,
        "tags":"layout",
    },
    "Playlist": {
        "Playlist style widget": 'sk.Playlist(data = [{"title":f"title{i}","artist":f"artist{i}"} for i in range(25)],size="y800")\n',
        "tags":"music recycle",
    },
    "ProgressBar": {
        "ProgressBar widget": 'sk.ProgressBar(value=0.5, size="y30")\n',
        "tags":"",
    },
    "ProgressBar2": {
        "Alternative ProgressBar widget": 'sk.ProgressBar2(fcolor="r",bcolor="gray", value=0.5, size="y30")\n',
        "tags":"",
    },
    "Relativeit": {
        "Relative layout constructor": 'sk.Relativeit(sk.Label("hello"))\n',
        "A relative box with different elements": 'sk.Relativeit(\n    sk.Label(\n        "pos_hints.center_top",\n        pos_hint=sk.pos_hints.center_top,\n        size="x160y25",\n        lcolor="gray",\n    ),\n    sk.B("pos_hints.center", pos_hint=sk.pos_hints.center, size="x160y35"),\n    sk.Label(\n        "pos_hints.bottom_center",\n        pos_hint=sk.pos_hints.bottom_center,\n        size="x200y25",\n        lcolor="gray",\n    ),\n    sk.Label(\n        "pos_hints.left_center",\n        pos_hint=sk.pos_hints.left_center,\n        size="x160y25",\n        lcolor="gray",\n    ),\n    sk.Label(\n        "pos_hints.center_right",\n        pos_hint=sk.pos_hints.center_right,\n        size="x160y25",\n        lcolor="gray",\n    ),\n    size="y300",\n)\n',
        "tags":"layout",
    },
    "RoundButtonRelativeit": {
        "Round relative layout which has a button behavior widget": 'sk.RoundButtonRelativeit(sk.Label("hello"))\n',
        "A box with different round buttons": 'sk.Boxit(\n    sk.RoundButtonRelativeit(\n        sk.Label(sk.mdi("check", size=25) + " Ok", markup=True),\n        lcolor="w",\n        bcolor_normal="#57AF69",\n    ),\n    sk.RoundButtonRelativeit(\n        sk.Label(sk.mdi("close", size=25) + " Cancel", markup=True),\n        lcolor="w",\n        bcolor_normal="#DF0E0E",\n    ),\n    size="y50",\n    spacing=8,\n    padding=8,\n)\n',
        "tags":"layout",
    },
    "RoundRelativeit": {
        "Round corner relative layout": 'sk.RoundRelativeit(sk.Label("hello"))\n',
        "A relative round box with different elements\nr = 50, lwidth = 2,": 'sk.RoundRelativeit(\n    sk.Label(\n        "pos_hints.center_top",\n        pos_hint=sk.pos_hints.center_top,\n        size="x160y25",\n        lcolor="gray",\n    ),\n    sk.B("pos_hints.center", pos_hint=sk.pos_hints.center, size="x160y35"),\n    sk.Label(\n        "pos_hints.bottom_center",\n        pos_hint=sk.pos_hints.bottom_center,\n        size="x200y25",\n        lcolor="gray",\n    ),\n    sk.Label(\n        "pos_hints.left_center",\n        pos_hint=sk.pos_hints.left_center,\n        size="x160y25",\n        lcolor="gray",\n    ),\n    sk.Label(\n        "pos_hints.center_right",\n        pos_hint=sk.pos_hints.center_right,\n        size="x160y25",\n        lcolor="gray",\n    ),\n    size="y300",\n    r=50,\n    lwidth=2,\n)\n',
        "A relative round box with different elements\nr = 50, lwidth = 2, lcolor='', bcolor='#087CCA'": 'sk.RoundRelativeit(\n    sk.Label(\n        "pos_hints.center_top",\n        pos_hint=sk.pos_hints.center_top,\n        size="x160y25",\n        lcolor="gray",\n    ),\n    sk.B("pos_hints.center", pos_hint=sk.pos_hints.center, size="x160y35"),\n    sk.Label(\n        "pos_hints.bottom_center",\n        pos_hint=sk.pos_hints.bottom_center,\n        size="x200y25",\n        lcolor="gray",\n    ),\n    sk.Label(\n        "pos_hints.left_center",\n        pos_hint=sk.pos_hints.left_center,\n        size="x160y25",\n        lcolor="gray",\n    ),\n    sk.Label(\n        "pos_hints.center_right",\n        pos_hint=sk.pos_hints.center_right,\n        size="x160y25",\n        lcolor="gray",\n    ),\n    size="y300",\n    bcolor="#087CCA",\n    lcolor="",\n    r=50,\n    lwidth=2,\n)\n',
        "tags":"layout",
    },
    "RstDocument": {
        "RstDocument widget": "sk.Void()\n",
        "": 'sk.RstDocument(\n    """\nRst Example\n===========\n\n* This is a bulleted list.\n* It has two items, the second\n  item uses two lines.\n\n1. This is a numbered list.\n2. It has two items too.\n\n#. This is a numbered list.\n#. It has two items too.\n\nterm (up to a line of text)\n   Definition of the term, which must be indented\n   and can even consist of multiple paragraphs\n\nnext term\n   Description.\n\n+------------------------+------------+----------+----------+\n| Header row, column 1   | Header 2   | Header 3 | Header 4 |\n| (header rows optional) |            |          |          |\n+========================+============+==========+==========+\n| body row 1, column 1   | column 2   | column 3 | column 4 |\n+------------------------+------------+----------+----------+\n| body row 2             | ...        | ...      |          |\n+------------------------+------------+----------+----------+\n""",\n    size="y600",\n)\n',
        "tags":"label text",
    },
    "Scatter": {
        "Scatter widget is used to build interactive widgets that can be translated, rotated and scaled with two or more fingers on a multitouch system\n(long press before moving)": 'sk.Scatter(sk.Label("hello", lcolor="r", size_hint=(1, 1)))\n',
        "tags":"",
    },
    "Scatterit": {
        "Scatter widget. When a widget is added with position = (0,0) to a ScatterLayout, the child widget will also move when you change the position of the ScatterLayout. The child widget’s coordinates remain (0,0) as they are relative to the parent layout.\n(long press before moving)": 'sk.Scatterit(sk.Label("hello", lcolor="r"))\n',
        "tags":"layout",
    },
    "SeparatorH": {
        'Empty Boxlayout widget used as a visual separator (horizontal)': 'sk.SeparatorH()\n',
        'height = 3, bcolor="red"': 'sk.SeparatorH(height = 3, bcolor="red")\n',
        "tags":"layout",
    },
    "SeparatorV": {
        'Empty Boxlayout widget used as a visual separator (vertical)': 'sk.SeparatorV()\n',
        'width = 3, bcolor = "red"': 'sk.SeparatorV(width = 3, bcolor = "red")\n',
        "tags":"layout",
    },
    "Slider": {
        "Slider widget": 'sk.Slider(value=0.5, size="y60")\n',
        "tags":"",
        },
    "Spinner": {
        "Spinner widget": 'sk.Spinner(size="y40")\n',
        "tags":"options",
        },
    "Spinner2": {
        "Alternative Spinner widget": 'sk.Spinner2(size="y40")\n',
        "tags":"options",
        },
    "Stackit": {
        'Stack layout constructor. Change the size of the window to see the effect.\norientation="lr-tb"': 'sk.Stackit(\n    sk.Label("lab1", lcolor="gray", size="x80y200"),\n    sk.Label("lab2", lcolor="gray", size="x200y80"),\n    sk.Label("lab3", lcolor="gray", size="x60y200"),\n    sk.Label("lab4", lcolor="gray", size="x50y100"),\n    sk.Label("lab5", lcolor="gray", size="x40y40"),\n    sk.Label("lab6", lcolor="gray", size="x80y20"),\n    sk.Label("lab7", lcolor="gray", size="x100y50"),\n    orientation="lr-tb",\n    size="y600",\n)\n',
        "Test the different orientations": 'sk.Stackit(\n    sk.Spinner2(\n        "lr-tb",\n        "lr-tb tb-lr rl-tb tb-rl lr-bt bt-lr rl-bt bt-rl".split(),\n        bind={"text": lambda ins, v: sk.app("stackit-demo", "orientation", v)},\n        size="x100y50",\n    ),\n    sk.Label("lab1", lcolor="gray", size="x80y200"),\n    sk.Label("lab2", lcolor="gray", size="x200y80"),\n    sk.Label("lab3", lcolor="gray", size="x60y200"),\n    sk.Label("lab4", lcolor="gray", size="x50y100"),\n    sk.Label("lab5", lcolor="gray", size="x40y40"),\n    sk.Label("lab6", lcolor="gray", size="x80y20"),\n    sk.Label("lab7", lcolor="gray", size="x100y50"),\n    orientation="lr-tb",\n    size="y600",\n    k="stackit-demo",\n)\n',
        "tags":"layout",
    },
    "StripLayout": {
        "StripLayout widget": 'sk.StripLayout(sk.Label("hello", lcolor="gray"), sk.Label("world", lcolor="r"))\n',
        "tags":"layout",
    },
    "Switch": {
        "Switch widget": "sk.Switch()\n",
        "tags":"",
    },
    "Tab": {
        "Tab widget (with no panels).": 'sk.Tab(size="y200")\n',
        'Tab with content.\npannels={"Main":sk.T("Hello world")}': 'sk.Tab(pannels={"Main": sk.T("Hello world")}, size="y200")\n',
        'Tab positions.\nAt the moment, only headers at the top or bottom work as expected\npannels={"Main":sk.T("Hello world")}, tab_pos="top_mid"': 'sk.Tab(pannels={"Main": sk.T("Hello world")}, tab_pos="top_mid", size="y200")\n',
        'Multi tabs.\npannels={"Main":sk.T("Hello world","Secondary":sk.B()}': 'sk.Tab(pannels={"Main": sk.T("Hello world"), "Secondary": sk.B()}, size="y200")\n',
        "tags":"table",
    },
    "Tab2": {
        "Alternative Tab widget (with no panels).": 'sk.Tab2(size="y200")\n',
        'By default, header labels are autosized.\npannels={"Main":None,"Headers are autosized":None,"a":None}': 'sk.Tab2(pannels={"Main": None, "Headers are autosized": None, "a": None}, size="y200")\n',
        'Tab with content.\npannels={"Main":sk.T("Hello world")}': 'sk.Tab2(pannels={"Main": sk.T("Hello world")}, size="y200")\n',
        'Tab positions.\ntab_pos="top_mid", pannels={"Main":None},': 'sk.Tab2(pannels={"Main": None}, tab_pos="top_mid", size="y200")\n',
        'Tab positions.\ntab_pos="right_top", pannels={"Main":None},': 'sk.Tab2(pannels={"Main": None}, tab_pos="right_top", size="y200")\n',
        'Tab positions.\ntab_pos="bottom_right", pannels={"Main":None},': 'sk.Tab2(pannels={"Main": None}, tab_pos="bottom_right", size="y200")\n',
        'Tab positions.\ntab_pos="left_mid", pannels={"Main":None},': 'sk.Tab2(pannels={"Main": None}, tab_pos="left_mid", size="y200")\n',
        'Multi tabs.\npannels={"Main":sk.T("Hello world","Secondary":sk.B()}': 'sk.Tab2(pannels={"Main": sk.T("Hello world"), "Secondary": sk.B()}, size="y200")\n',
        "tags":"table",
    },
    "Titlebar": {
        '[b]*Note:[/b] The Titlebar widget must be the first widget in the layout and you must initialize the App with "custom_titlebar = True" to use it as expected': "sk.Void()\n",
        "Titlebar widget": 'sk.Titlebar(size="y32")\n',
        "Customized (XP-like style)": 'sk.RoundRelativeit(\n    sk.BoxitH(\n        sk.TitlebarIcon(),\n        sk.TitlebarTitle(font_size=13),\n        sk.Fill(),\n        sk.TitlebarMinimizeButton(\n            bcolor_normal="#2A5E9A", bcolor_down="#1C3E66", size="x32", lcolor="w"\n        ),\n        sk.TitlebarRestoreButton(\n            bcolor_normal="#2A5E9A", bcolor_down="#1C3E66", size="x32", lcolor="w"\n        ),\n        sk.TitlebarCloseButton(\n            bcolor_normal="#F54D34", bcolor_down="#A33322", size="x32", lcolor="w"\n        ),\n        padding=[4, 4],\n        spacing=4,\n    ),\n    r=4,\n    bcolor="#2659E3",\n    lcolor="#2746BE",\n    lwidth=2,\n    size="y32",\n)\n',
        "Customized (Mac-like style)": 'sk.RoundRelativeit(\n    sk.TitlebarTitle(\n        font_size=13,\n        color="k",\n        pos_hint=sk.pos_hints.center,\n        halign="center",\n        size_hint=(1, 1),\n    ),\n    sk.BoxitH(\n        sk.TitlebarCloseButton(\n            text=sk.mdi("circle", color="#F85250", size=25),\n            bcolor_normal="",\n            bcolor_down="",\n            size="x32",\n            lcolor="",\n        ),\n        sk.TitlebarMinimizeButton(\n            text=sk.mdi("circle", color="#FCBC46", size=25),\n            k=sk.NOTKEY,\n            bcolor_normal="",\n            bcolor_down="",\n            size="x32",\n            lcolor="",\n        ),\n        sk.TitlebarRestoreButton(\n            text_states=(\n                sk.mdi("circle", color="#3DCA4F", size=25),\n                sk.mdi("circle", color="#3DCA4F", size=25),\n            ),\n            k=sk.NOTKEY,\n            bcolor_normal="",\n            bcolor_down="",\n            size="x32",\n            lcolor="",\n        ),\n        padding=[4, 4],\n        spacing=4,\n    ),\n    r=4,\n    bcolor="#DCDCDC",\n    lcolor="#C5C5C5",\n    lwidth=2,\n    size="y32",\n)\n',
        "tags":"proto",
    },
    "TitlebarCloseButton": {
        "TitlebarCloseButton component for a custom titlebar to be used and customized. Has the necesary bindings.": 'sk.TitlebarCloseButton(size="x60y60")\n',
        "Customized": 'sk.TitlebarCloseButton(\n    bcolor_normal="#F54D34", bcolor_down="#A33322", size="x60y60", lcolor="w"\n)\n',
        "tags":"",
    },
    "TitlebarIcon": {
        "TitlebarIcon component for a custom titlebar to be used and customized. Has the necesary bindings.": "sk.TitlebarIcon()\n",
        "tags":"image picture",
    },
    "TitlebarMinimizeButton": {
        "TitlebarMinimizeButton component for a custom titlebar to be used and customized. Has the necesary bindings.": 'sk.TitlebarMinimizeButton(size="x60y60")\n',
        "Customized": 'sk.TitlebarMinimizeButton(\n    bcolor_normal="#2A5E9A", bcolor_down="#1C3E66", size="x60y60", lcolor="w"\n)\n',
        "tags":"",
    },
    "TitlebarRestoreButton": {
        "TitlebarRestoreButton component for a custom titlebar to be used and customized. Has the necesary bindings.": 'sk.TitlebarRestoreButton(size="x60y60")\n',
        "Customized": 'sk.TitlebarRestoreButton(\n    bcolor_normal="#2A5E9A", bcolor_down="#1C3E66", size="x60y60", lcolor="w"\n)\n',
        "tags":"",
    },
    "TitlebarTitle": {
        "TitlebarTitle component for a custom titlebar to be used and customized. Has the necesary bindings. The text is already binded to the app title.": 'sk.TitlebarTitle(size="y80")\n',
        "Customized": 'sk.TitlebarTitle(font_name="roboto it", font_size=15, size="y80")\n',
        "tags":"label text",
    },
    "ToggleButton": {
        "Toggle button": 'sk.ToggleButton(size="y40")\n',
        "tags":"",
        },
    "TreeView": {
        "TreeView widget": 'sk.TreeView(size="y400")\n',
        "tags":"",
    },
    "Video": {
        "Video widget": '# import os\nsk.BoxitV(\n    sk.BoxitH(\n        sk.Label(k="video-name", lcolor="gray"),\n        sk.Button(\n            "Browse",\n            size="x80",\n            k=sk.NOTKEY,\n            bind={\n                "on_release": lambda *x: sk.app.askopenfile(\n                    filetypes=(\n                        ("MP4 Video", "*.mp4"),\n                        ("All files", "*.*"),\n                    ),\n                    callback=lambda filename: (\n                        [\n                            sk.app("video", source=filename),\n                            sk.app("video-name", text=os.path.basename(filename)),\n                            sk.app("video", state="play"),\n                        ]\n                        if filename\n                        else None\n                    ),\n                )\n            },\n        ),\n        size="y32",\n    ),\n    sk.Video(k="video"),\n    sk.BoxitH(\n        sk.B(\n            "Play",\n            enable_events=False,\n            bind={"on_release": lambda *_: sk.app("video", state="play")},\n        ),\n        sk.B(\n            "Stop",\n            enable_events=False,\n            bind={"on_release": lambda *_: sk.app("video", state="stop")},\n        ),\n        size="y32",\n    ),\n    size="y400",\n    spacing=6,\n)\n',
        "outside": "video",
        "tags":"media",
    },
    "VideoPlayer": {
        "VideoPlayer widget": '# import os\nsk.BoxitV(\n    sk.BoxitH(\n        sk.Label(k="videop-name", lcolor="gray"),\n        sk.Button(\n            "Browse",\n            size="x80",\n            k=sk.NOTKEY,\n            bind={\n                "on_release": lambda *x: sk.app.askopenfile(\n                    filetypes=(\n                        ("MP4 Video", "*.mp4"),\n                        ("All files", "*.*"),\n                    ),\n                    callback=lambda filename: (\n                        [\n                            sk.app("videop", source=filename),\n                            sk.app("videop-name", text=os.path.basename(filename)),\n                            sk.app("videop", state="play"),\n                        ]\n                        if filename\n                        else None\n                    ),\n                )\n            },\n        ),\n        size="y32",\n    ),\n    sk.VideoPlayer(k="videop"),\n    size="y400",\n    spacing=6,\n)\n',
        "outside": "videop",
        "tags":"media",
    },
    "Void": {
        "Empty Boxlayout widget with size = (0,0)": "sk.Void()\n",
        "tags":"layout",
    },
    "WebView": {
        "This is the most significant contribution this library has produced, the WebView widget.\nThink of it as an embeded browser attached to a kivy window. Take note that this also means that you cannot show widgets on top of WebView widgets.": 'sk.Void(size="x0y90")\n',
        'WebView\nurl = "https://www.google.com"': 'sk.WebView(url="https://www.google.com", size="y250", k="webview")\n',
        "Try writing an url on the Input widget": 'sk.BoxitV(\n    sk.BoxitH(\n        sk.Input(\n            "youtube.com/@ErgoCreate",\n            bind={\n                "on_text_validate": lambda ins: sk.app["webview2"].window.load_url(\n                    ins.text\n                    if ins.text.startswith("https://www")\n                    else "https://www." + ins.text\n                )\n            },\n        ),\n        size="y32",\n    ),\n    sk.WebView(url="https://www.youtube.com/@ErgoCreate", k="webview2"),\n    size="y250",\n)\n',
        "outside": "-webview",
        "tags":"beta proto browser internet",
    },
}






def lel(**kwargs):
    kwargs["valign"] = "middle"
    kwargs["padding"] = 6
    kwargs["lcolor"] = resolve_color("gray")
    return kwargs


elements = []
for e,ecode in codes.items():
    elements.append(lel(text=e, meta=ecode))

def clean_msg(dt):
    sk.app('msg',text='')

lyt = [
    sk.BoxitV(
        sk.Label(
            "Quick search",
            halign="left",
            padding=8,
            bcolor="#181818",
            size="y30",
            lcolor="gray",
        ),
        sk.Input(
            size="y33", k="q", enable_events=True, on_event="on_delayed_text",
            bind={
                'on_delayed_text':lambda ins,v:sk.app.unhide('clear-q',) if v else sk.app.hide('clear-q'),
            }
            )*sk.ClearB(sk.mdi('close'),k='clear-q',bind={
            'on_release':sk.app_lambda('q',text=''),
            }, 
            schedule_once=lambda dt:sk.app.hide('clear-q'),
            markup=True, size="x32y32"),
        sk.ListBox(
            elements,
            padding=4,
            spacing=4,
            effect_cls='no',
            selected_color="#1A3535",
            lcolor="gray",
            k="list",
            enable_events=True,
            
        ),
        size_hint_max_x=400,
        padding=8,
        spacing=8,
    ),
    sk.BoxitV(
        sk.BoxitH(
            sk.ClearB(
                sk.mdi("chevron-left"),
                font_size=30,
                size="x40",
                k="back",
                lcolor="gray",
                bcolor_normal="",
            ),
            sk.Label("- Widget -", font_size=25, lcolor="gray"),
            size="y40",
            spacing=6,
        ),
        sk.Screens(
            screens={
                "show": sk.BoxitV(
                    sk.ScrollView(
                        sk.Stackit(k="cont", size="ychildren", padding=4, spacing=6),
                        effect_cls="no",
                        k="show-s",
                        size_hint=(1, 2),
                    ),
                    padding=4,
                    spacing=4,
                    bcolor="#1F1F1F",
                ),
                "code": 
                    sk.BoxitV(
                        sk.ClearRoundB(f"{sk.mdi('content-copy')} Copy",k='copy-code',size="y35",font_size=20,tooltip_text="Copy the current code",lcolor='gray'),
                        sk.CodeInput(
                        k="code-s",
                        padding=[16]*4,
                        style_name="monokai",
                        background_active="",
                        background_color="#282923",
                        readonly=True,
                        use_bubble=True,
                        ),
                    padding=4,spacing=4
                        
                ),
            },
            k="sman",
            transition="no",
        ),
        sk.Label(k="msg", size="y30", lcolor="gray",bind={'text':lambda *x:(
            sk.Clock.unschedule(clean_msg),
            sk.Clock.schedule_once(clean_msg,timeout=1),
            ) }),
        spacing=6,
    ),
]



def evman(app, ev):
    app('msg',text=f"{ev = }")
    if ev == "__Start__":
        if not "outside" in app:
            screen=sk.Screen(
                    sk.BoxitV(
                        sk.Stackit(k="outside", padding=4, spacing=6),
                        bcolor="#1F1F1F",
                    ),
                    size_hint=(1, 1),
                    name="pop",
                    k="pop",
                )
            app.paw()
            app['sman'].add_widget(screen)
            
        app("cont", cols=2, rows=None, size_hint_y=None)
        app['list'].select(0)
    elif ev=='copy-code':
        Clipboard.copy(app['code-s'].text)
    elif ev == "back":
        app("sman", current="show")
    if ev == "list":
        app("msg", text="")
        app("sman", current="show")

        e = app["list"].data_selected[0]
        outside = e["meta"].get("outside", False)
        if outside == True:
            cont = app["outside"]
        elif isinstance(outside, str):
            if outside in app:
                app('sman',current="pop-" + outside)
                return
            else:
                on_open = lambda *_: print(f"entering"+outside)
                on_dismiss = lambda *_: None
                if outside == "-webview":

                    def on_open(*_):
                        (
                            app["webview"].ewin.show()
                            if hasattr(app["webview"], "ewin")
                            else None
                        )
                        (
                            app["webview2"].ewin.show()
                            if hasattr(app["webview2"], "ewin")
                            else None
                        )
                        print("entering webview")

                    def on_dismiss(*_):
                        print("leaving webview")
                        app["webview"].ewin.hide()
                        app["webview2"].ewin.hide()

                elif outside in ("videop", "video", "camera"):

                    def on_dismiss(*_):
                        print("leaving",outside,outside in app)
                        app(outside, state="stop")

                screen=sk.Screen(
                    sk.BoxitV(
                        sk.Stackit(k=outside, padding=4, spacing=6),
                        bcolor="#1F1F1F",
                    ),
                    size_hint=(1, 1),
                    name="pop-" + outside,
                    k="pop-" + outside,
                    bind={
                        "on_pre_enter": on_open,
                        "on_pre_leave": on_dismiss,
                    },
                )
                app['sman'].add_widget(screen)
                app.paw()
                cont = app[outside]

        else:
            pass
            cont = app["cont"]
        cont.clear_widgets()
        for k, c in e["meta"].items():
            if k in ("outside","tags"):
                continue

            row = sk.BoxitH(k=sk.NOTKEY)
            if k:
                lbl = sk.Label(
                    k,
                    size_hint_min_y=30,
                    markup=True,
                    k=sk.NOTKEY,
                    valign="top",
                    halign="left",
                    padding=[8, 8, 8, 8],
                )
            else:
                lbl = sk.Void()
            row.add_widget(lbl)

            code = c.strip()
            env_vars = {"sk": sk}
            for lc in code.splitlines():
                if "# import" in lc:
                    exec_scope = {}
                    other = {}
                    exec(lc.lstrip("#").strip(), other, exec_scope)
                    env_vars.update(exec_scope)
            widget = eval(code, env_vars)
            ncount = k.count("\n")
            if not ncount:
                ncount = 1
            else:
                ncount += 1
            row.height = 30 * ncount if widget.height < 30 * ncount else widget.height
            row.size_hint_y = None
            if getattr(widget, "is_void", False):
                widget_ = widget
            else:
                btn_code = sk.ClearB(
                    sk.mdi("file-code", size=20),
                    k=sk.NOTKEY,
                    size="x30",
                    tooltip_text="View code",
                    lcolor="gray",
                    pos_hint=sk.pos_hints.right_center,
                )
                setattr(btn_code, "code", code)

                def on_btn_code(ins, *x):
                    app("sman", current="code")
                    app("code-s", text=ins.code)
                    app("code-s", cursor=(0,0))

                btn_code.bind(on_release=on_btn_code)

                widget_ = sk.BoxitH(widget, btn_code, spacing=4, k=sk.NOTKEY,bcolor='k')
            row.add_widget(widget_)
            size_hint_min_y = 40

            cont.add_widget(row)
            cont.add_widget(sk.SeparatorH())
        app.paw()
        app("show-s", scroll_y=1)
        if outside == True:
            app('sman',current="pop")
        elif isinstance(outside, str):
            app('sman',current="pop-" + outside)
    elif ev == "pop-close":
        pass
    elif ev == "q":
        app['list'].deselect_all()
        q = app["q"].text.lower()
        nels = []
        elements = []
        for e, ecode in codes.items():
            text_search=e.lower() + ' ' + ecode.get('tags','')
            if q in text_search.strip():
                elements.append(lel(text=e, meta=ecode))
        app("list", data=elements)
def main():
    app = sk.MyApp(
        title="SimpleKivy - showcase",
        layout=lyt,
        event_manager=evman,
        layout_class=sk.kvw.BoxLayoutB,
        layout_args=dict(orientation="horizontal", padding=4, spacing=4),
    )
    app.run()

if __name__=='__main__':
    main()
    pass
