from kivy.uix.widget import Widget 
from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Rectangle
from kivy.core.window import Window

CURSOR_SIZE = 100
CURSOR_SOURCE = 'chenlang.png'

class Root(FloatLayout):
    pass

class Target(Widget):
    def __init__(self, pos=(CURSOR_SIZE*4,CURSOR_SIZE*4), size=(CURSOR_SIZE, CURSOR_SIZE), source = CURSOR_SOURCE, **kwargs):
        super(Target, self).__init__(**kwargs)
        self._pos=pos
        self._size=size
        self._source=source
        self._x = self._pos[0]
        self._y = self._pos[1]        
        with self.canvas:
            Rectangle(pos=self._pos, size=self._size, source=self._source)

class Cursor(Widget):
    def __init__(self, pos=(0,0), size=(CURSOR_SIZE, CURSOR_SIZE), source = CURSOR_SOURCE, **kwargs):
        super(Cursor, self).__init__(**kwargs)
        self._pos=pos
        self._size=size
        self._source=source
        self._x = self._pos[0]
        self._y = self._pos[1]
        
        with self.canvas:
            Rectangle(pos=self._pos, size=self._size, source=self._source)

        self._keyboard = Window.request_keyboard(self._keyboard_closed, self, 'text')
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        if keycode[1] == 'up'   : self._y += CURSOR_SIZE
        if keycode[1] == 'down' : self._y -= CURSOR_SIZE
        if keycode[1] == 'left' : self._x -= CURSOR_SIZE
        if keycode[1] == 'right': self._x += CURSOR_SIZE
        self._pos = (self._x, self._y)
        self._update_canvas()
        
    def _update_canvas(self):
        self.canvas.clear()
        with self.canvas:
            Rectangle(pos=self._pos, size=self._size, source=self._source)
        
class TraceGameApp(App):        
    def build(self):
        self.root_layout = Root()
        self.root_layout.add_widget(Cursor())
        self.root_layout.add_widget(Target())
        return self.root_layout
        
if __name__ == '__main__':
    TraceGameApp().run()
