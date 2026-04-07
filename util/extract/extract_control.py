"""
做提取器，把响应里的值放进上下文
"""

from dataclasses import field
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
            if isinstance(expr, str):
                self._jsonpath_extract(var_name, expr, data)
                continue

            if not isinstance(expr, dict):
                raise AssertionError(f"extract 配置格式错误: {var_name}={expr}")

            extract_type = expr.get("type")

            if extract_type == "conditional_find":
                self._conditional_find_extract(var_name, expr, data)
            else:
                raise AssertionError(f"不支持的提取类型: {extract_type}")

            # if isinstance(expr, dict) and expr.get("type") == "conditional_find":
            #     pass
            # else:
            #     self._jsonpath_extract(var_name,expr,self.response_body)
            # if isinstance()

    def _jsonpath_extract(self, var_name, expr, data):
        """原有 JSONPath 提取"""
        result = jsonpath(data, expr)
        assert (
            result not in (False, None) and len(result) > 0
        ), f"变量提取失败: {var_name}, jsonpath={expr}, body={data}"
        if len(result) == 1:
            ContextManager.set(var_name, result[0])
        else:
            ContextManager.set(var_name, result)

    def _conditional_find_extract(self, var_name, rule, data):
        source = rule.get("source")
        conditions = rule.get("conditions", [])
        pick_field = rule.get("pick_field")
        pick = rule.get("pick", "first")
        required = rule.get("required", False)
        error_message = rule.get("error_message", f"{var_name} 条件提取失败")

        result = jsonpath(data, source)
        assert (
            result not in (False, None) and len(result) > 0
        ), f"变量提取失败: {var_name}, source={source}, body={data}"
        source_data = result[0]
        items = self._normalize_items(source_data)

        matched_items = []
        for item in items:
            if not isinstance(item, dict):
                continue
            if self._match_conditions(item, conditions):
                matched_items.append(item)

        value = self._build_pick_value(
            matched_items=matched_items, pick_field=pick_field, pick=pick
        )

        if (value is None or value == "" or value == []):
            raise AssertionError(error_message)

        # 传进上下文
        ContextManager.set(var_name,value)

    def _normalize_items(self, source_data):
        """将字典或者列表 统一转为可循环的列表"""
        if isinstance(source_data, dict):
            return list(source_data.values())
        if isinstance(source_data, list):
            return source_data

        raise AssertionError(f"条件提取不支持的数据类型：{type(source_data)}")

    def _match_conditions(self, item, conditions):
        """条件匹配"""
        for condition in conditions:
            field = condition.get("field")
            op = condition.get("op")  # ==, !=, >, < 等
            expected = condition.get("value")
            actual = self._get_field_value(item, field)  # 支持 "a.b.c" 嵌套取值

            if not self._compare(actual, op, expected):
                return False

        return True

    def _get_field_value(self, item, field):
        """支持点号分隔的嵌套字段"""
        current = item
        for part in field.split("."):
            if not isinstance(current, dict):
                return None
            current = current.get(part)
        return current

    def _compare(self, actual, op, expected):
        """比较实际和期望值"""
        if actual is None:
            return False

        if op == ">":
            return actual > expected
        if op == "<":
            return actual < expected
        if op == ">=":
            return actual >= expected
        if op == "<=":
            return actual <= expected
        if op == "==":
            return actual == expected
        if op == "!=":
            return actual != expected

        raise AssertionError(f"不支持的条件操作符: {op}")

    def _build_pick_value(self, matched_items, pick_field, pick):
        if not matched_items: # 空列表 [] 的布尔值为 False
            return None
        if pick == "first":
            return self._get_field_value(matched_items[0], pick_field)
        if pick == "all":
            return [self._get_field_value(item,pick_field) for item in matched_items]
        
