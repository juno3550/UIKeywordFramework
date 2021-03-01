from conf.global_var import *
from test_script import case_script
from test_script import threading_script


# 封装混合驱动用例的执行函数，测试步骤sheet与测试数据sheet由主测试用例sheet提供
case_script.main_script_execute(TEST_DATA_FILE_PATH_1, "测试用例")
# 多线程任务函数所需的数据集合
thread_data = [[TEST_DATA_FILE_PATH_1, "测试用例"], [TEST_DATA_FILE_PATH_2, "测试用例"]]
# 多线程执行函数
threading_script.thread_main(thread_data, 2)