# from kivy.clock import Clock
import platform
import os
import sys
import traceback
import random
import time

platform='unknown'
if sys.platform.lower().startswith('win'):
	# return 'Windows'
	platform='win'
elif sys.platform.lower() == 'darwin':
	# return 'macOS'
	platform='macosx'
elif sys.platform.lower().startswith('linux'):
	# return 'Linux'
	platform='linux'
elif 'ANDROID_SDK_ROOT' in os.environ: # Android is usually in the environment, if not on the OS directly
	# return 'Android'
	platform='android'
elif 'ios' in str(platform.system().lower()):
	# return 'iOS'
	platform='ios'

if platform=='win':
    import win32con
    import win32gui
    import win32api
    import ctypes
    from ctypes import wintypes

    # Extended DWMWA constants
    DWMWA_USE_IMMERSIVE_DARK_MODE = 20
    DWMWA_CAPTION_COLOR = 35
    DWMWA_TEXT_COLOR = 36
    DWMWA_BORDER_COLOR = 34
    DWMWA_VISIBLE_FRAME_BORDER_THICKNESS = 37

    def hide_window_by_title(window_title):
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd:
            win32gui.ShowWindow(hwnd, win32con.SW_HIDE)
            return True
        return False
    def console_hide():
        utitle="".join([str(random.randint(0,9)) for i in range(7)])
        os.system(f'TITLE '+utitle)
        hide_window_by_title(utitle)

    def find_hwnd_by_title(title):
        hwnd = win32gui.FindWindow(None, title)
        if hwnd:
            return hwnd
        else:
            def callback(hwnd, hwnds):
                if title in win32gui.GetWindowText(hwnd):
                    hwnds.append(hwnd)
                return True
            hwnds = []
            win32gui.EnumWindows(callback, hwnds)
            if hwnds:
                return hwnds[0]
            else:
                raise Exception("Window not found!")

    

    class ExternalWindow:
        def __init__(self, hwnd):
            """
            Initialize with the window handle (hwnd).
            """
            if not win32gui.IsWindow(hwnd):
                raise ValueError(f"Invalid window handle: {hwnd}")
            self.hwnd = hwnd
            self._on_top=False

        @property
        def title(self):
            return win32gui.GetWindowText(self.hwnd)
        
        @property
        def on_top(self):
            return self._on_top
        
        @on_top.setter
        def on_top(self,v):
            self._on_top=v
            self.always_on_top(v)
        
        def move(self, x, y):
            x,y=int(x),int(y)
            """
            Move the window to a new position without resizing.
            """
            _, _, width, height = self.get_position()
            win32gui.MoveWindow(self.hwnd, x, y, width, height, True)
        
        def resize(self, width, height):
            width=int(width)
            height=int(height)
            """
            Resize the window without moving its position.
            """
            x, y, _, _ = self.get_position()
            win32gui.MoveWindow(self.hwnd, x, y, width, height, True)

        def move_n_resize(self, x, y, width, height):
            x,y=int(x),int(y)
            width=int(width)
            height=int(height)
            """
            Move and resize the window.
            """
            win32gui.MoveWindow(self.hwnd, x, y, width, height, True)
        

        def minimize(self):
            """
            Minimize the window.
            """
            win32gui.ShowWindow(self.hwnd, win32con.SW_MINIMIZE)
        
        def show(self):
            win32gui.ShowWindow(self.hwnd, win32con.SW_SHOW)
        def hide(self):
            win32gui.ShowWindow(self.hwnd, win32con.SW_HIDE)


        def maximize(self):
            """
            Maximize the window.
            """
            win32gui.ShowWindow(self.hwnd, win32con.SW_MAXIMIZE)

        def restore(self):
            """
            Restore the window (if minimized or maximized).
            """
            win32gui.ShowWindow(self.hwnd, win32con.SW_RESTORE)

        def always_on_top(self, enable=True):
            """
            Set or unset the window as always on top.
            """
            win32gui.SetWindowPos(
                self.hwnd,
                win32con.HWND_TOPMOST if enable else win32con.HWND_NOTOPMOST,
                0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
            )

        def unfocusable(self):
            """
            Make the window unfocusable.
            """
            style = win32gui.GetWindowLong(self.hwnd, win32con.GWL_EXSTYLE)
            win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, style | win32con.WS_EX_NOACTIVATE)

        def get_position(self):
            """
            Get the current position and size of the window.
            """
            rect = win32gui.GetWindowRect(self.hwnd)
            x, y, right, bottom = rect
            return x, y, right - x, bottom - y

        def get_rect(self):
            return win32gui.GetWindowRect(self.hwnd)

        def bring_to_front(self):
            """
            Bring the window to the front.
            """
            win32gui.SetForegroundWindow(self.hwnd)
        
        def close(self):
            """
            Close the window gracefully.
            """
            win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)
        
        def remove_titlebar(self):
            """
            Remove the title bar and border of the window.
            """
            style = win32gui.GetWindowLong(self.hwnd, win32con.GWL_STYLE)
            # Remove WS_CAPTION and WS_THICKFRAME styles
            new_style = style & ~win32con.WS_CAPTION & ~win32con.WS_THICKFRAME
            win32gui.SetWindowLong(self.hwnd, win32con.GWL_STYLE, new_style)
            # Apply the new style with a redraw
            win32gui.SetWindowPos(
                self.hwnd, None, 0, 0, 0, 0,
                win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_FRAMECHANGED
            )

        def is_open(self):
            """
            Check if the window is still open.
            """
            return win32gui.IsWindow(self.hwnd)


        @staticmethod
        def find_window(title=None, class_name=None):
            """
            Find a window by its title or class name and return its handle.
            """
            return win32gui.FindWindow(class_name, title)

        def set_parent(self,parent_hwnd):
            win32gui.SetParent(self.hwnd, parent_hwnd)
            set_constant_window_colors(parent_hwnd)
            new_ex_style=win32con.WS_EX_TOOLWINDOW #| win32con.WS_EX_STATICEDGE
            win32gui.SetWindowLong(self.hwnd, win32con.GWL_EXSTYLE, new_ex_style)

        def close(self):
            if win32gui.IsWindow(self.hwnd):
                win32gui.PostMessage(self.hwnd, win32con.WM_CLOSE, 0, 0)
                print(f"WM_CLOSE message sent to window with HWND: {self.hwnd}")
            else:
                print(f"Invalid HWND: {self.hwnd}. Window does not exist or is not a valid window.")


    import clr
    import time
    clr.AddReference("System.Windows.Forms")
    clr.AddReference('System.Drawing')
    clr.AddReference("System")
    # clr.AddReference('System.Action')
    import threading
    import System
    from System.Drawing import Bitmap, Color, Font, FontStyle, Size, Point, ContentAlignment
    from System.Windows.Forms import (
        Form, Application, PictureBox, Label, 
        FormBorderStyle, BorderStyle
    )

    class SplashScreen:
        def __init__(self, image_path=None, text="Loading...", font_size=12,keep_on_top=False):
            self.keep_on_top=keep_on_top
            if image_path==None:
                # from kivy.resources import resource_find,resource_add_path
                # image_path=resource_find("skdata/logo/simplekivy-splash-512.png")
                if not image_path:
                    SK_PATH_FILE = os.path.abspath(__file__)
                    SK_PATH = os.path.dirname(SK_PATH_FILE)
                    # resource_add_path(SK_PATH)
                    image_path=os.path.join(SK_PATH,"skdata/logo/simplekivy-splash-512.png")

                
                image_path=image_path
            self.image_path = image_path
            self.text = text
            self.font_size = font_size
            self.form = None
            self.thread = None
            self._close_requested = False
            self._lock = threading.Lock()
            self._closed=False
            self.open=self.show
        def show(self):
            """Start the splash screen in a separate thread."""

            if self.thread is not None and self.thread.is_alive():
                return

            self.thread = threading.Thread(target=self._run_form)
            self.thread.daemon = True
            self.thread.start()
            

        def close(self):
        	# self.form.Close()
        	# Application.Exit()
            """Request the splash screen to close from any thread."""
            try:
                with self._lock:
                    self._close_requested = True
                if self.form is not None and not self.form.IsDisposed:
                    # Use Invoke to safely close the form from any thread
                    self.form.Invoke(System.Action(self.form.Close))
                    # self.form.Invoke(System.Action(Application.Exit))
                # while not self._closed:
                # 	time.sleep(.001)
                # self.form.Close()
            except:
                traceback.print_exc()

        def _run_form(self):
            """Main method to run the form in the thread."""
            # Initialize the form
            # print('hell')
            self.form = Form()
            self.form.FormBorderStyle = getattr( FormBorderStyle,"None")
            self.form.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen
            self.form.TopMost = True
            self.form.ShowInTaskbar = False

            # Load the image
            try:
                bitmap = Bitmap(self.image_path)
                self.form.Size = bitmap.Size
                
                # PictureBox for the image
                picture_box = PictureBox()
                picture_box.Image = bitmap
                picture_box.Dock = System.Windows.Forms.DockStyle.Fill
                picture_box.SizeMode = System.Windows.Forms.PictureBoxSizeMode.StretchImage
                self.form.Controls.Add(picture_box)
                
                # Label for the text
                if self.text:
                    label = Label()
                    label.Text = self.text
                    label.ForeColor = Color.White
                    label.BackColor = Color.Transparent
                    label.Font = Font("Arial", self.font_size, FontStyle.Bold)
                    label.TextAlign = ContentAlignment.BottomCenter
                    label.Dock = System.Windows.Forms.DockStyle.Bottom
                    label.Height = 40  # Adjust as needed
                    label.Padding = System.Windows.Forms.Padding(0, 0, 0, 10)
                    picture_box.Controls.Add(label)
                
                # Check for close requests periodically
                timer = System.Windows.Forms.Timer()
                timer.Interval = 100  # Check every 100ms
                timer.Tick += self._check_close_request
                timer.Start()
                
                # Run the application
                Application.Run(self.form)
                self._closed=True
                # print('finished')
                
            except Exception as e:
                print(f"Error creating splash screen: {e}")
                if self.form is not None:
                    self.form.Close()

        def _check_close_request(self, sender, event_args):
            """Check if close was requested from another thread."""
            with self._lock:
                if self._close_requested and self.form is not None and not self.form.IsDisposed:
                    self.form.Close()
                else:
                    try:
                        self.form.TopMost = self.keep_on_top
                    except:
                        pass

    def set_constant_window_colors(hwnd, 
                                 bg_color=0x00000000,
                                 text_color=0xFFFFFF,
                                 border_color=0x00000000,  # Black border
                                 border_thickness=1):      # 1 pixel border
        """
        Set window colors that won't change when window loses focus
        
        Parameters:
        - hwnd: Window handle
        - bg_color: Title bar color (0xAARRGGBB)
        - text_color: Title text color (0xAARRGGBB)
        - border_color: Window border color (0xAARRGGBB)
        - border_thickness: Border width in pixels
        """
        if not hwnd:
            return False
        
        try:
            # First try Windows 11+ attributes
            if hasattr(ctypes.windll, 'dwmapi'):
                # Set border color (Windows 11 22H2+)
                border = ctypes.c_int(border_color)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_BORDER_COLOR,
                    ctypes.byref(border),
                    ctypes.sizeof(border)
                )
                
                # Set border thickness (Windows 11 22H2+)
                thickness = ctypes.c_int(border_thickness)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_VISIBLE_FRAME_BORDER_THICKNESS,
                    ctypes.byref(thickness),
                    ctypes.sizeof(thickness)
                )
                
                # Set title bar colors
                bg = ctypes.c_int(bg_color)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_CAPTION_COLOR,
                    ctypes.byref(bg),
                    ctypes.sizeof(bg)
                )
                
                text = ctypes.c_int(text_color)
                ctypes.windll.dwmapi.DwmSetWindowAttribute(
                    hwnd,
                    DWMWA_TEXT_COLOR,
                    ctypes.byref(text),
                    ctypes.sizeof(text)
                )
            
            # Fallback for Windows 10 or older
            else:
                # This will only work for the title bar, not the border
                style = win32gui.GetWindowLong(hwnd, win32con.GWL_STYLE)
                win32gui.SetWindowLong(hwnd, win32con.GWL_STYLE, style | win32con.WS_BORDER)
            
            # Force redraw
            win32gui.RedrawWindow(
                hwnd,
                None,
                None,
                win32con.RDW_FRAME | win32con.RDW_INVALIDATE | 
                win32con.RDW_UPDATENOW | win32con.RDW_ALLCHILDREN
            )
            
            return True
        except Exception as e:
            print(f"Error setting window attributes: {e}")
            return False


# s=SplashScreen()
# s.show()
# time.sleep(4)
# s.close()