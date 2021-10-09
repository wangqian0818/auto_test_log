# coding:utf-8
from common import baseinfo

proxy_ip = baseinfo.BG8010FrontOpeIp
dns_proxy_port = baseinfo.dns_proxy_port

dns_ip = proxy_ip + ':' + str(dns_proxy_port)

# 配置检查
# 列表里面的顺序依次为：查询命令，预期结果
case1_step1 = {
    "step1": ["cat /etc/jsac/customapp.stream", dns_ip]
}
case1_step11 = {
    "step1": ["netstat -anp |grep udp", dns_ip]
}
