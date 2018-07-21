import requests
from pyquery import PyQuery as pq
import json
import csv
import threading
import queue

headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36'}

page_q = queue.Queue()  # 页面

def load(page_q,pa):
	while True:
		page = page_q.get()*5
		print(page)
		baseUrl = 'https://www.zhihu.com/api/v4/questions/20434800/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%3F%28type%3Dbest_answerer%29%5D.topics&limit=5&offset='+str(page)+'&sort_by=default'
		html = requests.get(baseUrl,headers= headers).text
		dataJson = json.loads(html)
		datas = dataJson.get('data')
		for data in datas:
			voteup_count = data.get('voteup_count')
			content = data.get('content')
			with open('有哪些称得上优秀的网络小说2200条数据超过20赞回答.csv','a',encoding='utf-8') as csvfile:
				if voteup_count > 20:
					writer = csv.writer(csvfile)
					writer.writerow([voteup_count,content])
		page_q.task_done()

for page in range(284):
        page_q.put(page)
# load.load()
for i in range(100):
 	t = threading.Thread(target = load,args = (page_q,10))
 	t.setDaemon(True)
 	t.start()

page_q.join()