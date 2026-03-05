# -*- coding: utf-8 -*-
"""环境与路径配置"""

import os
from typing import Text

def root_path() -> Text:
    """拿到项目根路径 去掉两次文件名""" 
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def ensure_path_sep(path: Text) -> Text:
    """兼容 Windows / Linux 路径"""
    if "/" in path:
        path = os.sep.join(path.split("/"))
    if "\\" in path:
        path = os.sep.join(path.split("\\"))
    return root_path() + os.sep + path.lstrip("/\\")
