# -*- coding: utf-8 -*-

import frida
import sys

jscode = """
if(Java.available){
    Java.perform(function(){
        var util = Java.use("com.yestae.yigou.customview.HomeBannerView");//获取到类
        util.bannerStartPlay.implementation = function(){
            console.log("bannerStartPlay -------> ");
            this.bannerStartPlay();
        }
        
        util.updateView.overload("int","java.util.ArrayList").implementation = function(p1,p2){
            console.log("updateView --------->");
            console.log("p1 : " + p1);
            this.updateView(p1,p2);
        }

        util.setLimitSaleData.overload("java.util.List").implementation = function(p1){
            console.log("setLimitSaleData --------->");
            console.log("p1 : " + p1);
            this.setLimitSaleData(p1,p2);
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
session = frida.get_usb_device().attach('com.uustock.dayi')

# 在目标进程里创建脚本
script = session.create_script(jscode)

# 注册消息回调
script.on('message', on_message)

# 加载创建好的javascript脚本
script.load()

# 读取系统输入
sys.stdin.read()
