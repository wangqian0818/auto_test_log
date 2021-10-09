'''
ftp相关命令操作
ftp.cwd(pathname) #设置FTP当前操作的路径
ftp.dir() #显示目录下文件信息
ftp.nlst() #获取目录下的文件
ftp.mkd(pathname) #新建远程目录
ftp.pwd() #返回当前所在位置
ftp.rmd(dirname) #删除远程目录
ftp.delete(filename) #删除远程文件
ftp.rename(fromname, toname)#将fromname修改名称为toname。
ftp.storbinaly("STOR filename.txt",file_handel,bufsize) #上传目标文件
ftp.retrbinary("RETR filename.txt",file_handel,bufsize)#下载FTP文件
'''
from ftplib import FTP
import socket
import ftplib
import os

def connect_ftp(host, port, username, password):
    try:
        fp = FTP()
        fp.encoding = 'utf-8'
        fp.set_debuglevel(2)  # 打开调试级别2，显示详细信息
        # fp.set_debuglevel(0)   #关闭调试信息
        fp.connect(host, port)  # 连接
        print("*******已经成功连接'%s'服务器FTP服务！！！" % host)
    except(socket.error, socket.gaierror) as e:
        print("错误：无法访问'%s'服务器FTP服务！！！%s" % (host, e))
        return 0
    try:
        fp.login(username, password)  # 登录，如果匿名登录则用空串代替即可
        print('ftp登录成功')
    except Exception:
        print("ftp登录失败，请检查用户名和密码")
        return 0
    return fp


def uploadFile(fp, remotePath, localPath):
    try:

        # 创建ftp目录
        dirs = str(remotePath).split("/")
        curdir = ""
        for d in dirs:
            if (-1 != d.find(".")):
                break
            curdir = curdir + "/" + d
            print("creat dir:" + curdir)
            try:
                fp.cwd(curdir)
            except Exception as e:
                fp.mkd(curdir)

        fp.cwd("/")

        bufsize = 1024  # 设置的缓冲区大小
        f = open(localPath, "rb")
        fp.storbinary("STOR %s" % remotePath, f, bufsize)  # 上传目标文件
        f.close()
        return 1
    except Exception as e:
        print('Error:', e)
        return 0

#上传文件夹内的所有文件（包括文件和文件夹）
def uploadFileAll(fp, localDir):
    try:
        for root, dirs, files in os.walk(localDir, topdown=True):
            relative = root[len(localDir):].lstrip(os.sep)
            for d in dirs:
                fp.mkd(os.path.join(relative, d))

            for f in files:
                filePath = os.path.join(localDir, relative, f)
                fp.cwd(relative)
                with open(filePath, 'rb') as fileObj:
                    fp.storbinary('STOR ' + f, fileObj)
                fp.cwd('/')
        fp.quit()
        return 1
    except Exception as e:
        print('Error:', e)
        return 0


#上传文件夹内的所有文件夹（仅针对目录上传）
def UpLoadDir(fp, LocalDir, RemoteDir='/'):
    try:
        if os.path.isdir(LocalDir) == False:
            return False
        print("LocalDir:", LocalDir)
        LocalNames = os.listdir(LocalDir)
        print("list:", LocalNames)
        print(RemoteDir)
        fp.cwd(RemoteDir)
        for Local in LocalNames:
            src = os.path.join(LocalDir, Local)
            if os.path.isdir(src):
                UpLoadDir(fp, Local, src)
            else:
                uploadFile(fp, src, Local)
        fp.cwd("..")
        return 1
    except Exception as e:
        print('Error:', e)
        return 0

#下载文件夹内的所有文件夹（仅针对目录下载）
def DownDir(fp, RemoteDir, LocalDir):
    try:
        print("remoteDir:", RemoteDir)
        if os.path.isdir(LocalDir) == False:
            os.makedirs(LocalDir)
        fp.cwd(RemoteDir)
        RemoteNames = fp.nlst()
        print("RemoteNames", RemoteNames)
        print(fp.nlst(RemoteDir))
        for file in RemoteNames:
            Local = os.path.join(LocalDir, file)
            if checkFileDir(fp, file):
                DownDir(fp, file, Local )
            else:
                downFile(fp, file, Local)
        fp.cwd("..")
        return 1
    except Exception as e:
        print('Error:', e)
        return 0


