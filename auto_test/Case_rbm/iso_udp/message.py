
from common import baseinfo
import time


datatime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
front_ifname = baseinfo.BG8010FrontOpeIfname
back_ifname = baseinfo.BG8010BackOpeIfnameOutside
front_cardid = baseinfo.BG8010FrontCardid
back_cardid = baseinfo.BG8010BackCardid
iso_timeout = baseinfo.iso_timeout
serverIp = baseinfo.BG8010ServerOpeIp
clientIp = baseinfo.BG8010ClientOpeIp
dns_port = baseinfo.dns_port
dns_proxy_port = baseinfo.dns_proxy_port


addudp_dns_front = {
"AddCustomAppPolicy":{
"MethodName":"AddCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":front_ifname,
"Dip":serverIp,
"Sip":clientIp,
"Domain":"src",
"Cards":front_cardid,
"Applist":[{
"Sport":"1-65535",
"Action":"allow",
"Appid":5,
"L3protocol":"ipv4",
"Timeout":iso_timeout,
"Dport":dns_port,
"SeLabel":{},
"File":"off",
"Lport":dns_proxy_port,
"L4protocol":"udp"}]
}]}
}

addudp_dns_back = {
"AddCustomAppPolicy":{
"MethodName":"AddCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":back_ifname,
"Dip":serverIp,
"Sip":clientIp,
"Domain":"dest",
"Cards":back_cardid,
"Applist":[{
"Sport":"1-65535",
"Action":"allow",
"Appid":5,
"L3protocol":"ipv4",
"Timeout":iso_timeout,
"Dport":dns_port,
"SeLabel":{},
"File":"off",
"Lport":dns_proxy_port,
"L4protocol":"udp"}]
}]}
}

deludp_dns_front = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":front_ifname,
"Dip":serverIp,
"Sip":clientIp,
"Domain":"src",
"Cards":front_cardid,
"Applist":[{
"Sport":"1-65535",
"Action":"allow",
"Appid":5,
"L3protocol":"ipv4",
"Timeout":iso_timeout,
"Dport":dns_port,
"Lport":dns_proxy_port,
"L4protocol":"udp"}]
}]}
}

deludp_dns_back = {
"DelCustomAppPolicy":{
"MethodName":"DelCustomAppPolicy",
"MessageTime":datatime,
"Sender":"Centre0",
"Content":[{
"Ifname":back_ifname,
"Dip":serverIp,
"Sip":clientIp,
"Domain":"dest",
"Cards":back_cardid,
"Applist":[{
"Sport":"1-65535",
"Action":"allow",
"Appid":5,
"L3protocol":"ipv4",
"Timeout":iso_timeout,
"Dport":dns_port,
"Lport":dns_proxy_port,
"L4protocol":"udp"}]
}]}
}
