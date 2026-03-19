# 占位符解析
from math import isfinite
import re

from common.config import HOST

PLACEHOLDER_PATTERN = re.compile(r"\$\{\{([^}]+)\}\}")

def _call_func(expr:str):
    if expr == "host()":
        return HOST
    raise ValueError(f"不支持的占位符函数: {expr}")

def resolve_placeholders(values):
    if isinstance(values,str):
        def repl(match):
           expr =  match.group(1).strip()
           return _call_func(expr)
        return PLACEHOLDER_PATTERN.sub(repl,values)
    if isinstance(values,list):
        return [resolve_placeholders for v in values]
    if isinstance(values,dict):
        return {k:resolve_placeholders(v) for k,v in values.items()}
    
    return values


if __name__ == "__main__":
    result =  PLACEHOLDER_PATTERN.match("${{host()}}")
    print(result.group())

    PLACEHOLDER_PATTERN = re.compile(r"\$\{\{([^}]+)\}\}")
