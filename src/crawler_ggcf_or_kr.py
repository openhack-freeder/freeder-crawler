from bs4 import BeautifulSoup
import requests
import datetime 
urlfront ="http://www.ggcf.or.kr/pages/festival/list.asp?gotoPage="
urlback = "&pageSize=36&searchType=&searchText=&searchCategory=&searchYear=2018&searchMonth=&searchIdYN=&MU_IDX=36&Cul_Idx=&pageStatus=&searchOrder="
urlmain = "https://www.ggcf.or.kr/"

now = datetime.datetime.now()
nowDate = now.strftime('%Y.%m.%d')
flag = 0
output = open("ggcf_or_kr.txt","w")
result = ""
for i in range(1,7):
    urlObj = requests.get(urlfront + str(i) + urlback)
    bsObj = BeautifulSoup(urlObj.content,'html.parser')
    for tag in bsObj.find_all('div',{'class','float_wrap'}):
        for target in tag.find_all('div',{'class','text_line'}):
            result = target.find('h4').text+'\n'
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
            if result != '':
                output.write(result + urlmain+'\n')



output.close()
