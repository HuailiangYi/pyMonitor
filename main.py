# coding: utf-8

from __future__ import print_function
import subprocess
import psutil
import configparser
from collections import OrderedDict


def read_config():
    """
    读取配置文件
    :return: app 名称
    """
    cp = configparser.ConfigParser(allow_no_value=True)
    cp.optionxform = str  # 保持原本大小写
    cp.read('config.ini')

    return cp.items("App")


def get_process_id(name):
    """
    基于程序名称获取进程ID列表
    :param name:程序名称
    :return: PID 列表
    """
    child = subprocess.Popen(['pgrep', '-f', name], stdout=subprocess.PIPE, shell=False)
    response = child.communicate()[0]

    return [int(pid) for pid in response.split()]


def get_process_info(pid):
    """
    基于 pid 获取进程的运行数据信息
    :param pid: 进程 id
    :return: 进程状态字典
    """
    result = dict()

    p = psutil.Process(pid)
    result['pid'] = pid
    result['status'] = p.is_running()
    result['cpu'] = round(p.cpu_percent(), ndigits=2)
    result['memory'] = round(p.memory_percent(), ndigits=2)

    return result


def get_app_status(app_list):
    """
    获取列表程序的运行状态
    :param app_list: 程序列表
    :return: 程序运行结果
    """
    survival_app_dict = OrderedDict()
    dead_app_dict = OrderedDict()


    for app in app_list:
        pid_list = get_process_id(app)
        pid_info_list = [get_process_info(pid)for pid in pid_list]
        if len(pid_info_list) == 0:
            """程序挂了"""
            dead_app_dict[app] = {'pid_list': None, 'status': False }
        else:
            survival_app_dict[app] = {'pid_list': pid_info_list, 'status': True }

    return survival_app_dict, dead_app_dict


def output_result(result):
    print("总数：", len(result))
    for key, value in result.items():
        print(key, value)


if __name__ == "__main__":
    app_list = [app[0] for app in read_config()]
    survival_app_dict, dead_app_dict = get_app_status(app_list)

    print("#############正常运行的程序###############")
    output_result(survival_app_dict)

    print("############dump的程序#################")
    output_result(dead_app_dict)

