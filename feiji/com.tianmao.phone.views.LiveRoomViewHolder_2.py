# -*- coding: utf-8 -*-
import frida
import sys

jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.tianmao.phone.views.LiveRoomViewHolder");//获取到类
        util.setShowBarrage.overload("int","java.lang.String","int","java.lang.String").implementation = function(p1, p2, p3,p4){
            //打印堆栈
            //console.log(Java.use("android.util.Log").getStackTraceString(Java.use("java.lang.Exception").$new()));
            console.log("Hook Start...");
            console.log("p1 : " + p1);
            console.log("p2 : " + p2);
            console.log("p3 : " + p3);
            console.log("p4 : " + p4);
            //var p4_2 = p4.replace("手机用户", "电脑用户");
            //console.log("p4_2 : " + p4_2);
            this.setShowBarrage(p1, p2, p3,p4);
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
session = frida.get_usb_device().attach('com.tmfeiji11.phonelive1237')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()
