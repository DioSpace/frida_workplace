# -*- coding: utf-8 -*-
import frida, sys

#HOOK构造方法
jscode = """
if(Java.available){
    Java.perform(function(){
        var Classz = Java.use("com.wuba.imsg.chat.bean.ChatBaseMessage");
        Classz.$init.overload("java.lang.String").implementation=function(param1){
            console.log(param1);
            this.$init(param1);
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
session = frida.get_usb_device().attach('com.wuba')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()