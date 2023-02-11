#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 18:39:28 2022

@author: ytz
"""

# Part2:爬取静态页面的信息

##导入包
import requests
import xlsxwriter
from bs4 import BeautifulSoup
import re
import time
import json
import pandas as pd
import os

# 创建储存文件的文件夹
#f1 = os.makedirs("video")  # 没带路径保存在当下路径
#f2 = os.makedirs("author_img")
#f3 = os.makedirs("poster")
#f4 = os.makedirs("picture")



###创建好存数据的表：
##post_info文件
xls = xlsxwriter.Workbook('post_info.xlsx')  # 加入地址
sht1 = xls.add_worksheet('post_info')
sht2 = xls.add_worksheet('picture_url')
sht3 = xls.add_worksheet('comment_level1')
sht4 = xls.add_worksheet('comment_level2')
sht5 = xls.add_worksheet('biaoqingbao_url')

#个人信息表格
sht1.write(0, 0, 'No.') #去定义一个unqie Number
sht1.write(0, 1, 'author_name')
sht1.write(0, 2, 'author_imgscr')
sht1.write(0, 3, 'userid')
sht1.write(0, 4, 'user_brief')
sht1.write(0, 5, 'ip_location')
sht1.write(0, 6, 'user_url')

#关于post的变量
sht1.write(0, 7, 'keywords')
sht1.write(0, 8, 'title')
sht1.write(0, 9, 'contenttype')
sht1.write(0, 10, 'publish_date')
sht1.write(0, 11, 'content')
sht1.write(0, 12, 'content_clean')
sht1.write(0, 13, 'tag_@')
sht1.write(0, 14, 'tag|')
sht1.write(0, 15, 'tagall')
sht1.write(0, 16, 'at')
sht1.write(0, 17, 'videotime')
sht1.write(0, 18, 'posterscr')
sht1.write(0, 19, 'videoscr')
sht1.write(0, 20, 'videoid')


#picture_sheet
sht2.write(0, 0, 'No.')
sht2.write(0, 1, 'userid')
sht2.write(0, 2, 'Picture Number.')
sht2.write(0, 3, 'picture_url')
sht2.write(0, 4, 'pictureid')

#一级comment_sheet
sht3.write(0, 0, 'No.')
sht3.write(0, 1, 'userid')
sht3.write(0, 2, 'comment_name')
sht3.write(0, 3, 'comment_id')
sht3.write(0, 4, 'comment_time')
sht3.write(0, 5, 'comment_content') #爬取不同层的数据
sht3.write(0, 6, 'comment_content_clean')
sht3.write(0, 7, 'reply')


#二级comment_sheet
sht4.write(0, 0, 'No.')
sht4.write(0, 2, 'comment_id')
sht4.write(0, 1, 'comment_name')
sht4.write(0, 3, 'comment_time')
sht4.write(0, 4, 'comment_content') 
sht4.write(0, 5, "reply_floor")
sht4.write(0, 6, 'reply_name') 
sht4.write(0, 7, 'reply_content') 

#表情包
sht5.write(0, 0, 'brief_name')
sht5.write(0, 1, "biaoqingbao_url")

x = 975
y = 1
a = 1
c = 1

#url="https://www.xiaohongshu.com/discovery/item/61e18a87000000000102fb96"
#df = pd.read_csv(r"./demo.csv")['url']
#url_list=df.values.tolist()
# 伪装信息
# 请求头（建立词典）
headers = {
     'Accept-Encoding':'gzip, deflate',
  #   'Accept-Language':'zh-CN,zh-Hans;q=0.9',
  #   'Connection':'keep-alive',
     'Host':'www.xiaohongshu.com',
     'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15",
     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
     'Cookie': 'ggid=yY4d2KWyfS2KyY4d2KWySl9qWixJ2DqJk6h0j7K3TvSUdD88JvKh0k888qy88WY8SWjiJiif; gid.sign=9aoYpFaXebyd6Ju0c5uOPk2jy8k=; gid.ss=gSMQ9UOnDuZwH2oRGJG6BW6e4grs67TaYpnrW+8Wmd3vl7stZrwbRBm4bJFe+y4H; xhsTracker=url=noteDetail&xhsshare=CopyLink; a1=184e5671c7fh25b32gmvaikycpe2y6va5o9bgt3u600000310078; galaxy.creator.beaker.session.id=1670151789299063216577; customerBeakerSessionId=bf2896a07893654e8267e8201ab65b55014c0140gAJ9cQAoWBAAAABjdXN0b21lclVzZXJUeXBlcQFLAVgOAAAAX2NyZWF0aW9uX3RpbWVxAkdB2OMfmHLhSFgJAAAAYXV0aFRva2VucQNYQQAAADVlMzc4NzBiYjA4YzQwYzFiNzM5NTMxMzhlOGVjZDRiLTI3YjY2YTA2YTQ3ODRmZDQ4ZDExZTk4ZDYyMzRlNjQxcQRYDgAAAF9hY2Nlc3NlZF90aW1lcQVHQdjjH5sqj1xYAwAAAF9pZHEGWCAAAAAwYzUzZTIzMDRiNGE0MDFkYTg3NjJlYTczZGIyMzFiNXEHWAYAAAB1c2VySWRxCFgYAAAANWMwMGU2MGUwMDAwMDAwMDA1MDBjOTFlcQl1Lg==; customerClientId=533548039384630; timestamp2=16700728520465d8cc66f9f4cce1530034bbf4e06414d333e475ffa7b7fea51; timestamp2.sig=miD-fJxEp68dc1uoAZb5bavJPLEYFmsV067t5WYR8BY; web_session=030037a4b4ab371d7c7e0fb9ff244ab9bdc7fe; xhsTrackerId=5a7b5527-cc13-45ab-c55d-778ff0f87ae2'
}


# proxies = get_proxies()


# 访问并解析数据
def getHtml(url):
    #proxies = get_proxies()
    resp = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(resp.text, 'html.parser')
    return soup

#print(getHtml(url).prettify())

def getData(url):
   # proxies = get_proxies()
    global sht1, x, sht2, y, sht3, a, sht4, sht5,c
    time.sleep(5)  # 避免反爬，休息
    soup = getHtml(url)  # 调用前面定义的函数getHtml
    #print(soup.prettify())

    # 笔记标题
    #写入No.
    Number = "mikebao_" + str(x)
    print("爬取的第"+ Number + "条数据")
    #写入这条数据的序号
    sht1.write(x, 0, Number)
    try:
        title = soup.find(attrs={"property": "og:title"})['content']
    except:
        x += 1
        return
    time.sleep(0.2)
    print("title是：")
    print(title)

    # 作者名称
    author_name = soup.find('span', class_='name-detail').get_text()
    print("authorname是：")
    print(author_name)
    time.sleep(0.2)

    # 作者头像链接
    author_imgscr = soup.find('div', class_='left-img').find('img').get('src')
    print("author_imgscr是：")
    print(author_imgscr)
    time.sleep(0.2)

    # 获取笔记的keywords
    keywords = soup.find(attrs={"name": "keywords"})['content']
    print("keyword是：")
    print(keywords)
    time.sleep(0.2)

    # 判断笔记类型
    contenttype = soup.find(attrs={"property": "og:type"})['content']
    print("contenttype是：")
    print(contenttype)
    time.sleep(0.2)

    # 发布时间
    publish_date = soup.find('div', class_='publish-date').find('span').get_text().replace("发布于 ","")  # .get_text()#发布时间（用正则去掉发布于）
    print("publish_date是：")
    print(publish_date)
    time.sleep(0.2)

    # 帖子内容_全
    content = str(soup.find('div', class_='content')).replace("</p>","\n")# 这个地方要把复杂的链接都修改规范
    print("content是：")
    print(content)
    time.sleep(0.2)
    
    #提取表情包的src
    try:
        biaoqingbao = soup.find('div', class_='content').find('img').get('src')
    #print(biaoqingbao)

        biaoqingbao_name = str(biaoqingbao).replace("//ci.xiaohongshu.com/xy_emo_","").replace(".png?v=2","")
        print("biaoqingbao_name是：")
        print(biaoqingbao_name)

        biaoqingbaosrc = "http:" + biaoqingbao
        print("biaoqingbaosrc是：")
        print(biaoqingbaosrc)
    except:
        biaoqingbao_name = ""
        biaoqingbaosrc =""
    
    #清理content内容
    content1 = re.sub('<div class="content" data-v-96f154ce=\"\">','',content).replace("<h1 class=\"as-p\" data-v-96f154ce=\"\">","").replace("</h1><p data-v-96f154ce=\"\">","\n") #success
    content2 = re.sub('<p data-v-96f154ce=\"\">','',content1) #success
    content3 = re.sub('</div>','',content2).replace("</a>","")
    content4 = re.sub('<a class=\"mention\" data-v-96f154ce=\"\" href=\"/user/profile.........................\" owl=\"mention/........................\">',"",content3)
    content5 = re.sub('" data-v-96f154ce=""',"",content4).replace("<img class=\"shubaobao-expression","").replace("src=\"//ci.xiaohongshu.com/xy_emo_","").replace(".png?v=2\"/>","")
    print("content是：")
    print(content5)
    
    #提取tag
    ##第一种：爬取#的数据（格式为：#ABC）
    tag_list = re.findall("#+.*", content5)
    tag1 = ",".join(tag_list)
    print("tag1是：")
    print(tag1)
    
    ##第二种：爬取｜的标签（这个没有去除干净，一共50条，需要手动）
    content6 =content5.replace("｜","|")#统一格式,将竖线转化成 英文
  
    print(content6)

    tag_list2 = str(re.findall("\|.*", content6))#.replace("\|",",")
    print("tag_list2是：")
    print(tag_list2)
    
    #
    tag_all = tag1+";"+tag_list2
    tagall =tag_all.replace("|", ",")
    print("tag_all是：")
    print(tagall)
    
    #提取@
    at_list = re.findall("@.*", content5)
    at = ",".join(at_list)
    print("at是：")
    print(at)
    
    
    # userprofile_url
    user_url = json.loads(soup.find('script', {'type': 'application/ld+json'}).get_text(), strict=False).get("author").get("url")
    print(user_url)
    
    userid = user_url.replace("https://www.xiaohongshu.com/user/profile/", "")
    print(userid)

    # 爬取user_profile
    profile_html = requests.get(url=user_url, headers=headers)
    # print(profile_html.text)
    profile_soup = BeautifulSoup(profile_html.text, 'html.parser')
    user_brief1 = profile_soup.find_all(class_='user-brief')
    user_brief = "".join('%s' %id for id in user_brief1).replace("<div class=\"user-brief\" data-v-28c03e4b=\"\">","").replace("</div>","")
    print(user_brief)
    
    # 爬取location
    try:
        ip_location = profile_soup.find('span', class_='location-text').get_text()
        print(ip_location)
    except:
        ip_location = 'null'

    # 储存author_img
    author_img = requests.get(url=author_imgscr).content  ###
    #  author_img = requests.get(url= author_imgscr, headers = headers, proxies=proxies).content###
    file = r"author_img/" + str(Number) + '.jpg'
    print("正在抓：" + file)
    f = open(file, 'wb')
    f.write(author_img)
    f.close()

    # comment 这部分还需要改一下 1.内容(f， 2.杂乱(f， 3.提取表情包(f， 4.回复的评论， 5.加一个楼层
    comment = soup.find_all('div', class_='comment')
    for it in comment:
         #评论id
         comment_id = it.find(class_='user-nickname').find('a').get('href').replace("/user/profile/", "")
         print(comment_id)
         
         #评论名称
         comment_name = str(it.find('h4', class_='user-nickname')).replace("<h4 class=\"user-nickname\" data-v-0282beb8=\"\">","").replace("<a data-v-0282beb8=\"\" href=\"/user/","").replace("</a>","").replace("</h4>","")
         comment_name1 = re.sub("profile/........................\">","",comment_name)
         print(comment_name1)
         
         #评论时间
         comment_time = it.find('span', class_='publish-time').get_text()
         print(comment_time)
         
         #一级评论
         ##去掉标签
         comment_content = str(it.find('p', class_='content')).replace("<p class=\"content\" data-v-0282beb8=\"\" data-v-031852b8=\"\">","").replace("</p>","")
         #print(comment_content)
         
         ##去掉表情包
         comment1 = comment_content.replace("<img class=\"icon\" data-v-031852b8=\"\"","").replace("<img class=\"shubaobao-expression","").replace("src=\"//ci.xiaohongshu.com/xy_emo_","").replace(".png?v=2\"/>","")
         print(comment1)
         
        ##修改：reply 要循环回复
         try:
            reply = it.find_all('div', class_='reply')
            
            reply1 =str(reply)
            print(reply1)
            b =1
            for m in reply:
                #二级评论
                reply_content = str(m.find('p', class_='reply-content')).replace("</p>",'').replace("<p class=\"reply-content\" data-v-031852b8=\"\" data-v-43aa3553=\"\">","").replace("<img class=\"icon\" data-v-031852b8=\"\"","").replace("<img class=\"shubaobao-expression","").replace("src=\"//ci.xiaohongshu.com/xy_emo_","").replace(".png?v=2\"/>","")
                print(comment1)
                print(reply_content)
                #二级评论者name
                reply_name = str(m.find('span', class_='replier')).replace(": </span>","").replace("<span class=\"replier\" data-v-43aa3553=\"\">","")
                print(reply_name)
                
                sht4.write(c, 0, Number)
                sht4.write(c, 1, comment_name)
                sht4.write(c, 2, comment_id)
                sht4.write(c, 3, comment_time)
                sht4.write(c, 4, comment1)
                sht4.write(c, 5, b)
                b +=1
                sht4.write(c, 6, reply_name)
                sht4.write(c, 7, reply_content)
                
                c +=1
        
         except:
            reply1 = 'null'
            print(reply1)
            
         sht3.write(a, 0, Number)
         sht3.write(a, 1, userid)
         sht3.write(a, 2, comment_name)
         sht3.write(a, 3, comment_id)
         sht3.write(a, 4, comment_time)
         sht3.write(a, 5, comment_content)
         sht3.write(a, 6, comment1)
         sht3.write(a, 7, reply1)
        
         a += 1

    if contenttype == "video":
        # videotime
        videotime = soup.find(attrs={"tag": "sg:videotime"})['content']
        print(videotime)
        
        # posterscr
        poster1 = soup.find('div', class_='videoframe').find('video').get('poster')
        posterscr = "http:" + poster1
        print(posterscr)
        
        #posterid
        videoid = str(Number) +"_v"

        
        # poster下载
        poster = requests.get(url=posterscr).content  ###
        file = r"poster/" + str(Number)+ '.jpg'
        print("正在抓：" + file)
        f = open(file, 'wb')
        f.write(poster)
        f.close()
        

        # 获取并下载视频
        # 获取视频scr
        videoscr = soup.find('div', class_='videoframe').find('video').get('src')
        print(videoscr)
        
        videocontent = requests.get(url=videoscr).content  ###
        file = r"video/"  + str(Number) + "_v" + '.mp4'
        print("正在抓：" + file)
        f = open(file, 'wb')  # 这里要改为跟着视频进行命名
        f.write(videocontent)
        f.close()
        

    else:
        videotime = ''
        posterscr = ''
        videoscr = ''
        videoid = ''
        # 创建文件夹并下载图片 #并把链接
        pic_url1 = soup.find_all('span', class_='inner')
        z = 1
        for it in pic_url1:
            pic_url = 'http:' + it.get('style').replace("background-image:url(", "").replace(");", "")
            pictureid = str(Number) + '_P' + str(z)
            
            # 爬取图片信息
            picture_content = requests.get(url=pic_url).content  ####
            file = r"picture/" + str(Number) + '_P' + str(z) + '.jpg'
            print("正在抓:" + file)
            f = open(file, 'wb')  # 这里要改为跟着视频进行命名
            f.write(picture_content)
            f.close()
            
            #写入数据
            sht2.write(y, 0, Number)
            sht2.write(y, 1, userid)
            sht2.write(y, 2, z)
            sht2.write(y, 4, pictureid)
            z += 1
            sht2.write(y, 3, pic_url)
            y += 1
    # 存数据
    sht1.write(x, 1, author_name)
    sht1.write(x, 2, author_imgscr)
    sht1.write(x, 3, userid)
    sht1.write(x, 4, user_url)
    sht1.write(x, 5, user_brief)
    sht1.write(x, 6, ip_location)
    
    sht1.write(x, 7, keywords)
    sht1.write(x, 8, title)
    sht1.write(x, 9, contenttype)
    sht1.write(x, 10, publish_date)
    sht1.write(x, 11, content)
    sht1.write(x, 12, content5)
    sht1.write(x, 13, tag1)
    sht1.write(x, 14, tag_list2)
    sht1.write(x, 15, tagall)
    
    sht1.write(x, 16, at)    
    sht1.write(x, 17, videotime)
    sht1.write(x, 18, posterscr)
    sht1.write(x, 19, videoscr)
    sht1.write(x, 20, videoid)
    x += 1
    
    #表情包
    sht5.write(c, 0, biaoqingbao_name)
    sht5.write(c, 1, biaoqingbaosrc)
    c += 1


#url = 'https://www.xiaohongshu.com/discovery/item/6146de4b000000000102f943'
df = pd.read_csv(r"./22.csv")['url']
url_list=df.values.tolist()
#f = open('demo.csv', 'r', encoding='utf-8').readlines()
for url in url_list:
    getData(url)

xls.close()
