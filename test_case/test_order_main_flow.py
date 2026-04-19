import allure
import pytest

from util.case_runner import run_case

YAML_NAME = "order_main_flow.yaml"


@allure.epic("下单主流程")
@allure.feature("完整流程")
@pytest.mark.usefixtures("flow_context")
class TestMainFlow:
    @allure.story("用户登录")
    def test_login(self):
        run_case(YAML_NAME, "login")

    @allure.story("商品列表")
    def test_product_list(self):
        run_case(YAML_NAME, "product_list")

    @allure.story("商品详情")
    def test_product_detail(self):
        run_case(YAML_NAME, "product_detail")

    @allure.story("默认价格")
    def test_default_price(self):
        run_case(YAML_NAME, "default_price")

    @allure.story("个人中心")
    def test_user_center(self,login_init):
        run_case(YAML_NAME, "user_center")

    @allure.story("直接购买")
    def test_buy_now(self):
        run_case(YAML_NAME, "buy_now")

    @allure.story("检查发货")
    def test_check_shipping(self):
        run_case(YAML_NAME, "check_shipping")

    @allure.story("获取默认地址")
    def test_get_default_address(self):
        run_case(YAML_NAME, "get_default_address")

    @allure.story("订单确认")
    def test_order_confirm(self):
        run_case(YAML_NAME, "order_confirm")
