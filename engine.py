import eel
import sys
import os
import tkinter as tk
from threading import Thread, Timer
from PIL import Image, ImageTk



close_timer = None
should_close_loading = False

def sync_app():
    
    os._exit(0)


def get_script_dir():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    return str(application_path)
    
def show_loading_screen():
    global root
    root = tk.Tk()
    def check_status():
        if should_close_loading:
            root.destroy()
        else:
            root.after(100, check_status)\

    root.after(100, check_status)
    root.mainloop()

def read_utf8_file(filepath):

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        exit()
        return None
    except UnicodeDecodeError:
        print(f"Error: Could not decode file at {filepath} using UTF-8 encoding.")
        exit()
        return None

def write_utf8_file(filepath, text):

    try:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(text)

    except Exception as e:
        print(f"Error writing to file: {e}")
        exit()


def on_close(page, sockets):
    if not sockets:
        
        os._exit(0)
@eel.expose  
def keep_sync():
    global close_timer
   
    if close_timer:
        close_timer.cancel()

    close_timer = Timer(3.38, sync_app)
    close_timer.start()

@eel.expose
def close_loading_screen():
    global should_close_loading
    should_close_loading = True

loading_thread = Thread(target=show_loading_screen)
loading_thread.daemon = True
loading_thread.start()

        
settings = read_utf8_file("engine.txt").split('[,]')
web_root = get_script_dir()+'/'+settings[0]
chrome_path =  get_script_dir()+'/'+settings[1]
_port = settings[2]
index_script = settings[3]
browser_type = settings[4]

eel.browsers.set_path(browser_type, chrome_path)
eel.init(web_root, allowed_extensions=['.none']) 


eel.start(index_script, port=int(_port), suppress_error=True, close_callback=None)
