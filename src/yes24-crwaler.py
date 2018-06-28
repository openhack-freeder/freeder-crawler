from requests import *
from datetime import *
from bs4 import BeautifulSoup

def get_html(url):
    _html = ""
    resp = get(url)
    if resp.status_code == 200:
        _html = resp.text
    return _html

def scrap():
    url = "http://movie.yes24.com/Event/Event_List.aspx"
    html = get_html(url)
    soup = BeautifulSoup(html, 'html.parser')
    showTitle = soup.findAll("td", attrs={"class": "mv_tit"})
    showSubTitle = soup.findAll("td", attrs={"class": "mv_sub"})
    
    
    title = ""
    subtitle = ""
    
    for _showTitle in showTitle:
        title += _showTitle.find('a').text
        title += '\n'

    for _showSubTitle in showSubTitle:
        subtitle += str(_showSubTitle.img)
        subtitle += '\n'

    print(title)
    print(subtitle)

if __name__ == "__main__":
    now = datetime.now()
    nowDate = now.strftime('%Y-%m-%d')
    print(nowDate)
    scrap()
