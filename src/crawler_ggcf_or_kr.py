from bs4 import BeautifulSoup
import requests
import re
import datetime 
import csv
urlfront ="http://www.ggcf.or.kr/pages/festival/list.asp?gotoPage="
urlback = "&pageSize=36&searchType=&searchText=&searchCategory=&searchYear=2018&searchMonth=&searchIdYN=&MU_IDX=36&Cul_Idx=&pageStatus=&searchOrder="
urlmain = "https://www.ggcf.or.kr"

now = datetime.datetime.now()
nowDate = now.strftime('%Y.%m.%d')
flag = 0
output = open("../data/ggcf_or_kr.csv","w")
csv_output = csv.writer(output)
result = ""
region = '경기도'

for i in range(1,7):
    urlObj = requests.get(urlfront + str(i) + urlback)
    bsObj = BeautifulSoup(urlObj.content,'html.parser')
    for tag in bsObj.find_all('div',{'class','float_wrap'}):
        target = tag.find('div',{'class','text_line'})
        freeflag = '유료'
        index = title = term = time = place = ''
        #Is show free?
        if target is not None:
            target = str(target)
            if '요금' in target:
                for t in target.split('\n'):
                    if '요금' in t and (': -' in t or '무료' in t):
                        freeflag = '무료'
            else:
                freeflag= '무료'
        if freeflag == '유료':
            continue

        #show's type
        target = tag.find('span',{'class',re.compile('m_type *')})
        if target is not None:
            if '행사' in target.text or '콘서트' in target.text or '콘서트' in target.text:
                index = '축제,행사'

            elif '무용' in target.text:
                index = '무용,발레'

            elif '뮤지컬' in target.text or '연극' in target.text or '아동극' in target.text:
                index = '뮤지컬,연극'

            else:
                index = '기타'

        #show's info
        for target in tag.find_all('div',{'class','text_line'}):
            #show's title
            title = target.find('h4').text

            #show's place,time,term
            for att in target.find_all('li'):
                atts = att.text.split()
                if atts[0][0:2] == '기간':
                    if nowDate < atts[3]:
                        term = atts[1] +atts[2] + atts[3]
                    else:
                        term = 'timeout'
                elif atts[0][0:2] == '시간':
                    if not atts[1] == '-':
                        time = att.text[5:]
                else:
                    place = region+att.text[5:]

            #show write to .csv, if it is not timeout
            
            if term != 'timeout':
                csv_output.writerow([index,title ,term,time,place,urlmain])
                
            

output.close()
