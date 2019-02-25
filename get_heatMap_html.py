#!/usr/bin/python
#coding:utf-8

"""
Author: Andy Tian
Contact: tianjunning@126.com
Software: PyCharm
Filename: get_heatMap_html.py
Time: 2019/2/21 10:51
"""

import requests
import re

def get_html():
    '''
    获取百度热力图demo的源代码
    :return: h5代码
    '''
    url = "http://lbsyun.baidu.com/jsdemo/demo/c1_15.htm"
    header = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.6788.400 QQBrowser/10.3.2864.400",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "Accept-Encoding":"gzip, deflate",
        "Accept-Language":"zh-CN,zh;q=0.9"
    }
    htmlstr = requests.get(url,headers=header)._content.decode()
    htmlstr_formated = htmlstr.replace("\n",'').replace("\t",'')

    return htmlstr_formated

def modify_html(htmlstr):
    '''
    根据项目需要,对demo中的参数进行修改
    1)ak  修改为自己在百度中申请的密钥
    2)container{height:500px;width:100%;} 地图打开时的大小.
    3)points 热力图显示的坐标
    4)new BMap.point 地图打开时显示的重点位置
    5)heatmapOverlay = new BMapLib.HeatmapOverlay({"radius":20}) 热力显示半径
    6)# heatmapOverlay.setDataSet({data:points,max:100}); 数据大小,超过max后显示颜色一致,根据实际数据,修改max大小
    :param htmlstr:需要修改的h5代码
    :return: 修改好的代码
    '''
    data = open("G:\Python\Project\Spider\scrapyProject\lianjia\lon_lat.json")
    datastr = data.read()
    htmlstr = htmlstr.replace("height:500px","height:80%").replace('{"radius":20}','{"radius":10}').replace("max:100","max:120000")
    be_replaced_data = ",\n".join(re.findall(r'{"lng":.*"count":\d*}',htmlstr))
    htmlstr_modified = htmlstr.replace(be_replaced_data,datastr)
    return htmlstr_modified

def rewrite_html(str):
    '''
    h5代码写入文件
    :param str: h5代码
    :return: h5文档
    '''
    with open("heat.html","w",encoding="utf-8") as f:
        f.write(str)


if __name__ == "__main__":
    htmlstr = get_html()
    htmlstr_modified = modify_html(htmlstr)
    write_html(htmlstr_modified)

