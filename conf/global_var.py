import os


# 工程根路径
PROJECT_ROOT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 元素定位方法的ini配置文件路径
ELEMENT_FILE_PATH = os.path.join(PROJECT_ROOT_PATH, "conf", "ElementsRepository.ini")

# excel文件路径
TEST_DATA_FILE_PATH_1 = os.path.join(PROJECT_ROOT_PATH, "test_data", "混合驱动_测试用例_1.xlsx")
TEST_DATA_FILE_PATH_2 = os.path.join(PROJECT_ROOT_PATH, "test_data", "混合驱动_测试用例_2.xlsx")
TEST_DATA_FILE_PATH_3 = os.path.join(PROJECT_ROOT_PATH, "test_data", "混合驱动_测试用例_3.xlsx")

# 驱动路径
CHROME_DRIVER = "E:\\auto_test_driver\\chromedriver.exe"
IE_DRIVER = "E:\\auto_test_driver\\IEDriverServer.exe"
FIREFOX_DRIVER = "E:\\auto_test_driver\\geckodriver.exe"

# 截图路径
SCREENSHOT_PATH = os.path.join(PROJECT_ROOT_PATH, "screenshot_path")

# 日志配置文件路径
LOG_CONF_FILE_PATH = os.path.join(PROJECT_ROOT_PATH, "conf", "Logger.conf")

# 测试步骤sheet的列号
TEST_SCRIPT_KEYWORD_COL = 2
TEST_SCRIPT_LOCATE_METHOD_COL = 3
TEST_SCRIPT_LOCATE_EXP_COL = 4
TEST_SCRIPT_VALUE_COL = 5
TEST_SCRIPT_TEST_TIME_COL = 6
TEST_SCRIPT_TEST_RESULT_COL = 7
TEST_SCRIPT_EXCEPTION_INFO_COL = 8
TEST_SCRIPT_SCREENSHOT_PATH_COL = 9

# 主测试用例sheet列号
MAIN_CASE_CASE_NAME_COL = 3
MAIN_CASE_BROWSER_NAME_COL = 5
MAIN_CASE_SCRIPT_SHEET_COL = 6
MAIN_CASE_DATA_SHEET_COL = 7
MAIN_CASE_IS_EXECUTE_COL = 8
MAIN_CASE_TEST_TIME_COL = 9
MAIN_CASE_TEST_RESULT_COL = 10


if __name__ == "__main__":
    print(PROJECT_ROOT_PATH)