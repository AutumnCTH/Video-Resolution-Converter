import os
import sys


def pause():
    if sys.platform=='win32':
        os.system('pause')

def end(code):
    pause()
    exit(code)

def check(a,b):
    if not b:
        print(a +'invalid!', file=sys.stderr)
        if first_startup == 1:
            CONFIG.close()
            os.system("del config.txt")
        end(1)

def convert(_path, _width, _height, _bitrate):
    os.system(
        rf'{FFMPEG} -i "{_path}" -b:v {_bitrate} -s {_width}x{_height} "{_path[:-4] + ".scaled.mp4"}"'
    )

def convert_dir(_path, _width, _height, _bitrate):
    for _ in os.listdir(_path):
        if _.endswith(".mp4") and not _.endswith(".scaled.mp4"):
            convert(_path+'\\'+_,_width,_height,_bitrate)

def clear(_path):
    for i in os.listdir(_path):
        if i.endswith(".scaled.mp4"):
            os.system(rf'del "{_path}\{i}"')


if __name__ == "__main__":
    if os.path.exists('config.txt'):
        CONFIG = open('config.txt','r')
        first_startup = 0
    
    else:
        CONFIG = open('config.txt','w')
        first_startup = 1

        
    action = input("action: ")
    check('action ',action == 'convert' or action == 'clear' or action == "config")
    if first_startup == 0 and action == 'convert' or action == 'clear':
        isdefaut = input("Do you want to use config options?[y/N]: ")

    else:
        isdefaut = 'N'
        
    if action == 'convert':
        if first_startup == 1:
            FFMPEG = input("Locate the FFMPEG: ")
            check('FFMPEG ', os.path.exists(fr"{FFMPEG}"))
            
        else:
            FFMPEG = CONFIG.readline()[13:-1]
            check('FFMPEG ', os.path.exists(fr"{FFMPEG}"))
        
        if isdefaut == 'y':
            path = CONFIG.readline()[6:-1]
            check('path ',os.path.exists(fr'{path}'))
            
            width = CONFIG.readline()[7:-1]
            check('width ',str.isdigit(width) and int(width) > 0)
    
            height = CONFIG.readline()[8:-1]
            check('height ',str.isdigit(height) and int(height) > 0)
    
            bitrate = CONFIG.readline()[9:-1]
           
            
        elif isdefaut == "N":
            
            path = input("path: ")
            check('path ',os.path.exists(fr'{path}'))
            
            width = input("width: ")
            check('width ',str.isdigit(width) and int(width) > 0)
    
            height = input("height: ")
            check('height ',str.isdigit(height) and int(height) > 0)
    
            bitrate = input('bitrate: ')

            if first_startup == 1:
                CONFIG.write(f'''ffmpeg path: {FFMPEG}
path: {path}
width: 640
height: 360
bitrate: 1024k''')
                CONFIG.close()


        if os.path.isfile(fr'{path}'):
            convert(fr'{path}',fr'{width}', fr'{height}', fr'{bitrate}')
            
        else:
            convert_dir(fr'{path}',fr'{width}', fr'{height}', fr'{bitrate}')
        
        
    elif action == 'clear':
        if isdefaut == 'y':
            FFMPEG = CONFIG.readline()[13:-1]
            
            path = CONFIG.readline()[6:-1]
            check('path ',os.path.exists(fr'{path}'))
            
        elif isdefaut == 'N':
            path = input("path: ")
            check('path ',os.path.exists(fr'{path}'))
            
        clear(path)
        
        
    elif action == "config":
        CONFIG.close()
        os.system("del config.txt")
        CONFIG = open('config.txt','w')
        CONFIG.write('''ffmpeg path: 
path: 
width: 640
height: 360
bitrate: 1024k''')
        CONFIG.close()

#1.3.1.230707a:
#1.修复了clear功能使用默认配置时，将path错误定位到FFMPEG行的问题
