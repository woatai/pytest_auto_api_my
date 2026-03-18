import requests
from urllib3 import request, response


class RequestControl:
    def __init__(self) -> None:
        # 使用session 方便以后 做登录保持
        self.session = requests.Session()

    def send_request(
        self, method, url, headers=None, params=None, data=None, json=None, timeout=10
    ) -> dict:
        if url.startswith("http"):
            url = url
        # else:
        #     url = HOST.rstrip("/") + "/" + url.lstrip("/")

        # 先准备请求，异常时也能取到最终 headers
        req = requests.Request(
            method=method.upper(),
            url=url,
            headers=headers,
            params=params,
            data=data,
            json=json,
        )
        prep = self.session.prepare_request(req)
        request_headers = dict(prep.headers)

        try:
            # response = self.session.request(
            #     method=method.upper(),
            #     url=url,
            #     headers=headers,
            #     params=params,
            #     data=data,
            #     json=json,
            #     timeout=timeout,
            # )
            response = self.session.send(prep, timeout=timeout)
            # 成功后用真实发送的 headers 覆盖
            request_headers = dict(response.request.headers)
        except requests.RequestException as e:
            return {"status_code": None, "body": None, "text": str(e), "headers": None}
        # 尝试解析 JSON
        try:
            body = response.json()
            # 成功后用真实发送的 headers 覆盖
            request_headers = dict(response.request.headers)
        except ValueError:
            body = response.text

        # 统一返回结构
        return {
            "status_code": response.status_code,
            "body": body,
            "text": response.text,
            "headers": dict(response.headers),
            "request_debug": {
                "method": method,
                "url": url,
                "headers": request_headers,
                "params": params,
                "data": data,
                "json": json,
            },
        }
