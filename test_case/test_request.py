from util.requestsUtils.requestControl import RequestControl


def test_httpbin_get():
    # 测试request工具
    re = RequestControl()
    result = re.send_request(
        method="GET",
        url="/get",
        params={"name" : "test"}
    )

    print(result["body"])

    assert result["status_code"] == 200



