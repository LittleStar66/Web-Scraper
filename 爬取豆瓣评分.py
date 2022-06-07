# -*- coding: utf-8 -*-
"""
Created on Tue Jun  7 14:38:21 2022

@author: xl.li
"""

'''
需求：爬取电影的名字 评分 引言 详情页的url，每一页都爬取并且把数据保存到csv文件当中
步骤：
第一步 获取网页源码
第二步 获取电影信息
第三步 保存数据
'''
# 导入模块
import requests  # 获取源代码
import lxml  # 获取电影项目
from lxml import etree # 获取电影项目
import csv  # 保存数据

'''
第一步：获取网页源码
(1)分析目标url
(2)获取网页源代码
'''
# https://movie.douban.com/top250?start=0&filter= 第一页 （start=0）
# https://movie.douban.com/top250?start=25&filter= 第二页 （start=25）
# https://movie.douban.com/top250?start=50&filter= 第三页  （start=50）
# 目标url： https://movie.douban.com/top250?start=(i-1)*25&filter=  第i页 start=(i-1)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}
def get_source(url):
    response = requests.get(url,headers=headers)
    # print(response) # <Response [200]>
    response.encoding = 'utf-8'
    return response.text

'''
第二步：获取并保存电影项目
(1)获取项目
(2)保存电影项目
'''
def get_item(source):
    html_element = etree.HTML(source)
    movieItemList = html_element.xpath('//div[@class="info"]')
    # 定义一个空的列表
    movieList = []

    for eachMoive in movieItemList:

        # 创建一个字典 像列表中存储数据[{电影一},{电影二}......]
        movieDict = {}

        title = eachMoive.xpath('div[@class="hd"]/a/span[@class="title"]/text()') # 标题
        subtitle = eachMoive.xpath('div[@class="hd"]/a/span[@class="other"]/text()')  # 副标题
        link = eachMoive.xpath('div[@class="hd"]/a/@href')[0]  # url
        star = eachMoive.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()')[0] # 评分
        quote = eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()')  # 引言（名句）
        if quote:
            quote = quote[0]
        else:
            quote = ''
        # 保存数据
        movieDict['title'] = title
        movieDict['subtitle'] = subtitle
        movieDict['url'] = link
        movieDict['star'] = star
        movieDict['quote'] = quote

        movieList.append(movieDict)
        print(movieList)
    return movieList

# 保存数据
def writeData(movieList):
    with open('douban.csv','w',encoding='utf-8',newline='') as f:
        writer = csv.DictWriter(f,fieldnames=['title','subtitle','url','star','quote'])
        writer.writeheader() # 写入表头
        for each in movieList:
            writer.writerow(each)

movieList = []
for i in range(0,10):
    page = str(i*25)
    url = 'https://movie.douban.com/top250?start='+page+'&filter='
    print(url)
    source = get_source(url)
    movieList += get_item(source)
writeData(movieList)




