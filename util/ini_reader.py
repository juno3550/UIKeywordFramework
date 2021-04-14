import configparser


class IniParser:

    # 初始化打开指定ini文件并指定编码
    def __init__(self, file_path):
        self.cf = configparser.ConfigParser()
        self.cf.read(file_path, encoding="utf-8")

    # 获取所有分组名称
    def get_sections(self):
        return self.cf.sections()

    # 获取指定分组的所有键
    def get_options(self, section):
        return self.cf.options(section)

    # 获取指定分组的键值对
    def get_items(self, section):
        return self.cf.items(section)

    # 获取指定分组的指定键的值
    def get_value(self, section, key):
        return self.cf.get(section, key)


if __name__ == "__main__":
    from util.global_var import *
    parser = IniParser(ELEMENT_FILE_PATH)
    print(parser.get_sections())
    print(parser.get_options("126mail_indexPage"))
    print(parser.get_value("126mail_indexPage", 'indexpage.frame'))