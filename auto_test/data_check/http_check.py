from urllib import request
from urllib import parse
import requests,time
from contextlib import closing
from requests_toolbelt.multipart.encoder import MultipartEncoder,MultipartEncoderMonitor

#urlencode可以把key-value这样的键值对转换成我们想要的格式，返回的是a=1&b=2这样的字符串
#百度搜索的页面的请求为'http://www.baidu.com/s?wd=',wd为请求搜索的内容
#urlencode遇到中文会自动进行编码转化
#一个参数时可以采用'http://www.baidu.com/s?wd='+keywd的格式，
# 但是当keywd为中文的时候需要用urllib.request.quote(keywd)进行编码转换
def http_get(url, data=None, flag=0):
    # data = parse.urlencode(values)
    # response = request.urlopen(f'{url}/s?%s' % data)
    # html = response.read()
    # print(html.decode('utf-8'))
    # file = open(path,'wb')
    # file.write(html)
    # file.close()
    try:
        response = requests.get(url, data, timeout=20)
        if response.status_code == 200:
            if flag == 0:
                context = response.text
                response.raise_for_status() #如果状态不是200，则引发异常
                print('get请求成功')
                return context
            else:
                return response.status_code
        else:
            return response.status_code
    except requests.exceptions.ConnectionError:
        print('get连接出错，请等待3s')
        time.sleep(3)
        return 0
    except requests.exceptions.ChunkedEncodingError:
        print('get：服务器声明了chunked编码但发送了一个无效的chunk：请等待3s')
        return 0
    except requests.exceptions.Timeout:
        print('get请求超时')
        return 0
    except requests.exceptions.InvalidURL:
        print('get：无效的URL')
        return 0
    except Exception as err:
        print('get产生异常,异常原因是:{}'.format(err))
        return 0


def http_post(url, data=None, headers=None, flag=0):
    # data = parse.urlencode(values)
    #     # print(data)
    #     # # data = data.encode('utf-8')
    #     # req = request.Request(url, data)
    #     # req.add_header(header)
    #     # response = request.urlopen(req)
    #     #
    #     # html = response.read()
    #     # # print(html.decode('utf-8'))
    try:
        response = requests.post(url, data, headers, timeout=20)
        if response.status_code == 200:
            if flag == 0:
                context = response.text
                response.raise_for_status()  # 如果状态不是200，则引发异常
                # print(response.request)
                # print(response.headers)
                print('post请求成功')
                return context
            else:
                return response.status_code
        else:
            return response.status_code
    except requests.exceptions.ConnectionError:
        print('post连接出错，请等待3s')
        time.sleep(3)
        return 0
    except requests.exceptions.ChunkedEncodingError:
        print('post：服务器声明了chunked编码但发送了一个无效的chunk：请等待3s')
        return 0
    except requests.exceptions.Timeout:
        print('post请求超时')
        return 0
    except requests.exceptions.InvalidURL:
        print('post：无效的URL')
        return 0
    except Exception as err:
        print('post产生异常,异常原因是:{}'.format(err))
        return 0

# 下载文件，采用流式下载，边下载边保存，避免下载大文件时因缓存过满导致下载失败的问题
def http_download(file_url, file_localpath):
    try:
        start_time = time.time() # 文件开始下载时的时间
        # stream=True设置报文头和报文主体分开下载，由于开启stream=True报文不是一次性全部下载完毕, 所以在过程中中断下载需要使用Response.close.以保证请求连接的正确关闭
        with closing(requests.get(file_url, stream=True)) as response:
            chunk_size = 5120  # 单次请求最大值
            content_size = int(response.headers['content-length'])  # 提取报文头content-length字段的内容，即内容体总大小
            data_count = 0
            with open(file_localpath, "wb") as file:
                for data in response.iter_content(chunk_size=chunk_size): #边下载边存硬盘,chunk_size设置每次加载多少字节
                    file.write(data)
                    data_count = data_count + len(data)
                    now_progress = (data_count / content_size) * 100
                    speed = data_count / 1024 / (time.time() - start_time)
                    print("文件{}的下载进度：{:.2f}%({:d}/{:d}) 文件下载速度：{:.2f}KB/s".format(file_localpath, now_progress, data_count, content_size, speed))
        return 1
    except Exception as err:
        print('文件下载异常，异常原因是：{}'.format(err))
        return 0

def my_callback(monitor):
    progress = (monitor.bytes_read / monitor.len) * 100
    print("文件上传进度：{:.2f}%({:d}/{:d})".format(progress, monitor.bytes_read, monitor.len))


#采用requests-toolbelt进行流式上传文件，不同于requests全部读到内存中上传，requests-toolbelt是边读边上传
#requests-toolbelt还提供了个监视器(MultipartEncoderMonitor)，该监视器接受一个回调函数，我们可以在回调中实时跟踪进度
def http_upload(remote_path, filename, filepath, MIME_type):

    try:
        e = MultipartEncoder(fields={'file':(filename, open(filepath, 'rb'), MIME_type)})
        m = MultipartEncoderMonitor(e, my_callback)
        headers = {"Content-Type": m.content_type}
        r = requests.post(remote_path, data=m, headers=headers)
        return 1
    except Exception as err:
        print('文件上传异常，异常原因是：{}'.format(err))
        return 0


if __name__ == '__main__':
    url = 'http://192.168.30.54:2287'
    # data1 = "abc"
    # data = {'data': 'test'}
    # # path = 'C:/Users/admin/Desktop/1.html'
    # #指定content-type类型是post的上传功能，post的下载只能是放在uri的后缀curl http://10.10.88.9:2286/1.pdf -v
    # #MIME类型主要是限制用户下载的内容，请求MIME类型只能是get请求，post对请求文件没有动态处理能力，只有请求.php文件才可以进行处理
    # # headers = {'Content-Type': 'application/txt'}
    a=http_get(url,flag=1)
    # content = http_get(url)
    # b=http_post(url)
    # # print(content)
    # print(b)
    # fileUrl = 'http://10.10.88.146:80/10G.txt'
    # file_localpath = 'C:/Users/admin/Desktop/10G.txt'
    # a = http_download(fileUrl, file_localpath)
    # up_fileUrl = 'http://192.168.30.54:9999/file'  # 文件链接
    # up_filepath = "C:/Users/admin/Desktop/work/10G.txt"  # 文件路径
    # filename = '1.txt'
    # MIME_type = 'text/plain'
    # a = http_upload(up_fileUrl, filename, up_filepath, MIME_type)
    # print(a)

