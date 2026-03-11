import requests
from urllib3 import request
from common.config import HOST


class RequestControl:
    def __init__(self) -> None:
        # 使用session 方便以后 做登录保持
        self.session = requests.Session()

    def send_request(
        self, method, url, headers=None, params=None, data=None, json=None, timeout=10
    ) -> dict:
        url = HOST.rstrip("/") + "/" + url.lstrip("/")
        try:
            response = self.session.request(
                method=method.upper(),
                url=url,
                headers=headers,
                params=params,
                data=data,
                json=json,
                timeout=timeout,
            )
        except requests.RequestException as e:
            return {"status_code": None, "body": None, "text": str(e), "headers": None}
        # 尝试解析 JSON
        try:
            body = response.json()
        except ValueError:
            body = response.text

        # 统一返回结构
        return {
            "status_code": response.status_code,
            "body": body,
            "text": response.text,
            "headers": dict(response.headers),
            "request_debug": {
                method: method,
                url: url,
                params: params,
                data: data,
                json: json,
            },
        }
