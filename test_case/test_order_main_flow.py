import allure
import pytest

from util.case_runner import run_case
from util.case_runner import run_flow_steps

YAML_NAME = "order_main_flow.yaml"

ORDER_MAIN_FLOW = [
    ("login/login.yaml", "login_success", "用户登录"),
    ("product/product.yaml", "product_list", "商品列表"),
    ("product/product.yaml", "product_detail", "商品详情"),
    ("product/product.yaml", "default_price", "默认价格"),
    ("user/user.yaml", "user_center", "个人中心"),
    ("cart/cart.yaml", "buy_now", "直接购买"),
    ("order/order.yaml", "check_shipping", "检查发货"),
    ("user/address.yaml", "get_default_address", "获取默认地址"),
    ("order/order.yaml", "order_confirm", "订单确认"),

]

@allure.epic("下单主流程")
@allure.feature("完整流程")
@pytest.mark.usefixtures("flow_context")
class TestMainFlow:
    @allure.story("完整下单流程")
    def test_order_main_flow(self, api_client):
        run_flow_steps(ORDER_MAIN_FLOW, client=api_client)
