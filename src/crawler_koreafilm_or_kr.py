import csv
import requests
import datetime 
from bs4 import BeautifulSoup

url = "https://www.koreafilm.or.kr"
url_schedule = "https://www.koreafilm.or.kr/cinematheque/schedule"
now = datetime.datetime.now()
nowDate = now.strftime('%Y.%m.%d')
movie_set = set()

def crawling_mimint(csv_file=None):
    if csv_file is None:
        return
    urlObj = requests.get(url_schedule)
    bsObj = BeautifulSoup(urlObj.text,'html.parser')
    csv_file.writerow(["category","title","date","time","where","url"])

    for movie_month in bsObj.find_all('dl',{'class','list-kofa-calendar-1'}):

        for movies in movie_month.find_all('dl',{'class','list-day-1'}):

            for movie in movies.find_all('dd'):
                title = movie.find('p',{'class','txt-1'}).text
                if '상영작이 없습니다' in title:
                    continue
                else:
                    title = title.split('\n')[0]
                    title = title.replace("'",' ').strip()

                place = "시네마 테크 " + movie.find('li',{'class','txt-room'}).text

                termlist = movie.find('p',{'class','layer-txt-2'}).text.split()
                if '2018' not in termlist[0]:
                    termlist[0] = '2018.'+termlist[0]
                if '2018' not in termlist[2]:
                    termlist[2] = '2018.'+termlist[2]
                term = termlist[0][0:-4]+termlist[1]+termlist[2][0:-4]

                if title not in movie_set and nowDate <= termlist[2][0:-4]:
                    movie_set.add(title)
                    csv_file.writerow(["영화",title,term,None,place,url])


if __name__ == "__main__":
    file = open("../data/koreafilm_or_kr.csv","w",encoding='utf-8',newline='')
    csv_file = csv.writer(file)
    crawling_mimint(csv_file)
    file.close()

