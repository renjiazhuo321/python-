# -*- coding: utf-8 -*-
import requests
from pyquery import PyQuery as pq
import json
import csv
import threading
import queue
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq
headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'}

page_q = queue.Queue()  # 页面
baseUrl = 'https://www.ybdu.com/xiaoshuo/6/6914/'
html = requests.get(baseUrl,headers= headers).text
soup = BeautifulSoup(html,'lxml')
hrefs = soup.select('.mulu_list li a')
name = soup.title.text
for a in hrefs:
	href = a['href']
	contents = baseUrl+href
	page_q.put(contents)

def loadUrl(url,page_q):

	while True:
		contentUrl = page_q.get()
		contentHtml = requests.get(contentUrl,headers = headers).text
		contentPq = pq(contentHtml)#pyquery解析，方便去掉不需要的控件
		content = contentPq('.contentbox')#获取内容div
		div = content.find('div').remove()#去掉多余的控件
		title = contentPq('title').text()#获取标题
		content = content.text()
		print(content)#内容正文
		print(title)#标题
		with open(name+'.txt','a',encoding = 'utf-8') as file:
			title = title.replace('<br>','\n')
			content = content.replace('<br>','\n')
			content = content.replace('    ','\n    ')
			title = title.replace('    ','\n    ')
			print(content)
			print(title)

			file.write(title)
			file.write(content)
		page_q.task_done()

for i in range(10):
 	t = threading.Thread(target = loadUrl,args = (1,page_q))
 	t.setDaemon(True)
 	t.start()

page_q.join()