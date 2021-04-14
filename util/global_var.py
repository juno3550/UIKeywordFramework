import os


# 工程根路径
PROJECT_ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 元素定位方法的ini配置文件路径
ELEMENT_FILE_PATH = os.path.join(PROJECT_ROOT_PATH, "conf", "elements_repository.ini")

# excel文件路径
TEST_DATA_FILE_PATH = os.path.join(PROJECT_ROOT_PATH, "test_data", "test_case.xlsx")

# 驱动路径
CHROME_DRIVER = "E:\\auto_test_driver\\chromedriver.exe"
IE_DRIVER = "E:\\auto_test_driver\\IEDriverServer.exe"
FIREFOX_DRIVER = "E:\\auto_test_driver\\geckodriver.exe"

# 截图路径
SCREENSHOT_PATH = os.path.join(PROJECT_ROOT_PATH, "exception_pic")

# 日志配置文件路径
LOG_CONF_FILE_PATH = os.path.join(PROJECT_ROOT_PATH, "conf", "logger.conf")

# 测试报告存放路径
TEST_REPORT_FILE_DIR = os.path.join(PROJECT_ROOT_PATH, "test_report")

# 对应excel测试数据文件中具体模块sheet中的列号
TEST_SCRIPT_NAME_COL = 1
TEST_SCRIPT_ACTION_COL = 2
TEST_SCRIPT_LOCATE_METHOD_COL = 3
TEST_SCRIPT_LOCATE_EXPRESSION_COL = 4
TEST_SCRIPT_VALUE_COL = 5
TEST_SCRIPT_IS_EXECUTE_COL = 6
TEST_SCRIPT_TEST_TIME_COL = 7
TEST_SCRIPT_TEST_RESULT_COL = 8
TEST_SCRIPT_EXCEPTION_INFO_COL = 9
TEST_SCRIPT_SCREENSHOT_PATH_COL = 10

# 对应excel测试数据文件中“测试用例集”sheet列号
MAIN_CASE_CASE_NAME_COL = 3
MAIN_CASE_BROWSER_NAME_COL = 5
MAIN_CASE_SCRIPT_SHEET_COL = 6
MAIN_CASE_DATA_SOURCE_SHEET_COL = 7
MAIN_CASE_IS_EXECUTE_COL = 8
MAIN_CASE_TEST_TIME_COL = 9
MAIN_CASE_TEST_RESULT_COL = 10

# 测试结果统计
TOTAL_CASE = 0
PASS_CASE = 0
FAIL_CASE = 0


if __name__ == "__main__":
    print(PROJECT_ROOT_PATH)