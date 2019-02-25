#!/usr/bin/python
#coding:utf-8

"""
Author: Andy Tian
Contact: tianjunning@126.com
Software: PyCharm
Filename: get_lon_lat.py
Time: 2019/2/18 21:47
"""
import csv
import requests
import json
import time
from urllib import parse

def get_lon_lat(address):
    '''
    http://api.map.baidu.com/place/v2/suggestion?query=天安门&region=北京&city_limit=true&output=json&ak=你的ak //GET请求
    通过访问百度的api 返回某个地点的经纬度
    query: str,必须,查询地点
    region:str,必须,省一级地区单位
    city_limit:boole,true返回指定region结果,false返回所有结果
    output:str 返回数据的类型
    ak:str 百度申请的密钥
    '''
    base_url = "http://api.map.baidu.com/place/v2/suggestion?"
    sparams = {"query" :address,
            "region":"北京",
            "city_limit":"true",
            "output":"json",
            "ak":"XQSxj8hik3LqooCWhLXTtrWA2Lo3hMO4"}
    url = base_url + parse.urlencode(sparams)
    resp = requests.get(url).text
    temp = json.loads(resp)

    return temp  # 返回包含地点信息的json数据

with open('lon_lat.json',"a",encoding='utf-8') as f:
    house_price = open('.\\lianjia\\lianjia\\bj_house_price.csv','r',encoding='utf-8')
    csv_reader_lines = csv.reader(house_price)
    times01,times02 = 1,1
    for line in csv_reader_lines:
        xiaoqu = line[1]
        mean = line[2]
        print(xiaoqu,mean)
        temp = get_lon_lat(xiaoqu)
        if temp['status'] == 0:
                if len(temp['result']) == 0:
                    print('百度检索不到{}小区'.format(xiaoqu),"标记{}".format(times01))
                    times01 += 1
                else:
                    if "location" in temp['result'][0].keys():
                        lng = temp['result'][0]['location']['lng']
                        lat = temp['result'][0]['location']['lat']
                        content = '{"lng":' + str(lng) + ',"lat":' + str(lat) + ',"count":' + str(mean) + "},\n"
                        f.write(content)
        elif temp['status'] != 0:
            print('第{}次超过并发配额,限制访问'.format(times02),"--缺失数据{}{}".format(xiaoqu,mean))
            times02 += 1
        time.sleep(1/2)
        if times02 % 10 == 0:
            time.sleep(20)




