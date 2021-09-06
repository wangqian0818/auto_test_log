'''
修订人：王谦
修订时间：2021/06/28
修订内容：新增方法：get_dut_version() 实现html的log中显示当前设备的组件版本号

修订人：李皖秋
修订时间：2021/07/22
修订内容：增加函数get_nginx_worker，获取nginx的子进程id
'''
#encoding='utf-8'
try:
	import os,sys,time
except Exception as err:
	print('导入CPython内置函数库失败!错误信息如下:')
	print(err)
	sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序

base_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))#获取当前项目文件夹
base_path=base_path.replace('\\','/')
sys.path.insert(0,base_path)#将当前目录添加到系统环境变量,方便下面导入版本配置等文件
try:
	import common.pcap as c_pacp
	import common.rabbitmq as c_rbm
	import common.ssh_wq as c_ssh
	import common.baseinfo as info
except Exception as err:
	print('导入基础函数库失败!请检查相关文件是否存在.\n文件位于: '+str(base_path)+'/common/ 目录下.\n分别为:pcap.py  rabbitmq.py  ssh.py\n错误信息如下:')
	print(err)
	sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
else:
	del sys.path[0]#及时删除导入的环境变量,避免重复导入造成的异常错误

pcap_sip = info.clientOpeIp
pcap_dip = info.serverOpeIp
qos_port = info.qos_port

ssh_gw=c_ssh.ssh(info.gwManageIp,info.gwUser,info.gwPwd)
ssh_c=c_ssh.ssh(info.clientIp,info.clientUser,info.clientPwd)
ssh_s=c_ssh.ssh(info.serverIp,info.serverUser,info.serverPwd)
ssh_vlanA = c_ssh.ssh(info.vlanAIp,info.vlanAUser,info.vlanAPwd)
ssh_vlanB = c_ssh.ssh(info.vlanBIp,info.vlanBUser,info.vlanBPwd)
rbm = c_rbm.rabbitmq(info.rbmIp,info.rbmWebUser,info.rbmWebPwd,base_path)
ssh_FrontDut = c_ssh.ssh(info.BG8010FrontIp,info.BG8010FrontUser,info.BG8010FrontPwd)
ssh_BackDut = c_ssh.ssh(info.BG8010BackIp,info.BG8010BackUser,info.BG8010BackPwd)
ssh_BG8010Client = c_ssh.ssh(info.BG8010ClientIp,info.BG8010ClientUser,info.BG8010ClientPwd)
ssh_BG8010Server = c_ssh.ssh(info.BG8010ServerIp,info.BG8010ServerUser,info.BG8010ServerPwd)
ssh_httpServer = c_ssh.ssh(info.http_server,info.http_server_user,info.http_server_pass)
# ssh_gw.connect()
# ssh_c.connect()
# ssh_s.connect()
print('base_path: '+str(base_path))
# rbm.connect()
# mac=['gw']
mac=['gw','c','s','FrontDut','BackDut','BG8010Client','BG8010Server','httpServer','vlanA','vlanB']

def cmd(cmd='',domain='',thread=0,timeout=None,list_flag=False):#cmd执行函数
	if not cmd:
		print('请输入cmd指令!')
		sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
	if domain not in mac:
		print('请输入有效的ssh主机代号!')
		sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
	ssh_name='ssh_'+str(domain)
	return globals()[ssh_name].cmd(cmd=cmd,thread=thread,timeout=timeout,list_flag=list_flag)#调用globals()把文本名变成object对象


def ssh_close(domain=1):#ssh连接关闭
	if domain not in mac:
		print('请输入有效的ssh主机代号!')
		sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
	ssh_name='ssh_'+str(domain)
	return globals()[ssh_name].close()#调用globals()把文本名变成object对象

def search(path,end,domain=1): #查找文件
	if domain not in mac:
		print('请输入有效的ssh主机代号!')
		sys.exit(0)
	ssh_name='ssh_'+str(domain)
	return globals()[ssh_name].search(path,end)

#从远程服务器读取文件到本地
def read(path='',fun='read',mode='r',text='',domain=1):
	if domain not in mac:
		print('请输入有效的ssh主机代号!')
		sys.exit(0)
	ssh_name='ssh_'+str(domain)
	return globals()[ssh_name].open(path,fun,mode,text)

def send(exc,method,domain,path):#向Rabbitmq发送信息
	if (not exc) or (not method) or (not domain):
		print('请输入有效的Rabbitmq发送信息参数!')
		sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
	rbm.send(exc,method,domain,path)

def rbm_close():#关闭Rabbitmq连接
	rbm.close()

def pkt_capture(iface,filter_,num,pkt_name): #开启抓包，只获取命令，不运行
	capture_pkt="python3 /opt/pkt/sniff.py %s %s %d /opt/pkt/%s"%(iface,filter_,num,pkt_name)
	# capture_pkt = os.system('python E:/卓讯/自动化测试/auto_test/pkt_server/sniff.py %s %s %d %s'%(iface, filter_, num, pkt_name))
	return capture_pkt

