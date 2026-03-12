"""
断言类型封装
"""

from typing import Any, Dict
import json
from unittest import result
from jsonpath import jsonpath

class AssertControl:

    def __init__(self, assert_data: dict[str, Any], response: Dict[str, any]) -> None:
        self.assert_data = assert_data or {}
        self.response = response or {}
        self.status_code = self.response.get("status_code")
        self.response_body = self.response.get("body")
        # 兼容后续在 RequestControl 里加的请求调试信息
        self.request_bug = self.response.get("request_debug", {})

    def run(self) -> None:
        assert self.assert_data, " assert 配置不能为空 "

        # 状态码的断言
        self._assert_status_code()

        # 业务断言
        for name, rule in self.assert_data.items():
            if name == "status_code":
                continue
            if not isinstance(rule, dict):
                raise AssertionError(f"断言规则格式错误: {name}={rule}")
            self._assert_json_rule(field_name=name, rule=rule)

    def _assert_status_code(self):
        expected = self.assert_data.get("status_code")
        if expected == None:
            return

        assert self.status_code == expected, self._build_fail_msg(
            field_name="status_code",
            expected=expected,
            actual=self.status_code,
            op="eq",
            jsonpath_expr=None,
        )

    # json断言
    def _assert_json_rule(self, field_name: str, rule: dict[str:any]):
        jsonPah = rule.get("jsonpath")
        type = rule.get("type").lower()
        expected = rule.get("value")

        # 提取实际值
        actual = self._extract_jsonpath(self.response_body, jsonPah)
        

    # 通过jsonpath在body去提取实际变量
    @staticmethod
    def _extract_jsonpath(body: any, expr: str) -> any:
        data = body
        if isinstance(data,str):
            try:
                data = json.loads(data) # 解析成python对象
            except:
                raise AssertionError(f"响应体不是 JSON,无法执行 jsonpath: {expr}. body={body}")
        result = jsonpath(data,expr)
        assert result not in (False,None) and len(result) >0 ,  f"jsonpath 提取失败: expr={expr}, body={data}" 

    # 拼接错误信息
    def _build_fail_msg(
        self,
        field_Name: str,  # 断言的字段名
        expected: any,  # 期望值
        actual: any,  # 实际值
        op: str,  # 断言操作符
        jsonpath_expr: str | None,  # JSONPath 断言
    ) -> str:
        req_method = self.request_debug.get("method")
        req_url = self.request_debug.get("url")
        req_params = self.request_debug.get("params")
        req_data = self.request_debug.get("data")
        req_json = self.request_debug.get("json")
        return (
            f"\n[ASSERT FAIL] {field_Name} ({op})"
            f"\n[ASSERT FAIL] expected={expected} actual={actual}"
            f"\n[ASSERT FAIL] jsonpath={jsonpath_expr or 'N/A'}"
            f"\n[REQUEST] method={req_method or 'N/A'} url={req_url or 'N/A'}"
            f"\n[REQUEST] params={req_params or 'N/A'}"
            f"\n[REQUEST] data={req_data or 'N/A'}"
            f"\n[REQUEST] json={req_json or 'N/A'}"
            f"\n[RESPONSE] status_code={self.status_code} body={self.response_body}"
        )


"""
from __future__ import annotations

import json
from typing import Any, Dict

from jsonpath import jsonpath


class AssertControl:
 
    def run(self) -> None:
        assert self.assert_data, "assert 配置不能为空"

        self._assert_status_code()

        for name, rule in self.assert_data.items():
            if name == "status_code":
                continue
            if not isinstance(rule, dict):
                raise AssertionError(f"断言规则格式错误: {name}={rule}")
            self._assert_json_rule(field_name=name, rule=rule)

    def _assert_status_code(self) -> None:
        expected = self.assert_data.get("status_code")
        if expected is None:
            return

        assert self.status_code == expected, self._build_fail_msg(
            field_name="status_code",
            expected=expected,
            actual=self.status_code,
            op="eq",
            jsonpath_expr=None,
        )

    def _assert_json_rule(self, field_name: str, rule: Dict[str, Any]) -> None:
        jsonpath_expr = rule.get("jsonpath")
        op = (rule.get("type") or "eq").lower()
        expected = rule.get("value")

        if not jsonpath_expr:
            raise AssertionError(f"{field_name} 缺少 jsonpath")

        actual = self._extract_jsonpath(self.response_body, jsonpath_expr)
        passed = self._compare(actual=actual, expected=expected, op=op)

        assert passed, self._build_fail_msg(
            field_name=field_name,
            expected=expected,
            actual=actual,
            op=op,
            jsonpath_expr=jsonpath_expr,
        )

    @staticmethod
    def _extract_jsonpath(body: Any, expr: str) -> Any:
        data = body
        if isinstance(data, str):
            try:
                data = json.loads(data)
            except json.JSONDecodeError:
                raise AssertionError(f"响应体不是 JSON，无法执行 jsonpath: {expr}. body={body}")

        result = jsonpath(data, expr)
        assert result not in (False, None) and len(result) > 0, (
            f"jsonpath 提取失败: expr={expr}, body={data}"
        )

        return result[0] if len(result) == 1 else result

    @staticmethod
    def _compare(actual: Any, expected: Any, op: str) -> bool:
        if op in ("eq", "==", "equals"):
            return actual == expected
        if op in ("ne", "!="):
            return actual != expected
        if op == "in":
            return str(expected) in str(actual)
        if op == "contains":
            return str(expected) in str(actual)

        raise AssertionError(f"不支持的断言类型 type={op}")

    def _build_fail_msg(
        self,
        field_name: str,
        expected: Any,
        actual: Any,
        op: str,
        jsonpath_expr: str | None,
    ) -> str:
        req_method = self.request_debug.get("method")
        req_url = self.request_debug.get("url")
        req_params = self.request_debug.get("params")
        req_data = self.request_debug.get("data")
        req_json = self.request_debug.get("json")

        return (
            f"\n[ASSERT FAIL] field={field_name}, op={op}, expected={expected}, actual={actual}"
            f"\n[ASSERT FAIL] jsonpath={jsonpath_expr}"
            f"\n[REQUEST] method={req_method}, url={req_url}"
            f"\n[REQUEST] params={req_params}"
            f"\n[REQUEST] data={req_data}"
            f"\n[REQUEST] json={req_json}"
            f"\n[RESPONSE] status_code={self.status_code}, body={self.response_body}"
        )
"""
