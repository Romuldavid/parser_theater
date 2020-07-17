#https://habr.com/ru/post/444460/

import requests
#pip install requests
import numpy as np
#pip install numpy
from bs4 import BeautifulSoup
#pip install beautifulsoup4
#pip install lxml


def get_text(url):
#из URL вытаскиваем html
    r = requests.get(url)
    text=r.text
    return text


"""
из всего html-текста собираем "грязные" url-ки, т.е. с какой-то обвеской. В нашем случае выдергиваем их через top_name и class_name
итог выглядит как-то так
<a class="c_theatre2 c_chamber_halls" href="//tickets.mariinsky.ru/ru/performance/WWpGeDRORFUwUkRjME13/">Купить билет</a>
"""
def get_items(text,top_name,class_name):
    soup = BeautifulSoup(text, "lxml")
    film_list = soup.find('div', {'class': top_name})
    items = film_list.find_all('div', {'class': [class_name]})
    dirty_link=[]
    for item in items:
        dirty_link.append(str(item.find('a')))
    return dirty_link

def get_links(dirty_list,start,end):
#из "грязной" версии забираем чистые URL-ы
    links=[]
    for row in dirty_list:
        if row!='None':
            i_beg=row.find(start)
            i_end=row.rfind(end)
            if i_beg!=-1 & i_end!=-1:
                links.append(row[i_beg:i_end])
    return links

#пользователь вводит, в каком месяце ищем, так как афиша по месяцам
num=int(input('Введите номер месяца для поиска: '))

#URL афиши зафиксирован. Год можно подтягивать из текущей даты, но так тоже окей=)
url ='https://www.mariinsky.ru/ru/playbill/playbill/?year=2019&month='+str(num)

#ключевые слова для поиска
top_name='container content gr_top'
class_name='t_button'
start='tickets'
end='/">Купить'

#вызов функций
text=get_text(url)
dirty_link=get_items(text,top_name,class_name)

#и получаем списочек URL-адресов, ведущих на покупку билетов
links=get_links(dirty_link,start,end)
