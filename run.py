#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sys
import traceback
import pytest

PROJECT_NAME = "pytest_auto_api_my"
ALLURE_RESULT_DIR = "./report/tmp"
ALLURE_HTML_DIR = "./report/html"


def run():
    try:
        print(
            f"""
========================================
开始执行 {PROJECT_NAME} 项目...
========================================
"""
        )

        # 支持运行指定测试文件
        # 例如: python run.py test_case/test_order_main_flow.py
        target = sys.argv[1] if len(sys.argv) > 1 else None

        pytest_args = []
        if target:
            pytest_args.append(target)

        # 执行 pytest
        exit_code = pytest.main(pytest_args)

        print(
            f"""
========================================
pytest 执行完成，退出码: {exit_code}
========================================
"""
        )

        # 生成可通过 file:// 直接打开的 Allure 单文件报告
        subprocess.run(
            [
                "allure",
                "generate",
                ALLURE_RESULT_DIR,
                "-o",
                ALLURE_HTML_DIR,
                "--clean",
                "--single-file",
            ],
            check=True,
        )

        print(
            f"""
========================================
Allure HTML 报告已生成
文件: {ALLURE_HTML_DIR}/index.html
========================================
"""
        )


    except Exception:
        print("run.py 执行过程中出现异常：")
        print(traceback.format_exc())
        raise


if __name__ == "__main__":
    run()

"""pytest test_case/test_order_main_flow.py -q -s -k test_product_list"""
