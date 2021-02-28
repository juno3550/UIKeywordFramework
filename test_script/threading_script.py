import traceback
import queue
import threading
from test_script.case_script import *
from util.log_util import *


# 多线程任务函数：
def thread_task(q):
    """
    :param q: 队列（存储的是测试数据文件）
    :return: None
    """
    try:
        if not isinstance(q, queue.Queue):
            warning("多线程任务函数入参有误：需为队列对象!")
            return
        while q.qsize() > 0:
            test_data_file, main_case_sheet = q.get()
            main_script_execute(test_data_file, main_case_sheet)
    except:
        error("多线程任务函数执行异常!")
        traceback.print_exc()


# 多线程执行函数
def thread_main(thread_data, thread_num):
    """
    :param thread_data: 多线程任务函数所需要的测试数据集（二维数组）参数
    :param thread_num: 需要开启的线程数
    :return: None
    """
    try:
        if not isinstance(thread_data, list):
            warning("多线程任务函数入参有误：需为数组对象!")
            return
        for li in thread_data:
            if not isinstance(li, list):
                warning("多线程任务函数入参有误：需为二维数组对象!")
                return
        if not (isinstance(thread_num, int) and thread_num > 0):
            warning("多线程任务函数入参有误：需为正整数对象!")
            return
        q = queue.Queue()
        for data in thread_data:
            q.put(tuple(data))
        thread_list = []
        # 初始化多线程
        for i in range(thread_num):
            t = threading.Thread(target=thread_task, args=(q,))
            thread_list.append(t)
        # 启动多线程
        for t in thread_list:
            t.start()
        # 等待所有子线程结束
        for t in thread_list:
            t.join()
    except:
        error("多线程执行函数执行异常!")
        traceback.print_exc()


if __name__ == "__main__":
    thread_data = [[TEST_DATA_FILE_PATH_1, "测试用例"], [TEST_DATA_FILE_PATH_2, "测试用例"],
                   [TEST_DATA_FILE_PATH_3, "测试用例"]]
    # 多线程执行函数
    thread_main(thread_data, 3)