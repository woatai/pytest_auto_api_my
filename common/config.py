from util.readFileUtils.yamlControl import yamlControl

_config = yamlControl.read_yaml("common/config.yaml")

current_env = _config["current_env"]

HOST = _config["env"][current_env]["host"]
