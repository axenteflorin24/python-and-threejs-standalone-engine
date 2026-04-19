import eel
import sys
import os
import tkinter as tk
from threading import Thread
from PIL import Image, ImageTk

def get_script_dir():
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    return str(application_path)
    


def show_loading_screen():
    global root
    root = tk.Tk()
    root.title("Three.js")
    
    window_width, window_height = 600, 380
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int(screen_width/2 - window_width/2)
    center_y = int(screen_height/2 - window_height/2)
    root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

    img_open = Image.open("SplashScreen.data")

    img_open = img_open.resize((600, 380))
        
    photo = ImageTk.PhotoImage(img_open)
        
    
    img_label = tk.Label(root, image=photo, bg="white")
    img_label.image = photo
    img_label.pack()
    
    label = tk.Label(root, text="", pady=20)
    label.pack()
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
    print(f"Fereastra {page} a fost închisă. Închid aplicația...")
    sys.exit()

@eel.expose
def close_loading_screen():
    if 'root' in globals():
        root.after(0, root.destroy)

loading_thread = Thread(target=show_loading_screen)
loading_thread.start()


        
settings = read_utf8_file("engine.txt").split('[,]')
web_root = get_script_dir()+'/'+settings[0]
chrome_path =  get_script_dir()+'/'+settings[1]
_port = settings[2]
index_script = settings[3]
browser_type = settings[4]

eel.browsers.set_path(browser_type, chrome_path)
eel.init(web_root)


eel.start(index_script, port=int(_port), close_callback=on_close)
