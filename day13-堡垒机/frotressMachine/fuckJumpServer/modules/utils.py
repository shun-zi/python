__author__ = "Alex Li"
import yaml
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

def print_err(msg,quit=False):
    '''
    :param msg: error message
    :param quit: whether sign out system
    :return:
    '''
    output = "\033[31;1mError: %s\033[0m" % msg
    if quit:
        exit(output)
    else:
        print(output)


def yaml_parser(yml_filename):
    '''
    load yaml file and return
    :param yml_filename:
    :return:
    '''
    #yml_filename = "%s/%s.yml" % (settings.StateFileBaseDir,yml_filename)
    try:
        # 打开yal格式的文件,从中以字典的形式读取内容,并返回.
        yaml_file = open(yml_filename,'r')
        data = yaml.load(yaml_file)
        return data
    except Exception as e:
        # 输出错误信息
        print_err(e)
