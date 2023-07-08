import os
import sys


def pause():
    if sys.platform == "win32":
        os.system("pause")


def end(code):
    pause()
    exit(code)


def check(a, b):
    if not b:
        print(a + "invalid!", file=sys.stderr)
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
            convert(_path + "\\" + _, _width, _height, _bitrate)


def clear(_path):
    for i in os.listdir(_path):
        if i.endswith(".scaled.mp4"):
            os.system(rf'del "{_path}\{i}"')


if __name__ == "__main__":
    if os.path.exists("config.txt"):
        CONFIG = open("config.txt", "r")
        first_startup = 0

    else:
        CONFIG = open("config.txt", "w")
        first_startup = 1

    action = input("action[convert/clear/config/help]: ")
    check(
        "action ",
        action == "convert"
        or action == "clear"
        or action == "config"
        or action == "help",
    )
    if first_startup == 0 and action == "convert" or action == "clear":
        isdefaut = input("Do you want to use config options?[y/N]: ")

    else:
        isdefaut = "N"

    if action == "convert":
        if first_startup == 1:
            FFMPEG = input("Locate the FFMPEG: ")
            check("FFMPEG ", os.path.exists(rf"{FFMPEG}"))

        else:
            FFMPEG = CONFIG.readline()[13:-1]
            check("FFMPEG ", os.path.exists(rf"{FFMPEG}"))

        if isdefaut == "y":
            path = CONFIG.readline()[6:-1]
            check("path ", os.path.exists(rf"{path}"))

            width = CONFIG.readline()[7:-1]
            check("width ", str.isdigit(width) and int(width) > 0)

            height = CONFIG.readline()[8:-1]
            check("height ", str.isdigit(height) and int(height) > 0)

            bitrate = CONFIG.readline()[9:-1]
            check("bitrate ", bitrate.endswith("k" or "m" or "g"))

        elif isdefaut == "N":
            path = input("path: ")
            check("path ", os.path.exists(rf"{path}"))

            width = input("width: ")
            check("width ", str.isdigit(width) and int(width) > 0)

            height = input("height: ")
            check("height ", str.isdigit(height) and int(height) > 0)

            bitrate = input("bitrate: ")
            check("bitrate ", bitrate.endswith("k" or "m" or "g"))

            if first_startup == 1:
                CONFIG.write(
                    f"""ffmpeg path: {FFMPEG}
path: {path}
width: 640
height: 360
bitrate: 1024k"""
                )
                CONFIG.close()

        if os.path.isfile(rf"{path}"):
            convert(rf"{path}", rf"{width}", rf"{height}", rf"{bitrate}")

        else:
            convert_dir(rf"{path}", rf"{width}", rf"{height}", rf"{bitrate}")

    elif action == "clear":
        if isdefaut == "y":
            FFMPEG = CONFIG.readline()[13:-1]

            path = CONFIG.readline()[6:-1]
            check("path ", os.path.exists(rf"{path}"))

        elif isdefaut == "N":
            path = input("path: ")
            check("path ", os.path.exists(rf"{path}"))

        clear(path)

    elif action == "config":
        CONFIG.close()
        os.system("del config.txt")
        CONFIG = open("config.txt", "w")
        CONFIG.write(
            """ffmpeg path: 
path: 
width: 640
height: 360
bitrate: 1024k"""
        )
        CONFIG.close()

    elif action == "help":
        print(
            """Actions Instruction:
        convert    the main function
        clear      clear the converted files
        config     create a config file
        help       show this list"""
        )

# 1.4.0.230707b
# 1.加入了检查bitrate是否带有单位的功能
