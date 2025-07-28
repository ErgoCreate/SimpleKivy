import SimpleKivy.SimpleKivy as sk

sk.auto_config()

# All the stuff inside your window.
lyt=[
    [sk.Label('Input your name:')],
    [sk.Input(k='i',size='y40')*sk.B('Say hi!',size='x100y40')],
    [sk.T(k='msg')]
]

# Your backend code must be inside a function with 2 arguments (app, event)
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
