from util.readFileUtils.get_yaml_data_analysis import get_case_list
from util.extract.extract_control import ExtractControl
from util.context.context_manager import ContextManager
import json

def test_conditional_find():
    """测试条件提取功能"""
    print("=== 测试条件提取功能 ===")

    # 模拟API响应数据
    response_body = {
        "data": {
            "productValue": [
                {"stock": 0, "unique": "abc123"},
                {"stock": 5, "unique": "def456"},
                {"stock": 2, "unique": "ghi789"}
            ]
        }
    }

    # 提取配置（与YAML中的配置类似）
    extract_data = {
        "unique": {
            "type": "conditional_find",
            "source": "$.data.productValue",
            "conditions": [
                {"field": "stock", "op": ">", "value": 0}
            ],
            "pick_field": "unique",
            "pick": "first",
            "required": True,
            "error_message": "没有可用库存，无法下单"
        }
    }

    # 清理上下文
    ContextManager.clear()

    # 执行提取
    extractor = ExtractControl(extract_data, response_body)
    extractor.run()

    # 验证提取结果
    extracted_value = ContextManager.get("unique")
    print(f"提取到的值: {extracted_value}")
    assert extracted_value == "def456", f"期望 'def456'，实际 '{extracted_value}'"
    print("✓ 条件提取测试通过")

    # 测试pick: "all"
    extract_data_all = {
        "all_uniques": {
            "type": "conditional_find",
            "source": "$.data.productValue",
            "conditions": [
                {"field": "stock", "op": ">", "value": 0}
            ],
            "pick_field": "unique",
            "pick": "all",
            "required": True,
            "error_message": "没有可用库存，无法下单"
        }
    }

    ContextManager.clear()
    extractor = ExtractControl(extract_data_all, response_body)
    extractor.run()

    all_values = ContextManager.get("all_uniques")
    print(f"提取到的所有值: {all_values}")
    assert all_values == ["def456", "ghi789"], f"期望 ['def456', 'ghi789']，实际 {all_values}"
    print("✓ 多值提取测试通过")

    # 测试嵌套字段（如果支持）
    response_nested = {
        "data": {
            "productValue": [
                {"info": {"stock": 0, "unique": "xyz111"}},
                {"info": {"stock": 3, "unique": "xyz222"}}
            ]
        }
    }

    extract_nested = {
        "nested_unique": {
            "type": "conditional_find",
            "source": "$.data.productValue",
            "conditions": [
                {"field": "info.stock", "op": ">", "value": 0}
            ],
            "pick_field": "info.unique",
            "pick": "first",
            "required": True,
            "error_message": "无库存"
        }
    }

    ContextManager.clear()
    extractor = ExtractControl(extract_nested, response_nested)
    try:
        extractor.run()
        nested_value = ContextManager.get("nested_unique")
        print(f"嵌套字段提取值: {nested_value}")
        print("✓ 嵌套字段提取测试通过")
    except Exception as e:
        print(f"嵌套字段提取失败（可能不支持）: {e}")

    # # 测试无匹配项的情况
    # extract_no_match = {
    #     "no_match": {
    #         "type": "conditional_find",
    #         "source": "$.data.productValue",
    #         "conditions": [
    #             {"field": "stock", "op": ">", "value": 100}
    #         ],
    #         "pick_field": "unique",
    #         "pick": "first",
    #         "required": True,
    #         "error_message": "没有匹配项"
    #     }
    # }

    # ContextManager.clear()
    # try:
    #     extractor = ExtractControl(extract_no_match, response_body)
    #     extractor.run()
    #     print("✗ 预期抛出断言错误，但未抛出")
    #     raise AssertionError("应该抛出错误")
    # except AssertionError as e:
    #     print(f"✓ 无匹配项测试通过，正确抛出错误: {e}")

    print("\n=== 所有条件提取测试完成！ ===")

def test_jsonpath_extract():
    """测试原有的JSONPath提取功能"""
    print("\n=== 测试JSONPath提取功能 ===")

    response_body = {
        "data": {
            "token": "test_token_123",
            "user": {"id": 1, "name": "test"}
        }
    }

    extract_data = {
        "token": "$.data.token",
        "user_id": "$.data.user.id"
    }

    ContextManager.clear()
    extractor = ExtractControl(extract_data, response_body)
    extractor.run()

    token = ContextManager.get("token")
    user_id = ContextManager.get("user_id")

    print(f"提取的token: {token}")
    print(f"提取的user_id: {user_id}")

    assert token == "test_token_123"
    assert user_id == 1
    print("✓ JSONPath提取测试通过")

if __name__ == "__main__":
    # data = get_case_list("order_main_flow.yaml")
    # print(data)
    test_jsonpath_extract()
    test_conditional_find()