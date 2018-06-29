from requests import *
from bs4 import BeautifulSoup
import csv

def get_html(url):
    _html = ""
    resp = get(url)
    if resp.status_code == 200:
        _html = resp.text
    return _html
def parse_string(string):
        string = string.replace(u'\xa0',' ')
        string = string.replace('\t',' ')
        string = string.replace('\n',' ')
        string = string.strip()
        return string

def scrap(file):
    file.writerow(["catergory","title","date","time","where","url"])
    url = "http://movie.yes24.com/Event/Event_List.aspx"
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')   
    contents_tags = soup.find_all('td',{'class','vtop'})

    for targets in contents_tags:
        title = targets.find('td',{'class','mv_tit'})
        if title is not None:        
            title = parse_string(title.text)
        else:
            title = None

        contents = targets.find_all('td',{'class','mv_sub'})
        term = time = place = None
        for target in contents:
            if target is not None:
                target = parse_string(target.text).split(' : ')
                index = target[0]
                attr = target[1]
                if '추후' in attr:
                    continue
                if '응모기간' in index:
                    attr = attr.split(' ~ ')
                    term = attr[0] + '~' + attr[1]
                elif '시사회일시' in index:
                    time = attr
                elif '시사회장소' in index:
                    place = attr
        if len(contents) is not 0:
            file.writerow(["영화",title,term,time,place,url])


if __name__ == "__main__":
    file = open("../data/yes24.csv","w",encoding='utf-8',newline='')
    writefile = csv.writer(file)
    scrap(writefile)
    file.close()
    
