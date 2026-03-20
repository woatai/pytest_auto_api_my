from util.readFileUtils.get_yaml_data_analysis import get_case_list

if __name__ =="__main__":
    data = get_case_list("order_main_flow.yaml")
    print(data)
