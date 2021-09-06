# -*- coding: utf-8 -*-
import smtplib
from email.mime.text import MIMEText
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication


# 封装一个方法直接传入邮件标题和内容
def post_email(sender, receivers, cc_list, bcc_list, mail_host, mail_port, mail_user, mail_pass, attach_path, file, title, context, cc_flag=0,part_flag=0):
    # 三个参数：第一个为文本内容，第二个 plain 设置文本格式，第三个 utf-8 设置编码
    msg = MIMEMultipart()
    msg['From'] = Header(sender)  # 发送者
    msg['To'] = Header(str(";".join(receivers)))  # 接收者,注意，不是分号
    msg['Cc'] = ','.join(cc_list)
    msg['Bcc'] = ','.join(bcc_list)
    msg['Subject'] = Header(title)  #邮件主题
    context = str(context)
    txt = MIMEText(context, 'plain', 'utf-8')
    msg.attach(txt)
    if part_flag == 1:
        print("准备添加附件...")
        # 添加附件，从本地路径读取。如果添加多个附件，可以定义part_2,part_3等，然后使用part_2.add_header()和msg.attach(part_2)即可。
        part = MIMEApplication(open(attach_path, 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename=file)  # 给附件重命名,一般和原文件名一样,改错了可能无法打开.
        msg.attach(part)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host,mail_port)
        # smtpObj = smtplib.SMTP_SSL(mail_host, mail_port)      #qq邮箱的设置
        smtpObj.login(mail_user, mail_pass)
        if cc_flag == 0:
            smtpObj.sendmail(sender, receivers, msg.as_string())
        elif cc_flag == 1:
            smtpObj.sendmail(sender, receivers+cc_list+bcc_list, msg.as_string())
        smtpObj.quit()  #关闭邮箱连接
        return 1
    except smtplib.SMTPException:
        return 0

#
# if __name__ == '__main__':
#     sender = 'liwanqiu66@163.com'  # 发件人
#     receivers = ['m53667987@163.com']  # 收件人
#     cc_list = ['liwanqiu66@163.com', 'm53667987@163.com']  # 抄送人
#     bcc_list = ['liwanqiu66@163.com', 'm53667987@163.com']  # 暗送人
#     mail_host = "10.10.88.55"  # 设置服务器,发件人的服务器代理
#     mail_port = 8885  # 设置服务器端口
#     mail_user = "liwanqiu66@163.com"  # 邮件登录地址
#     mail_pass = "lwq5945"  # 授权码
#     attach_path = r'C:\Users\admin\Desktop\work\1.xls'  # 本地附件路径
#     file = '1.xls'
#     title = '测试'
#     context = '测试测试测试'
#     result = post_email(sender, receivers, cc_list, bcc_list, mail_host, mail_port, mail_user, mail_pass, attach_path, file, title, context, 0,0)
#     print(result)