def pkt_send(iface,num,pkt_name): #发包命令
	# proto=pkt_name.split('__')
	# send_pkt="tcpreplay -i %s -l %d /opt/pkt/%s/%s"%(iface,num,proto,pkt_name)
	send_pkt = "tcpreplay -i %s -l %d /opt/pkt/%s" % (iface, num, pkt_name)
	return send_pkt

def pkt_read(pkt_name,pkt_id): #解析报文，返回标记字段，只获取命令，不运行
	read_pkt="python3 /opt/pkt/read.py /opt/pkt/%s %d"%(pkt_name,pkt_id)
	# read_pkt = os.system('python E:/卓讯/自动化测试/auto_test/pkt_server/read.py %s %d'%(pkt_name,pkt_id))
	return read_pkt

def mss_read(pkt_name,pkt_id): #解析报文，返回标记字段，只获取命令，不运行
	read_mss="python3 /opt/pkt/read_mss.py /opt/pkt/%s %d"%(pkt_name,pkt_id)
	# read_pkt = os.system('python E:/卓讯/自动化测试/auto_test/pkt_server/read.py %s %d'%(pkt_name,pkt_id))
	return read_mss

def vxlan_read(pkt_name,pkt_id): #解析报文，返回标记字段，只获取命令，不运行
	read_vxlan="python3 /opt/pkt/read_vxlan.py /opt/pkt/%s %d"%(pkt_name,pkt_id)
	# read_pkt = os.system('python E:/卓讯/自动化测试/auto_test/pkt_server/read.py %s %d'%(pkt_name,pkt_id))
	return read_vxlan

# def pid_kill(cap_pcap):
# 	# 判断抓包程序是否停止，如果进程还在则停止
# 	pid = cmd(f'ps -ef | grep python | grep {pcap_dip}', 's')
# 	print(pid)
# 	if (cap_pcap in pid):
# 		# 获取进程ID
# 		pid = pid.split()[1]
# 		print(pid)
# 		cmd("kill -9 %s" % pid, "s")

def pid_kill(content, process='python', non_content='bash', gw='s'):
    # 判断抓包程序是否停止，如果进程还在则停止
    cmd1 = f'ps -ef | grep {process} |grep -v grep'
    if process == 'python':
        cmd1 = f'ps -ef | grep {process} | grep {pcap_dip} | grep {content} |grep -v grep'
    while True:
        a = cmd(cmd1, gw)
        print('命令为：{}'.format(cmd1))
        print('命令获取的结果为：{}'.format(a))
        ls = a.split('\n')
        print('将结果分割后的列表为：{}'.format(ls))
        for pro in ls:
            # if 'bash' in pro:
            # 	return
            if content in pro and non_content not in pro:
                kpid = pro.split()[1]
                print('kpid: ', kpid)
                cmd("kill -9 %s" % kpid, gw)
            elif non_content in pro:
                continue
        break


def iperf_kill():
	# 判断抓包程序是否停止，如果进程还在则停止
	pid = cmd(f'ps -ef | grep iperf3 | grep {qos_port}', 's')
	print(pid)
	if ('iperf3' in pid):
		# 获取进程ID
		pid = pid.split()[1]
		print(pid)
		cmd("kill -9 %s" % pid, "s")

def cipso_category(a,b):
	value = ''
	for i in range(a, b):
		value = value + ' ' + str(i)
		if i == b - 1:
			return value

def pkt_scp(scp_name,scp_dip):  # 上传命令
	scp_pkt = f"sshpass -p {info.serverPwd} scp /opt/pkt/%s root@%s:/opt/pkt" %(scp_name,scp_dip)
	return scp_pkt

def pkt_wget(wget_name,wget_dip):
	wget_pkt="wget %s /opt/pkt/%s" % (wget_name,wget_dip)
	return wget_pkt

def qos_speed(file,s_txt,qbucket = 'p'):
	with open(file, 'w') as f:
		f.write(s_txt)

	result = []
	with open(file, 'r') as f:
		for line in f:
			result.append(list(line.strip('\n').split(',')))

	if qbucket == 'p':
		result1 = result[-24:-28]
		speed_list = []
		for i in result1:
			str_i = str(i)
			p_speed = str_i.split()[6]
			speed_list.append(p_speed)
			print(speed_list)
		return speed_list
	elif qbucket == 's':
		result1 = str(result[-30])
		s_speed = result1.split()[5]
		return s_speed

