from ddos_attack import index
import time
import json
datatime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
cardid0_1=index.card_id0_1

setddos_open = {
"SetDdosEnable":{
"MethodName":"SetDdosEnable",
 "MessageTime":datatime,
 "Content":[{"Enable":1,"Cards":cardid0_1}]
}
}