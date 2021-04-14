from business_process.main_process import *
from util.report_util import *


# 组装测试场景
# 冒烟测试
def smoke_test(report_name):
    excel, _ = suite_process(TEST_DATA_FILE_PATH, "登录（非数据驱动）")
    excel, _ = suite_process(excel, "关闭浏览器")
    # 生成测试报告并发送邮件
    create_excel_report_and_send_email(excel, ['itsjuno@163.com', '182230124@qq.com'], report_name, "请查收附件：UI自动化测试报告")


# 全量测试：执行主sheet的用例集
def suite_test(report_name):
    excel = main_suite_process(TEST_DATA_FILE_PATH, "测试用例集")
    create_excel_report_and_send_email(excel, ['itsjuno@163.com', '182230124@qq.com'], report_name, "请查收附件：UI自动化测试报告")


if __name__ == "__main__":
    # smoke_test("UI自动化测试报告_冒烟测试")
    suite_test("UI自动化测试报告_全量测试")

