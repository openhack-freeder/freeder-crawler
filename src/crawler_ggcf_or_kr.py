from bs4 import BeautifulSoup
import requests
import re
import datetime 
urlfront ="http://www.ggcf.or.kr/pages/festival/list.asp?gotoPage="
urlback = "&pageSize=36&searchType=&searchText=&searchCategory=&searchYear=2018&searchMonth=&searchIdYN=&MU_IDX=36&Cul_Idx=&pageStatus=&searchOrder="
urlmain = "https://www.ggcf.or.kr/"

now = datetime.datetime.now()
nowDate = now.strftime('%Y.%m.%d')
flag = 0
output = open("../data/ggcf_or_kr.txt","w")
result = ""

for i in range(1,7):
    urlObj = requests.get(urlfront + str(i) + urlback)
    bsObj = BeautifulSoup(urlObj.content,'html.parser')
    for tag in bsObj.find_all('div',{'class','float_wrap'}):
        target = tag.find('div',{'class','text_line'})
        result = ''
        freeflag = '유료'

        #Is show free?
        if target is not None:
            target = str(target)
            if '요금' in target:
                for t in target.split('\n'):
                    if '요금' in t and (': -' in t or '무료' in t):
                        freeflag = '무료'
            else:
                freeflag= '무료'

        #show's type
        target = tag.find('span',{'class',re.compile('m_type *')})
        if target is not None:
            if '행사' in target.text or '콘서트' in target.text or '콘서트' in target.text:
                result += '축제,행사\n'

            elif '무용' in target.text:
                result += '무용,발레\n'

            elif '뮤지컬' in target.text or '연극' in target.text or '아동극' in target.text:
                result += '뮤지컬,연극\n'

            else:
                result += '기타\n'

        #show's info
        for target in tag.find_all('div',{'class','text_line'}):
            #show's title
            result += target.find('h4').text+'\n'

            #show's place,time,term
            for att in target.find_all('li'):
                if result == '':
                    break
                atts = att.text.split()
                if atts[0][0:2] == '기간':
                    if nowDate < atts[3]:
                        result +=att.text[5:]+'\n'
                    else:
                        result = ''
                elif atts[0][0:2] == '시간' and atts[1] == '-':
                        result += 'None\n'
                else:
                    result += att.text[5:]+'\n'

            #show's url link
            if result != '' and freeflag is '무료':
                output.write(result  + '경기\n' + urlmain+'\n')

output.close()
