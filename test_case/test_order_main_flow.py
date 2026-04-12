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
        url = case["url"]
        method = case["method"]
        data = case.get("data")
        # 非必填
        headers = case.get("headers")
        params = case.get("params")
        resp = RequestControl().send_request(
            method=method, url=url, headers=headers, json=data
        )
        AssertControl(assert_data=case.get("assert"), response=resp).run()
        ExtractControl(case.get("extract"), resp["body"]).run()

    @allure.story("商品列表")
    def test_product_list(self):
        # ContextManager.clear()

        raw_case = get_case_by_id(yaml_name, "product_list")
        case = resolve_placeholders(raw_case)

        # 必填
        url = case["url"]
        method = case["method"]
        # 非必填
        headers = case.get("headers")
        params = case.get("params")
        resp = RequestControl().send_request(
            method=method, url=url, headers=headers, params=params
        )
        AssertControl(assert_data=case.get("assert"), response=resp).run()
        ExtractControl(case.get("extract"), resp["body"]).run()
        assert ContextManager.get("product_id") is not None, "没有提取到 product_id"

    @allure.story("商品详情")
    def test_product_detail(self):
        raw_case = get_case_by_id(yaml_name, "product_detail")
        case = resolve_placeholders(raw_case)

        url = case["url"]
        method = case["method"]
        # 非必填
        headers = case.get("headers")
        params = case.get("params")
        resp = RequestControl().send_request(
            method=method, url=url, headers=headers, params=params
        )
        AssertControl(assert_data=case.get("assert"), response=resp).run()
        ExtractControl(case.get("extract"), resp["body"]).run()
        assert ContextManager.get("unique") is not None, "没有提取到 unique"

    @allure.story("默认价格")
    def test_default_price(self):
        raw_case = get_case_by_id(yaml_name, "default_price")
        case = resolve_placeholders(raw_case)

        # 必填
        url = case["url"]
        method = case["method"]
        data = case.get("data")
        # 非必填
        headers = case.get("headers")
        params = case.get("params")
        resp = RequestControl().send_request(
            method=method, url=url, headers=headers, json=data
        )
        AssertControl(assert_data=case.get("assert"), response=resp).run()
        ExtractControl(case.get("extract"), resp["body"]).run()

    @allure.story("个人中心")
    def test_user_center(self):
        raw_case = get_case_by_id(yaml_name, "user_center")
        case = resolve_placeholders(raw_case)

        # 必填
        url = case["url"]
        method = case["method"]
        data = case.get("data")
        # 非必填
        headers = case.get("headers")
        params = case.get("params")
        resp = RequestControl().send_request(
            method=method, url=url, headers=headers, json=data
        )
        AssertControl(assert_data=case.get("assert"), response=resp).run()
        ExtractControl(case.get("extract"), resp["body"]).run()

    @allure.story("直接购买")
    def test_buy_now(self):
        raw_case = get_case_by_id(yaml_name, "buy_now")
        case = resolve_placeholders(raw_case)

        # 必填
        url = case["url"]
        method = case["method"]
        data = case.get("data")
        # 非必填
        headers = case.get("headers")
        params = case.get("params")
        resp = RequestControl().send_request(
            method=method, url=url, headers=headers, json=data
        )
        AssertControl(assert_data=case.get("assert"), response=resp).run()
        ExtractControl(case.get("extract"), resp["body"]).run()

    
    @allure.story("检查发货")
    def test_check_shipping(self):
        raw_case = get_case_by_id(yaml_name, "check_shipping")
        case = resolve_placeholders(raw_case)

        # 必填
        url = case["url"]
        method = case["method"]
        data = case.get("data")
        # 非必填
        headers = case.get("headers")
        params = case.get("params")
        resp = RequestControl().send_request(
            method=method, url=url, headers=headers, json=data
        )
        AssertControl(assert_data=case.get("assert"), response=resp).run()
        ExtractControl(case.get("extract"), resp["body"]).run()

    @allure.story("获取默认地址")
    def test_get_default_address(self):
        raw_case = get_case_by_id(yaml_name, "get_default_address")
        case = resolve_placeholders(raw_case)

        # 必填
        url = case["url"]
        method = case["method"]
        data = case.get("data")
        # 非必填
        headers = case.get("headers")
        params = case.get("params")
        resp = RequestControl().send_request(
            method=method, url=url, headers=headers, json=data
        )
        AssertControl(assert_data=case.get("assert"), response=resp).run()
        ExtractControl(case.get("extract"), resp["body"]).run() 

    @allure.story("订单确认")
    def test_order_confirm(self):
        raw_case = get_case_by_id(yaml_name, "order_confirm")
        case = resolve_placeholders(raw_case)

        # 必填
        url = case["url"]
        method = case["method"]
        data = case.get("data")
        # 非必填
        headers = case.get("headers")
        params = case.get("params")
        resp = RequestControl().send_request(
            method=method, url=url, headers=headers, json=data
        )
        AssertControl(assert_data=case.get("assert"), response=resp).run()
        ExtractControl(case.get("extract"), resp["body"]).run()


