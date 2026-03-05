import os
from common.setting import root_path
from util.readFileUtils.yamlControl import yamlControl
"""解析 data 目录下的 yaml 用例，返回用例列表（供测试或代码生成使用）
    输入yaml名字 输出 :dict"""
def get_yaml_case_data(yaml_name:str) -> dict:
    """读取data下单的yaml文件,返回完整内容"""
    path = os.path.join(root_path(),"data",yaml_name)
    if not path.endswith(".yaml") and not path.endswith(".yml"):# 检查
      print("后缀不对，不是 yaml/yml")
    return yamlControl.read_yaml(path)

""""""