"""全局夹具配置文件 
所有测试共用的前置、后置入口
"""
import pytest

import common.config as config_module
import util.readFileUtils.placeholder as placeholder_module
import util.requestsUtils.requestControl as request_module
from util.context.context_manager import ContextManager
from util.case_runner import run_case


def pytest_addoption(parser):
    parser.addoption( # 给 pytest 增加一个'开关'或者 输入参数
        "--env",
        action="store", # 把命令行里传进来的值保存下来。
        default=None,
        help="运行环境，例如 dev / test / prod",
    )


@pytest.fixture(scope="session",autouse=True) 
def active_env(pytestconfig):
    """
    读取当前运行环境，并把 host 应用到项目里。
    """
    env_name = pytestconfig.getoption("--env") or config_module.current_env
    host = config_module._config["env"][env_name]["host"]
    
    # 临时修改某个变量、属性、环境变量，测试结束后还能恢复。
    mp = pytest.MonkeyPatch()

    # 当前项目里是 `from common.config import HOST` 的写法，
    # 所以切环境时，不能只改 common.config.HOST，
    # 还要把已经导入 HOST 的模块一起补丁掉。
    mp.setattr(config_module, "current_env", env_name, raising=False) # 修改某个对象上的属性
    mp.setattr(config_module, "HOST", host, raising=False)
    mp.setattr(request_module, "HOST", host, raising=False)
    mp.setattr(placeholder_module, "HOST", host, raising=False)

    yield {"name": env_name, "host": host} # 返回给这个fixture的测试
    mp.undo() # 恢复测试的环境

@pytest.fixture(scope= "class") # 自动执行不用参数配置、类清理
def flow_context():
    """流程前后清空上下文"""
    ContextManager.clear()
    yield
    ContextManager.clear()

@pytest.fixture(scope="function")
def case_context():
    """独立测试，前后清空上下文"""
    ContextManager.clear()
    yield
    ContextManager.clear()
# 登录初始化fixture
@pytest.fixture(scope="class")
def login_init(flow_context):
    """
    预留：如果某些流程一开始就需要已登录状态，
    可以把登录放进 fixture，而不是每个类都手写一遍。
    """
    resp = run_case("order_main_flow.yaml","login")

    return resp

