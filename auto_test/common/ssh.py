#encoding='utf-8'
try:
	import os,sys,paramiko,datetime
except Exception as err:
	print('导入os,sys,paramiko三个库失败!应当是未安装paramiko库.\n可以调用help(ssh)查看帮助文档,进行安装.\n错误内容如下:')
	print(err)
	sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序

class ssh():
	'''
	程序默认环境为CentOS7.5；支持Python3.6～3.7
	ssh需要paramiko第三方库支持,没有相关配置执行如下命令即可:
	sudo yum install python-devel
	sudo pip3 install pycrypto
	sudo pip3 install paramiko
	'''
	def __init__(self,host='',name='',passwd='',port=''):
		'''初始化ssh类:host为ssh服务器地址；port为服务器端口；name为登陆名；passwd为登陆密码
		类的实例化方法为:实例化类名.ssh('远程ssh服务器地址','ssh登陆帐号:可以留空','ssh登陆密码:可以留空','ssh端口号:可以留空')
		'''
		if (not host) or (not name) or (not passwd):
			print('ssh服务器地址,帐号和密码都不能为空!')
			sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
		else:
			'''
			如果python的执行目录不是当前目录,递归查找的时候,容易出现异常错误,避免出现异常,写死查找路径
			'''
			base_path=os.path.dirname(os.path.abspath(__file__))#获取当前项目文件夹
			base_path=base_path.replace('\\','/')
			sys.path.insert(0,base_path)#将当前目录添加到系统环境变量,方便下面导入版本配置等文件

			try:#导入版本配置等文件
				import baseinfo as info
			except Exception as err:
				print('版本配置文件导入失败!请检查: '+base_path+'/common/baseinfo.py 文件是否存在.\n错误信息如下:')
				print(err)
				sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			else:
				del sys.path[0]#及时删除导入的环境变量,避免重复导入造成的异常错误
				try:
					self.__version=info.version#获取版本号
				except Exception as err:
					print('版本号获取失败!请检查是否设置了版本号.错误信息如下:')
					print(err)
					sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			base_path=os.path.dirname(base_path)#获取当前项目的上级文件夹
			self.__logs_path=base_path
			#验证并创建log保存目录
			if not os.path.exists(base_path+'/Logs/'+str(self.__version)):#如果保存当前版本的logs目录不存在,就创建
				try:
					os.makedirs(base_path+'/Logs/'+str(self.__version))
				except Exception as err:
					print('保存当前版本的Logs目录创建失败!请检查文件夹是否有操作权限.\n错误信息如下:')
					print(err)
					sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			self.__host=str(host)
			self.__name=str(name)
			self.__passwd=str(passwd)
			if port:
				self.__port=int(port)
			else:
				self.__port=22
			#创建ssh_client对象
			try:
				self.__ssh = paramiko.SSHClient()
			except Exception as err:
				print('调用paramiko.SSHClient()创建ssh连接对象失败!错误内容如下:')
				print(err)
				sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			#将信任的主机添加到host_allow
			try:
				self.__ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
			except Exception as err:
				print('将信任的主机: '+str(self.__host)+'添加到host_allow失败!错误内容如下:')
				print(err)
				sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			else:
				#ssh服务器连接状态
				self.__state=0
				print('ssh初始化: '+str(self.__host)+'完成!')

	def connect(self,timeout=None):
		'''
		连接ssh服务器
		调用方式为:实例化类名.connect()
		'''
		print("ssh 连接开始")
		if self.__state:
			print('ssh服务器: '+str(self.__host)+'已连接,如果想重建新的连接,请执行:实例化类名.close()关闭连接后,重新执行本方法.')
			sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
		if timeout:#确认时间限制,避免错误输入
			if not isinstance(timeout,int):
				print('ssh连接的时间限制应为整数!')
				sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			else:
				if timeout<1:
					timeout=None
		else:
			'''连接ssh服务器'''
			try:
				self.__ssh.connect(self.__host,self.__port,self.__name,self.__passwd,timeout=timeout)
			except Exception as err:
				print('ssh服务器: '+str(self.__host)+' 连接失败!错误信息如下:')
				print(err)
				sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			else:
				self.__state=1
				print('ssh服务器: '+str(self.__host)+'连接成功')
	
	def close(self):
		'''
		关闭ssh服务器连接
		调用方式为:实例化类名.close()
		'''
		if self.__state:
			try:
				self.__ssh.close()
			except Exception as err:
				print('连接向ssh服务器'+str(self.__host)+'的连接关闭失败,错误内容如下:')
				print(err)
				sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			else:
				self.__state=0
				print('连接向ssh服务器'+str(self.__host)+'的连接已关闭')
		else:
			print('ssh服务器: '+str(self.__host)+'在此之前未成功连接!请检查在此之前是否成功调用了ssh连接函数.')
			sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序

	def cmd(self,cmd='',thread=0,timeout=None):
		'''
		执行命令的方法:操作本方法前需要连接远程服务器
		调用方式为:实例化类名.cmd('指令')
		cmd='':以str的形式输入的指令
		timeout=None:cmd指令的时间限制,单位为秒,默认不限制时间
		'''
		if not self.__state:
			print('ssh服务器: '+str(self.__host)+'未连接或连接失败,请执行:实例化类名.connect()连接ssh服务器后再执行当前方法')
			sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
		else:
			if not cmd:
				print('指令不能为空,请输入指令!')
				sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			try:
				self.timeout=None
				if timeout and isinstance(timeout,int):#判断是否输入了时间限制
					self.timeout=int(timeout)
				if thread==1:
					stdout=self.__ssh.get_transport().open_session().exec_command(cmd)
				else:
					try:
						stdin,stdout,stderr=self.__ssh.exec_command(command=cmd,timeout=10)
					except Exception as err:
						print('ssh 连接错误！'.format(err))
						return None
				'''
				stdout保存输出结果;stderr保存错误信息.报错的结果是内存地址,需调用read()进行读取,读取的结果为二进制文本,需要通过decode('utf-8')转换为utf-8格式文本
				'''
			except Exception as err:
				print(str(cmd)+' 指令发送失败!错误内容如下!')
				print(err)
				sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			else:
				with open(self.__logs_path+'/Logs/'+str(self.__version)+'/ssh.logs','a',encoding='utf-8') as f:
					msg=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' '+'Domain: '+str(self.__host)+' Send: '+str(cmd)+'\n'
					f.write(msg)
				if thread!=1:
					stderr=stderr.read().decode('utf-8')
					if not stderr:#返回的错误内容为空,就输出结果
						print(str(cmd)+' 指令发送成功!')
						if stdout:
							stdout=stdout.read().decode('utf-8')
							with open(self.__logs_path+'/Logs/'+str(self.__version)+'/ssh.logs','a',encoding='utf-8') as f:
								msg=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")+' '+'Domain: '+str(self.__host)+' Receive: '+stdout+'\n'
								f.write(msg)
							return stdout
						else:
							return None
					else:
						print(str(cmd)+' 指令发送成功!但操作失败!\n如果提示命令不存在,请以超级管理员root登陆ssh服务器:'+str(self.__host)+'\n错误内容如下!')
						print(stderr)
						sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
				else:
					return None
	def sftp(self,local_path='',ssh_path='',method='get'):
		'''
		上传和下载文件:操作本方法前!!!不需要!!!连接远程服务器
		调用方式为:实例化类名.sftp('本地路径','远程路径','获取方式')
		local_path为本地路径地址;ssh_path为远程路径地址
		method为操作方式,get为从远程获取文件;put为从本地上传到远程服务器
		'''
		try:		
			transport=paramiko.Transport((self.__host,int(self.__port)))
		except Exception as err:
			print('sftp文件传输通道初始化失败!请检查ssh服务器地址和端口号是否正确.\n错误内容如下:')
			print(err)
			sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
		try:
			transport.connect(username=self.__name,password=self.__passwd)
		except Exception as err:
			print('sftp文件传输通道连接失败!请检查ssh服务器登陆名和密码是否正确.\n错误内容如下:')
			print(err)
			sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
		try:
			sftp=paramiko.SFTPClient.from_transport(transport)
		except Exception as err:
			print('sftp文件传输通道创建失败!请检查网络和服务器状态.\n服务器地址和帐号都没问题.\n错误内容如下:')
			print(err)
			sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
		if (not local_path) or (not ssh_path):
			print('本地路径和远程路径都不能为空!')
			sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
		if method=='get':
			try:
				sftp.get(ssh_path,local_path)
			except Exception as err:
				print('错误!!!将远程: '+str(ssh_path)+'文件下载到本地: '+str(local_path)+' 失败!错误内容如下:')
				print(err)
				sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			else:
				print('成功!!!将远程: '+str(ssh_path)+'文件下载到本地: '+str(local_path)+' 完成!')
				sftp.close()#及时关闭sftp连接,下次需要重新调用当前方法就可创建新的连接
		elif method=='put':
			try:
				sftp.put(local_path,ssh_path)
			except Exception as err:
				print('错误!!!将本地: '+str(local_path)+'文件上传到ssh服务器: '+str(ssh_path)+' 失败!错误内容如下:')
				print(err)
				sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			else:
				print('成功!!!将本地: '+str(local_path)+'文件上传到ssh服务器: '+str(ssh_path)+' 完成!')
				sftp.close()#及时关闭sftp连接,下次需要重新调用当前方法就可创建新的连接
		else:
			print('sftp操作文件方式只有get(下载文件)和put(上传文件)两种,其它操作无效!\n默认操作方式为get,下载文件.请检查sftp方法的参数是否有误.')
			sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序

	def open(self,file_path='',fun='read',mode='r',text=''):
		'''
		读写远程文件:操作本方法前需连接远程服务器
		调用方式为:实例化类名.open('文件路径','操作模式','操作方式')
		file_path为远程文件路径;
		
		fun为文件操作方式,默认为'read',可选参数及意义如下:
		方法	描述
		read	从文件中读取所有内容
		write	将内容写入文件

		mode为操作模式,默认为'r',可选参数及意义如下:
		模式	描述
		t	文本模式 (默认)。
		x	写模式，新建一个文件，如果该文件已存在则会报错。
		b	二进制模式。
		+	打开一个文件进行更新(可读可写)。
		r	以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。
		rb	以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。一般用于非文本文件如图片等。
		r+	打开一个文件用于读写。文件指针将会放在文件的开头。
		rb+	以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。一般用于非文本文件如图片等。
		w	打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
		wb	以二进制格式打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。一般用于非文本文件如图片等。
		w+	打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。
		wb+	以二进制格式打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。一般用于非文本文件如图片等。
		a	打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
		ab	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。
		a+	打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。
		ab+	以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。
		
		text为写模式下,要写入的内容
		'''
		if not self.__state:
			print('ssh服务器未连接或连接失败,请执行:实例化类名.connect()连接ssh服务器后再执行当前方法')
			sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
		else:
			if not file_path:
				print('请输入要操作的远程文件路径!')
				sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			try:			
				sftp_open=self.__ssh.open_sftp()
			except Exception as err:
				print('sftp操作文件通道创建失败!错误内容如下:')
				print(err)
				sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			else:
				try:
					fun_file=sftp_open.open(file_path,mode)
				except Exception as err:
					print('文件 '+str(self.__host)+':'+str(file_path)+' 连接失败!错误内容如下:')
					print(err)
					sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
				else:
					if fun=='read':
						try:
							file_text=fun_file.read()#如果执行的是读文件操作,就返回文件读取结果
						except Exception as err:
							print('文件 '+str(self.__host)+':'+str(file_path)+' 读取失败!错误内容如下:')
							print(err)
							sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
						else:
							print('文件 '+str(self.__host)+':'+str(file_path)+' 读取成功!')
							fun_file.close()#执行完毕及时关闭文件连接
							return file_text
					elif fun=='write':
						if not text:
							print('当前写入内容为空!!!')
						try:
							fun_file.write(text)
						except Exception as err:
							print('文件 '+str(self.__host)+':'+str(file_path)+' 写入失败!错误内容如下:')
							print(err)
							sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
						else:
							print('向文件: '+str(self.__host)+':'+str(file_path)+' 中写入: '+str(text)+' 成功')
							fun_file.close()#执行完毕及时关闭文件连接
							return 'ok'#写成功返回特定字符串,为了和读操作进行匹配,避免无返回值的空值操作
					else:
						print('当前仅支持read和write操作!!!请检查操作方法是否有误.')
						sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序

	def search(self,path='',end=''):
		'''
		搜索(查找)文件:操作本方法前需要连接远程服务器
		调用方式为:实例化类名.search('远程路径','文件后缀')
		path为要搜索的ssh服务器路径,默认搜索主目录下的所有文件和文件夹,并以列表的形式返回
		end为想要返回的文件后缀名,可以留空,意味着返回所有的文件类型
		'''
		if not self.__state:
			print('ssh服务器未连接或连接失败,请执行:实例化类名.connect()连接ssh服务器后再执行当前方法')
			sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
		else:
			try:
				sftp_search=self.__ssh.open_sftp()
			except Exception as err:
				print('ssh查找文件通道创建失败!请检查网络和ssh服务器地址,端口号,帐号和密码是否有误.\n错误内容如下:')
				print(err)
				sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			else:
				try:#查找文件夹
					if path:
						file_name=sftp_search.listdir(path)
					else:
						file_name=sftp_search.listdir()
				except Exception as err:
					print('查找路径: '+str(path)+'下的所有文件和文件夹失败!错误内容如下:')
					print(err)
					sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
				else:
					if end:
						try:#查找path目录下以end结尾的文件
							file_name_0=[]
							for i in file_name:
								if i.endswith(end):
									file_name_0.append(i)
							file_name=file_name_0[:]
						except Exception as err:
							print('查找路径: '+str(path)+'下的所有以: '+str(end)+' 结尾的文件失败!错误内容如下:')
							print(err)
							sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
					return file_name

if __name__ == '__main__':
    hostname = '10.10.88.54'
    username = "root"
    password = "1q2w3e"
    ssh = ssh(host=hostname, passwd=password, name=username)
    ssh.connect()
    print(ssh.cmd(cmd='echo $PATH'))
	# print(ssh.cmd(cmd='echo $PATH'))
    # print(ssh.cmd(cmd='ip a'))
    # print(ssh.cmd(cmd='ps -ef |grep nginx'))
    # ssh.cmd(cmd='ip a')
    ssh.close()