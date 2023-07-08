import os.path
import sys

from ruamel import yaml


def parse_config(path='config.yml'):
    _CONFIG_DATA = {
        'ffmpeg_path': {
            'input_msg': '''Input the location of ffmpeg''',
            'err_msg': '''Invalid path!''',
            'check': lambda _: os.path.exists(_) and os.path.isfile(_),
        },
        'path': {
            'input_msg': '''Input the path of the source media file or direction''',
            'err_msg': '''Invalid path!''',
            'check': lambda _: os.path.exists(_),
        },
        'bitrate': {
            'input_msg': '''Input the target bitrate''',
            'err_msg': '''Invalid bitrate!''',
            'check': lambda _: _ and str(_)[-1] in 'kmg' and str.isdigit(_[:-1]) and int(_[:-1]) > 0
        },
        'width': {
            'input_msg': '''Input the target width''',
            'err_msg': '''Invalid width!''',
            'check': lambda _: (_ and str.isdigit(str(_))) and int(_) > 0,
        },
        'height': {
            'input_msg': '''Input the target height''',
            'err_msg': '''Invalid height!''',
            'check': lambda _: (_ and str.isdigit(str(_))) and int(_) > 0,
        },
    }

    # 打开配置文件.
    try:
        with open(path, encoding='UTF-8') as _file:
            _config = yaml.safe_load(_file)
            _file.close()
    except IOError as error:
        print(error, file=sys.stderr)

    _edited = False
    for _k in _CONFIG_DATA:
        while True:
            _v = input(
                _CONFIG_DATA[_k]['input_msg'] +
                (
                    f''' (default: {_config[_k]})''' if
                    _config.get(_k) and _CONFIG_DATA[_k]['check'](_config.get(_k)) else
                    ''
                ) +
                ''': '''
            )
            if not _v and _config.get(_k) and _CONFIG_DATA[_k]['check'](_config.get(_k)):
                break
            if not _CONFIG_DATA[_k]['check'](_v):
                print(_CONFIG_DATA[_k]['err_msg'], file=sys.stderr)
            else:
                _edited = True
                _config[_k] = _v
                break

    for _k in ['width', 'height']:
        _config[_k] = int(_config[_k])

    return _config, _edited


def convert(ffmpeg_path, path, width, height, bitrate):
    print(
        r'{} -i {} -b:v {} -s {}x{} "{}"'.format(
            ffmpeg_path,
            path,
            bitrate,
            width,
            height,
            os.path.splitext(path)[0],
        ),
    )


def write(config, path='config.yml'):
    _file = open(path, 'w', encoding='UTF-8')
    yaml.dump(config, _file, Dumper=yaml.RoundTripDumper)
    _file.close()


def main():
    _config, _edited = parse_config()

    convert(*[
        _config[_k]
        for _k in ['ffmpeg_path', 'path', 'width', 'height', 'bitrate']
    ])

    if _edited:
        while True:
            _c = input('Update the config file? (y/N)')
            if not _c or _c in 'Nn':
                break
            elif _c in 'Yy':
                write(_config)
                break


if __name__ == '__main__':
    main()
