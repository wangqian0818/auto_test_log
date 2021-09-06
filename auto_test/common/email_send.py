# coding:utf-8
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import os
import sys
base_path=os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))#获取当前项目文件夹
base_path=base_path.replace('\\','/')
sys.path.insert(0,base_path)#将当前目录添加到系统环境变量,方便下面导入版本配置等文件
import common.baseinfo as info
del sys.path[0]

subject="auto test"
def emailSend(message):
	print('---------------email send-----------')
	receiver_list=list(info.receiver)
	smtp = smtplib.SMTP()
	smtp.connect(info.smtp_server,25)
	smtp.login(info.sender,info.sender_passwd)
	msg=MIMEText(message,"plain","utf-8")
	msg["Subject"]=Header(subject,"utf-8")  #头部信息:标题
	msg["From"]=info.sender
	msg["To"]=",".join(receiver_list)
	smtp.sendmail(info.sender,receiver_list,msg.as_string())
	smtp.quit()




    


