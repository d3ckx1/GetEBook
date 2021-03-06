# /env/bin/python
# -*- coding=utf-8 -*-

import requests
import os
import sys
import time
import re
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8') #ascii编码问题解决

banner = '''

         ______     __  ________                __  
        / ____/__  / /_/ ____/ /_  ____  ____  / /__
       / / __/ _ \/ __/ __/ / __ \/ __ \/ __ \/ //_/
      / /_/ /  __/ /_/ /___/ /_/ / /_/ / /_/ / ,<   
      \____/\___/\__/_____/_.___/\____/\____/_/|_|  
                                                                                        
                  code by d3ckx1
'''
print banner

heads = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

def getebook():
    ebook = sys.argv[1]  #输入url

    req = requests.get(ebook, headers=heads, timeout=5)
    req.encoding = "utf-8" #设置编码
    #获取html—title
    html = req.text
    selector = etree.HTML(html)
    #title = selector.xpath('//title/text()') #获取html—title
    booktitle = selector.xpath('//div[@class="info"]//h2/text()')[0] ##获取小说名

    print '-----------------------------------------------------------'
    print "[+] 正在爬取 %s" % ebook
    print "[+] 小说名称: " + booktitle
    print '-----------------------------------------------------------'
    #findlinks = selector.xpath("//div[@class='listmain']//dd/a/@href")  #获取目录url
    # findnames = selector.xpath("//div[@class='box_con']//dd/a/text()")[0]  # 获取目录名称
    findlinks = selector.xpath("//div[@class='listmain']/dl/dd/a/@href")[12:]  #获取目录url,去掉前面的最新章节

    list = []

    for links in findlinks:
        list.append(ebook + links)
    #print list

    cd = "/Users/d3ckx1-home/Desktop/getebook/xiaoshuo/"
    if os.path.exists(cd) == False:  # 如果磁盘路径没有这个目录就创建xiaoshuo文件夹
        os.mkdir(cd)

    for i in list:  # 遍历章节链接，获取小说内容
        response = requests.get(i, headers=heads, timeout=3)
        response.encoding="utf-8"
        html = response.text
        elem = etree.HTML(html)

        conText = elem.xpath("//div[@id='content']/text()")  # 小说内容
        ts = elem.xpath("//div[@class='content']/h1/text()")[0]  # 小说章节标题
        ts = re.sub(u"[^\u4e00-\u9fa5\u0030-\u0039]", "", ts)  # 只保留标题中的中文
        for val in conText:  # 保存小说内容
            with open(cd + ts + ".txt", "a+") as f:
                f.write(val + "\n")
                f.
        f.close()
        print("%s —— %s  下载完成：%s" % (booktitle, ts, i))  # 输出保存信息，防止出错。
        time.sleep(1)


if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] == '-h':
        print('Usage :python getebook.py http://www.sizhicn.com/txt/127117/')

    else:
        getebook()


