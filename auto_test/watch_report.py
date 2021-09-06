#encoding='utf-8'
try:
	import os,sys
except Exception as err:
	print('导入库失败!请检查是否安装相关库后重试.')
	sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序

def main(report_path=''):
	if not report_path:
		base_path=os.path.dirname(os.path.abspath(__file__))#获取当前项目文件夹
		base_path=base_path.replace('\\','/')
		sys.path.insert(0,base_path)#将当前目录添加到系统环境变量,方便下面导入版本配置等文件

		try:#导入版本配置等文件
			import common.baseinfo as info
		except Exception as err:
			print('版本配置文件导入失败!请检查: '+base_path+'/common/baseinfo.py 文件是否存在.\n错误信息如下:')
			print(err)
			sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
		else:
			try:
				version=info.version#获取版本号
			except Exception as err:
				print('版本号获取失败!请检查是否设置了版本号.错误信息如下:')
				print(err)
				sys.exit(0)#避免程序继续运行造成的异常崩溃,友好退出程序
			else:
				report_path=base_path+'/report/'+str(version)#根据版本号,获取report目录
	try:
		os.system('allure open -h 127.0.0.1 -p 8083 '+str(report_path))
	except Exception as err:
		print('自动化测试已完成,但创建web服务浏览失败!\n当前测试报告地址保存在: '+str(report_path)+'\n直接浏览html文件会导致数据加载失败!\n可以新建一个web服务,将web目录指向: '+str(report_path))

if __name__=='__main__':
	main()
