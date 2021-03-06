# -*- coding: utf-8 -*-
import frida, sys

# HOOK
jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.lalamove.huolala.http.HttpsUtils$MyTrustManager");//获取到类
        util.getAcceptedIssuers.implementation = function(){
            console.log("Hook Start 111 ...");
        }
        
        var util2 = Java.use("com.lalamove.huolala.http.HttpsUtils");//获取到类
        util2.verifyHost.implementation = function(p1,p2){
            console.log("Hook Start 222 ...");
        }
    });
}
"""


def on_message(message, data):
    if message['type'] == 'send':
        print(" {0}".format(message['payload']))
    else:
        print(message)


# 查找USB设备并附加到目标进程
session = frida.get_usb_device().attach('com.lalamove.huolala.client')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()
