import traceback
import re
from action.keyword import *
from util.excel_util import Excel
from util.screenshot import take_screenshot
from util.datetime_util import *
from util.log_util import *


# 测试步骤sheet用例的执行函数
def execute_case(driver, test_data_file_path, test_script_sheet_name, test_data, head_flag=True):
    """
    :param driver: selenium的driver对象
    :param test_data_file_path: 测试数据excel文件名称 或 excel实例化对象
    :param test_script_sheet_name: 测试步骤的sheet名称
    :param test_data: 测试数据sheet中的指定行数据，格式如[{"登录用户名": "xxx", "登录密码": "xxx", ...}, {...}, ...]
    :param head_flag: 是否在测试结果sheet中写入标题行，默认只写入一次标题行
    :return: 指定行的用例/用例集的执行结果
    """
    case_suite_result = "成功"
    # 如果传入的是excel对象，则无需再次初始化；多次初始化会导致后续写入失败
    if isinstance(test_data_file_path, Excel):
        excel = test_data_file_path
    # 初始化excel工具类对象
    else:
        excel = Excel(test_data_file_path)
    excel.change_sheet(test_script_sheet_name)
    all_row_data = excel.get_all_row_data()
    excel.change_sheet("测试结果")
    # 在测试结果sheet中，标题行仅写入一次
    if head_flag:
        excel.write_row_data(all_row_data[0], "red")
    # 除标题行外，遍历所有行数据
    for row_data in all_row_data[1:]:
        # 若某行用例是其他sheet的用例集，则先递归执行完其他sheet的用例
        if "other_test_cases" in row_data[TEST_SCRIPT_KEYWORD_COL]:
            case_result = execute_case(driver, excel, row_data[TEST_SCRIPT_VALUE_COL], test_data, False)
        else:
            keyword = row_data[TEST_SCRIPT_KEYWORD_COL]
            locate_method = row_data[TEST_SCRIPT_LOCATE_METHOD_COL]
            locate_exp = row_data[TEST_SCRIPT_LOCATE_EXP_COL]
            value = row_data[TEST_SCRIPT_VALUE_COL]
            # 数据驱动，将${}格式的值替换为数据集（test_data）中的数据进行执行
            if re.search(r"\$\{(.*)\}", str(value)):
                key = re.search(r"\$\{(.*)\}", str(value)).group(1)
                # 如[{"登录用户名": "xxx", "登录密码": "xxx", ...}, {...}, ...]
                value = test_data[key]
                # 在测试结果sheet中，也要将${}格式的值替换为数据集（test_data）中的数据
                row_data[TEST_SCRIPT_VALUE_COL] = value
            # 存在4种关键字执行函数类型
            if locate_method and locate_exp:
                if value:
                    command = "{}(driver, '{}', '{}', '{}')".format(keyword, locate_method, locate_exp, value)
                else:
                    command = "{}(driver, '{}', '{}')".format(keyword, locate_method, locate_exp)
            else:
                if value:
                    command = "{}(driver, '{}')".format(keyword, value)
                else:
                    command = "{}(driver)".format(keyword)
            try:
                # 执行关键字函数用例
                eval(command)
                info("用例执行成功：{}".format(command))
                case_result = "成功"
            except:
                error("用例执行失败：{}".format(command))
                traceback.print_exc()
                # 写入本用例的执行结果
                case_result = "失败"
                # 写入本用例集的执行结果
                case_suite_result = "失败"
                # 进行截图
                screenshot_file_path = take_screenshot(driver)
                # 截图路径记录
                row_data[TEST_SCRIPT_SCREENSHOT_PATH_COL] = screenshot_file_path
                # 异常信息记录
                row_data[TEST_SCRIPT_EXCEPTION_INFO_COL] = traceback.format_exc()
        # 测试时间记录
        row_data[TEST_SCRIPT_TEST_TIME_COL] = get_english_datetime()
        # 测试结果记录
        row_data[TEST_SCRIPT_TEST_RESULT_COL] = case_result
        # 将测试结果写入excel
        excel.write_row_data(row_data)
        excel.save()
    # 返回测试集合的测试结果（只要有一条用例不通过，整个测试集合均不通过）
    return case_suite_result


