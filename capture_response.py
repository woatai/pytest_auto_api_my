#!/usr/bin/env python
"""
临时脚本用于捕获API响应数据，用于设计精确断言
"""

import sys
import json
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from util.readFileUtils.get_yaml_data_analysis import get_case_by_id
from util.readFileUtils.placeholder import resolve_placeholders
from util.requestsUtils.requestControl import RequestControl
from util.context.context_manager import ContextManager

def capture_login_response():
    """捕获登录接口响应"""
    print("=== 捕获登录接口响应 ===")

    try:
        # 获取登录用例
        raw_case = get_case_by_id("order_main_flow.yaml", "login")
        print(f"原始用例配置: {json.dumps(raw_case, ensure_ascii=False, indent=2)}")

        # 解析占位符
        case = resolve_placeholders(raw_case)
        print(f"\n解析后用例: {json.dumps(case, ensure_ascii=False, indent=2)}")

        # 发送请求
        print(f"\n发送请求: {case['method']} {case['host']}{case['url']}")
        resp = RequestControl().send_request(
            method=case['method'],
            host=case['host'],
            url=case['url'],
            headers=case.get('headers'),
            json=case.get('data')
        )

        # 打印完整响应
        print(f"\n=== 登录响应数据 ===")
        print(f"状态码: {resp.get('status_code')}")
        print(f"响应头: {resp.get('headers')}")
        print(f"响应文本: {resp.get('text', '')[:500]}...")  # 限制长度
        print(f"响应体类型: {type(resp.get('body'))}")

        # 格式化JSON响应体
        body = resp.get('body')
        if isinstance(body, (dict, list)):
            print(f"\n响应体 (JSON):")
            print(json.dumps(body, ensure_ascii=False, indent=2))
        elif isinstance(body, str):
            try:
                parsed = json.loads(body)
                print(f"\n响应体 (JSON 解析后):")
                print(json.dumps(parsed, ensure_ascii=False, indent=2))
            except:
                print(f"\n响应体 (原始文本):")
                print(body[:1000])
        else:
            print(f"\n响应体: {body}")

        # 提取关键字段示例
        print(f"\n=== 关键字段分析 ===")
        if isinstance(body, dict):
            for key in ['msg', 'code', 'data', 'token', 'userInfo', 'uid']:
                if key in body:
                    print(f"{key}: {body[key]}")
                elif 'data' in body and isinstance(body['data'], dict):
                    if key in body['data']:
                        print(f"data.{key}: {body['data'][key]}")

        return resp

    except Exception as e:
        print(f"捕获登录响应失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def capture_product_list_response(login_resp=None):
    """捕获商品列表接口响应
    Args:
        login_resp: 可选的登录响应，如果不提供则重新登录
    """
    print("\n\n=== 捕获商品列表接口响应 ===")
    # 清除之前的上下文数据
    ContextManager.clear()

    try:
        # 如果需要，先运行登录获取token
        if not login_resp:
            login_resp = capture_login_response()
            if not login_resp:
                print("登录失败，无法继续")
                return None

        # 从登录响应中提取token (简化处理，实际应该用ExtractControl)
        login_body = login_resp.get('body')
        token = None
        if isinstance(login_body, dict) and 'data' in login_body and 'token' in login_body['data']:
            token = login_body['data']['token']
            print(f"提取到的token: {token}")
            # 将token设置到ContextManager，供placeholder解析使用
            ContextManager.set("token", token)
        else:
            print("警告: 未从登录响应中提取到token")
            # 尝试从ContextManager获取（如果之前有存储）

        # 获取商品列表用例
        raw_case = get_case_by_id("order_main_flow.yaml", "product_list")
        case = resolve_placeholders(raw_case)

        # 如果有token，更新headers
        if token and 'headers' in case:
            case['headers']['Authorization'] = f"Bearer {token}"

        print(f"\n发送请求: {case['method']} {case['host']}{case['url']}")
        resp = RequestControl().send_request(
            method=case['method'],
            host=case['host'],
            url=case['url'],
            headers=case.get('headers'),
            params=case.get('params')
        )

        # 打印完整响应
        print(f"\n=== 商品列表响应数据 ===")
        print(f"状态码: {resp.get('status_code')}")

        body = resp.get('body')
        if isinstance(body, (dict, list)):
            print(f"\n响应体 (JSON):")
            print(json.dumps(body, ensure_ascii=False, indent=2))

            # 分析数据结构
            print(f"\n=== 商品列表数据结构分析 ===")
            if isinstance(body, dict):
                if 'data' in body:
                    data = body['data']
                    if isinstance(data, dict):
                        if 'list' in data:
                            products = data['list']
                            if isinstance(products, list) and len(products) > 0:
                                print(f"商品数量: {len(products)}")
                                print(f"第一个商品示例:")
                                first_product = products[0]
                                for key, value in first_product.items():
                                    print(f"  {key}: {value}")
                            else:
                                print("商品列表为空或不是数组")
                        else:
                            print(f"data中缺少list字段，现有字段: {list(data.keys())}")
                    else:
                        print(f"data字段类型为: {type(data)}")
                else:
                    print(f"响应中缺少data字段，现有字段: {list(body.keys())}")
        elif isinstance(body, str):
            try:
                parsed = json.loads(body)
                print(f"\n响应体 (JSON 解析后):")
                print(json.dumps(parsed, ensure_ascii=False, indent=2))
            except:
                print(f"\n响应体 (原始文本):")
                print(body[:1000])

        return resp

    except Exception as e:
        print(f"捕获商品列表响应失败: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    print("开始捕获API响应数据...")

    # 捕获登录响应
    login_resp = capture_login_response()

    # 捕获商品列表响应（传递登录响应避免重复登录）
    if login_resp:
        product_resp = capture_product_list_response(login_resp)
    else:
        print("登录失败，跳过商品列表捕获")

    print("\n=== 捕获完成 ===")