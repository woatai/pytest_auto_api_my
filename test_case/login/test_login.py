# 登录测试
import allure
import pytest

from util.readFileUtils.get_yaml_data_analysis import get_case_list
from util.requestsUtils.requestControl import RequestControl
from util.assertion.assert_control import AssertControl

@allure.epic("下单主流程")
@allure.feature("完整流程")
class TestLogin:
    @allure.story("登录")
    # 把 get_case_list("login.yaml") 返回的每一组 参数名 (case_id, case)  数据依次传给 test_login，
    @pytest.mark.parametrize("case_id, case", get_case_list("login.yaml")) 
    def test_login(self, case_id, case):
        url = case["url"]
        method = case["method"]
        headers = case.get("headers")
        data = case.get("data")
 
        resp = RequestControl().send_request(
            method=method, url=url, headers=headers, json=data
        )
        # 手动断言
        # assert resp["status_code"] == case["assert"]["status_code"]
        AssertControl(assert_data=case.get("assert"),response=resp).run()    



