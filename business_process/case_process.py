import traceback
import re
from util.global_var import *
from util.log_util import *
from util.datetime_util import *
from util.excel_util import Excel
from action.page_action import *


# 执行一条测试用例（即一行测试数据）
def execute_case(excel_file_path, case_data, test_data_source=None):
    # 用例数据格式校验
    if not isinstance(case_data, (list, tuple)):
        error("测试用例数据格式有误！测试数据应为列表或元组类型！【%s】" % case_data)
        case_data[TEST_SCRIPT_EXCEPTION_INFO_COL] = "测试用例数据格式有误！应为列表或元组类型！【%s】" % case_data
        case_data[TEST_SCRIPT_TEST_RESULT_COL] = "Fail"
    # 该用例无需执行
    if case_data[TEST_SCRIPT_IS_EXECUTE_COL].lower() == "n":
        info("测试用例步骤【%s】无需执行" % case_data[TEST_SCRIPT_NAME_COL])
        return
    # excel对象初始化
    if isinstance(excel_file_path, Excel):
        excel = excel_file_path  # 如果传入的是excel对象，则直接使用
    else:
        excel = Excel(excel_file_path)  # 如果传入的是文件路径，则初始化excel对象
    # 获取各关键字
    operation_action = case_data[TEST_SCRIPT_ACTION_COL]  # 操作动作（即函数名）
    locate_method = case_data[TEST_SCRIPT_LOCATE_METHOD_COL]  # 定位方式
    locate_expression = case_data[TEST_SCRIPT_LOCATE_EXPRESSION_COL]  # 定位表达式
    operation_value = case_data[TEST_SCRIPT_VALUE_COL]  # 操作值
    # 由于数据驱动，需要进行参数化的值
    if test_data_source:
        if re.search(r"\$\{\w+\}", str(operation_value)):
            # 取出需要参数化的值
            key = re.search(r"\$\{(\w+)\}", str(operation_value)).group(1)
            operation_value = re.sub(r"\$\{\w+\}", str(test_data_source[key]), str(operation_value))
            # 将参数化后的值回写excel测试结果中，便于回溯
            case_data[TEST_SCRIPT_VALUE_COL] = operation_value
    # 拼接关键字函数
    if locate_method and locate_expression:
        if operation_value:
            func = "%s('%s', '%s', '%s')" % (operation_action, locate_method, locate_expression, operation_value)
        else:
            func = "%s('%s', '%s')" % (operation_action, locate_method, locate_expression)
    else:
        if operation_value:
            func = "%s('%s')" % (operation_action, operation_value)
        else:
            func = "%s()" % operation_action
    # 执行用例
    try:
        eval(func)
        info("测试用例步骤执行成功：【{}】 {}".format(case_data[TEST_SCRIPT_NAME_COL], func))
        case_data[TEST_SCRIPT_TEST_RESULT_COL] = "Pass"
    except:
        info("测试用例步骤执行失败：【{}】 {}".format(case_data[TEST_SCRIPT_NAME_COL], func))
        case_data[TEST_SCRIPT_TEST_RESULT_COL] = "Fail"
        error(traceback.format_exc())
        # 进行截图
        case_data[TEST_SCRIPT_SCREENSHOT_PATH_COL] = take_screenshot()
        # 异常信息记录
        case_data[TEST_SCRIPT_EXCEPTION_INFO_COL] = traceback.format_exc()
    # 测试时间记录
    case_data[TEST_SCRIPT_TEST_TIME_COL] = get_english_datetime()
    return case_data


if __name__ == "__main__":
    excel = Excel(TEST_DATA_FILE_PATH)
    excel.get_sheet("登录（调试用）")
    all_data = excel.get_all_row_data()
    for data in all_data[1:]:
        execute_case(excel, data)
