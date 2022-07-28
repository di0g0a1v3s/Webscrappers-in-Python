from urllib.request import Request, urlopen
from bs4 import BeautifulSoup,Tag
import re
import requests
import os

number_menu_pages = 20
categories = ['garage-and-workshop', 'office-and-hobby-room', 'outdoor-living', 'closet-and-storage', 'kitchen', 'bedroom', 'bathroom', 'dining-room', 'kid-spaces-and-play-room', 'living-room', 'entryway-and-laundry', 'other']
for category in categories:
    menu_base = 'https://learn.kregtool.com/projects-plans/search/page/'
    menu_base_tail = '/?categories=' + category

    for menu_num in range(1,number_menu_pages):
        url = menu_base + str(menu_num) + menu_base_tail
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        try:
            mybytes = urlopen(req)
        except:
            break
        soup=BeautifulSoup(mybytes,'html.parser')


        for article in soup.findAll('div',{'class':re.compile('project-card')}):
            try:
                project_link = article.find('a')['href']
            except:
                continue
            
            
            req = Request(project_link, headers={'User-Agent': 'Mozilla/5.0'})
            try:
                mybytes = urlopen(req)
            except:
                break
            soup=BeautifulSoup(mybytes,'html.parser')

            

            for article in soup.findAll('ul',{'class':re.compile('article-options')}):
                try:
                    download_link = article.findAll('a')[2]['href']
                    download_link = 'https://learn.kregtool.com/' + download_link
                except:
                    continue
                
                filename = download_link.rsplit('plan_name=', 1)[1]
                print(filename)
                if not os.path.exists(category + "/" + filename + '.pdf'):
                    r = requests.get(download_link, allow_redirects=True)
                    print("-----"+ filename+"--------")
                    if not os.path.exists(category):
                        os.mkdir(category)
                    open(category + "/" + filename + '.pdf', 'wb').write(r.content)



        
