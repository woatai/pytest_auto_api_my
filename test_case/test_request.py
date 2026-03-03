from util.requestsUtils.requestControl import RequestControl


def test_httpbin_get():
    re = RequestControl()
    result = re.send_request(
        method="GET",
        url="https://httpbin.org/get",
        params={"name" : "test"}
    )

    print(result["body"])

    assert result["status_code"] == 200
