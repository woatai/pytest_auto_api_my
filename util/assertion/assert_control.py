"""
断言类型封装
"""


class AssertControl:

    def __init__(self, assert_data: dict[str, any], response: dict[str, any]) -> None:
        self.assert_data = assert_data or {}
        self.response = response or {}
        self.status_code = self.response.get("status_code")
        self.response_body = self.response.get("body")
        # 兼容后续在 RequestControl 里加的请求调试信息
        self.request_bug = self.response.get("request_debug", {})

"""
from util.assertion.assert_control import AssertControl

# ...
resp = RequestControl().send_request(
    method=method,
    url=url,
    headers=headers,
    json=data
)

AssertControl(assert_data=case.get("assert"), response=resp).run()
"""