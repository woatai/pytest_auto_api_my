"""
上下文管理器
主流程执行过程中的临时变量仓库
"""
class ContextManager:
    _data = {} # 定义一个空字典

    @classmethod
    def set(cls,key:str,value):
        cls._data[key] = value
    
    @classmethod
    def get(cls,key:str,default = None):
        return cls._data.get(key,default)

    # 清理全部数据
    @classmethod
    def clear(cls):
        cls._data.clear()

    @classmethod
    def all(cls):
        return cls._data

