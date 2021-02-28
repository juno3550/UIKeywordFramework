import traceback
import os
from util.datetime_util import *
from conf.global_var import *


# 截图函数
def take_screenshot(driver):
    # 创建当前日期目录
    dir = os.path.join(SCREENSHOT_PATH, get_chinese_date())
    if not os.path.exists(dir):
        os.makedirs(dir)
    # 以当前时间为文件名
    file_name = get_chinese_time()
    file_path = os.path.join(dir, file_name+".png")
    try:
        driver.get_screenshot_as_file(file_path)
        # 返回截图文件的绝对路径
        return file_path
    except:
        print("截图发生异常【{}】".format(file_path))
        traceback.print_exc()
        return file_path