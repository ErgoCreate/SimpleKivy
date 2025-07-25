from SimpleKivy.utils import auto_config
import SimpleKivy.SimpleKivy as sk

auto_config( size=(800,800) )

layout=[
    [sk.T('Hello world!')]
]

app=sk.MyApp(title='My frist app',layout=layout)
app.run()