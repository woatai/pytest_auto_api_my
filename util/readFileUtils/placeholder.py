"""
占位符解析器
"""

import re
from util.context.context_manager import ContextManager
from common.config import HOST

# 连续匹配一个或多个“不是右大括号 }”的字符，并把这部分内容捕获出来
PLACEHOLDER_PATTERN = re.compile(r"\$\{\{([^}]+)\}\}")

def _call_func(expr:str):
    if expr == "host()":
        return HOST
    raise ValueError(f"不支持的占位符函数: {expr}")

def _resolve_expr(expr:str):
    expr = expr.strip() # 去除前后格

    if expr.endswith("()"):
        return _call_func(expr)
    
    value = ContextManager.get(expr)
    if value is None:
        raise ValueError(f"上下文变量不存在: {expr}")
    return value



def resolve_placeholders(values):
    if isinstance(values,str):
        def repl(match):
           expr =  match.group(1).strip()
           return str(_resolve_expr(expr))
        return PLACEHOLDER_PATTERN.sub(repl,values)
    if isinstance(values,list):
        return [resolve_placeholders(v) for v in values]
    if isinstance(values,dict):
        return {k:resolve_placeholders(v) for k,v in values.items()}
    
    return values


if __name__ == "__main__":
    result =  PLACEHOLDER_PATTERN.match("${{host()}}")
    print(result.group())

    PLACEHOLDER_PATTERN = re.compile(r"\$\{\{([^}]+)\}\}")