def downFile(fp, remotePath, localPath):
    bufsize = 1024  # 设置的缓冲区大小

    try:
        f = open(localPath, "wb")
        fp.retrbinary("RETR %s" % remotePath, f.write, bufsize)  # 下载目标文件
        # fp.quit()  # 退出ftp
        f.close()
        return 1
    except Exception as e:
        print('Error:', e)
        # fp.quit()
        return 0

# 获取目录下文件或文件夹的列表信息，并清洗去除“. ..”
def nlstListInfo(fp):
    files_list = fp.nlst()
    return [file for file in files_list if file != "." and file !=".."]

# 判断文件与目录
def checkFileDir(ftp,file_name):
    rec = ""
    try:
        rec = ftp.cwd(file_name)   # 需要判断的元素
        ftp.cwd("..")   # 如果能通过路径打开则为文件夹，在此返回上一级
    except ftplib.error_perm as e:
        rec = e # 不能通过路径打开必为文件，抓取其错误信息
    finally:
        if "550 Failed to change directory" in str(rec):
            return "File"
        elif "250 Directory successfully changed" in str(rec):
            return "Dir"
        else:
            return "Unknow"


def deleallFile(fp, Path, filename=None):
    try:
        try:
            fp.cwd(Path)
        except ftplib.error_perm:
            print('无法进入目录：{}'.format(Path))
        print("当前所在位置:{}".format(fp.pwd()))  # 返回当前所在位置
        ftp_f_list = fp.nlst()  # 获取目录下文件、文件夹列表
        print(ftp_f_list)
        if (filename in ftp_f_list) and (filename != None):
            fp.delete(filename)  # 删除文件
            print("{}已删除！".format(filename))
            fp.close()
            return 1
        elif filename == None:
            filelist = nlstListInfo(fp)
            print(filelist)
            tmp = []
            for i in filelist:
                if checkFileDir(fp, i) == "File":
                    fp.delete(i)  # 删除文件
                    print("{}是文件，已删除！".format(i))
                    tmp.append(i)
                elif checkFileDir(fp, i) == "Dir":
                    print("{}是文件夹".format(i))
                else:
                    print("{}无法识别，跳过".format(i))
            print(tmp)
            fp.close()
            if tmp != []:
                return 1
        else:
            print("{}未找到，删除中止！".format(filename))
    except Exception as e:
        print('Error:', e)
        # fp.quit()
        return 0



if __name__ == '__main__':
    host = '192.168.30.13'
    port = 2121
    username = 'test'
    password = '1q2w3e'
    # path = '/ftp_李皖秋/ftp_del'
    # filename = 'utmp2log-0.0.22.tar.gz'
    upremotePath = '/home/ftp/ftp_auto/10G.txt'
    uplocalPath = 'C:/Users/admin/Desktop/work/10G.txt'

    downremotePath = '/home/ftp/ftp_auto/1.txt'
    downlocalPath = 'C:/Users/admin/Desktop/work/1.txt'

    localDir = 'C:/Users/admin/Desktop/work/uploadDir'
    remoteDir = '/ly'

    fp = connect_ftp(host, port, username, password)
    print('欢迎语是：{}'.format(fp.getwelcome()))
    assert '220' in fp.getwelcome()
    # print(fp)
    path = '/home/ftp/ftp_auto/ftp_del/wq_test.txt'
    result = deleallFile(fp, path)
    print(result)

    # result = uploadFile(fp, upremotePath, uplocalPath)
    # print(result)
    # result = downFile(fp, downremotePath, downlocalPath)
    # result = uploadFileAll(fp,localDir)
    # print(result)
    # result2 = DownDir(fp,remoteDir, localDir)
    # print(result2)

