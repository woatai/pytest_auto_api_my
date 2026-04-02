"""
做提取器，把响应里的值放进上下文
"""

import json

from jsonpath import jsonpath
from util.context.context_manager import ContextManager


class ExtractControl:
    def __init__(self, extract_data: dict, response_body) -> None:
        self.extract_data = extract_data or {}
        self.response_body = response_body

    def run(self):
        if not self.extract_data:
            return

        data = self.response_body
        if isinstance(data, str):
            data = json.loads(data)  # 把字符串转为字典

        for var_name, expr in self.extract_data.items():
            if isinstance(expr, dict) and expr.get("type") == "conditional_find":
                


                
            else:
                self._jsonpath_extract(var_name,expr,self.response_body)


    def _jsonpath_extract(self, var_name, expr, data):
        """ 原有 JSONPath 提取 """
        result = jsonpath(self.response_body, expr)
        assert (
            result not in (False, None) and len(result) > 0
        ), f"变量提取失败: {var_name}, jsonpath={expr}, body={data}"
        if len(result) == 1:
            ContextManager.set(var_name, result[0])
        else:
            ContextManager.set(var_name, result)
