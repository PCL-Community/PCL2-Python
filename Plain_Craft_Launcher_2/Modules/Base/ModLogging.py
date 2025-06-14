# -*- coding: utf-8 -*-
import datetime
from enum import Enum
from traceback import format_exc as getTraceBack
from os import remove as removeFile, makedirs
from os.path import exists, dirname, abspath, join
import sys


def get_program_dir():
    if getattr(sys, 'frozen', False):
        # Nuitka、PyInstaller 打包后
        return dirname(sys.executable)
    else:
        return dirname(abspath(__file__))


launcher_data_folder = join(get_program_dir(), 'logs')

# 确保日志目录存在
if not exists(launcher_data_folder):
    makedirs(launcher_data_folder)


def now() -> str:
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


class LoggingType(Enum):
    INFO = 'Info'
    WARN = 'Warn'
    ERROR = 'Error'
    FATAL = 'Fatal'

    def __str__(self) -> str:
        return self.value

    def __repr__(self) -> str:
        return self.value


class ModLogging():
    def __init__(
            self,
            module_name: str | None = 'Logging',
    ) -> None:
        """
        Module (Custom) Logging
        
        1. Initializing With Args:
        ---------------------------------
        module_name : str | None = 'Logging' # tell what module use this Logging lib
        
        2. Return:
        ---------------
        None
        """
        self.module_name = module_name

        for i in range(4, 0, -1):
            old_log = f'{launcher_data_folder}/Log{i}.log'
            new_log = f'{launcher_data_folder}/Log{i + 1}.log'
            try:
                with open(old_log, 'r', encoding='utf-8') as f1:
                    with open(new_log, 'w', encoding='utf-8') as f2:
                        f2.write(f1.read())
            except FileNotFoundError:
                pass
        open(f'{launcher_data_folder}/Log1.log', 'w', encoding='utf-8').close()
        try:
            removeFile('crash.log')
        except:
            pass

    def write(
            self,
            message: str,
            log_level: LoggingType
    ) -> None:
        r'''
        Writing A Log Into File
        
        1. Initializaing With Args:
        ---------------------------------
        message : str  # Message want to log
        log_level: str | None = 'INFO' # Log Level
        
        2. Return:
        ---------------
        None
        '''
        try:
            space_map = {
                'Info': '  ',
                'Warn': '  ',
                'Error': ' ',
                'Fatal': ' '
            }
            log_level_str = str(log_level)
            with open(f'{launcher_data_folder}/Log1.log', 'a', encoding='utf-8') as f:
                f.write(f'[{log_level_str}]{space_map[log_level_str]}[{self.module_name}] {now()} > {message}\n')
            color_map = {
                'Info': green,
                'Warn': yellow,
                'Error': red,
                'Fatal': red
            }
            print(
                f'{color_map[log_level_str]}[{log_level_str}]{clear}{space_map[log_level_str]}[{self.module_name}] {now()} > {message}')
        except Exception as ex:
            time = now()
            print(f'[{red}FATAL{clear}] [Logging] {time} > 记录日志时发生错误')
            print(f'[{red}FATAL{clear}] 错误信息：{type(ex).__name__}')
            print(f'[{red}FATAL{clear}] 错误堆栈信息：\n{str(getTraceBack())}')
            with open('crash.log', 'a', encoding='utf-8') as fatal:
                fatal.write(f'[FATAL] [Logging] {time} > 记录日志时发生错误\n')
                fatal.write(f'[FATAL] 错误类型：{type(ex).__name__}\n')
                fatal.write(f'[FATAL] 错误堆栈信息：\n{str(getTraceBack())}\n')


# Console Color Code, using f-string to insert, like {red}[Error]{clear}Exception
clear = '\033[0m'
black = '\033[30m'
red = '\033[31m'
green = '\033[32m'
yellow = '\033[33m'
blue = '\033[34m'
magenta = '\033[35m'
cyan = '\033[36m'
white = '\033[37m'
