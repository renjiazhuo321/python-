# -*-coding:utf-8-*-
# time: 2018.1.23
# author : Corleone
from bs4 import BeautifulSoup
import lxml
import Queue
import requests
import re,os,sys,random
import threading
import logging
import json,hashlib,urllib
from requests.exceptions import ConnectTimeout,ConnectionError,ReadTimeout,SSLError,MissingSchema,ChunkedEncodingError
import random
from lxml import etree
from openpyxl import workbook  # 写入Excel表所用
from openpyxl import load_workbook  # 读取Excel表所用
os.chdir('C:\Users\Administrator\Desktop')  # 更改工作目录为桌面
reload(sys)
sys.setdefaultencoding('gbk')

# 日志模块
logger = logging.getLogger("AppName")
formatter = logging.Formatter('%(asctime)s %(levelname)-5s: %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter
logger.addHandler(console_handler)
logger.setLevel(logging.INFO)

q = Queue.Queue()   # url队列
page_q = Queue.Queue()  # 页面
wb = workbook.Workbook()  # 创建Excel对象
ws = wb.active  # 获取当前正在操作的表对象
# 往表中写入标题行,以列表形式写入！
ws.append(['名称', '图片地址', '视频地址'])
def downlaod(q,x,path):
    urlhash = "https://weibomiaopai.com/"
    try:
        html = requests.get(urlhash).text
    except SSLError:
        logger.info(u"网络不稳定 正在重试")
        html = requests.get(urlhash).text
    reg = re.compile(r'var hash="(.*?)"', re.S)
    result = reg.findall(html)
    hash_v = result[0]

    while True:
        data = q.get()
        
        url, name,img = data[0], data[1],data[2].strip().replace("|", "")
        file = os.path.join(path, '%s' + ".mp4") % name
        print 'url:'+data[0]
        print 'name:'+data[1]
        print 'img:'+img+'\n'

        # api = "https://steakovercooked.com/api/video/?cached&hash=afa458323c59a4741658ee4339b0a855&video=" + url
        # api2 = "https://helloacm.com/api/video/?cached&hash=afa458323c59a4741658ee4339b0a855&video=" + url
        # try:
        #     res = requests.get(api)
            
        #     result = json.loads(res.text)
        # except (ValueError,SSLError):
        #     try:
        #         res = requests.get(api2)
                
        #         result = json.loads(res.text)
        #     except (ValueError,SSLError):
        #         q.task_done()
        #         return False
        # vurl = result['url']
        # logger.info(u"正在下载：%s" %name)
        # logger.info(u"图片地址:%s" %img)
        # try:
        #     r = requests.get(vurl)
        # except SSLError:
        #     r = requests.get(vurl)
        # except MissingSchema:
        #     q.task_done()
        #     continue
        # try:
        # with open(file,'wb') as f:
        #     f.write("name:"+name+"\n"+"图片地址:"+img+"\n"+"url:"+vurl)
        # except IOError:
        #     name = u'好开心么么哒 %s' % random.randint(1,9999)
        #     file = os.path.join(path, '%s' + ".mp4") % name
        #     with open(file,'wb') as f:
        #         f.write(r.content)
        logger.info(u"下载完成：%s" %name)
        q.task_done()

def get_page(keyword,page_q):
        #  创建Excel表并写入数据
    
    while True:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
        }
        #指定打开的文件名
        page = page_q.get()
        url = "https://www.youtube.com/results?search_query=" + keyword + "&page=" + str(page)
        try:
            html = requests.get(url, headers=headers).text
        except (ConnectTimeout,ConnectionError):
            print u"不能访问youtube 检查是否已翻墙"
            os._exit(0)
        reg = re.compile(r'"url":"/watch\?v=(.*?)","webPageType"', re.S)
        result = reg.findall(html)
        logger.info(u"第 %s 页" % page)
        name1 = [] 
        vurl1 = []
        imgPath1 = []
        i = 0
        for x in result:
            vurl = "https://www.youtube.com/watch?v=" + x

            try:
                res = requests.get(vurl).text
            except (ConnectionError,ChunkedEncodingError):
                logger.info(u"网络不稳定 正在重试")
                try:
                    res = requests.get(vurl).text
                except SSLError:
                    continue
            reg2 = re.compile(r"<title>(.*?)YouTube",re.S)
            name = reg2.findall(res)[0].replace("-","")
            imgArray= re.split('/',x)
            imgPath = 'https://i.ytimg.com/vi/'+imgArray[0]+'/sddefault.jpg'
            # print (name)
            print (imgPath)
            print(vurl)
            name1.append(name)
            imgPath1.append(imgPath)
            vurl1.append(vurl)
            ws.append([name1[i], imgPath1[i], vurl1[i]])   
            i = i+1
            # with open('D:/youtube/3Dvideo1','wb') as f:
            #     print (name)
            #     print (imgArray[0])
            #     print(vurl)
            #     f.write("name:"+name+"\n"+"img:"+imgArray[0]+"\n"+"url:"+vurl)
                 #  创建Excel表并写入数据

            #q.put([vurl, name,imgArray[0]])
            
            # if u'\u4e00' <= keyword <= u'\u9fff':
            #     q.put([vurl, name])
            # else:
            #     # 调用金山词霸
            #     logger.info(u"正在翻译")
            #     url_js = "http://www.iciba.com/" + name
            #     html2 = requests.get(url_js).text
            #     soup = BeautifulSoup(html2, "lxml")
            #     try:
            #         res2 = soup.select('.clearfix')[0].get_text()
            #         title = res2.split("\n")[2]
            #     except IndexError:
            #         title = u'好开心么么哒 %s' % random.randint(1, 9999)

            #     print 'title:'+title    
            #     q.put([vurl, title])

        page_q.task_done()
        
        
def main():
    # 使用帮助
    # keyword = raw_input(u"请输入关键字：").decode("gbk")
    # threads = int(raw_input(u"请输入线程数量(建议1-10): "))
    keyword = "3Dvideo"
    threads = 5

    # 判断目录
    path = 'D:\youtube\%s' % keyword
    if os.path.exists(path) == False:
        os.makedirs(path)
    # 解析网页
    logger.info(u"开始解析网页")
    for page in range(11,40):
        page_q.put(page)
    for y in range(threads):
        t = threading.Thread(target=get_page,args=(keyword,page_q))
        t.setDaemon(True)
        t.start()
    page_q.join()
    logger.info(u"共 %s 视频" % q.qsize())
    # # 多线程下载
    # logger.info(u"开始下载视频")
    # # for x in range(threads):
    # #     t = threading.Thread(target=downlaod,args=(q,x,path))
    # #     t.setDaemon(True)
    # #     t.start()
    # # q.join()
    logger.info(u"全部视频下载完成！")
    wb.save("youtubeUrl_11_40.xlsx")  # 存入所有信息后，保存为filename.xlsx
main()