def wait_data(command,device,context,name='进程',number=300,timeout=0.1,flag='存在'):
	print('当前时间为{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
	a = cmd(command, device)
	print('第一次获取的结果为：{}'.format(a))
	tmp = 0
	time.sleep(1)
	if flag == '存在':
		while context not in a:
			if tmp < number:
				time.sleep(timeout)
				tmp += 1
				print('这是{}的第{}次等待'.format(name,tmp))
				a = cmd(command, device)
				print(a)
			else:
				print('{}检查结果失败'.format(name))
				return 0
	else:
		while context in a:
			if tmp < number:
				print(a)
				time.sleep(timeout)
				tmp += 1
				print('这是{}的第{}次等待'.format(name,tmp))
				a = cmd(command, device)
			else:
				print('{}检查结果失败'.format(name))
				return 0
	return a

def nginx_worker(command, device,context,non_context1='nginx: worker process is shutting down',non_context2='systemctl reload nginx_kernel',name='进程',number=300,timeout=0.1):
	print('当前时间为{}'.format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
	a = cmd(command, device)
	print('第一次获取的结果为：{}'.format(a))
	tmp = 0
	num = 0
	res = 0
	time.sleep(5)
	while num != 24:
		if tmp < number:
			num = 0	#每次循环，进程数需重新置为0
			time.sleep(timeout)
			tmp += 1
			print('这是{}的第{}次等待'.format(name, tmp))
			b = cmd(command, device)
			print(b)
			if non_context2 in b:
				continue
			else:
				c = b.split('\n')
				for i in c:
					if context in i and non_context1 not in i:
						num += 1
				print('当前有{}个{}启动成功'.format(num,name))
			if num == 24:
				print('{}个{}全部启动成功'.format(num,name))
				res = 1
				break
		else:
			print('{}启动失败'.format(name))
			break
	return res


def get_nginx_worker( str, split_str='root',context='worker',non_context='nginx: worker process is shutting down'):
	resultList = []
	list = str.split(split_str)
	for i in list:
		if context in i and non_context not in i:
			# print(i.strip(' ').strip('\n').split(' '))
			workerID = i.strip(' ').strip('\n').split(' ')[0]
			resultList.append(workerID)
	return resultList


def get_dut_version(case):
    print('获取设备版本号，并写入到文件dut_version.txt')
    result_file = base_path + r'/auto_test/dut_version.txt'
    # 清空文件： result_temp.txt
    with open(result_file, 'w') as file:
        file.seek(0)
        file.truncate()
    with open(result_file, 'a') as file:
        # 包含iso的用例均为隔离的用例
        if 'iso' in case:
            ssh_FrontDut.connect()
            ssh_BackDut.connect()
            # 隔离的前置机查询
            print('-------------------------- 隔离前置机版本号 -----------------------------')
            file.write('---------------------------- 隔离前置机版本号 ---------------------------\n')
            re = cmd('rpm -qa | grep agentjsac', 'FrontDut')
            assert re is not None, '查询 agentjsac 失败'
            file.write(re)
            re = cmd('rpm -qa | grep driver', 'FrontDut')
            assert re is not None, '查询 driver 失败'
            file.write(re)
            re = cmd('rpm -qa | grep libhostapi', 'FrontDut')
            assert re is not None, '查询 libhostapi 失败'
            file.write(re)
            re = cmd('rpm -qa | grep tsthostapi', 'FrontDut')
            assert re is not None, '查询 tsthostapi 失败'
            file.write(re)
            re = cmd('rpm -qa | grep nginx', 'FrontDut')
            assert re is not None, '查询 nginx 失败'
            file.write(re)
            re = cmd('/usr/local/proxyjsac/jsac_proxy -v', 'FrontDut')
            assert re is not None, '查询隔离版本失败'
            file.write(re)

            # 隔离的后置机查询
            print('-------------------------- 隔离后置机版本号 -------------------------------')
            file.write('--------------------------- 隔离后置机版本号 ----------------------------\n')
            re = cmd('rpm -qa | grep agentjsac', 'BackDut')
            assert re is not None, '查询 agentjsac 失败'
            file.write(re)
            re = cmd('rpm -qa | grep driver', 'BackDut')
            assert re is not None, '查询 driver 失败'
            file.write(re)
            re = cmd('rpm -qa | grep libhostapi', 'BackDut')
            assert re is not None, '查询 libhostapi 失败'
            file.write(re)
            re = cmd('rpm -qa | grep tsthostapi', 'BackDut')
            assert re is not None, '查询 tsthostapi 失败'
            file.write(re)
            re = cmd('rpm -qa | grep nginx', 'BackDut')
            assert re is not None, '查询 nginx 失败'
            file.write(re)
            re = cmd('/usr/local/proxyjsac/jsac_proxy -v', 'BackDut')
            assert re is not None, '查询隔离版本失败'
            file.write(re)
            ssh_FrontDut.close()
            ssh_BackDut.close()
        else:
            ssh_gw.connect()
            print('------------------------- 网关设备版本号 ------------------------------')
            file.write('-------------------------- 网关设备版本号 -----------------------------\n')
            re = cmd('rpm -qa | grep agentjsac', 'gw')
            assert re is not None, '查询 agentjsac 失败'
            file.write(re)
            re = cmd('rpm -qa | grep driver', 'gw')
            assert re is not None, '查询 driver 失败'
            file.write(re)
            re = cmd('rpm -qa | grep libhostapi', 'gw')
            assert re is not None, '查询 libhostapi 失败'
            file.write(re)
            re = cmd('rpm -qa | grep tsthostapi', 'gw')
            assert re is not None, '查询 tsthostapi 失败'
            file.write(re)
            re = cmd('rpm -qa | grep nginx', 'gw')
            assert re is not None, '查询 nginx 失败'
            file.write(re)
            ssh_gw.close()