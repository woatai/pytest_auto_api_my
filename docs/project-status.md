# pytest-auto-api-my 项目状态

更新时间：2026-08-12

职责：记录当前代码、配置、测试、工作区和验证结果的事实，提供已知问题与下一步行动入口。本文件不保存教程、旧日期计划或大段待实现代码；历史变化通过 Git 提交记录追踪。

## 当前阶段

当前项目是基于 Python、`pytest`、`requests`、PyYAML、`jsonpath` 和 Allure Pytest 的轻量接口自动化框架，已经形成以下职责边界：

- 模块 YAML 描述单个接口的请求数据、断言和普通 JSONPath 提取。
- `run_case()` 统一执行一个 `yaml_name + case_id`。
- `test_case/test_order_main_flow.py` 显式编排下单顺序，并处理选择有库存规格等业务逻辑。
- `ContextManager` 在同一流程中传递 `token`、`product_id`、`unique` 和 `cartId`。

项目不再走“流程 YAML + Python 流程列表 + `run_flow_steps()`”路线。工作区已删除未接入运行时的 `data/order_main_flow.yaml`，同时删除 `ORDER_MAIN_FLOW` 和 `run_flow_steps()`；流程顺序只保留在 Python 测试中。

当前分支为 `master`，HEAD 为 `6f99d7a 添加 Jenkins 流水线`。工作区不是干净状态，包含本次流程重构，以及此前已有的 `run.py` 和 `docs/` 变更；当前运行事实应以工作区代码为准，而不是只看 HEAD。

环境与工具：

- Python：3.12.13
- pytest：9.1.1
- 默认环境：`test`
- 可选环境：`test`、`prod`

## 最近验证

2026-08-12 使用仓库 `.venv` 验证：

- `pytest --collect-only -q`：成功收集 6 条测试，其中 5 条本地框架测试、1 条远程下单主流程测试。
- `pytest test_case/test_framework_basics.py -q`：5 条全部通过。
- `pytest test_case/test_framework_basics.py -q --env=test`：5 条全部通过。
- `pytest test_case/test_framework_basics.py -q --env=prod`：4 条通过、1 条失败。请求层已切换到 prod，但测试模块在 fixture 执行前通过 `from common.config import HOST` 保存了 test 环境旧值，导致默认 Host 断言使用旧期望值。
- 使用本地 fake client 手工走通九步下单流程：`productValue` 为列表或字典时都能选择第一条 `stock > 0` 的规格，并完成 `product_id -> unique -> cartId` 传递。
- 使用本地 fake client 验证无库存分支：执行到商品详情后抛出 `没有可用库存，无法下单`，后续接口不再执行。
- `compileall` 和 `git diff --check` 通过。

本次没有执行真实 `test` 环境的下单主流程，也没有通过 `run.py` 重新生成 Allure HTML。真实流程包含订单确认请求，当前测试账号、远程服务、商品库存和下单结果均未重新确认。

## 当前主流程

真正生效的执行链路如下：

```text
pytest 收集 TestMainFlow.test_order_main_flow()
-> class 级 flow_context 在流程前清空 ContextManager
-> Python 测试按业务顺序创建 Allure step
-> 每个接口调用 run_case(yaml_name, case_id, client)
-> get_case_by_id() / get_case_list() 读取模块 YAML
-> case_common 与目标 case 浅合并
-> resolve_placeholders() 读取 ContextManager 变量
-> RequestControl.send_request() 组装 URL、请求头和 Bearer Token
-> AssertControl.run() 先执行状态码和 JSONPath 业务断言
-> ExtractControl.run() 执行普通 JSONPath 提取并写入 ContextManager
-> 商品详情返回后，Python 遍历 productValue
-> 选择第一条 stock > 0 的规格并写入 unique
-> 后续接口继续通过 ${{unique}} 和其他上下文变量执行
-> flow_context 在测试类结束后清空 ContextManager
```

断言失败、提取失败、无库存或其他未捕获异常都会立即中断当前测试，因此流程天然 fail-fast。

## 下单流程矩阵

