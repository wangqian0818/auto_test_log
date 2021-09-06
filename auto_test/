#encoding='utf-8'
try:
	import os,sys,pytest,allure,time
except Exception as err:
	print('导入CPython内置函数库失败!错误信息如下:')
	print(err)
	sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序

base_path=os.path.dirname(os.path.abspath(__file__))#获取当前项目文件夹
base_path=base_path.replace('\\','/')
sys.path.insert(0,base_path)#将当前目录添加到系统环境变量,方便下面导入版本配置等文件
import index
del sys.path[0]
#dir_dir_path=os.path.abspath(os.path.join(os.getcwd()))
sys.path.append(os.getcwd())
from common import fun
from common import clr_env
#del sys.path[0]


class Test_acl():
	
	def setup(self):
		#获取参数
		self.clr_env=clr_env.clear_env
		self.pre_env=index.pre_env
		self.case_step=index.case_step
		self.pkt_cfg=index.pkt_cfg

	@allure.feature('测试1')
	def test_a1(self):
		#清空环境

		for i in self.clr_env:
			print(i)
			dd=fun.cmd(i,'gw_c')
			print(dd)

		#设置初始环境
		cap_iface,cap_filter,cap_num,cap_pcap=self.pre_env["capture"][0],self.pre_env["capture"][1],self.pre_env["capture"][2],self.pre_env["capture"][3]
		pre_cfg=fun.pkt_capture(cap_iface,cap_filter,cap_num,cap_pcap)
		fun.cmd(pre_cfg,'gw_c',thread=1)
		print('step wait')
		time.sleep(3)

		#下发配置并检查结果
		for key in self.case_step:
			fun.cmd(self.case_step[key][0],'gw_c')
			re=fun.cmd(self.case_step[key][1],'gw_c')
			assert self.case_step[key][2] in re
		
		#发送报文
		c_iface,c_num,c_pcap=self.pkt_cfg["send"][0],self.pkt_cfg["send"][1],self.pkt_cfg["send"][2]
		send_cmd=fun.pkt_send(c_iface,c_num,c_pcap)
		fun.cmd(send_cmd,'gw_s')
	
		#检查报文是否存在
		pcap_file=fun.search('/opt/pkt','pcap','gw_c')
		assert cap_pcap in pcap_file
		
		#读包
		read_name,read_id=self.pkt_cfg["read"][0],self.pkt_cfg["read"][1]
		read_cmd=fun.pkt_read(read_name,read_id)
		read_re=fun.cmd(read_cmd,'gw_c')
		print(read_re)

		#获取期望结果
		exp=self.pkt_cfg["expect"][0]	
		assert exp in read_re
	
	@pytest.mark.skip(reseason="skip")
	def test_rabbitmq(self):
		#清空环境
		for i in clr_env.clear_env:
			fun.cmd(i,'gw_s')
		
		#下发配置
		fun.send('ManageExchange','AddAclPolicy','hf.f1203.g01.cs_12.wg5')

		#检查配置下发是否成功
		re=fun.cmd(command.result_check_gwc[0],'gw_s')
		#assert command.case_result_gwc[0] in re

		#开启接收端抓包
		fun.cmd(command.pre_env[0],'gw_c',thread=1)
		time.sleep(3)
		
		#客户端发送报文
		fun.cmd(command.case_step_c[0],'gw_s')
		
		#解析接收端抓包
		re=fun.cmd(command.result_check_c[0],'gw_c')
		assert command.case_result_c[0] in re
		
	def teardown(self):
		#回收环境
		for i in clr_env.clear_env:
			fun.cmd(i,'gw_c')
		for i in fun.mac:
			fun.ssh_close(i)

