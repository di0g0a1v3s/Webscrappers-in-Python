from urllib.request import Request, urlopen
from bs4 import BeautifulSoup,Tag
import re
import urllib
import pdfkit
from pathlib import Path
import requests

def download_file_from_google_drive(id):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)
        
    destination = re.search(r'filename\=\"(.*)\"', response.headers['Content-Disposition']).group(1)
    my_file = Path(destination)
    if not my_file.is_file():
        save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768


    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)


#next_page = "https://woodworkingformeremortals.com/why-should-you-make-this-push-block-essential-woodworking-jig-and-shop-project/"
next_page = "https://woodworkingformeremortals.com/make-a-wooden-book-keepsake-box/"
while True:
    url = next_page
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})

    try:
        mybytes = urlopen(req)
    except:
        break
    soup=BeautifulSoup(mybytes,'html.parser')
    for a in soup.findAll('a',{'rel':'prev'}):
        next_page = a['href']  
        print('Next page: ', next_page)
    
    for href in soup.findAll('a',{'href':re.compile('docs.google.com/')}):
        print('Plans Drive: ', href['href'])
        plans_link = href['href']
        try:
            file_id = re.search('d/(.*)/', plans_link).group(1)
        except:
            file_id = re.search('id=(.*)', plans_link).group(1)
        if "&" in file_id:
            file_id = re.search('(.*)&', file_id).group(1)
        print('ID = ',file_id)
        download_file_from_google_drive(file_id)


    for href in soup.findAll('a',{'href':re.compile('bit.ly/WWMM')}):
        print('Bitly: ',href['href'])
        plans_link = requests.head(href['href']).headers['location']
        print('Plans Drive: ', plans_link)
        try:
            file_id = re.search('d/(.*)/', plans_link).group(1)
        except:
            file_id = re.search('id=(.*)', plans_link).group(1)

        print('ID = ',file_id, file_id.find("&"))
        
        download_file_from_google_drive(file_id)

    for href in soup.findAll('a',{'href':re.compile('drive.google.com/')}):
        print('Plans Drive: ', href['href'])
        plans_link = href['href']
        try:
            file_id = re.search('d/(.*)/', plans_link).group(1)
        except:
            file_id = re.search('id=(.*)', plans_link).group(1)
        if "&" in file_id:
            file_id = re.search('(.*)&', file_id).group(1)
        print('ID = ',file_id)
        download_file_from_google_drive(file_id)


    

'''
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

print(count_total,count_missing)'''