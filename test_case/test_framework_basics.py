import pytest
import requests

from common.config import HOST
from util.assertion.assert_control import AssertControl
from util.context.context_manager import ContextManager
from util.extract.extract_control import ExtractControl
from util.readFileUtils.placeholder import resolve_placeholders
from util.requestsUtils.requestControl import RequestControl


class FakeResponse:
    def __init__(self, prepared_request):
        self.status_code = 200
        self.headers = {"Content-Type": "application/json"}
        self.text = '{"ok": true}'
        self.request = prepared_request

    def json(self):
        return {"ok": True}


def test_request_control_uses_default_host(monkeypatch):
    captured = {}

    def fake_send(self, prepared_request, timeout=None):
        captured["url"] = prepared_request.url
        captured["method"] = prepared_request.method
        captured["timeout"] = timeout
        return FakeResponse(prepared_request)

    monkeypatch.setattr(requests.Session, "send", fake_send)

    response = RequestControl().send_request(method="GET", url="/health")

    assert captured["url"] == f"{HOST.rstrip('/')}/health"
    assert captured["method"] == "GET"
    assert captured["timeout"] == 10
    assert response["status_code"] == 200
    assert response["body"] == {"ok": True}


def test_placeholder_resolves_context_value():
    ContextManager.clear()
    ContextManager.set("token", "abc123")

    resolved = resolve_placeholders(
        {"headers": {"Authorization": "Bearer ${{token}}"}}
    )

    assert resolved["headers"]["Authorization"] == "Bearer abc123"


def test_placeholder_missing_context_raises():
    ContextManager.clear()

    with pytest.raises(ValueError, match="上下文变量不存在: token"):
        resolve_placeholders({"headers": {"Authorization": "Bearer ${{token}}"}})


def test_assert_control_runs_with_local_response():
    response = {
        "status_code": 200,
        "body": {"msg": "success", "data": {"id": 1}},
        "request_debug": {"method": "GET", "url": "http://local/api"},
    }
    assert_data = {
        "status_code": 200,
        "msg": {"jsonpath": "$.msg", "type": "contains", "value": "succ"},
        "id": {"jsonpath": "$.data.id", "type": "eq", "value": 1},
    }

    AssertControl(assert_data=assert_data, response=response).run()


def test_extract_control_supports_jsonpath_and_conditional_find():
    ContextManager.clear()
    response_body = {
        "data": {
            "token": "token_123",
            "productValue": [
                {"stock": 0, "unique": "abc123"},
                {"stock": 5, "unique": "def456"},
            ],
        }
    }

    ExtractControl(
        {
            "token": "$.data.token",
            "unique": {
                "type": "conditional_find",
                "source": "$.data.productValue",
                "conditions": [{"field": "stock", "op": ">", "value": 0}],
                "pick_field": "unique",
                "pick": "first",
                "required": True,
            },
        },
        response_body,
    ).run()

    assert ContextManager.get("token") == "token_123"
    assert ContextManager.get("unique") == "def456"
