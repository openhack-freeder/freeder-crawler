import csv
import requests
import datetime 
from bs4 import BeautifulSoup

url = "http://www.mimint.co.kr/"
urlfront = "http://www.mimint.co.kr/event_n/event_list.asp?cate=0&page="
urlback = "&pageblock=1"
now = datetime.datetime.now()
nowDate = now.strftime('%Y.%m.%d')

def crawling_mimint(csv_file=None):
    if csv_file is None:
        return
    csv_file.writerow(["catergory","title","date","time","where","url"])
    for i in range(1,3):
        urlObj = requests.get(urlfront + str(i) + urlback)
        bsObj = BeautifulSoup(urlObj.text,'html.parser')
        event_list = bsObj.find_all('li') 
        for li_tags in event_list:
            for content in li_tags.find_all('dl'):
                end_flag = False
                index=title = term = time = place =None
                #show's title
                for content_head in content.find_all('dt'):
                    content_head = content_head.find('span',{'class','txt'})
                    if content_head is not None :
                        title = content_head.text
                        
                #show's term
                attrs = content.find('dd')
                for attr in attrs.find_all('li'):
                    if attr.em.text == '기간':
                        term_list = attr.strong.text.split()
                        if '20'+term_list[2] < nowDate:
                            end_flag = True
                        else:
                            term = '20' + term_list[0] + term_list[1] + '20' + term_list[2]
                #if show is not over
                if end_flag is False:
                    if '영화' in title or '시사회' in title:
                        index = '영화'
                    elif '축제' in title or '행사' in title or '콘서트' in title:
                        index = '축제,행사'
                    elif '무용' in title or '발레' in title:
                        index = '무용,발레'
                    elif '뮤지컬' in title or '연극' in title:
                        index = '뮤지컬,연극'
                    else:
                        index = '기타'
                    csv_file.writerow([index,title,term,time,place,url])

if __name__ == "__main__":
    file = open("../data/mimint_co_kr.csv","w",encoding='utf-8',newline='')
    csv_file = csv.writer(file)
    crawling_mimint(csv_file)
    file.close()

