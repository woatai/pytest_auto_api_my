from util.assertion.assert_control import AssertControl
from util.extract.extract_control import ExtractControl
from util.readFileUtils.get_yaml_data_analysis import get_case_by_id
from util.readFileUtils.placeholder import resolve_placeholders
from util.requestsUtils.requestControl import RequestControl


def run_case(yaml_name, case_id, client=None):
    raw_case = get_case_by_id(yaml_name, case_id)
    case = resolve_placeholders(raw_case)

    client = client or RequestControl()
    response = client.send_request(
        method=case["method"],
        url=case["url"],
        headers=case.get("headers"),
        params=case.get("params"),
        json=case.get("data"),
    )

    AssertControl(assert_data=case.get("assert"), response=response).run()
    ExtractControl(case.get("extract"), response["body"]).run()
    return response
