import os
import yaml

from  common.setting import ensure_path_sep

# 读yaml文件
class yamlControl:
    
    @staticmethod
    def read_yaml(path:str) -> dict:
        """读取yaml 文件,path可为相对项目根的路径""" 
        if not os.path.isabs(path):
            path = ensure_path_sep(os.sep + path.lstrip("/\\")) # 如果不是绝对路径就转换成绝对路径
        with open(path,encoding="utf-8") as f:
            return yaml.safe_load(f)