# 获取测试数据的执行函数
# 每行数据作为一个字典，存储在一个列表中。如[{"登录用户名": "xxx", "登录密码": "xxx", ...}, {...}, ...]
def get_dict_test_data(test_data_file_path, test_data_sheet_name):
    """
    :param test_data_file_path: 测试数据excel文件名称 或 excel实例化对象
    :param test_data_sheet_name: 测试数据的sheet名称
    :return: 测试数据sheet中的所有数据行，格式为{标题: 值}
    """
    # 如果传入的是excel对象，则无需再次初始化
    if isinstance(test_data_file_path, Excel):
        excel = test_data_file_path
    else:
        excel = Excel(test_data_file_path)
    excel.change_sheet(test_data_sheet_name)
    result = []
    all_row_data = excel.get_all_row_data()
    keys = all_row_data[0]
    for row_data in all_row_data[1:]:
        dict = {}
        for i in range(len(keys)):
            dict[keys[i]] = row_data[i]
        result.append(dict)
    return result


# 混合驱动用例的执行函数
# 测试步骤sheet与测试数据sheet分离（封装基础用例执行函数与获取测试数据执行函数）
def mix_case_execute(browser_name, test_data_file_path, test_script_sheet_name,
                     test_data_sheet_name=None, head_flag=True):
    """
    :param browser_name: 需要初始化的浏览器名称
    :param test_data_file_path: 测试数据excel文件名称 或 excel实例化对象
    :param test_script_sheet_name: 测试步骤的sheet名称
    :param test_data_sheet_name: 测试数据的sheet名称
    :param head_flag: 是否在测试结果sheet中写入标题行，默认只写入一次标题行
    :return: 指定行的用例/用例集的执行结果
    """
    case_result = "成功"
    if test_data_sheet_name:
        test_data = get_dict_test_data(test_data_file_path, test_data_sheet_name)
        for data in test_data:
            info("测试用例数据：{}".format(data))
            driver = init_browser(browser_name)
            result = execute_case(driver, test_data_file_path, test_script_sheet_name, data, head_flag)
            if result == "失败":
                case_result = "失败"
    else:
        driver = init_browser(browser_name)
        result = execute_case(driver, test_data_file_path, test_script_sheet_name, None, head_flag)
        if result == "失败":
            case_result = "失败"
    return case_result


# 封装混合驱动用例的执行函数
# 测试步骤sheet与测试数据sheet由主测试用例sheet提供
def main_script_execute(test_data_file_path, main_case_sheet_name):
    """
    :param test_data_file_path: 测试数据excel文件名称
    :param main_case_sheet_name: 测试用例的主sheet名称
    :return: None
    """
    excel = Excel(test_data_file_path)
    excel.change_sheet(main_case_sheet_name)
    all_row_data = excel.get_all_row_data()
    for row_data in all_row_data[1:]:
        if row_data[MAIN_CASE_IS_EXECUTE_COL].lower() == "y":
            case_name = row_data[MAIN_CASE_CASE_NAME_COL]
            info("开始执行测试用例集【{}】".format(case_name))
            if row_data[MAIN_CASE_DATA_SHEET_COL]:
                test_result = mix_case_execute(row_data[MAIN_CASE_BROWSER_NAME_COL], excel,
                                               row_data[MAIN_CASE_SCRIPT_SHEET_COL], row_data[MAIN_CASE_DATA_SHEET_COL])
            else:
                test_result = mix_case_execute(row_data[MAIN_CASE_BROWSER_NAME_COL], excel,
                                               row_data[MAIN_CASE_SCRIPT_SHEET_COL], row_data[MAIN_CASE_DATA_SHEET_COL])
        else:
            continue
        excel.change_sheet("测试结果")
        excel.write_row_data(all_row_data[0], "red")
        row_data[MAIN_CASE_TEST_TIME_COL] = get_english_datetime()
        row_data[MAIN_CASE_TEST_RESULT_COL] = test_result
        excel.write_row_data(row_data)
        excel.save()


if __name__ == "__main__":
    # 基础用例的执行函数
    # execute_case(driver, TEST_DATA_FILE_PATH_1, "添加联系人1")
    # 获取测试数据的执行函数，如[{"登录用户名": "xxx", "登录密码": "xxx", ...}, {...}, ...]
    # print(get_dict_test_data(TEST_DATA_FILE_PATH_1, "联系人数据"))
    # 混合驱动用例的执行函数，测试步骤sheet与测试数据sheet分离（封装基础用例执行函数与获取测试数据执行函数）
    # mix_case_execute("chrome", TEST_DATA_FILE_PATH_1, "添加联系人", "联系人数据")
    # 封装混合驱动用例的执行函数，测试步骤sheet与测试数据sheet由主测试用例sheet提供
    main_script_execute(TEST_DATA_FILE_PATH_1, "测试用例")