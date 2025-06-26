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
            log_level: LoggingType,
            action: str = "",
            status: str = "正常"
    ) -> None:
        r'''
        Writing A Log Into File
        
        Args:
            message: str - 程序发生了什么
            log_level: LoggingType - 日志级别
            action: str - 干了什么动作（可选）
            status: str - 执行状态（可选，默认为"正常"）
        '''
        try:
            # 获取调用栈信息来确定代码位置
            import inspect
            caller_frame = inspect.currentframe().f_back
            code_location = f"{caller_frame.f_code.co_filename}:{caller_frame.f_lineno}"
            
            # 格式化日志内容：级别+代码位置+时间+干了什么+程序发生了什么+状态
            action_str = f"[{action}] " if action else ""
            log_content = f"[{log_level}] [{code_location}] [{now()}] {action_str}{message} (状态：{status})"
            
            # 写入文件
            with open(f'{launcher_data_folder}/Log1.log', 'a', encoding='utf-8') as f:
                f.write(log_content + '\n')
            
            # 控制台输出带颜色
            color_map = {
                'Info': green,
                'Warn': yellow,
                'Error': red,
                'Fatal': red
            }
            print(f"{color_map[str(log_level)]}{log_content}{clear}")

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