| 顺序 | YAML 用例 | 请求依赖 | 当前行为 |
| ---: | --- | --- | --- |
| 1 | `login/login.yaml::login_success` | YAML 中的测试账号 | 断言 HTTP 状态、业务状态和消息；提取 `token` |
| 2 | `product/product.yaml::product_list` | 请求层自动注入 `token` | 断言商品列表；提取第一项 `product_id` |
| 3 | `product/product.yaml::product_detail` | `product_id` | YAML 断言商品详情；Python 从列表或字典形式的 `productValue` 中选择首个 `stock > 0` 的规格并保存 `unique` |
| 4 | `product/product.yaml::default_price` | `product_id`、`unique` | 断言 HTTP 状态和业务消息 |
| 5 | `user/user.yaml::user_center` | 请求层自动注入 `token` | 只断言 HTTP 200 |
| 6 | `cart/cart.yaml::buy_now` | `product_id`、`unique` | 只断言 HTTP 200；提取 `cartId` |
| 7 | `order/order.yaml::check_shipping` | `cartId` | 只断言 HTTP 200 |
| 8 | `user/address.yaml::get_default_address` | 请求层自动注入 `token` | 只断言 HTTP 200；没有提取地址 ID |
| 9 | `order/order.yaml::order_confirm` | `cartId`，地址 ID 固定为 `0` | 只断言 HTTP 200；没有业务断言或订单号提取 |

“请求执行到最后一步”不等于“订单业务结果已被充分验证”。当前默认地址没有进入确认参数，最后一步也没有验证业务状态或提取订单号。

## 当前设计边界

- 接口 YAML 只负责单接口配置，不负责完整业务流程编排。
- `extract` 只接受普通 JSONPath 字符串；不再支持 `conditional_find`、`jsonpath_first` 或自定义条件表达式。
- 直接响应字段通过 `ExtractControl` 提取；“选择哪个规格”等业务决策留在 Python 测试。
- `run_case()` 保持单用例执行边界，不加入流程回调、钩子或条件分支。
- 当前没有流程 YAML loader，也不计划把 `data/order_main_flow.yaml` 恢复为运行入口。

## 核心模块

- `test_case/test_order_main_flow.py`：显式编排九步下单流程，创建 Allure step，并在商品详情之后选择有库存规格。
- `util/case_runner.py`：`run_case()` 负责读取一个 YAML case、解析占位符、发送请求、断言、提取并返回标准响应。
- `util/readFileUtils/get_yaml_data_analysis.py`：从 `data/` 读取模块 YAML，排除 `case_common`，通过 `{**common, **case}` 做一层浅合并，再按 `case_id` 选择用例；没有 schema 或字段预检。
- `util/readFileUtils/placeholder.py`：递归处理字符串、列表和字典；支持 `${{host()}}` 和 `${{变量名}}`。替换结果进入字符串，不支持时间戳、UUID、随机值、Faker 或带参数函数。
- `util/requestsUtils/requestControl.py`：支持相对 URL 和完整 URL，默认超时 10 秒，设置 JSON Content-Type，并在上下文存在 token 时注入 `Bearer <token>`。请求异常返回标准字典，不直接抛出网络异常。
- `util/assertion/assert_control.py`：支持 `status_code` 以及 JSONPath `eq/==/equals`、`ne/!=`、`in`、`contains`、`exists`。失败信息包含请求和响应详情，目前没有敏感字段脱敏。
- `util/extract/extract_control.py`：只支持从响应体执行普通 JSONPath；单个结果保存标量，多个结果保存列表。
- `util/context/context_manager.py`：使用进程内类字典保存流程变量，提供 `set/get/clear/all`；没有并发隔离或多层作用域。
- `conftest.py`：提供 session 级 `active_env`、class 级 `api_client` 和 `flow_context`、function 级 `case_context`，以及尚未被收集测试使用的 `login_init`。
- `run.py`：调用 pytest 后使用 `allure generate --single-file` 生成报告，并通过 `subprocess.run(check=True)` 检查 Allure 命令；但目前没有把 pytest 的非零退出码返回给 shell，也不会因 pytest 失败而跳过报告生成。
- `Jenkinsfile`：在 `python-api` 节点创建 `.venv-ci`、安装依赖、执行 5 条离线框架测试并归档 `report/tmp/**`；暂未执行离线完整流程或真实环境 smoke 测试。

## 测试覆盖与入口

| 测试模块 | 数量 | 覆盖内容 |
| --- | ---: | --- |
| `test_case/test_framework_basics.py` | 5 | 默认 Host 与超时、上下文占位符、缺失变量、统一断言、普通 JSONPath 提取 |
| `test_case/test_order_main_flow.py` | 1 | 远程九步下单流程和库存规格业务选择 |

