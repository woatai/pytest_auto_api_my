from util.readFileUtils.get_yaml_data_analysis import get_case_list

if __name__ =="__main__":
    data = get_case_list("login.yaml")
    print(data)
