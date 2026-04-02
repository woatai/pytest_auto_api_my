import allure
import pytest
from jsonpath import jsonpath
from util.readFileUtils.placeholder import resolve_placeholders
from util.assertion.assert_control import AssertControl
from util.context.context_manager import ContextManager
from util.extract.extract_control import ExtractControl
from util.readFileUtils.get_yaml_data_analysis import get_case_by_id
from util.requestsUtils.requestControl import RequestControl

yaml_name = "order_main_flow.yaml"


# 总流程测试
@allure.epic("下单主流程")
@allure.feature("完整流程")
class Test_main_flow:
    @allure.story("用户登录")
    def test_login(self):
        raw_case = get_case_by_id(yaml_name, "login")
        case = resolve_placeholders(raw_case)

        # 必填
        host = case["host"]
        url = case["url"]
        method = case["method"]
        data = case.get("data")
        # 非必填
        headers = case.get("headers")
        params = case.get("params")
        resp = RequestControl().send_request(
            method=method, host=host, url=url, headers=headers, json=data
        )
        AssertControl(assert_data=case.get("assert"), response=resp).run()
        ExtractControl(case.get("extract"), resp["body"]).run()

    @allure.story("商品列表")
    def test_product_list(self):
        # ContextManager.clear()

        raw_case = get_case_by_id(yaml_name, "product_list")
        case = resolve_placeholders(raw_case)

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
        AssertControl(assert_data=case.get("assert"), response=resp).run()
        ExtractControl(case.get("extract"), resp["body"]).run()
        assert ContextManager.get("product_id") is not None, "没有提取到 product_id"

    @allure.story("商品详情")
    def test_product_detail(self):
        raw_case = get_case_by_id(yaml_name, "product_detail")
        case = resolve_placeholders(raw_case)

        host = case["host"]
        url = case["url"]
        method = case["method"]
        # 非必填
        headers = case.get("headers")
        params = case.get("params")
        resp = RequestControl().send_request(
            method=method, host=host, url=url, headers=headers, params=params
        )
        AssertControl(assert_data=case.get("assert"), response=resp).run()
        
    
"""pytest test_case/test_order_main_flow.py -q -s -k test_product_list"""
