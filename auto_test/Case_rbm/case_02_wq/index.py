#coding:utf-8
#此文件的参数配置均与用例强相关，与执行环境无关
#适用用例范围


from common import baseinfo

pcap_sip = baseinfo.clientOpeIp
pcap_dip = baseinfo.serverOpeIp
ciface = baseinfo.pcapSendIface
siface = baseinfo.pcapReadIface
strip = baseinfo.strip
dport=2299
attack_port=8889
card_id0='CS807304LV10082N021'
card_id1='CS807304LV09082N070'
card_id0_1=card_id0+','+card_id1

#获取ddos开关状态
ddos={"syn-cookie": "on","filter noflow": "on","check no option": "on"}
for key,value in ddos.items():
    ddos_open=key +': '+str(value)
    #print(ddos_open)

#报文发送,读取和预期结果
#列表里面的命令依次为：
#发送端杀掉进程参数
#服务端杀掉进程参数
#发送端：发送报文接口，发送报文数量，发送报文名称；
#抓包：接口名称，过滤规则，抓包数量，报文命名（以用例名称.pcap命名）
#报文读取：保存的报文名称，要读取的包的序号；这里读取的报文名称和上面抓包的保存报文名称应该一致
#期望结果：预期结果（协议字段），是否有偏差（保留），偏差值（保留）

pkt1_cfg={
    "hping3":[f"hping3 -i u1000 -R -p {attack_port} {pcap_dip} --rand-source --tcp-timestamp"],
    "http":[f"python2.7 -m SimpleHTTPServer {dport}"],
    #"send":[ciface,1,"0001_acl.pcap"],
    "capture":[siface,f"tcp and host {pcap_dip}",1,"test_ddos_rst_flood.pcap"],
    "read":["test_ddos_rst_flood.pcap",0],
    "expect":[strip,0,0]
}
pkt2_cfg={
    "hping3":[f"hping3 -i u1000 -F -A -p {attack_port} {pcap_dip} --rand-source --tcp-timestamp"],
    "http":[f"python2.7 -m SimpleHTTPServer {dport}"],
    #"send":[ciface,1,"0001_acl.pcap"],
    "capture":[siface,f"tcp and host {pcap_dip}",1,"test_ddos_fin_flood.pcap"],
    "read":["test_ddos_fin_flood.pcap",0],
    "expect":[strip,0,0]
}
pkt3_cfg={
    "hping3":[f"hping3 -i u1000 -A -p {attack_port} {pcap_dip} --rand-source --tcp-timestamp"],
    "http":[f"python2.7 -m SimpleHTTPServer {dport}"],
    #"send":[ciface,1,"0001_acl.pcap"],
    "capture":[siface,f"tcp and host {pcap_dip}",1,"test_ddos_ack_flood.pcap"],
    "read":["test_ddos_ack_flood.pcap",0],
    "expect":[strip,0,0]
}
pkt4_cfg={
    "hping3":[f"hping3 -i u1000 -SA -p {attack_port} {pcap_dip} --rand-source --tcp-timestamp"],
    "http":[f"python2.7 -m SimpleHTTPServer {dport}"],
    #"send":[ciface,1,"0001_acl.pcap"],
    "capture":[siface,f"tcp and host {pcap_dip}",1,"test_ddos_syn_ack_flood.pcap"],
    "read":["test_ddos_syn_ack_flood.pcap",0],
    "expect":[strip,0,0]
}
pkt5_cfg={
    "hping3":[f"hping3 -i u1000 -S -p {attack_port} {pcap_dip} -a {pcap_dip} --tcp-timestamp"],
    "http":[f"python2.7 -m SimpleHTTPServer {dport}"],
    #"send":[ciface,1,"0001_acl.pcap"],
    "capture":[siface,f"tcp and host {pcap_dip}",1,"test_ddos_sameSipDip_syn_flood.pcap"],
    "read":["test_ddos_sameSipDip_syn_flood.pcap",0],
    "expect":[strip,0,0]
}
pkt6_cfg={
    "hping3":[f"hping3 -i u1000 -S -p {attack_port} {pcap_dip} --rand-source --tcp-timestamp"],
    "http":[f"python2.7 -m SimpleHTTPServer {dport}"],
    #"send":[ciface,1,"0001_acl.pcap"],
    "capture":[siface,f"tcp and host {pcap_dip}",1,"test_ddos_randomSipSport_syn_flood.pcap"],
    "read":["test_ddos_ddos_randomSipSport_syn_flood.pcap",0],
    "expect":[strip,0,0]
}



#配置下发
#列表里面的顺序依次为：配置命令，查询命令，预期结果

case1_step={
    "step1":['cardid=0&&defconf --show','cardid=1&&defconf --show',ddos_open],
}
