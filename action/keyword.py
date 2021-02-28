from selenium import webdriver
import time
from conf.global_var import *
from util.find_element_util import *
from util.ini_parser import *


# 初始化浏览器
def init_browser(browser_name):
    if browser_name.lower() == "chrome":
        driver = webdriver.Chrome(CHROME_DRIVER)
    elif browser_name.lower() == "firefox":
        driver = webdriver.Firefox(FIREFOX_DRIVER)
    elif browser_name.lower() == "ie":
        driver = webdriver.Ie(IE_DRIVER)
    else:
        return "Error browser name!"
    return driver


# 访问指定url
def visit(driver, url):
    driver.get(url)


# 输入操作
def input(driver, locate_method, locate_exp, value):
    # 方式1：直接传定位方式和定位表达式
    if locate_method in ["id", "xpath", "classname", "name", "tagname", "linktext",
                             "partial link text", "css selector"]:
        find_element(driver, locate_method, locate_exp).send_keys(value)
    # 方式2：通过ini文件的key找到value，再分割定位方式和定位表达式
    else:
        parser = IniParser(ELEMENT_FILE_PATH)
        locate_method, locate_exp = tuple(parser.get_value(locate_method, locate_exp).split(">"))
        find_element(driver, locate_method, locate_exp).send_keys(value)


# 点击操作
def click(driver, locate_method, locate_exp):
    # 方式1：直接传定位方式和定位表达式
    if locate_method in ["id", "xpath", "classname", "name", "tagname", "linktext",
                             "partial link text", "css selector"]:
        find_element(driver, locate_method, locate_exp).click()
    # 方式2：通过ini文件的key找到value，再分割定位方式和定位表达式
    else:
        parser = IniParser(ELEMENT_FILE_PATH)
        locate_method, locate_exp = tuple(parser.get_value(locate_method, locate_exp).split(">"))
        find_element(driver, locate_method, locate_exp).click()


# 清空输入框操作
def clear(driver, locate_method, locate_exp):
    # 方式1：直接传定位方式和定位表达式
    if locate_method in ["id", "xpath", "classname", "name", "tagname", "linktext",
                             "partial link text", "css selector"]:
        find_element(driver, locate_method, locate_exp).clear()
    # 方式2：通过ini文件的key找到value，再分割定位方式和定位表达式
    else:
        parser = IniParser(ELEMENT_FILE_PATH)
        locate_method, locate_exp = tuple(parser.get_value(locate_method, locate_exp).split(">"))
        find_element(driver, locate_method, locate_exp).clear()


# 切换frame
def switch_frame(driver, locate_method, locate_exp):
    # 方式1：直接传定位方式和定位表达式
    if locate_method in ["id", "xpath", "classname", "name", "tagname", "linktext",
                             "partial link text", "css selector"]:
        driver.switch_to.frame(find_element(driver, locate_method, locate_exp))
    # 方式2：通过ini文件的key找到value，再分割定位方式和定位表达式
    else:
        parser = IniParser(ELEMENT_FILE_PATH)
        locate_method, locate_exp = tuple(parser.get_value(locate_method, locate_exp).split(">"))
        driver.switch_to.frame(find_element(driver, locate_method, locate_exp))


# 切换主frame
def switch_home_frame(driver):
    driver.switch_to.default_content()


# 断言
def assert_word(driver, keyword):
    assert keyword in driver.page_source


# 休眠
def sleep(driver, times):
    time.sleep(int(times))


# 关闭浏览器
def quit(driver):
    driver.quit()


if __name__ == "__main__":
    driver = init_browser("chrome")
    visit(driver, "http://mail.126.com")
    switch_frame(driver, "xpath", "//iframe[contains(@id,'x-URS-iframe')]")
    clear(driver, "xpath", "//input[@name='email']")
    input(driver, "xpath", "//input[@name='email']", "juno3550")
    input(driver, "xpath", "//input[@name='password']", "258978aa")
    click(driver, "id", "dologin")
    sleep(driver, 2)
    assert_word(driver, "退出")
    # 通过配置文件传参
    quit(driver)
    driver = init_browser("chrome")
    visit(driver, "http://mail.126.com")
    switch_frame(driver, "126mail_indexPage", "indexPage.frame")
    clear(driver, "126mail_indexPage", "indexPage.username")
    input(driver, "126mail_indexPage", "indexPage.username", "juno3550")
    input(driver, "126mail_indexPage", "indexPage.password", "258978aa")
    click(driver, "126mail_indexPage", "indexPage.loginbutton")
    sleep(2)
    assert_word(driver, "退出")
    quit(driver)

