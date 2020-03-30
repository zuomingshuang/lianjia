import requests
from bs4 import BeautifulSoup
import lxml
import os
from xlwt import Workbook
from datetime import datetime
from get_house_messge import city
from get_house_messge import page


#city='wh'
#获取城市
url='https://'+city+'.lianjia.com/ershoufang/'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
res=requests.get(url,headers=headers)
html=res.content.decode('utf-8')
soup=BeautifulSoup(html,'lxml')
city_text=soup.find('meta',attrs={'name':'keywords'})['content'].split(',')[0]

book=Workbook(encoding='utf-8')
sht=book.add_sheet(city_text)
sht.write(0,0,'爬取时间：'+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
sht.write(0,1,'爬取条件：'+city_text)
sht.write(1,0,'卖点')
sht.write(1,1,'楼层')
sht.write(1,2,'发布时间')
sht.write(1,3,'标签')
sht.write(1,4,'地点')
sht.write(1,5,'小区')
sht.write(1,6,'户型')
sht.write(1,7,'面积')
sht.write(1,8,'朝向')
sht.write(1,9,'装修')
sht.write(1,10,'是否电梯房')
sht.write(1,11,'总金额')
sht.write(1,12,'单价')
i=2
def get_msg(city='sz',page=None):
    global i
    page='pg'+str(page)+'/'
    url='https://'+str(city)+'.lianjia.com/ershoufang/'+page
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
    res=requests.get(url,headers=headers)
    html=res.content.decode('utf-8')
    soup=BeautifulSoup(html,'lxml')
    li_list=soup.find('ul',class_='sellListContent').find_all('li',class_='clear LOGCLICKDATA')
    for li in li_list:
        try:
            div=li.find('div',class_='info clear')
            title=div.find('div',class_='title').text #卖点
            address=div.find('div',class_='address').text
            flood=div.find('div',class_='flood').text.split('-')[0] #楼层
            dd=div.find('div',class_='flood').text.split('-')[1] #地点
            followInfo=div.find('div',class_='followInfo').text #关注人数和带看次数和发布时间
            tag=div.find('div',class_='tag').text #房本满五年，标签
            price=div.find('div',class_='priceInfo').text
            
            address_list=address.split('|')
            xq=address_list[0] #小区
            hx=address_list[1] #户型
            mj=address_list[2] #面积 
            cx=address_list[3] #朝向
            zx=address_list[4] #装修
            dt=address_list[5] #是否有电梯
            
            total_money=price.split('单价')[0] #总金额  
            per_money=price.split('单价')[1] #单

            sht.write(i,0,title)
            sht.write(i,1,flood)
            sht.write(i,2,followInfo)
            sht.write(i,3,tag)
            sht.write(i,4,xq)
            sht.write(i,5,dd)
            sht.write(i,6,hx)
            sht.write(i,7,mj)
            sht.write(i,8,cx)
            sht.write(i,9,zx)
            sht.write(i,10,dt)
            sht.write(i,11,total_money)
            sht.write(i,12,per_money)
            i+=1

        except:
            pass


for page in range(1,page+1):
    get_msg(city=city,page=page)

sht.write(0,2,'爬取条数：'+str(i-2)+'条')
cur_path=os.path.dirname(__file__)+'/爬取结果'
book.save(os.path.join(cur_path,city_text+'信息.xls'))
