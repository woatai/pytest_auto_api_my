# pytest-auto-api-my 简单说明

## 1. 项目简介

这是一个基于 `pytest + requests + yaml` 的接口自动化测试项目。

它的目标是把接口测试数据写在 `yaml` 文件里，再通过 `pytest` 自动读取、发送请求、执行断言。

## 2. 基本功能

当前项目的基础功能包括：

- 读取 YAML 测试用例
- 支持公共参数合并
- 支持简单占位符替换
- 封装 HTTP 请求发送
- 使用 pytest 参数化执行用例
- 统一处理接口断言

## 3. 目录结构

```text
pytest_auto_api_my
├─ common                # 配置文件与环境管理
├─ data                  # YAML 测试数据
├─ docs                  # 项目文档
├─ test_case             # pytest 测试用例
├─ util
│  ├─ assertion          # 断言工具
│  ├─ context            # 上下文管理
│  ├─ extract            # 数据提取
│  ├─ readFileUtils      # YAML 读取与占位符处理
│  └─ requestsUtils      # 请求封装
├─ pytest.ini            # pytest 配置
└─ run.py                # 本地调试入口
```

## 4. 执行流程

```text
编写 YAML 用例
    ↓
读取并解析 YAML
    ↓
替换占位符
    ↓
发送接口请求
    ↓
执行断言
    ↓
输出 pytest 结果
```

## 5. YAML 用例示例

```yaml
case_common:
  headers:
    Content-Type: application/json

login_success:
  url: /login
  method: post
  data:
    username: test
    password: 123456
  assert:
    status_code: 200
```

## 6. 测试代码示例

```python
import pytest

from util.readFileUtils.get_yaml_data_analysis import get_case_list
from util.requestsUtils.requestControl import RequestControl
from util.assertion.assert_control import AssertControl


@pytest.mark.parametrize("case_id, case", get_case_list("login.yaml"))
def test_login(case_id, case):
    resp = RequestControl().send_request(
        method=case["method"],
        url=case["url"],
        headers=case.get("headers"),
        json=case.get("data"),
    )
    AssertControl(assert_data=case.get("assert"), response=resp).run()
```

## 7. 运行命令

```bash
pytest
```

```bash
pytest test_case/login/test_login.py -q -s
```

## 8. 后续可扩展方向

- 登录鉴权统一处理
- 关联接口数据提取
- 更丰富的断言方式
- allure 测试报告
- 日志记录
- 多环境切换

这个文件目前作为一个最简单的文档示例，后面可以继续扩展成正式的 README 或框架说明文档。
