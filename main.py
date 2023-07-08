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
        FFMPEG = CONFIG.readline()[13:-1]
        first_startup = 0
    
    else:
        CONFIG = open('config.txt','w')
        FFMPEG = input("Locate the FFMPEG: ")
        first_startup = 1

        
    action = input("action: ")
    check('action ',action == 'convert' or action == 'clear')
    if first_startup == 0:
        isdefaut = input("Do you want to use config options?[y/N]: ")

    else:
        isdefaut = 'N'
        
    if action == 'convert':
        
        if isdefaut == 'y':
            path = CONFIG.readline()[6:-1]
            check('path ',os.path.exists(path))
            
            width = CONFIG.readline()[7:-1]
            check('width ',str.isdigit(width) and int(width) > 0)
    
            height = CONFIG.readline()[8:-1]
            check('height ',str.isdigit(height) and int(height) > 0)
    
            bitrate = CONFIG.readline()[9:-1]
           
        elif isdefaut == "N":
            path = input("path: ")
            check('path ',os.path.exists(path))
            
            width = input("width: ")
            check('width ',str.isdigit(width) and int(width) > 0)
    
            height = input("height: ")
            check('height ',str.isdigit(height) and int(height) > 0)
    
            bitrate = input('bitrate: ')

            if first_startup == 1:
                CONFIG.write(f'''ffmpeg path: {FFMPEG}
path: {path}
width: {width}
height: {height}
bitrate: {bitrate}''')
                CONFIG.close()

        (convert if os.path.isfile(path) else convert_dir)(
            path, width, height, bitrate
        )
        
    elif action=='clear':
        if isdefaut == 'y':
            path = CONFIG.readline()[6:-1]
            
        elif isdefaut == 'N':
            path = input("path: ")
        clear(path)


#23w0628a:
#加入了首次启动生成配置文件