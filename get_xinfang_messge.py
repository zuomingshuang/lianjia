import requests
from bs4 import BeautifulSoup
import lxml
import os
from xlwt import Workbook
from datetime import datetime
from get_house_messge import city
from get_house_messge import page


#获取城市
url='https://'+city+'.fang.lianjia.com/loupan/'+'pg1'+'/'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
res=requests.get(url,headers=headers)
html=res.content.decode('utf-8')
soup=BeautifulSoup(html,'lxml')
city_text=soup.find('meta',attrs={'name':'keywords'})['content'].split(',')[0]
#############################################
book=Workbook(encoding='utf-8')
sht=book.add_sheet(city_text)
sht.write(0,0,'爬取时间：'+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
sht.write(1,0,'标题')
sht.write(1,1,'类型')
sht.write(1,2,'状态')
sht.write(1,3,'位置')
sht.write(1,4,'房间数')
sht.write(1,5,'面积')
sht.write(1,6,'标签')
sht.write(1,7,'价格')

i=2
def get_xinfang(city,page):
    global i
    page='pg'+str(page)
    url='https://'+city+'.fang.lianjia.com/loupan/'+page+'/'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    res=requests.get(url,headers=headers)
    html=res.content.decode('utf-8')
    soup=BeautifulSoup(html,'lxml')
    ul=soup.find('ul',class_='resblock-list-wrapper')
    li_list=ul.find_all('li',class_='resblock-list post_ulog_exposure_scroll has-results')

    try:
        for li in li_list:
            title=li.find('a')['title']  #标题
            type=li.find('span',class_='resblock-type').text #类型
            status=li.find('span',class_='sale-status').text   #状态
            location=li.find('div',class_='resblock-location').text  #位置
            room_num=li.find('a',class_='resblock-room').text  #房间数
            area=li.find('div',class_='resblock-area').text  #面积
            tag=li.find('div',class_='resblock-tag').text  #标签
            price=li.find('div',class_='resblock-price').text #价格
            sht.write(i, 0, title)
            sht.write(i, 1, type)
            sht.write(i, 2, status)
            sht.write(i, 3, location)
            sht.write(i, 4, room_num)
            sht.write(i, 5, area)
            sht.write(i, 6, tag)
            sht.write(i, 7, price)
            i+=1
    except:
        pass


for page in range(1,page+1):
    get_xinfang(city,page)

sht.write(0,2,'爬取条数：'+str(i-2)+'条')
cur_path=os.path.dirname(__file__)+'/爬取结果'
book.save(os.path.join(cur_path,city_text+'.xls'))