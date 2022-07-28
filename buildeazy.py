from urllib.request import Request, urlopen
from bs4 import BeautifulSoup,Tag
import re

number_menu_pages = 9

menu_base = "https://www.buildeazy.com/category/free-plans/page/"

for menu_num in range(1,number_menu_pages):
    url = menu_base + str(menu_num)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        mybytes = urlopen(req)
    except:
        break
    soup=BeautifulSoup(mybytes,'html.parser')


    for article in soup.findAll('article',{'class':re.compile('post-')}):
        try:
            link = article.find('a', {'class':'entry-title-link'})['href']
        except:
            continue
        try:
            page_nums = article.findAll('a', {'class':'post-page-numbers'})
            num_pages = int(page_nums[len(page_nums)-1].text[len('Page '):])
        except:
            num_pages = 1
        print(link, num_pages)
            



        url_base = link
        n = num_pages

        elements = [
            {'1stpageonly':True,'name':'div','attributes':{'class':'authority-featured-image'}},
            {'1stpageonly':True,'name':'header','attributes':{'class':'entry-header'}},
            {'1stpageonly':True,'name':'div','attributes':{'id':'toc-np-container'}},
            {'1stpageonly':False,'name':'nav','attributes':{'id':'genesis-nav-social'}},
            {'1stpageonly':False,'name':'header','attributes':{'class':'site-header'}},
            {'1stpageonly':False,'name':'section','attributes':{'class':'author-box'}},
            {'1stpageonly':False,'name':'div','attributes':{'class':'entry-comments'}},
            {'1stpageonly':False,'name':'div','attributes':{'class':'comment-respond'}},
            {'1stpageonly':False,'name':'div','attributes':{'class':'footer-widgets'}},
            {'1stpageonly':False,'name':'footer','attributes':{'class':'site-footer'}},
            {'1stpageonly':False,'name':'div','attributes':{'id':'ez-cookie-dialog'}},
            {'1stpageonly':False,'name':'script','attributes':{'type':'text/javascript'}},
            {'1stpageonly':False,'name':'span','attributes':{'class':re.compile('ezoic-ad')}},
            {'1stpageonly':False,'name':'h2','attributes':{'class':'screen-reader-text'}},
            {'1stpageonly':False,'name':'ul','attributes':{'class':'genesis-skip-link'}},
            {'1stpageonly':False,'name':'script','attributes':{}},
            {'1stpageonly':False,'name':'div','attributes':{'class':'ezmob-footer ezoic-floating-bottom ezo_ad ezmob-footer-desktop'}}

        ]

        f_output = open(url_base[url_base.find('/',url_base.find('/',url_base.find('/')+1)+1)+1:url_base.rfind('/')]+".html", "wb")
        for j in range(1,n+1):
            url = url_base + str(j)
            req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            mybytes = urlopen(req)
            soup=BeautifulSoup(mybytes,'html.parser')

            for element in elements:
                if element['1stpageonly'] == True and j==1:
                    continue
                try:
                    for i in soup.findAll(element['name'], element['attributes']):
                        i.decompose()
                except:
                    print(j, element['name'], element['attributes'])


            for i in soup.findAll('img'):
                try:
                    i['src'] = i['data-lazy-src']
                except:
                    continue
            
            
            f_output.write(soup.prettify("utf-8"))  
