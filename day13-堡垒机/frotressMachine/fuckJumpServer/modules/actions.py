__author__ = "Alex Li"

from conf import action_registers
from modules import utils

def help_msg():
    '''
    print help msgs
    output the methods that ftotress machine have.
    :return:
    '''
    print("\033[31;1mAvailable commands:\033[0m")
    for key in action_registers.actions:
        print("\t",key)

def excute_from_command_line(argvs):
    '''
    :param argvs:命令行参数
    :return:
    '''
    if len(argvs) < 2:
        # 命令行参数的长度小于2个时调用帮助函数.
        help_msg()
        exit()
    if argvs[1] not in action_registers.actions:
        # 通过命令行输入的方法不存在时报错.
        utils.print_err("Command [%s] does not exist!" % argvs[1], quit=True)
    # 根据命令行输入的方法调用相应的函数
    action_registers.actions[argvs[1]](argvs[1:])