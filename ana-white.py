from urllib.request import Request, urlopen
from bs4 import BeautifulSoup,Tag
import re
import urllib
import pdfkit
from pathlib import Path

number_menu_pages = 100
menu_base = "https://www.ana-white.com/woodworking-projects?page="
count_total = 0
count_missing = 0
for menu_num in range(number_menu_pages):
    print(menu_num)
    url = menu_base + str(menu_num)
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        mybytes = urlopen(req)
    except:
        break
    soup=BeautifulSoup(mybytes,'html.parser')

    
    for article in soup.findAll('article',{'class':re.compile('plan')}):
        try:
            link = "https://www.ana-white.com" + article.find('a')['href']
            
            count_total=count_total+1
        except Exception as e:
            print(e)
            continue

    
        url = link
        file_name = url[url.rfind('/')+1:]

        my_file = Path(file_name+".html")
        my_file2 = Path('%'+file_name+".html")
        if not my_file.is_file():
            if not my_file2.is_file():
                count_missing=count_missing+1
                print(file_name)
                elements = [
                            
                            {'name':'script','attributes':{}},
                            {'name':'header','attributes':{'id':'navbar'}},
                            {'name':'div','attributes':{'role':'banner'}},
                            {'name':'ol','attributes':{'class':'breadcrumb'}},
                            {'name':'section','attributes':{'id':'block-anonymousflag'}},
                            {'name':'aside','attributes':{'class':'col-sm-3'}},
                            {'name':'section','attributes':{'class':'comments'}},
                            {'name':'ul','attributes':{'class':'links inline list-inline'}},
                            {'name':'footer','attributes':{'class':'footer-cta container-fluid'}},
                            {'name':'footer','attributes':{'class':'footer container-fluid'}},
                            {'name':'a','attributes':{'class':'print'}},
                        ]


                req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

                mybytes = urlopen(req)

                soup=BeautifulSoup(mybytes,'html.parser')

                

                for element in elements:
                    try:
                        for i in soup.findAll(element['name'], element['attributes']):
                            i.decompose()
                    except:
                        pass

                for i in soup.findAll():
                    try:
                        if i['href'][0] == '/':
                            i['href'] = "https://www.ana-white.com" + i['href']
                    except:
                        pass
                    try:
                        if i['src'][0] == '/':
                            i['src'] = "https://www.ana-white.com" + i['src']
                    except:
                        pass
                
                worthkeeping = len(soup.findAll('div',{'class':'field field--name-field-shoppinglist field--type-text-long field--label-above'}))+ len(soup.findAll('div',{'class':'field field--name-field-cutlist field--type-text-long field--label-above'}))+ len(soup.findAll('div',{'class':'field field--name-field-tools field--type-list-string field--label-above'}))

                if worthkeeping == 0:
                    file_name = '%'+file_name
                
                f_output = open(file_name+".html", "wb")
                f_output.write(soup.prettify("utf-8"))  
                f_output.close()
                try:
                    pdfkit.from_url(file_name+'.html', file_name+'.pdf')
                except:
                    pass

print(count_total,count_missing)