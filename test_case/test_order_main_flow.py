import allure
import pytest
from jsonpath import jsonpath
from util.assertion.assert_control import AssertControl
from util.readFileUtils.get_yaml_data_analysis import get_case_by_id
from util.requestsUtils.requestControl import RequestControl
yaml_name = "order_main_flow.yaml"


# 总流程测试
@allure.epic("下单主流程")
@allure.feature("完整流程")
class Test_main_flow:
    @allure.story("商品列表")
    def test_product_list(self):
        case = get_case_by_id(yaml_name, "product_list")
        # 必填
        host = case["host"]
        url = case["url"]
        method = case["method"]
        # 非必填
        headers = case.get("headers")
        params = case.get("params")
        resp = RequestControl().send_request(
            method=method, host=host, url=url, headers=headers, params=params
        )
        AssertControl(assert_data=case.get("assert"),response=resp).run()

"""pytest test_case/test_order_main_flow.py -q -s -k test_product_list"""