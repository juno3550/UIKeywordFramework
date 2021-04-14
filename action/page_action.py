from selenium import webdriver
import time
import traceback
from util.datetime_util import *
from util.find_element_util import *
from util.ini_reader import *
from util.log_util import *


DRIVER = ""


# 初始化浏览器
def init_browser(browser_name):
    global DRIVER
    if browser_name.lower() == "chrome":
        DRIVER = webdriver.Chrome(CHROME_DRIVER)
    elif browser_name.lower() == "firefox":
        DRIVER = webdriver.Firefox(FIREFOX_DRIVER)
    elif browser_name.lower() == "ie":
        DRIVER = webdriver.Ie(IE_DRIVER)
    else:
        warning("浏览器【%s】不支持，已默认启动chrome" % browser_name)
        DRIVER = webdriver.Chrome(CHROME_DRIVER)


# 访问指定url
def visit(url):
    global DRIVER
    DRIVER.get(url)


# 输入操作
def input(locate_method, locate_exp, value):
    global DRIVER
    # 方式1：直接传定位方式和定位表达式
    if locate_method in ["id", "xpath", "classname", "name", "tagname", "linktext",
                             "partial link text", "css selector"]:
        find_element(DRIVER, locate_method, locate_exp).send_keys(value)
    # 方式2：通过ini文件的key找到value，再分割定位方式和定位表达式
    else:
        parser = IniParser(ELEMENT_FILE_PATH)
        locate_method, locate_exp = tuple(parser.get_value(locate_method, locate_exp).split(">"))
        find_element(DRIVER, locate_method, locate_exp).send_keys(value)


# 点击操作
def click(locate_method, locate_exp):
    global DRIVER
    # 方式1：直接传定位方式和定位表达式
    if locate_method in ["id", "xpath", "classname", "name", "tagname", "linktext",
                             "partial link text", "css selector"]:
        find_element(DRIVER, locate_method, locate_exp).click()
    # 方式2：通过ini文件的key找到value，再分割定位方式和定位表达式
    else:
        parser = IniParser(ELEMENT_FILE_PATH)
        locate_method, locate_exp = tuple(parser.get_value(locate_method, locate_exp).split(">"))
        find_element(DRIVER, locate_method, locate_exp).click()


# 清空输入框操作
def clear(locate_method, locate_exp):
    global DRIVER
    # 方式1：直接传定位方式和定位表达式
    if locate_method in ["id", "xpath", "classname", "name", "tagname", "linktext",
                             "partial link text", "css selector"]:
        find_element(DRIVER, locate_method, locate_exp).clear()
    # 方式2：通过ini文件的key找到value，再分割定位方式和定位表达式
    else:
        parser = IniParser(ELEMENT_FILE_PATH)
        locate_method, locate_exp = tuple(parser.get_value(locate_method, locate_exp).split(">"))
        find_element(DRIVER, locate_method, locate_exp).clear()


# 切换frame
def switch_frame(locate_method, locate_exp):
    global DRIVER
    # 方式1：直接传定位方式和定位表达式
    if locate_method in ["id", "xpath", "classname", "name", "tagname", "linktext",
                             "partial link text", "css selector"]:
        DRIVER.switch_to.frame(find_element(DRIVER, locate_method, locate_exp))
    # 方式2：通过ini文件的key找到value，再分割定位方式和定位表达式
    else:
        parser = IniParser(ELEMENT_FILE_PATH)
        locate_method, locate_exp = tuple(parser.get_value(locate_method, locate_exp).split(">"))
        DRIVER.switch_to.frame(find_element(DRIVER, locate_method, locate_exp))


# 切换主frame
def switch_home_frame():
    global DRIVER
    DRIVER.switch_to.default_content()


# 断言
def assert_word(keyword):
    global DRIVER
    assert keyword in DRIVER.page_source


# 休眠
def sleep(times):
    time.sleep(int(times))


# 关闭浏览器
def quit():
    global DRIVER
    DRIVER.quit()


# 截图函数
def take_screenshot():
    global DRIVER
    # 创建当前日期目录
    dir = os.path.join(SCREENSHOT_PATH, get_chinese_date())
    if not os.path.exists(dir):
        os.makedirs(dir)
    # 以当前时间为文件名
    file_name = get_chinese_time()
    file_path = os.path.join(dir, file_name+".png")
    try:
        DRIVER.get_screenshot_as_file(file_path)
        # 返回截图文件的绝对路径
        return file_path
    except:
        error("截图发生异常【{}】\n{}".format(file_path, traceback.format_exc()))
        return file_path


if __name__ == "__main__":
    init_browser("chrome")
    visit("http://mail.126.com")
    print(take_screenshot())

