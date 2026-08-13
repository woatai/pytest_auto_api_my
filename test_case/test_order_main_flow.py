import allure
import pytest

from util.case_runner import run_case
from util.context.context_manager import ContextManager


@allure.epic("下单主流程")
@allure.feature("完整流程")
@pytest.mark.usefixtures("flow_context")
class TestMainFlow:
    @allure.story("完整下单流程")
    def test_order_main_flow(self, api_client):
        with allure.step("用户登录"):
            run_case("login/login.yaml", "login_success", client=api_client)

        with allure.step("商品列表"):
            run_case("product/product.yaml", "product_list", client=api_client)

        with allure.step("商品详情"):
            response = run_case(
                "product/product.yaml", "product_detail", client=api_client
            )

        with allure.step("选择有库存的商品规格"):
            product_values = response["body"]["data"]["productValue"]
            if isinstance(product_values, dict):
                product_values = product_values.values()
            available_product = next(
                (item for item in product_values if item["stock"] > 0),
                None,
            )
            assert available_product is not None, "没有可用库存，无法下单"
            ContextManager.set("unique", available_product["unique"])

        with allure.step("默认价格"):
            run_case("product/product.yaml", "default_price", client=api_client)

        with allure.step("个人中心"):
            run_case("user/user.yaml", "user_center", client=api_client)

        with allure.step("直接购买"):
            run_case("cart/cart.yaml", "buy_now", client=api_client)

        with allure.step("检查发货"):
            run_case("order/order.yaml", "check_shipping", client=api_client)

        with allure.step("获取默认地址"):
            run_case("user/address.yaml", "get_default_address", client=api_client)

        with allure.step("订单确认"):
            run_case("order/order.yaml", "order_confirm", client=api_client)
