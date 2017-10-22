import re
import time
import random
from bs4 import BeautifulSoup
import multiprocessing
import pymongo
import requests
from selenium import webdriver

#get free IP
def get_IP():
    proxy = []
    fp = open('D:\PycharmProjects\spider/spyder0/proxy/host_tested.txt','r')
    ips = fp.readlines()
    for i in ips:
        ip = i.strip('\n')
        proxy.append(eval(ip))
    fp.close()
    return proxy


#create a list of url
def get_url():
    url_Queue = []
    for page in range(10):
        url = 'https://movie.douban.com/top250?start='+str(page*25)
        url_Queue.append({
            'url': url,
            'status':False
        })
    return url_Queue


def spider(urls,headers,proxy):

    movie = []

    for url in urls:
        print(url)
        try:
            responce = requests.get(url['url'], headers=headers,proxies=random.choice(proxy))
            bs = BeautifulSoup(responce.text,'lxml')
            #movie
            items = bs.find_all('div', class_='item')
            for item in items:
                #number
                number = item.select('.pic em')[0].text
                #title
                title = ''
                for title_1 in item.select('.hd a span'):
                     title += title_1.text.replace('\xa0','').replace(' ','')
                #score
                score = item.select('.star .rating_num')[0].text
                #description
                try:
                    description = item.select('.quote .inq')[0].text
                except:
                    description = ''
                finally:
                    movie.append({
                        'number': number,
                        'title': title,
                        'score':score,
                        'description':description
                    })
                    print(1)
        except Exception as e:
            urls.append(url)
            print(e)
    return movie




if __name__ == '__main__':
    #user_agent pool
    USER_AGENT = ['Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
                  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1500.95 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; rv:11.0) like Gecko)',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.2) Gecko/2008070208 Firefox/3.0.1',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070309 Firefox/2.0.0.3',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1) Gecko/20070803 Firefox/1.5.0.12',
                  'Opera/9.27 (Windows NT 5.2; U; zh-cn)',
                  'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
                  'Opera/8.0 (Macintosh; PPC Mac OS X; U; en)',
                  'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.12) Gecko/20080219 Firefox/2.0.0.12 Navigator/9.0.0.6',
                  'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Win64; x64; Trident/4.0)',
                  'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; Trident/4.0)',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2; .NET4.0C; .NET4.0E; QQBrowser/7.3.9825.400)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:21.0) Gecko/20100101 Firefox/21.0 ',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
                  'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0; BIDUBrowser 2.x)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11'
                  ]
    #header
    headers = {
        'User-Agent': random.choice(USER_AGENT),
        'Accept': 'text / html, application / xhtml + xml, application / xml; q = 0.9, image / webp, image / apng, * / *;q = 0.8',
        'Accept - Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh - CN, zh;q = 0.8',
        'Connection': 'keep - alive',
        'cookie': 'll="118281"; bid=qB5d_1csbk0; viewed="10590856"; gr_user_id=ef021111-0bbe-419f-b145-be752f0b0932; __yadk_uid=Ol1tQPAJUQUbWahD4i4LxSQAJ5z4FGo0; _vwo_uuid_v2=61829040D3AF99B00BC5CBC68E6A7C45|756f445fcf534833ca9124d7a499d6cf; ps=y; ap=1; as="https://sec.douban.com/b?r=https%3A%2F%2Fmovie.douban.com%2Ftop250"; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1508381477%2C%22https%3A%2F%2Fwww.google.com.hk%2F%22%5D; _pk_id.100001.4cf6=d01fe3a3c2fd78d6.1508229760.5.1508381918.1508334665.; _pk_ses.100001.4cf6=*; hibext_instdsigdip=1',
        'DNT': '1',
        'Host': 'movie.douban.com',
        'Referer': 'https://movie.douban.com/top250'
    }

    proxy = get_IP()
    urls = get_url()
    movie = spider(urls,headers,proxy)
    #write data in database
    connection = pymongo.MongoClient()
    db = connection.movie
    collection = db.top_250
    collection.insert_many(movie)