`test_case/login/test_login.py` 的方法名是 `login` 而不是 `test_*`，所以其中 3 组参数化登录 case 不会被 pytest 收集；它仍是手工读取、请求和断言的旧式示例。

常用命令：

```bash
.venv/bin/python -m pytest --collect-only -q
.venv/bin/python -m pytest test_case/test_framework_basics.py -q -s
.venv/bin/python -m pytest test_case/test_framework_basics.py -q -s --env=test
.venv/bin/python -m pytest test_case/test_framework_basics.py -q -s --env=prod
.venv/bin/python -m pytest test_case/test_order_main_flow.py -q -s
python run.py test_case/test_order_main_flow.py
```

最后两条命令会访问远程环境；执行前应确认账号、测试数据和下单副作用可接受。`pytest.ini` 默认把 Allure 结果写入 `report/tmp`。

## 已知问题

1. **离线完整流程验证尚未固化为 pytest 测试**
   本次用 fake client 手工验证了成功和无库存分支，但仓库中还没有可重复执行的离线流程测试，Jenkins 也只运行框架基础测试。

2. **下单结果验证不完整**
   后半段多个步骤只断言 HTTP 200；默认地址没有提取并传入确认接口，`order_confirm` 固定使用 `addressId: 0`，也没有验证业务状态、订单号或最终订单数据。

3. **多环境测试基线仍有 1 条失败**
   `active_env` 能修改请求层 Host，但框架测试在模块导入时缓存了旧 `HOST`，所以 `--env=prod` 的默认 Host 断言失败；未知环境名也会直接产生 `KeyError`。

4. **pytest 收集范围不完整**
   参数化登录模块存在 3 条 YAML case，但测试方法未使用 `test_*` 命名，也没有迁移到 `run_case()`。

5. **YAML 缺少执行前校验**
   `url`、`method`、`assert` 和 `extract` 等错误只有运行到对应代码时才暴露；`case_common` 只是浅合并，嵌套公共字段可能被整段覆盖。

6. **错误定位和敏感信息保护不足**
   网络异常被转换成 `status_code=None` 的响应；断言失败可能输出 password、token、Authorization、请求体和响应体，登录账号密码仍直接保存在 YAML 中。

7. **上下文依赖顺序且不支持并发隔离**
   `ContextManager` 是进程内全局类字典。fixture 能在流程前后清理，但没有依赖声明、快照、分层作用域或并发隔离。

8. **运行入口不能可靠返回测试失败**
   `run.py` 会记录 pytest 退出码，但不会 `sys.exit(exit_code)`；只要 Allure 生成成功，调用进程可能看不到 pytest 失败。

9. **框架能力仍是基础版**
   断言不支持大小比较、regex、长度和类型；提取不支持响应头、默认值或可选失败；占位符不支持 timestamp、UUID、随机值和 Faker。

## 下一步

1. 把本次 fake client 验证固化为 pytest：离线覆盖九步调用顺序、`productValue` 列表和字典、首个有库存规格、无库存立即失败，以及 `token -> product_id -> unique -> cartId` 传递；随后把它加入 Jenkins。
2. 补足下单业务校验：提取真实地址 ID 并传入 `order_confirm`，为 user、cart、shipping、address、confirm 增加业务断言，提取并校验订单号或最终结果。
3. 修复多环境测试：让 Host 断言读取 fixture 生效后的配置，并为非法 `--env` 提供明确错误，保证 test/prod 本地基线都通过。
4. 决定旧登录示例的去留：若保留，则改为 `test_*` 并复用 `run_case()`；若只作为历史示例，则移出 pytest 测试目录。
5. 增加最小 YAML case 校验，优先检查 `url`、`method`、`assert` 和 `extract`，并在发请求前报告 YAML 文件、case_id 和字段路径。
6. 改进诊断与安全：分类网络、占位符、断言和提取错误；给 Allure 添加脱敏后的请求/响应附件；把账号凭据移出版本库 YAML。
7. 修正 `run.py` 的 pytest 退出码传递，再扩展 Jenkins 的离线覆盖范围；真实环境流程继续作为显式 smoke/integration 测试运行。

相关资料：

- [项目说明](../Readme.md)
- [从零开始搭建接口自动化框架](./从零开始搭建接口自动化框架.md)
- [云起科技 CRM 接口测试面试准备](./云起科技CRM接口测试面试准备.md)
