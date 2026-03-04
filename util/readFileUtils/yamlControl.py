import os
import yaml

from  common.setting import ensure_path_sep

# 读yaml文件
class yamlControl:
    
    @staticmethod
    def read_yaml(path:str) -> dict:
        """读取yaml 文件,path可为相对项目根的路径""" 
        ensure_path_sep(os.sep + path.lstrip("/\\")) # 去掉“/\”
        with open(path,encoding="utf-8") as f:
            return yaml.safe_load(f)