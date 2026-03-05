from util.readFileUtils.get_yaml_data_analysis import get_yaml_case_data
if __name__ =="__main__":
    data = get_yaml_case_data("login.yaml")
    print(data)