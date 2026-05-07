import eel
import sys
import os
import tkinter as tk
from threading import Thread, Timer
from PIL import Image, ImageTk
import hashlib


close_timer = None
sync_scripts = None
should_close_loading = False
INI = {"Assets": "", "BrowserDir": "", "BrowserType" : "", "ServerPort" : "", "MainScript" : ""}


def md5(link):

  try:
    with open(link, 'rb') as f:
      md5_hash = hashlib.md5()
      while True:
        chunk = f.read(4096)
        if not chunk:
          break
        md5_hash.update(chunk)
    return md5_hash.hexdigest()
  except FileNotFoundError:
    
    return None
  except Exception as e:
   
    return None

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
    root.title("Three.js")
 
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
   
    
    
    window_width = 600
    window_height = 380

    x = int((screen_width - window_width) / 2)
    y = int((screen_height - window_height) / 2)
    
    
    try:
        LoadingScreen = Image.open("LoadingScreen")
        LoadingScreen = LoadingScreen.resize((window_width, window_height), Image.LANCZOS)
        _LoadingScreen = ImageTk.PhotoImage(LoadingScreen)
    
    except FileNotFoundError:
        _LoadingScreen = None
        
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    
    
    tk_LoadingScreen = tk.Label(root, image= _LoadingScreen)
    tk_LoadingScreen.place(x=0, y=0, relwidth=1, relheight=1)

  
    
    def check_status():
        if should_close_loading:
            root.destroy()
        
        else:
            root.after(100, check_status)

    root.after(100, check_status)
    root.mainloop()

def read_utf8_file(link):

    try:
        with open(link, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    except FileNotFoundError:
        print(f"Error: File not found at {link}")
        exit()
        return None
    except UnicodeDecodeError:
        print(f"Error: Could not decode file at {link} using UTF-8 encoding.")
        exit()
        return None
        
def ini_filter(data):
    result = []
    item = len(data[0])-1
    
    length = 0
    check = True
    text=''
    
    while item>=length:
        CHR = data[0][item]
        
        if not CHR == ' ' and check == True:
            check = False    
        
        if check == False:      
            text = text+CHR
        
        item=item-1
    result.append(text[::-1])     
    
    item = 0
    length = len(data[1])-1
    check = True
    text=''
    while item<=length:
        CHR = data[1][item]
        
        if not CHR == ' ' and check == True:
            check = False    
        
        if check == False:      
            text = text+CHR
        
        item=item+1
    result.append(text)
    return result
    
def ini_reader(link):
    global INI
    data = read_utf8_file(link).split(chr(10))
    
    for row in data:
        
        if not row == '':
            
            if '=' in row:
                
                Option = row.split('=')
                lenOption = len(Option)
                
                if lenOption > 1:
                    
                    Option = ini_filter(Option)
                    
                    if Option[0] in INI:                        
                        INI[Option[0]] = Option[1]
    
    
    return None

def on_close(page, sockets):
    if not sockets:
        os._exit(0)
 

def init_scripts(Type="init"):
    global sync_scripts
    global web_root
    if sync_scripts is None:
        sync_scripts = []    
    
    array_scripts = read_utf8_file('sync_scripts.txt').split(chr(10))
    
    if Type == "init":    
        for item in array_scripts:
            sync_scripts.append(md5(web_root+'/'+item))
        return None
    else:
        
        if not sync_scripts == []:
            item_id = 0
            for item in array_scripts:
                if item_id<= len(array_scripts)-1:
                    if not md5(web_root+'/'+item) == sync_scripts[item_id]:
                        sync_scripts = []
                        init_scripts(Type="init")
                        return 'true'
                item_id = item_id+1
        
        return 'false'

 
@eel.expose  
def keep_sync():
    global close_timer
    
    if close_timer:
        close_timer.cancel()

    close_timer = Timer(3.38, sync_app)
    close_timer.start()
    
    if init_scripts(Type="sync") == 'false':
    
        return "false"
        
    else:
        
        return "true"        
    
@eel.expose
def close_loading_screen():
    global should_close_loading
    should_close_loading = True

ini_reader('engine.ini')

web_root = get_script_dir()+'/'+INI['Assets']
chrome_path =  get_script_dir()+'/'+INI['BrowserDir']
_port = INI['ServerPort']
index_script = INI['MainScript']
browser_type = INI['BrowserType']


init_scripts()


loading_thread = Thread(target=show_loading_screen)
loading_thread.daemon = True
loading_thread.start()

eel.browsers.set_path(browser_type, chrome_path)
eel.init(web_root, allowed_extensions=['.none']) 


eel.start(index_script, port=int(_port), suppress_error=True, close_callback=None)
