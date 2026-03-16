"""
import re
from common.config import HOST

PLACEHOLDER_PATTERN = re.compile(r"\$\{\{([^}]+)\}\}")

def _call_func(expr: str) -> str:
    if expr == "host()":
        return HOST
    raise ValueError(f"不支持的占位符函数: {expr}")

def resolve_placeholders(value):
    if isinstance(value, str):
        def repl(match):
            expr = match.group(1).strip()
            return _call_func(expr)
        return PLACEHOLDER_PATTERN.sub(repl, value)

    if isinstance(value, list):
        return [resolve_placeholders(v) for v in value]

    if isinstance(value, dict):
        return {k: resolve_placeholders(v) for k, v in value.items()}

    return value
    """
"""
from util.readFileUtils.placeholder import resolve_placeholders

def get_yaml_case_data(yaml_name: str) -> dict:
    data = yamlControl.read_yaml(path)
    return resolve_placeholders(data)
"""

"""
if url.startswith("http"):
    full_url = url
else:
    full_url = HOST.rstrip("/") + "/" + url.lstrip("/")

"""