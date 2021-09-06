# encoding='utf-8'


try:
    import os, sys, pytest, allure, time, re, time
except Exception as err:
    print('导入CPython内置函数库失败!错误信息如下:')
    print(err)
    sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序

base_path = os.path.dirname(os.path.abspath(__file__))  # 获取当前项目文件夹
base_path = base_path.replace('\\', '/')
sys.path.insert(0, base_path)  # 将当前目录添加到系统环境变量,方便下面导入版本配置等文件
print("---- base_path: ", base_path)
# try:
#     from case_01_wq import index
#     from case_01_wq import message
#     from common import fun
#     import common.ssh as c_ssh
# except Exception as err:
#     print(
#         '导入基础函数库失败!请检查相关文件是否存在.\n文件位于: ' + str(base_path) + '/common/ 目录下.\n分别为:pcap.py  rabbitmq.py  ssh.py\n错误信息如下:')
#     print(err)
#     sys.exit(0)  # 避免程序继续运行造成的异常崩溃,友好退出程序
# else:
#     del sys.path[0]  # 及时删除导入的环境变量,避免重复导入造成的异常错误
# # import index
# # del sys.path[0]
# # dir_dir_path=os.path.abspath(os.path.join(os.getcwd()))
# # sys.path.append(os.getcwd())
#
# from common import baseinfo
# from common.rabbitmq import *
#
# datatime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
#
# rbmDomain = baseinfo.rbmDomain
# rbmExc = baseinfo.rbmExc
# url = baseinfo.http_url
# http_content = baseinfo.http_content


class Test_case_01():

    # def setup_method(self,browser):
    #     print("\n------ setup_method")
    #
    # def teardown_method(self):
    #     print("\n------ teardown_method")

    def test_01(self):
        print("Test_case_01：用例内容")
        assert 4 + 1 == 0

    # @pytest.mark.skip(reseason="skip")
    def test_02(self):
        print("Test_case_02：用例内容")

    def test_03(self):
        print("Test_case_03：用例内容")
        assert 4 + 4 == 0

    def test_04(self):
        print("Test_case_04：用例内容")
        assert 4 + 4 == 8

    # 检查一定的输入和期望输出测试功能  如果调用的是函数传参，则需要加上参数indirect=True，查看文档14节
    # @pytest.mark.parametrize("test_input,expected",   # 入参和期望值
    #                          [("3+3", 6),
    #                           ("3+3", 2),
    #                           pytest.param("5*9", 54,marks=pytest.mark.xfail)]) # 预期是错的
    # def test_parameter(self, test_input, expected):
    #     assert eval(test_input) == expected
    #
    # # 多个参数化参数的所有组合，可以堆叠参数化装饰器
    # @pytest.mark.parametrize("x",[0,1])
    # @pytest.mark.parametrize("y",[5,6])
    # def test_para_group(self,x,y):
    #     print("测试数据组合：x->%s, y->%s" % (x, y))
    #
    # # 命令行传参,用例可以读到命令行赋予的参数值  --cmdopt
    # def test_answer(self,cmdopt):
    #     if cmdopt == "type1":
    #         print("first")
    #     elif cmdopt == "type2":
    #         print("second")
    #     assert 0
    #
    # # 标记关键字
    # @pytest.mark.webtest
    # def test_mark(self):
    #     print('test_mark')
    #
    # # 如果fixture失败，则标记失败 =================================
    # canshu = [{"user": "amdin", "psw": "123"}]
    # @pytest.mark.parametrize("login", canshu, indirect=True)
    # def test_04(self, login):
    #     '''用例1登录'''
    #     result = login
    #     print("用例1：%s" % result)
    #     assert result == True
    #
    # @pytest.mark.parametrize("login", canshu, indirect=True)
    # def test_05(self, login):
    #     result = login
    #     print("用例3,登录结果：%s" % result)
    #     if not result:
    #         pytest.xfail("登录不成功, 标记为xfail")
    #
    #     assert 1 == 1
    #
    # @pytest.mark.parametrize("login", canshu, indirect=True)
    # def test_测试中文(self, login):
    #     result = login
    #     print("用例3,登录结果：%s" % result)
    #     if not result:
    #         pytest.xfail("登录不成功, 标记为xfail")
    #
    #     assert 1 == 1
    # ==========================================================
