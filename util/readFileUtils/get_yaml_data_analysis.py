
import os
from common.setting import root_path
from util.readFileUtils.yamlControl import yamlControl
# from util.readFileUtils.placeholder import resolve_placeholders

"""解析 data 目录下的 yaml 用例，返回用例列表（供测试或代码生成使用）
    输入yaml名字 输出 :dict"""


def get_yaml_case_data(yaml_name: str) -> dict:
    """读取data下单的yaml文件,返回完整内容"""
    path = os.path.join(root_path(), "data", yaml_name)
    if not path.endswith(".yaml") and not path.endswith(".yml"):  # 检查
        print("后缀不对，不是 yaml/yml")
    data =  yamlControl.read_yaml(path)
    # return resolve_placeholders(data)
    return data


# 解析 yaml 用例，返回 [ (case_id, case_data), ... ]
# 排除 case_common 和 case_common 下字段。
def get_case_list(yaml_name: str) -> list:
    data = get_yaml_case_data(yaml_name)
    if not data:
        return []
    common = data.get("case_common", {})
    cases = []
    for k, v in data.items():
        if k == "case_common" or not isinstance(v, dict):
            continue
        # 将 allrue yaml文件拼接到每个用例
        merage = {**common, **v}  
        merage["case_id"] = k
        cases.append((k, merage))
    return cases

# 获取case_id
def get_case_by_id(yaml_name:str,case_id:str) -> dict:
    cases = get_case_list(yaml_name)
    for current_case_id,case in cases:
        if current_case_id == case_id:
            return case
    raise ValueError(f"未找到用例: {case_id}")